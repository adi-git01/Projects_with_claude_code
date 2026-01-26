"""
Configuration management for the WiFi optimizer.
"""

import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path

from .network import NetworkDevice, Location, DeviceType


@dataclass
class NetworkConfig:
    """Stores the user's network configuration."""
    devices: List[NetworkDevice] = field(default_factory=list)
    locations: List[Location] = field(default_factory=list)
    config_file: str = "wifi_config.json"

    def add_device(self, device: NetworkDevice):
        """Add a network device."""
        # Remove existing device with same name
        self.devices = [d for d in self.devices if d.name != device.name]
        self.devices.append(device)

    def add_location(self, location: Location):
        """Add a location."""
        self.locations = [l for l in self.locations if l.name != location.name]
        self.locations.append(location)

    def get_main_router(self) -> Optional[NetworkDevice]:
        """Get the main ISP router."""
        for device in self.devices:
            if device.device_type == DeviceType.MAIN_ROUTER:
                return device
        return None

    def get_repeaters(self) -> List[NetworkDevice]:
        """Get all repeaters."""
        return [d for d in self.devices if d.device_type == DeviceType.REPEATER]

    def get_priority_locations(self) -> List[Location]:
        """Get locations sorted by priority."""
        return sorted(self.locations, key=lambda l: l.priority)

    def save(self, filepath: Optional[str] = None):
        """Save configuration to file."""
        filepath = filepath or self.config_file
        data = {
            'devices': [d.to_dict() for d in self.devices],
            'locations': [l.to_dict() for l in self.locations]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Configuration saved to {filepath}")

    @classmethod
    def load(cls, filepath: str = "wifi_config.json") -> 'NetworkConfig':
        """Load configuration from file."""
        config = cls(config_file=filepath)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
            config.devices = [NetworkDevice.from_dict(d) for d in data.get('devices', [])]
            config.locations = [Location.from_dict(l) for l in data.get('locations', [])]
            print(f"Configuration loaded from {filepath}")
        return config

    def print_summary(self):
        """Print a summary of the configuration."""
        print("\n" + "=" * 60)
        print("NETWORK CONFIGURATION SUMMARY")
        print("=" * 60)

        print("\nDevices:")
        if not self.devices:
            print("  No devices configured")
        for device in self.devices:
            print(f"  - {device.name} ({device.device_type.value})")
            print(f"    SSID: {device.ssid}")
            if device.bssid:
                print(f"    BSSID: {device.bssid}")
            if device.ip_address:
                print(f"    IP: {device.ip_address}")

        print("\nLocations:")
        if not self.locations:
            print("  No locations configured")
        for loc in sorted(self.locations, key=lambda l: l.priority):
            priority_str = "★" * (4 - min(loc.priority, 3))
            print(f"  - {loc.name} (Priority: {priority_str})")
            if loc.description:
                print(f"    {loc.description}")

        print("=" * 60 + "\n")
