"""
Data models for WiFi networks, devices, and measurements.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DeviceType(Enum):
    MAIN_ROUTER = "main_router"
    REPEATER = "repeater"
    ACCESS_POINT = "access_point"


class FrequencyBand(Enum):
    BAND_2_4GHZ = "2.4GHz"
    BAND_5GHZ = "5GHz"
    BAND_6GHZ = "6GHz"


@dataclass
class WiFiNetwork:
    """Represents a detected WiFi network."""
    ssid: str
    bssid: str  # MAC address
    signal_dbm: int  # Signal strength in dBm
    channel: int
    frequency: int  # MHz
    frequency_band: FrequencyBand
    security: str
    channel_width: Optional[int] = None  # MHz (20, 40, 80, 160)

    @property
    def signal_quality(self) -> str:
        """Human-readable signal quality."""
        if self.signal_dbm >= -50:
            return "Excellent"
        elif self.signal_dbm >= -60:
            return "Good"
        elif self.signal_dbm >= -70:
            return "Fair"
        elif self.signal_dbm >= -80:
            return "Weak"
        else:
            return "Dead Zone"

    @property
    def signal_percentage(self) -> int:
        """Convert dBm to percentage (approximate)."""
        # -30 dBm = 100%, -90 dBm = 0%
        percentage = min(100, max(0, 2 * (self.signal_dbm + 100)))
        return percentage


@dataclass
class NetworkDevice:
    """Represents a router or repeater in your network."""
    name: str  # User-friendly name (e.g., "Airtel Main", "Tenda Living Room")
    device_type: DeviceType
    ssid: str
    bssid: Optional[str] = None  # MAC address if known
    ip_address: Optional[str] = None
    admin_url: Optional[str] = None
    current_channel_2_4: Optional[int] = None
    current_channel_5: Optional[int] = None
    channel_width_2_4: Optional[int] = 20
    channel_width_5: Optional[int] = 40

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'device_type': self.device_type.value,
            'ssid': self.ssid,
            'bssid': self.bssid,
            'ip_address': self.ip_address,
            'admin_url': self.admin_url,
            'current_channel_2_4': self.current_channel_2_4,
            'current_channel_5': self.current_channel_5,
            'channel_width_2_4': self.channel_width_2_4,
            'channel_width_5': self.channel_width_5
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'NetworkDevice':
        data['device_type'] = DeviceType(data['device_type'])
        return cls(**data)


@dataclass
class Location:
    """Represents a physical location in your home."""
    name: str  # e.g., "Living Room", "Bedroom 1", "Kitchen"
    description: Optional[str] = None
    priority: int = 1  # 1 = highest priority, need best coverage here
    floor: int = 0  # Floor number (0 = ground floor)

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'priority': self.priority,
            'floor': self.floor
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Location':
        return cls(**data)


@dataclass
class Measurement:
    """A WiFi signal measurement at a specific location."""
    location: Location
    network: WiFiNetwork
    timestamp: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            'location': self.location.to_dict(),
            'ssid': self.network.ssid,
            'bssid': self.network.bssid,
            'signal_dbm': self.network.signal_dbm,
            'channel': self.network.channel,
            'frequency': self.network.frequency,
            'frequency_band': self.network.frequency_band.value,
            'signal_quality': self.network.signal_quality,
            'timestamp': self.timestamp.isoformat(),
            'notes': self.notes
        }


@dataclass
class ChannelInfo:
    """Information about a WiFi channel."""
    channel: int
    frequency: int
    band: FrequencyBand
    networks_count: int = 0
    avg_signal: float = 0.0
    interference_score: float = 0.0  # 0 = no interference, 100 = heavy interference

    @property
    def is_recommended(self) -> bool:
        """Non-overlapping channels for 2.4GHz are 1, 6, 11."""
        if self.band == FrequencyBand.BAND_2_4GHZ:
            return self.channel in [1, 6, 11]
        return True  # All 5GHz channels are non-overlapping
