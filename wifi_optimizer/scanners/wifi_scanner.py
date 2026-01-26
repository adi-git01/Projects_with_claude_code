"""
WiFi network scanner using system tools.
Supports Linux (nmcli, iw, iwlist) and provides fallback for other platforms.
"""

import subprocess
import re
import platform
import shutil
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime

from ..models.network import WiFiNetwork, FrequencyBand


class WiFiScanner(ABC):
    """Abstract base class for WiFi scanners."""

    @abstractmethod
    def scan(self) -> List[WiFiNetwork]:
        """Scan for WiFi networks and return list of detected networks."""
        pass

    @abstractmethod
    def get_interface(self) -> Optional[str]:
        """Get the WiFi interface name."""
        pass

    def _determine_band(self, frequency: int) -> FrequencyBand:
        """Determine frequency band from frequency in MHz."""
        if frequency < 3000:
            return FrequencyBand.BAND_2_4GHZ
        elif frequency < 6000:
            return FrequencyBand.BAND_5GHZ
        else:
            return FrequencyBand.BAND_6GHZ

    def _frequency_to_channel(self, frequency: int) -> int:
        """Convert frequency (MHz) to channel number."""
        if frequency >= 2412 and frequency <= 2484:
            if frequency == 2484:
                return 14
            return (frequency - 2412) // 5 + 1
        elif frequency >= 5170 and frequency <= 5825:
            return (frequency - 5170) // 5 + 34
        elif frequency >= 5955 and frequency <= 7115:  # 6GHz
            return (frequency - 5955) // 5 + 1
        return 0


class NmcliScanner(WiFiScanner):
    """WiFi scanner using nmcli (NetworkManager CLI)."""

    def get_interface(self) -> Optional[str]:
        """Get WiFi interface using nmcli."""
        try:
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'DEVICE,TYPE', 'device'],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.strip().split('\n'):
                if ':wifi' in line:
                    return line.split(':')[0]
        except Exception:
            pass
        return None

    def scan(self) -> List[WiFiNetwork]:
        """Scan using nmcli."""
        networks = []
        try:
            # Rescan first
            subprocess.run(
                ['nmcli', 'device', 'wifi', 'rescan'],
                capture_output=True, timeout=15
            )

            # Get list of networks
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'SSID,BSSID,SIGNAL,FREQ,CHAN,SECURITY', 'device', 'wifi', 'list'],
                capture_output=True, text=True, timeout=15
            )

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                parts = line.split(':')
                if len(parts) >= 6:
                    try:
                        ssid = parts[0] or "<Hidden>"
                        bssid = ':'.join(parts[1:7])  # MAC has colons
                        # Adjust parsing for the MAC address
                        remaining = ':'.join(parts[7:])
                        remaining_parts = remaining.split(':')

                        signal_pct = int(remaining_parts[0]) if remaining_parts[0] else 0
                        freq_str = remaining_parts[1] if len(remaining_parts) > 1 else "2412"
                        chan_str = remaining_parts[2] if len(remaining_parts) > 2 else "1"
                        security = remaining_parts[3] if len(remaining_parts) > 3 else "Open"

                        # Convert signal % to dBm (approximate)
                        signal_dbm = int((signal_pct / 2) - 100)
                        frequency = int(freq_str.replace(' MHz', ''))
                        channel = int(chan_str) if chan_str.isdigit() else self._frequency_to_channel(frequency)

                        network = WiFiNetwork(
                            ssid=ssid,
                            bssid=bssid,
                            signal_dbm=signal_dbm,
                            channel=channel,
                            frequency=frequency,
                            frequency_band=self._determine_band(frequency),
                            security=security
                        )
                        networks.append(network)
                    except (ValueError, IndexError) as e:
                        continue

        except subprocess.TimeoutExpired:
            print("Warning: WiFi scan timed out")
        except Exception as e:
            print(f"Warning: nmcli scan failed: {e}")

        return networks


class IwScanner(WiFiScanner):
    """WiFi scanner using iw command."""

    def get_interface(self) -> Optional[str]:
        """Get WiFi interface using iw."""
        try:
            result = subprocess.run(
                ['iw', 'dev'],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split('\n'):
                if 'Interface' in line:
                    return line.split()[-1]
        except Exception:
            pass
        return None

    def scan(self) -> List[WiFiNetwork]:
        """Scan using iw."""
        networks = []
        interface = self.get_interface()
        if not interface:
            print("No WiFi interface found")
            return networks

        try:
            result = subprocess.run(
                ['sudo', 'iw', interface, 'scan'],
                capture_output=True, text=True, timeout=30
            )

            current_network = {}
            for line in result.stdout.split('\n'):
                line = line.strip()

                if line.startswith('BSS '):
                    if current_network.get('bssid'):
                        networks.append(self._create_network(current_network))
                    bssid_match = re.search(r'([0-9a-fA-F:]{17})', line)
                    current_network = {
                        'bssid': bssid_match.group(1) if bssid_match else '',
                        'ssid': '<Hidden>',
                        'signal_dbm': -100,
                        'frequency': 2412,
                        'channel': 1,
                        'security': 'Open'
                    }
                elif line.startswith('SSID:'):
                    ssid = line.replace('SSID:', '').strip()
                    current_network['ssid'] = ssid if ssid else '<Hidden>'
                elif line.startswith('signal:'):
                    signal_match = re.search(r'(-?\d+)', line)
                    if signal_match:
                        current_network['signal_dbm'] = int(signal_match.group(1))
                elif line.startswith('freq:'):
                    freq_match = re.search(r'(\d+)', line)
                    if freq_match:
                        current_network['frequency'] = int(freq_match.group(1))
                elif 'WPA' in line or 'RSN' in line:
                    current_network['security'] = 'WPA2/WPA3'
                elif 'WEP' in line:
                    current_network['security'] = 'WEP'

            if current_network.get('bssid'):
                networks.append(self._create_network(current_network))

        except subprocess.TimeoutExpired:
            print("Warning: WiFi scan timed out")
        except PermissionError:
            print("Warning: Need sudo for iw scan. Try running with sudo.")
        except Exception as e:
            print(f"Warning: iw scan failed: {e}")

        return networks

    def _create_network(self, data: dict) -> WiFiNetwork:
        """Create WiFiNetwork from parsed data."""
        frequency = data.get('frequency', 2412)
        return WiFiNetwork(
            ssid=data.get('ssid', '<Hidden>'),
            bssid=data.get('bssid', ''),
            signal_dbm=data.get('signal_dbm', -100),
            channel=self._frequency_to_channel(frequency),
            frequency=frequency,
            frequency_band=self._determine_band(frequency),
            security=data.get('security', 'Open')
        )


class MockScanner(WiFiScanner):
    """Mock scanner for testing or when no WiFi tools available."""

    def get_interface(self) -> Optional[str]:
        return "mock0"

    def scan(self) -> List[WiFiNetwork]:
        """Return mock networks for testing."""
        print("\n⚠️  Using MOCK scanner (no WiFi tools detected)")
        print("    Install nmcli or iw for real scanning\n")
        return [
            WiFiNetwork(
                ssid="Airtel_Home",
                bssid="AA:BB:CC:DD:EE:01",
                signal_dbm=-45,
                channel=6,
                frequency=2437,
                frequency_band=FrequencyBand.BAND_2_4GHZ,
                security="WPA2"
            ),
            WiFiNetwork(
                ssid="Airtel_Home_5G",
                bssid="AA:BB:CC:DD:EE:02",
                signal_dbm=-50,
                channel=36,
                frequency=5180,
                frequency_band=FrequencyBand.BAND_5GHZ,
                security="WPA2"
            ),
            WiFiNetwork(
                ssid="Neighbor_WiFi",
                bssid="11:22:33:44:55:01",
                signal_dbm=-70,
                channel=6,
                frequency=2437,
                frequency_band=FrequencyBand.BAND_2_4GHZ,
                security="WPA2"
            ),
            WiFiNetwork(
                ssid="Neighbor_5G",
                bssid="11:22:33:44:55:02",
                signal_dbm=-75,
                channel=36,
                frequency=5180,
                frequency_band=FrequencyBand.BAND_5GHZ,
                security="WPA2"
            ),
            WiFiNetwork(
                ssid="CoffeeShop",
                bssid="22:33:44:55:66:01",
                signal_dbm=-80,
                channel=11,
                frequency=2462,
                frequency_band=FrequencyBand.BAND_2_4GHZ,
                security="Open"
            ),
        ]


def get_scanner() -> WiFiScanner:
    """Get the appropriate scanner for the current system."""
    system = platform.system().lower()

    if system == 'linux':
        # Try nmcli first (most common on modern Linux)
        if shutil.which('nmcli'):
            scanner = NmcliScanner()
            if scanner.get_interface():
                return scanner

        # Try iw
        if shutil.which('iw'):
            scanner = IwScanner()
            if scanner.get_interface():
                return scanner

    # Fallback to mock scanner
    return MockScanner()


def print_scan_results(networks: List[WiFiNetwork], your_ssids: List[str] = None):
    """Pretty print scan results."""
    your_ssids = your_ssids or []

    print("\n" + "=" * 80)
    print("WIFI NETWORK SCAN RESULTS")
    print("=" * 80)
    print(f"{'SSID':<25} {'Signal':>8} {'Quality':<10} {'Ch':>4} {'Band':<8} {'Security':<15}")
    print("-" * 80)

    # Sort by signal strength
    sorted_networks = sorted(networks, key=lambda n: n.signal_dbm, reverse=True)

    for net in sorted_networks:
        marker = " ★" if net.ssid in your_ssids else ""
        signal_bar = "█" * (net.signal_percentage // 10) + "░" * (10 - net.signal_percentage // 10)

        print(f"{(net.ssid + marker):<25} {net.signal_dbm:>4} dBm {net.signal_quality:<10} "
              f"{net.channel:>4} {net.frequency_band.value:<8} {net.security:<15}")
        print(f"{'':>25} [{signal_bar}] {net.signal_percentage}%")

    print("=" * 80)
    print(f"Total networks found: {len(networks)}")
    if your_ssids:
        print(f"★ = Your networks")
    print()
