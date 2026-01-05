#!/usr/bin/env python3
"""
Stock Monitor - Automated monitoring and alerting for stock metrics
"""
import os
import sys
import logging
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore, Style, init

from src.services.monitor import StockMonitor

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def is_market_hours() -> bool:
    """Check if current time is within market hours"""
    now = datetime.now()
    market_open_hour = int(os.getenv('MARKET_OPEN_HOUR', '9'))
    market_close_hour = int(os.getenv('MARKET_CLOSE_HOUR', '15'))
    market_close_minute = int(os.getenv('MARKET_CLOSE_MINUTE', '30'))

    # Skip weekends
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False

    # Check time
    if now.hour < market_open_hour:
        return False
    if now.hour > market_close_hour:
        return False
    if now.hour == market_close_hour and now.minute > market_close_minute:
        return False

    return True


def run_monitoring():
    """Run a monitoring cycle"""
    try:
        # Check if within market hours
        if not is_market_hours():
            logger.info("Outside market hours. Skipping monitoring cycle.")
            return

        logger.info("="*80)
        logger.info("Starting monitoring cycle...")
        logger.info("="*80)

        # Create monitor and load stocks
        monitor = StockMonitor()

        if not monitor.load_stocks():
            logger.error("Failed to load stocks. Exiting.")
            return

        # Run monitoring
        alerts_count, errors_count = monitor.monitor_all()

        # Display summary
        monitor.alerter.send_summary(
            total_stocks=len(monitor.stocks),
            alerts_count=alerts_count,
            errors_count=errors_count
        )

        # Save state
        monitor.save_state()

        # Display stock status
        print("\n" + monitor.get_stock_status() + "\n")

    except Exception as e:
        logger.error(f"Error in monitoring cycle: {str(e)}", exc_info=True)


def run_once():
    """Run monitoring once and exit"""
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Stock Monitor - Single Run Mode")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

    run_monitoring()


def run_scheduled():
    """Run monitoring on a schedule"""
    interval_minutes = int(os.getenv('CHECK_INTERVAL_MINUTES', '15'))

    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Stock Monitor - Scheduled Mode")
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.GREEN}Monitoring every {interval_minutes} minutes")
    print(f"{Fore.GREEN}Market hours: 9:00 AM - 3:30 PM (Mon-Fri)")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

    # Schedule the monitoring job
    schedule.every(interval_minutes).minutes.do(run_monitoring)

    # Run once immediately
    run_monitoring()

    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Monitoring stopped by user.{Style.RESET_ALL}")
        sys.exit(0)


def main():
    """Main entry point"""
    # Create logs directory
    os.makedirs('logs', exist_ok=True)

    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'once':
            run_once()
        elif command == 'status':
            monitor = StockMonitor()
            if monitor.load_stocks():
                print(monitor.get_stock_status())
        elif command == 'help':
            print(f"""
{Fore.CYAN}Stock Monitor - Usage{Style.RESET_ALL}

Commands:
  python main.py              Run in scheduled monitoring mode
  python main.py once         Run monitoring once and exit
  python main.py status       Show current status of all stocks
  python main.py help         Show this help message

Configuration:
  Edit .env file to configure monitoring settings
  Edit config/stocks.csv to add/remove stocks

For more information, see README.md
            """)
        else:
            print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")
            print(f"Run 'python main.py help' for usage information")
    else:
        # Default: run scheduled monitoring
        run_scheduled()


if __name__ == '__main__':
    main()
