#!/usr/bin/env python3
"""
WiFi Optimizer - Interactive CLI

A tool to optimize your home WiFi network by:
- Scanning for networks and analyzing interference
- Collecting signal measurements at different locations
- Recommending optimal channel settings
- Suggesting repeater placement
"""

import sys
import os
from typing import List, Optional

from .models.network import NetworkDevice, Location, DeviceType
from .models.config import NetworkConfig
from .scanners.wifi_scanner import get_scanner, print_scan_results
from .collectors.measurement_collector import MeasurementCollector
from .analyzers.channel_analyzer import ChannelAnalyzer
from .analyzers.placement_advisor import PlacementAdvisor


class WiFiOptimizerCLI:
    """Interactive CLI for WiFi optimization."""

    def __init__(self):
        self.config = NetworkConfig()
        self.scanner = get_scanner()
        self.collector = MeasurementCollector(self.scanner)
        self.channel_analyzer = ChannelAnalyzer()
        self.placement_advisor = PlacementAdvisor(self.collector)

    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print application header."""
        print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    📡  WiFi Optimizer v1.0  📡                       ║
║              Home Network Optimization Tool                          ║
╚══════════════════════════════════════════════════════════════════════╝
        """)

    def print_menu(self):
        """Print main menu."""
        print("""
┌──────────────────────────────────────────────────────────────────────┐
│  MAIN MENU                                                           │
├──────────────────────────────────────────────────────────────────────┤
│  1. Setup Devices     - Define your routers and repeaters            │
│  2. Setup Locations   - Define rooms/areas to measure                │
│  3. Scan Networks     - Scan for WiFi networks nearby                │
│  4. Collect Data      - Measure signal at each location              │
│  5. Analyze Channels  - Find optimal channel settings                │
│  6. Placement Advice  - Get repeater placement recommendations       │
│  7. Full Report       - Generate complete optimization report        │
│  8. View Config       - Show current configuration                   │
│  9. Save/Load         - Save or load your configuration              │
│  0. Exit                                                             │
└──────────────────────────────────────────────────────────────────────┘
        """)

    def get_input(self, prompt: str, default: str = None) -> str:
        """Get user input with optional default."""
        if default:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "

        try:
            value = input(prompt).strip()
            return value if value else (default or "")
        except (EOFError, KeyboardInterrupt):
            print("\n")
            return default or ""

    def get_int_input(self, prompt: str, default: int = None) -> Optional[int]:
        """Get integer input."""
        value = self.get_input(prompt, str(default) if default else None)
        try:
            return int(value) if value else default
        except ValueError:
            print("Invalid number, using default.")
            return default

    def setup_devices(self):
        """Interactive device setup."""
        print("\n" + "=" * 60)
        print("DEVICE SETUP")
        print("=" * 60)
        print("\nLet's set up your network devices.\n")

        # Main Router
        print("📡 MAIN ROUTER (ISP Router - e.g., Airtel)")
        print("-" * 40)
        name = self.get_input("Device name", "Airtel Main Router")
        ssid = self.get_input("WiFi SSID (network name)")
        ip = self.get_input("Router IP address", "192.168.1.1")

        main_router = NetworkDevice(
            name=name,
            device_type=DeviceType.MAIN_ROUTER,
            ssid=ssid,
            ip_address=ip,
            admin_url=f"http://{ip}"
        )
        self.config.add_device(main_router)
        print(f"✓ Added: {name}")

        # Repeaters
        num_repeaters = self.get_int_input("\nHow many repeaters do you have?", 2)

        for i in range(num_repeaters):
            print(f"\n📶 REPEATER {i + 1} (e.g., Tenda)")
            print("-" * 40)
            name = self.get_input("Device name", f"Tenda Repeater {i + 1}")
            rep_ssid = self.get_input("SSID (same as main or different?)", ssid)

            repeater = NetworkDevice(
                name=name,
                device_type=DeviceType.REPEATER,
                ssid=rep_ssid
            )
            self.config.add_device(repeater)
            print(f"✓ Added: {name}")

        # Set SSIDs for tracking
        ssids = list(set([d.ssid for d in self.config.devices if d.ssid]))
        self.collector.set_your_networks(ssids)
        self.channel_analyzer.set_your_ssids(ssids)

        print("\n✓ Device setup complete!")
        input("\nPress Enter to continue...")

    def setup_locations(self):
        """Interactive location setup."""
        print("\n" + "=" * 60)
        print("LOCATION SETUP")
        print("=" * 60)
        print("\nDefine the locations where you want to measure WiFi signal.")
        print("These should be places where you use WiFi most often.\n")

        print("Enter locations one at a time. Type 'done' when finished.\n")

        while True:
            name = self.get_input("Location name (or 'done' to finish)")
            if name.lower() == 'done':
                break
            if not name:
                continue

            priority = self.get_int_input(
                "Priority (1=highest, 3=lowest)", 2
            )

            location = Location(
                name=name,
                priority=priority
            )
            self.config.add_location(location)
            print(f"✓ Added: {name}\n")

        print(f"\n✓ Added {len(self.config.locations)} locations!")
        input("\nPress Enter to continue...")

    def scan_networks(self):
        """Scan for nearby WiFi networks."""
        print("\n" + "=" * 60)
        print("SCANNING FOR WIFI NETWORKS...")
        print("=" * 60)

        networks = self.scanner.scan()
        self.channel_analyzer.set_networks(networks)

        # Get your SSIDs
        your_ssids = [d.ssid for d in self.config.devices if d.ssid]
        print_scan_results(networks, your_ssids)

        input("\nPress Enter to continue...")

    def collect_measurements(self):
        """Collect signal measurements at each location."""
        if not self.config.locations:
            print("\n⚠️  No locations configured. Please set up locations first.")
            input("\nPress Enter to continue...")
            return

        print("\n" + "=" * 60)
        print("SIGNAL MEASUREMENT COLLECTION")
        print("=" * 60)
        print("\nYou'll need to move your laptop to each location.")
        print("Take your laptop to each location and press Enter to measure.\n")

        for i, location in enumerate(self.config.locations, 1):
            print(f"\n📍 Location {i}/{len(self.config.locations)}: {location.name}")
            print("-" * 40)

            ready = self.get_input(
                f"Move to '{location.name}' and press Enter to measure (or 's' to skip)"
            )

            if ready.lower() == 's':
                print(f"   Skipped {location.name}")
                continue

            self.collector.collect_at_location(location, num_samples=2)

        print("\n✓ Measurement collection complete!")
        self.collector.print_coverage_report()

        input("\nPress Enter to continue...")

    def analyze_channels(self):
        """Analyze channels and show recommendations."""
        print("\n" + "=" * 60)
        print("CHANNEL ANALYSIS")
        print("=" * 60)
        print("\nScanning networks to analyze channel usage...")

        networks = self.scanner.scan()
        self.channel_analyzer.set_networks(networks)

        self.channel_analyzer.print_channel_analysis()
        self.channel_analyzer.print_recommendations()

        input("\nPress Enter to continue...")

    def placement_advice(self):
        """Show repeater placement recommendations."""
        num_repeaters = len(self.config.get_repeaters())
        if num_repeaters == 0:
            num_repeaters = 2

        self.placement_advisor.set_devices(self.config.devices)
        self.placement_advisor.print_placement_report(num_repeaters)

        input("\nPress Enter to continue...")

    def full_report(self):
        """Generate and display full optimization report."""
        print("\n" + "=" * 70)
        print("📊 COMPLETE WIFI OPTIMIZATION REPORT")
        print("=" * 70)

        # Step 1: Current Configuration
        self.config.print_summary()

        # Step 2: Network Scan
        print("\n🔍 Scanning networks...")
        networks = self.scanner.scan()
        self.channel_analyzer.set_networks(networks)
        your_ssids = [d.ssid for d in self.config.devices if d.ssid]
        print_scan_results(networks, your_ssids)

        # Step 3: Channel Analysis
        self.channel_analyzer.print_channel_analysis()
        self.channel_analyzer.print_recommendations()

        # Step 4: Coverage Report (if measurements exist)
        if self.collector.location_data:
            self.collector.print_coverage_report()

            # Weak spots
            weak_spots = self.collector.find_weak_spots()
            if weak_spots:
                print("\n⚠️  Weak Signal Locations:")
                for loc, ssid, signal in weak_spots[:5]:
                    print(f"   - {loc}: {signal:.0f} dBm ({ssid})")

        # Step 5: Placement Recommendations
        self.placement_advisor.set_devices(self.config.devices)
        self.placement_advisor.print_placement_report(
            len(self.config.get_repeaters()) or 2
        )

        # Step 6: Action Items
        print("\n" + "=" * 70)
        print("✅ ACTION ITEMS - DO THESE IN ORDER")
        print("=" * 70)

        recs = self.channel_analyzer.get_configuration_recommendations()

        print(f"""
   1. LOGIN TO AIRTEL ROUTER ({self.config.get_main_router().ip_address if self.config.get_main_router() else '192.168.1.1'})
      - Change 2.4GHz channel to: {recs['2.4GHz']['channel']}
      - Change 2.4GHz width to: 20 MHz
      - Change 5GHz channel to: {recs['5GHz']['channel']}
      - Change 5GHz width to: 40 MHz

   2. PLACE TENDA REPEATER 1
      - Location: See recommendations above
      - Configure same SSID as main router
      - Set same channels as main router

   3. PLACE TENDA REPEATER 2
      - Location: See recommendations above
      - Configure same SSID
      - Set same channels

   4. TEST COVERAGE
      - Walk around with phone
      - Verify signal improvement
      - Adjust placement if needed

   5. FINAL OPTIMIZATION
      - After 24 hours, re-scan for channels
      - Neighbors may change their settings
      - Re-run this tool to verify
""")
        print("=" * 70)

        input("\nPress Enter to continue...")

    def view_config(self):
        """Show current configuration."""
        self.config.print_summary()
        input("\nPress Enter to continue...")

    def save_load_menu(self):
        """Save or load configuration."""
        print("\n" + "=" * 60)
        print("SAVE/LOAD CONFIGURATION")
        print("=" * 60)
        print("\n1. Save configuration")
        print("2. Load configuration")
        print("3. Back to main menu")

        choice = self.get_input("\nChoice", "3")

        if choice == "1":
            filepath = self.get_input("Save to file", "wifi_config.json")
            self.config.save(filepath)
            self.collector.save(filepath.replace('.json', '_measurements.json'))
        elif choice == "2":
            filepath = self.get_input("Load from file", "wifi_config.json")
            self.config = NetworkConfig.load(filepath)
            # Update references
            ssids = [d.ssid for d in self.config.devices if d.ssid]
            self.collector.set_your_networks(ssids)
            self.channel_analyzer.set_your_ssids(ssids)
            self.placement_advisor.set_devices(self.config.devices)

        input("\nPress Enter to continue...")

    def quick_start(self):
        """Quick start wizard for first-time users."""
        self.clear_screen()
        self.print_header()

        print("""
┌──────────────────────────────────────────────────────────────────────┐
│  🚀 QUICK START WIZARD                                               │
│                                                                      │
│  This wizard will help you:                                          │
│  1. Set up your devices (router + repeaters)                         │
│  2. Define locations to measure                                      │
│  3. Scan your WiFi environment                                       │
│  4. Get optimization recommendations                                 │
└──────────────────────────────────────────────────────────────────────┘
        """)

        proceed = self.get_input("Start quick setup? (y/n)", "y")
        if proceed.lower() != 'y':
            return

        # Step 1: Devices
        self.setup_devices()

        # Step 2: Locations
        self.clear_screen()
        self.print_header()
        print("\n📍 Now let's define the locations in your home.\n")
        print("Common locations: Living Room, Bedroom, Kitchen, Study, Balcony\n")
        self.setup_locations()

        # Step 3: Scan
        self.clear_screen()
        self.print_header()
        self.scan_networks()

        # Step 4: Collect measurements?
        self.clear_screen()
        self.print_header()
        print("\n" + "=" * 60)
        print("COLLECT MEASUREMENTS?")
        print("=" * 60)
        print("""
   For best recommendations, you should collect signal measurements
   at each location. This requires moving your laptop around.

   Skip this if you just want quick channel recommendations.
        """)

        collect = self.get_input("Collect measurements now? (y/n)", "n")
        if collect.lower() == 'y':
            self.collect_measurements()

        # Step 5: Show report
        self.clear_screen()
        self.print_header()
        self.full_report()

    def run(self):
        """Main application loop."""
        # Check for existing config
        if os.path.exists("wifi_config.json"):
            self.config = NetworkConfig.load("wifi_config.json")
            ssids = [d.ssid for d in self.config.devices if d.ssid]
            self.collector.set_your_networks(ssids)
            self.channel_analyzer.set_your_ssids(ssids)

        # First run?
        if not self.config.devices:
            self.quick_start()

        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()

            choice = self.get_input("Select option", "0")

            if choice == "1":
                self.setup_devices()
            elif choice == "2":
                self.setup_locations()
            elif choice == "3":
                self.scan_networks()
            elif choice == "4":
                self.collect_measurements()
            elif choice == "5":
                self.analyze_channels()
            elif choice == "6":
                self.placement_advice()
            elif choice == "7":
                self.full_report()
            elif choice == "8":
                self.view_config()
            elif choice == "9":
                self.save_load_menu()
            elif choice == "0":
                print("\n👋 Goodbye! Happy optimizing!\n")
                break
            else:
                print("Invalid option. Please try again.")
                input("\nPress Enter to continue...")


def main():
    """Entry point."""
    try:
        cli = WiFiOptimizerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
