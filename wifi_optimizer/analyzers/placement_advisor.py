"""
Analyzes signal measurements and provides repeater placement recommendations.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from ..models.network import Location, NetworkDevice, DeviceType
from ..collectors.measurement_collector import MeasurementCollector


@dataclass
class PlacementRecommendation:
    """A placement recommendation for a repeater."""
    repeater_name: str
    recommended_location: str
    should_connect_to: str  # SSID or device to connect to
    signal_at_location: float
    reasoning: List[str]
    priority: int  # 1 = most important


@dataclass
class CoverageGap:
    """Represents a gap in WiFi coverage."""
    location: str
    best_signal: float
    needs_improvement: bool
    priority: int


class PlacementAdvisor:
    """Advises on optimal repeater placement based on measurements."""

    def __init__(self, collector: MeasurementCollector = None):
        self.collector = collector
        self.devices: List[NetworkDevice] = []
        self.main_router_ssid: str = ""

    def set_collector(self, collector: MeasurementCollector):
        """Set the measurement collector."""
        self.collector = collector

    def set_devices(self, devices: List[NetworkDevice]):
        """Set the network devices."""
        self.devices = devices
        # Find main router SSID
        for device in devices:
            if device.device_type == DeviceType.MAIN_ROUTER:
                self.main_router_ssid = device.ssid
                break

    def analyze_coverage_gaps(self) -> List[CoverageGap]:
        """Identify coverage gaps based on collected measurements."""
        if not self.collector:
            return []

        coverage = self.collector.get_your_networks_coverage()
        gaps = []

        for loc_name, signals in coverage.items():
            if not signals:
                gaps.append(CoverageGap(
                    location=loc_name,
                    best_signal=-100,
                    needs_improvement=True,
                    priority=1
                ))
                continue

            best_signal = max(signals.values())

            needs_improvement = best_signal < -65
            if best_signal < -80:
                priority = 1  # Critical
            elif best_signal < -70:
                priority = 2  # High
            elif best_signal < -65:
                priority = 3  # Medium
            else:
                priority = 4  # Low (acceptable)

            gaps.append(CoverageGap(
                location=loc_name,
                best_signal=best_signal,
                needs_improvement=needs_improvement,
                priority=priority
            ))

        return sorted(gaps, key=lambda g: (g.priority, g.best_signal))

    def find_ideal_repeater_spots(self) -> List[str]:
        """
        Find ideal locations for repeaters.

        Ideal spot = location with fair signal (-60 to -70 dBm) from router
        This ensures repeater receives good signal to extend.
        """
        if not self.collector:
            return []

        coverage = self.collector.get_your_networks_coverage()
        ideal_spots = []

        for loc_name, signals in coverage.items():
            if self.main_router_ssid in signals:
                signal = signals[self.main_router_ssid]
                # Ideal placement zone: fair but not weak signal
                if -70 <= signal <= -55:
                    ideal_spots.append((loc_name, signal))

        # Sort by signal strength (prefer stronger)
        ideal_spots.sort(key=lambda x: x[1], reverse=True)
        return [spot[0] for spot in ideal_spots]

    def get_placement_recommendations(self, num_repeaters: int = 2) -> List[PlacementRecommendation]:
        """Generate placement recommendations for repeaters."""
        recommendations = []

        if not self.collector:
            return self._get_generic_recommendations(num_repeaters)

        coverage = self.collector.get_your_networks_coverage()
        gaps = self.analyze_coverage_gaps()
        ideal_spots = self.find_ideal_repeater_spots()

        # Categorize locations by signal quality
        strong_signal_locs = []  # > -55 dBm
        medium_signal_locs = []  # -55 to -70 dBm
        weak_signal_locs = []    # < -70 dBm

        for loc_name, signals in coverage.items():
            if self.main_router_ssid in signals:
                signal = signals[self.main_router_ssid]
                if signal > -55:
                    strong_signal_locs.append((loc_name, signal))
                elif signal > -70:
                    medium_signal_locs.append((loc_name, signal))
                else:
                    weak_signal_locs.append((loc_name, signal))

        # Sort each category
        medium_signal_locs.sort(key=lambda x: x[1], reverse=True)
        weak_signal_locs.sort(key=lambda x: x[1])

        # Generate recommendations
        placed_repeaters = 0
        used_locations = set()

        # First repeater: Place at best medium-signal location
        if medium_signal_locs and placed_repeaters < num_repeaters:
            loc, signal = medium_signal_locs[0]
            reasoning = [
                f"Signal from main router: {signal:.0f} dBm (Good for repeating)",
                "This location can receive strong signal and extend coverage",
                "Place here to bridge between router and far areas"
            ]

            # Find what weak areas this could help
            helped_areas = [w[0] for w in weak_signal_locs[:3]]
            if helped_areas:
                reasoning.append(f"Will improve coverage in: {', '.join(helped_areas)}")

            recommendations.append(PlacementRecommendation(
                repeater_name="Tenda Repeater 1",
                recommended_location=loc,
                should_connect_to=self.main_router_ssid,
                signal_at_location=signal,
                reasoning=reasoning,
                priority=1
            ))
            used_locations.add(loc)
            placed_repeaters += 1

        # Second repeater: Extend from first repeater or cover remaining gaps
        if placed_repeaters < num_repeaters:
            # Look for a location that's between the first repeater and dead zones
            remaining_medium = [(l, s) for l, s in medium_signal_locs if l not in used_locations]

            if remaining_medium:
                loc, signal = remaining_medium[0]
            elif weak_signal_locs:
                # If no medium spots, find the least weak spot
                loc, signal = max(weak_signal_locs, key=lambda x: x[1])
            else:
                loc, signal = "Between router and far area", -65

            reasoning = [
                f"Signal at this location: {signal:.0f} dBm",
                "Position to extend coverage to remaining weak areas",
                "Can connect to Repeater 1 (daisy chain) if main router signal is weak here"
            ]

            recommendations.append(PlacementRecommendation(
                repeater_name="Tenda Repeater 2",
                recommended_location=loc,
                should_connect_to="Tenda Repeater 1 or Main Router (whichever is stronger)",
                signal_at_location=signal,
                reasoning=reasoning,
                priority=2
            ))

        return recommendations

    def _get_generic_recommendations(self, num_repeaters: int) -> List[PlacementRecommendation]:
        """Generic recommendations when no measurements available."""
        recommendations = [
            PlacementRecommendation(
                repeater_name="Tenda Repeater 1",
                recommended_location="Halfway between router and first dead zone",
                should_connect_to="Main Router",
                signal_at_location=-60,
                reasoning=[
                    "Place where you still have 2-3 bars of WiFi signal",
                    "Should be able to 'see' the main router (minimal walls)",
                    "Elevated position (shelf height) is better than floor",
                    "Avoid placing near microwaves, cordless phones, or metal objects"
                ],
                priority=1
            )
        ]

        if num_repeaters >= 2:
            recommendations.append(PlacementRecommendation(
                repeater_name="Tenda Repeater 2",
                recommended_location="Halfway between Repeater 1 and remaining dead zone",
                should_connect_to="Tenda Repeater 1 or Main Router",
                signal_at_location=-65,
                reasoning=[
                    "Extends coverage to far areas",
                    "Should receive good signal from Repeater 1",
                    "Can daisy-chain from Repeater 1 for greater range",
                    "Keep elevated and away from interference sources"
                ],
                priority=2
            ))

        return recommendations

    def print_placement_report(self, num_repeaters: int = 2):
        """Print a detailed placement report."""
        recommendations = self.get_placement_recommendations(num_repeaters)

        print("\n" + "=" * 70)
        print("📍 REPEATER PLACEMENT RECOMMENDATIONS")
        print("=" * 70)

        if self.collector and self.collector.location_data:
            # Print coverage analysis first
            gaps = self.analyze_coverage_gaps()
            print("\n📊 Coverage Analysis:")
            print("-" * 50)

            for gap in gaps:
                if gap.priority == 1:
                    status = "🔴 Critical"
                elif gap.priority == 2:
                    status = "🟠 Needs Help"
                elif gap.priority == 3:
                    status = "🟡 Could Improve"
                else:
                    status = "🟢 Good"

                print(f"   {gap.location:<20} {gap.best_signal:>4.0f} dBm  {status}")

        print("\n🎯 Recommended Placements:")
        print("-" * 50)

        for i, rec in enumerate(recommendations, 1):
            print(f"\n   {rec.repeater_name}:")
            print(f"   └─ Location: {rec.recommended_location}")
            print(f"   └─ Connect to: {rec.should_connect_to}")
            print(f"   └─ Expected signal: {rec.signal_at_location:.0f} dBm")
            print(f"   └─ Why:")
            for reason in rec.reasoning:
                print(f"      • {reason}")

        print("\n" + "=" * 70)
        print("💡 GENERAL TIPS:")
        print("=" * 70)
        print("""
   1. TEST BEFORE PERMANENT PLACEMENT
      - Use your phone's WiFi signal meter
      - Walk around to verify coverage improvement

   2. OPTIMAL HEIGHT
      - Place repeaters at desk/shelf height (3-4 feet)
      - Not on floor, not at ceiling

   3. AVOID INTERFERENCE
      - Keep away from: microwaves, baby monitors, cordless phones
      - Minimize walls between devices (especially concrete/brick)
      - Metal objects and mirrors reflect/block signal

   4. SAME SSID VS DIFFERENT SSID
      - Same SSID: Seamless roaming (devices auto-switch)
      - Different SSID: Manual control over which network you connect to
      - Recommendation: Use SAME SSID for convenience

   5. CHANNEL CONFIGURATION
      - All devices should use SAME channel
      - Different channels cause interference, not isolation
""")
        print("=" * 70)
