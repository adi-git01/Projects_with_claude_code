#!/usr/bin/env python3
"""
WiFi Optimizer - Quick Start Script

Usage:
    python run_wifi_optimizer.py              # Interactive mode
    python run_wifi_optimizer.py --scan       # Quick scan only
    python run_wifi_optimizer.py --analyze    # Scan + channel analysis
    python run_wifi_optimizer.py --help       # Show help
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wifi_optimizer.scanners.wifi_scanner import get_scanner, print_scan_results
from wifi_optimizer.analyzers.channel_analyzer import ChannelAnalyzer
from wifi_optimizer.analyzers.placement_advisor import PlacementAdvisor
from wifi_optimizer.cli import WiFiOptimizerCLI


def quick_scan():
    """Perform a quick WiFi scan and show results."""
    print("\n📡 Quick WiFi Scan")
    print("=" * 60)

    scanner = get_scanner()
    networks = scanner.scan()
    print_scan_results(networks)

    return networks


def analyze_channels(networks=None):
    """Analyze channels and show recommendations."""
    if networks is None:
        scanner = get_scanner()
        networks = scanner.scan()

    analyzer = ChannelAnalyzer(networks)
    analyzer.print_channel_analysis()
    analyzer.print_recommendations()


def show_help():
    """Show help message."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    📡  WiFi Optimizer  📡                            ║
╚══════════════════════════════════════════════════════════════════════╝

USAGE:
    python run_wifi_optimizer.py [OPTIONS]

OPTIONS:
    (none)      Start interactive mode (recommended)
    --scan      Quick scan of nearby WiFi networks
    --analyze   Scan and analyze channels for best settings
    --help      Show this help message

EXAMPLES:
    python run_wifi_optimizer.py              # Full interactive wizard
    python run_wifi_optimizer.py --scan       # Just see nearby networks
    python run_wifi_optimizer.py --analyze    # Get channel recommendations

REQUIREMENTS:
    - Linux: nmcli (NetworkManager) or iw
    - Run with sudo for best results: sudo python run_wifi_optimizer.py

WHAT THIS TOOL DOES:
    1. Scans nearby WiFi networks
    2. Analyzes channel congestion and interference
    3. Collects signal measurements at different locations
    4. Recommends optimal channel settings for your router
    5. Suggests where to place your WiFi repeaters

FOR BEST RESULTS:
    1. Run the interactive mode
    2. Set up your devices (main router + repeaters)
    3. Define locations in your home
    4. Walk around and collect measurements
    5. Get personalized recommendations
    """)


def main():
    """Main entry point."""
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        show_help()
    elif '--scan' in args:
        quick_scan()
    elif '--analyze' in args:
        networks = quick_scan()
        analyze_channels(networks)
    else:
        # Interactive mode
        cli = WiFiOptimizerCLI()
        cli.run()


if __name__ == "__main__":
    main()
