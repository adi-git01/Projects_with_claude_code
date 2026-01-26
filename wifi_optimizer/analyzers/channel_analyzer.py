"""
Analyzes WiFi channels and provides optimization recommendations.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict

from ..models.network import WiFiNetwork, FrequencyBand, ChannelInfo


# 2.4GHz channel overlap matrix
# Channels 1, 6, 11 are non-overlapping
# Each 2.4GHz channel is 22MHz wide, channels are 5MHz apart
CHANNEL_2_4_OVERLAP = {
    1: [1, 2, 3, 4, 5],
    2: [1, 2, 3, 4, 5, 6],
    3: [1, 2, 3, 4, 5, 6, 7],
    4: [1, 2, 3, 4, 5, 6, 7, 8],
    5: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    6: [2, 3, 4, 5, 6, 7, 8, 9, 10],
    7: [3, 4, 5, 6, 7, 8, 9, 10, 11],
    8: [4, 5, 6, 7, 8, 9, 10, 11],
    9: [5, 6, 7, 8, 9, 10, 11, 12, 13],
    10: [6, 7, 8, 9, 10, 11, 12, 13],
    11: [7, 8, 9, 10, 11, 12, 13],
    12: [8, 9, 10, 11, 12, 13],
    13: [9, 10, 11, 12, 13],
}


@dataclass
class ChannelRecommendation:
    """A channel recommendation with reasoning."""
    channel: int
    band: FrequencyBand
    score: float  # 0-100, higher is better
    interference_level: str
    reasoning: List[str]
    width_recommendation: int  # 20, 40, 80 MHz


class ChannelAnalyzer:
    """Analyzes WiFi channels and recommends optimal settings."""

    def __init__(self, networks: List[WiFiNetwork] = None):
        self.networks = networks or []
        self.your_ssids: List[str] = []

    def set_networks(self, networks: List[WiFiNetwork]):
        """Set the list of detected networks."""
        self.networks = networks

    def set_your_ssids(self, ssids: List[str]):
        """Set your network SSIDs."""
        self.your_ssids = ssids

    def analyze_channel_usage(self) -> Dict[FrequencyBand, Dict[int, ChannelInfo]]:
        """Analyze which channels are being used and their congestion."""
        channel_data = {
            FrequencyBand.BAND_2_4GHZ: {},
            FrequencyBand.BAND_5GHZ: {},
            FrequencyBand.BAND_6GHZ: {}
        }

        # Initialize 2.4GHz channels
        for ch in range(1, 14):
            freq = 2412 + (ch - 1) * 5
            channel_data[FrequencyBand.BAND_2_4GHZ][ch] = ChannelInfo(
                channel=ch, frequency=freq, band=FrequencyBand.BAND_2_4GHZ
            )

        # Initialize common 5GHz channels
        for ch in [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112,
                   116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165]:
            freq = 5000 + ch * 5
            channel_data[FrequencyBand.BAND_5GHZ][ch] = ChannelInfo(
                channel=ch, frequency=freq, band=FrequencyBand.BAND_5GHZ
            )

        # Count networks per channel
        for network in self.networks:
            band = network.frequency_band
            ch = network.channel

            if ch in channel_data[band]:
                info = channel_data[band][ch]
                info.networks_count += 1
                # Weighted by signal strength (stronger = more interference)
                weight = max(0, (100 + network.signal_dbm) / 50)  # -50dBm = 1.0, -100dBm = 0
                info.avg_signal = (info.avg_signal * (info.networks_count - 1) + network.signal_dbm) / info.networks_count

        # Calculate interference scores
        self._calculate_interference_scores(channel_data)

        return channel_data

    def _calculate_interference_scores(self, channel_data: Dict):
        """Calculate interference scores for each channel."""
        # 2.4GHz - consider overlapping channels
        for ch, info in channel_data[FrequencyBand.BAND_2_4GHZ].items():
            interference = 0
            overlapping = CHANNEL_2_4_OVERLAP.get(ch, [ch])

            for overlap_ch in overlapping:
                if overlap_ch in channel_data[FrequencyBand.BAND_2_4GHZ]:
                    overlap_info = channel_data[FrequencyBand.BAND_2_4GHZ][overlap_ch]
                    # Weight by proximity (same channel = full weight)
                    distance = abs(ch - overlap_ch)
                    weight = 1 - (distance * 0.15)  # Reduce impact for farther channels
                    interference += overlap_info.networks_count * weight * 10

            # Penalize non-standard channels
            if ch not in [1, 6, 11]:
                interference += 15

            info.interference_score = min(100, interference)

        # 5GHz - generally less interference
        for ch, info in channel_data[FrequencyBand.BAND_5GHZ].items():
            interference = info.networks_count * 15
            # DFS channels (52-144) may have radar restrictions
            if 52 <= ch <= 144:
                interference += 5  # Small penalty for DFS complexity
            info.interference_score = min(100, interference)

    def get_best_channels(self, band: FrequencyBand, top_n: int = 3) -> List[ChannelRecommendation]:
        """Get the best channel recommendations for a band."""
        channel_data = self.analyze_channel_usage()
        recommendations = []

        if band == FrequencyBand.BAND_2_4GHZ:
            # Only recommend non-overlapping channels
            preferred_channels = [1, 6, 11]

            for ch in preferred_channels:
                if ch in channel_data[band]:
                    info = channel_data[band][ch]
                    score = 100 - info.interference_score
                    reasoning = []

                    if info.networks_count == 0:
                        reasoning.append(f"Channel {ch} is completely free")
                    else:
                        reasoning.append(f"Channel {ch} has {info.networks_count} network(s)")

                    if info.interference_score < 30:
                        interference_level = "Low"
                    elif info.interference_score < 60:
                        interference_level = "Medium"
                    else:
                        interference_level = "High"

                    reasoning.append(f"Interference level: {interference_level}")
                    reasoning.append("Non-overlapping channel (recommended)")

                    recommendations.append(ChannelRecommendation(
                        channel=ch,
                        band=band,
                        score=score,
                        interference_level=interference_level,
                        reasoning=reasoning,
                        width_recommendation=20  # 20MHz for 2.4GHz with repeaters
                    ))

        else:  # 5GHz
            # Prefer UNII-1 channels (36-48) as they don't require DFS
            unii1_channels = [36, 40, 44, 48]
            other_channels = [149, 153, 157, 161, 165]  # UNII-3, also no DFS

            for ch in unii1_channels + other_channels:
                if ch in channel_data[band]:
                    info = channel_data[band][ch]
                    score = 100 - info.interference_score
                    reasoning = []

                    if info.networks_count == 0:
                        reasoning.append(f"Channel {ch} is completely free")
                    else:
                        reasoning.append(f"Channel {ch} has {info.networks_count} network(s)")

                    if ch in unii1_channels:
                        reasoning.append("UNII-1 band (no DFS, reliable)")
                        score += 5
                    elif ch in other_channels:
                        reasoning.append("UNII-3 band (no DFS)")
                        score += 3

                    if info.interference_score < 20:
                        interference_level = "Low"
                    elif info.interference_score < 50:
                        interference_level = "Medium"
                    else:
                        interference_level = "High"

                    recommendations.append(ChannelRecommendation(
                        channel=ch,
                        band=band,
                        score=min(100, score),
                        interference_level=interference_level,
                        reasoning=reasoning,
                        width_recommendation=40  # 40MHz good balance for 5GHz
                    ))

        # Sort by score
        recommendations.sort(key=lambda r: r.score, reverse=True)
        return recommendations[:top_n]

    def print_channel_analysis(self):
        """Print a detailed channel analysis."""
        channel_data = self.analyze_channel_usage()

        print("\n" + "=" * 70)
        print("CHANNEL ANALYSIS")
        print("=" * 70)

        # 2.4GHz Analysis
        print("\n📡 2.4GHz Band:")
        print("-" * 50)
        print(f"{'Channel':<10} {'Networks':<12} {'Interference':<15} {'Status'}")
        print("-" * 50)

        for ch in [1, 6, 11]:  # Show only non-overlapping
            if ch in channel_data[FrequencyBand.BAND_2_4GHZ]:
                info = channel_data[FrequencyBand.BAND_2_4GHZ][ch]
                bar = "█" * int(info.interference_score / 10) + "░" * (10 - int(info.interference_score / 10))
                status = "✓ Recommended" if info.interference_score < 40 else "⚠ Congested"
                print(f"Ch {ch:<6} {info.networks_count:<12} [{bar}] {info.interference_score:>3.0f}%  {status}")

        # 5GHz Analysis
        print("\n📡 5GHz Band:")
        print("-" * 50)

        for ch in [36, 40, 44, 48, 149, 153, 157, 161]:
            if ch in channel_data[FrequencyBand.BAND_5GHZ]:
                info = channel_data[FrequencyBand.BAND_5GHZ][ch]
                bar = "█" * int(info.interference_score / 10) + "░" * (10 - int(info.interference_score / 10))
                status = "✓ Good" if info.interference_score < 30 else "⚠ Busy"
                print(f"Ch {ch:<6} {info.networks_count:<12} [{bar}] {info.interference_score:>3.0f}%  {status}")

        print("=" * 70)

    def get_configuration_recommendations(self) -> Dict:
        """Get complete configuration recommendations."""
        best_2_4 = self.get_best_channels(FrequencyBand.BAND_2_4GHZ, 1)
        best_5 = self.get_best_channels(FrequencyBand.BAND_5GHZ, 1)

        recommendations = {
            '2.4GHz': {
                'channel': best_2_4[0].channel if best_2_4 else 1,
                'width': 20,
                'reasoning': best_2_4[0].reasoning if best_2_4 else ["Default to channel 1"]
            },
            '5GHz': {
                'channel': best_5[0].channel if best_5 else 36,
                'width': 40,
                'reasoning': best_5[0].reasoning if best_5 else ["Default to channel 36"]
            }
        }

        return recommendations

    def print_recommendations(self):
        """Print configuration recommendations."""
        recs = self.get_configuration_recommendations()

        print("\n" + "=" * 70)
        print("📋 RECOMMENDED CONFIGURATION")
        print("=" * 70)

        print("\n🔧 Main Router (Airtel) Settings:")
        print(f"   2.4GHz Channel: {recs['2.4GHz']['channel']}")
        print(f"   2.4GHz Width:   {recs['2.4GHz']['width']} MHz")
        for reason in recs['2.4GHz']['reasoning']:
            print(f"      → {reason}")

        print(f"\n   5GHz Channel:   {recs['5GHz']['channel']}")
        print(f"   5GHz Width:     {recs['5GHz']['width']} MHz")
        for reason in recs['5GHz']['reasoning']:
            print(f"      → {reason}")

        print("\n🔧 Repeater (Tenda) Settings:")
        print(f"   Use SAME channels as main router")
        print(f"   2.4GHz: Channel {recs['2.4GHz']['channel']}, Width 20 MHz")
        print(f"   5GHz:   Channel {recs['5GHz']['channel']}, Width 40 MHz")
        print(f"   Use same SSID and password for seamless roaming")

        print("\n" + "=" * 70)
