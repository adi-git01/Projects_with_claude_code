"""
Collects WiFi signal measurements at different locations.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field

from ..models.network import WiFiNetwork, Location, Measurement, FrequencyBand
from ..scanners.wifi_scanner import WiFiScanner, get_scanner


@dataclass
class LocationMeasurements:
    """Stores all measurements for a specific location."""
    location: Location
    measurements: List[Measurement] = field(default_factory=list)

    def get_networks_by_ssid(self) -> Dict[str, List[Measurement]]:
        """Group measurements by SSID."""
        by_ssid = {}
        for m in self.measurements:
            if m.network.ssid not in by_ssid:
                by_ssid[m.network.ssid] = []
            by_ssid[m.network.ssid].append(m)
        return by_ssid

    def get_best_signal_for_ssid(self, ssid: str) -> Optional[int]:
        """Get the best signal strength for a given SSID."""
        signals = [m.network.signal_dbm for m in self.measurements if m.network.ssid == ssid]
        return max(signals) if signals else None

    def get_avg_signal_for_ssid(self, ssid: str) -> Optional[float]:
        """Get average signal strength for a given SSID."""
        signals = [m.network.signal_dbm for m in self.measurements if m.network.ssid == ssid]
        return sum(signals) / len(signals) if signals else None


class MeasurementCollector:
    """Collects and manages WiFi measurements across locations."""

    def __init__(self, scanner: WiFiScanner = None, data_file: str = "wifi_measurements.json"):
        self.scanner = scanner or get_scanner()
        self.data_file = data_file
        self.location_data: Dict[str, LocationMeasurements] = {}
        self.your_ssids: List[str] = []

    def set_your_networks(self, ssids: List[str]):
        """Set the SSIDs of your networks to track."""
        self.your_ssids = ssids

    def collect_at_location(self, location: Location, num_samples: int = 3) -> LocationMeasurements:
        """
        Collect WiFi measurements at a specific location.
        Takes multiple samples and averages them for accuracy.
        """
        print(f"\n📍 Collecting measurements at: {location.name}")
        print(f"   Taking {num_samples} samples...")

        if location.name not in self.location_data:
            self.location_data[location.name] = LocationMeasurements(location=location)

        loc_measurements = self.location_data[location.name]

        for i in range(num_samples):
            print(f"   Sample {i + 1}/{num_samples}...", end=" ", flush=True)
            networks = self.scanner.scan()

            for network in networks:
                measurement = Measurement(
                    location=location,
                    network=network,
                    timestamp=datetime.now()
                )
                loc_measurements.measurements.append(measurement)

            print(f"Found {len(networks)} networks")

            # Small delay between samples (handled by scanner)

        print(f"   ✓ Collection complete at {location.name}")
        return loc_measurements

    def get_signal_map(self) -> Dict[str, Dict[str, float]]:
        """
        Generate a signal map: location -> SSID -> average signal.
        """
        signal_map = {}
        for loc_name, loc_data in self.location_data.items():
            signal_map[loc_name] = {}
            by_ssid = loc_data.get_networks_by_ssid()

            for ssid, measurements in by_ssid.items():
                signals = [m.network.signal_dbm for m in measurements]
                signal_map[loc_name][ssid] = sum(signals) / len(signals)

        return signal_map

    def get_your_networks_coverage(self) -> Dict[str, Dict[str, float]]:
        """Get coverage map for only your networks."""
        full_map = self.get_signal_map()
        filtered_map = {}

        for loc_name, ssid_signals in full_map.items():
            filtered_map[loc_name] = {
                ssid: signal
                for ssid, signal in ssid_signals.items()
                if ssid in self.your_ssids
            }

        return filtered_map

    def print_coverage_report(self):
        """Print a coverage report for your networks."""
        coverage = self.get_your_networks_coverage()

        print("\n" + "=" * 70)
        print("COVERAGE REPORT - YOUR NETWORKS")
        print("=" * 70)

        if not coverage:
            print("No measurements collected yet.")
            return

        # Header
        ssids = self.your_ssids
        header = f"{'Location':<20}"
        for ssid in ssids:
            header += f" {ssid[:15]:<17}"
        print(header)
        print("-" * 70)

        # Data rows
        for loc_name, signals in coverage.items():
            row = f"{loc_name:<20}"
            for ssid in ssids:
                if ssid in signals:
                    signal = signals[ssid]
                    quality = self._signal_to_quality(signal)
                    row += f" {signal:>4.0f} dBm ({quality:<6})"
                else:
                    row += f" {'N/A':^17}"
            print(row)

        print("=" * 70)
        print("\nSignal Quality Guide:")
        print("  Excellent: > -50 dBm  |  Good: -50 to -60  |  Fair: -60 to -70")
        print("  Weak: -70 to -80      |  Dead Zone: < -80 dBm")
        print()

    def _signal_to_quality(self, signal_dbm: float) -> str:
        """Convert signal to quality string."""
        if signal_dbm >= -50:
            return "Great"
        elif signal_dbm >= -60:
            return "Good"
        elif signal_dbm >= -70:
            return "Fair"
        elif signal_dbm >= -80:
            return "Weak"
        else:
            return "Dead"

    def find_weak_spots(self, threshold_dbm: int = -70) -> List[tuple]:
        """Find locations with weak signal for your networks."""
        weak_spots = []
        coverage = self.get_your_networks_coverage()

        for loc_name, signals in coverage.items():
            for ssid, signal in signals.items():
                if signal < threshold_dbm:
                    weak_spots.append((loc_name, ssid, signal))

        return sorted(weak_spots, key=lambda x: x[2])

    def find_dead_zones(self) -> List[str]:
        """Find locations where none of your networks have good signal."""
        dead_zones = []
        coverage = self.get_your_networks_coverage()

        for loc_name, signals in coverage.items():
            if not signals:
                dead_zones.append(loc_name)
                continue

            best_signal = max(signals.values()) if signals else -100
            if best_signal < -80:
                dead_zones.append(loc_name)

        return dead_zones

    def save(self, filepath: str = None):
        """Save measurements to file."""
        filepath = filepath or self.data_file
        data = {
            'your_ssids': self.your_ssids,
            'locations': {}
        }

        for loc_name, loc_data in self.location_data.items():
            data['locations'][loc_name] = {
                'location': loc_data.location.to_dict(),
                'measurements': [m.to_dict() for m in loc_data.measurements]
            }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Measurements saved to {filepath}")

    def load(self, filepath: str = None):
        """Load measurements from file."""
        filepath = filepath or self.data_file
        if not os.path.exists(filepath):
            print(f"No existing data file found at {filepath}")
            return

        with open(filepath, 'r') as f:
            data = json.load(f)

        self.your_ssids = data.get('your_ssids', [])
        # Note: Full reconstruction would require more complex deserialization
        print(f"Loaded data from {filepath}")
        print(f"Your SSIDs: {self.your_ssids}")
