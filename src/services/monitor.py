"""
Stock monitoring service that checks prices and triggers alerts
"""
import logging
from typing import List
from datetime import datetime
import csv
from pathlib import Path

from src.models.stock import Stock
from src.services.price_fetcher import PriceFetcher
from src.services.alerter import Alerter, Alert

logger = logging.getLogger(__name__)


class StockMonitor:
    """Monitors stocks and triggers alerts based on configured conditions"""

    def __init__(self, config_file: str = 'config/stocks.csv'):
        self.config_file = config_file
        self.stocks: List[Stock] = []
        self.price_fetcher = PriceFetcher()
        self.alerter = Alerter()

    def load_stocks(self):
        """Load stock configuration from CSV file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.stocks = []

                for row in reader:
                    # Parse entry zone (can be single value or range)
                    entry_zone_min = None
                    entry_zone_max = None
                    entry_zone = row.get('entry_zone', '').strip()

                    if entry_zone:
                        if '-' in entry_zone or 'to' in entry_zone.lower():
                            # Range format: "₹80 - ₹84" or "80-84"
                            parts = entry_zone.replace('₹', '').replace('to', '-').split('-')
                            if len(parts) == 2:
                                try:
                                    entry_zone_min = float(parts[0].strip())
                                    entry_zone_max = float(parts[1].strip())
                                except ValueError:
                                    pass
                        else:
                            # Single value or "CMP" or "Above X"
                            if entry_zone.lower() not in ['cmp', 'watch', '---']:
                                try:
                                    # Extract number from formats like "₹525", ">₹525", "Above ₹3,950"
                                    clean_value = entry_zone.replace('₹', '').replace(',', '').replace('>', '').replace('Above', '').strip()
                                    value = float(clean_value)
                                    entry_zone_min = value
                                    entry_zone_max = value * 1.02  # 2% range
                                except ValueError:
                                    pass

                    # Parse other numeric fields
                    def parse_price(value: str) -> float:
                        if not value or value.strip() in ['---', 'Open', '']:
                            return None
                        try:
                            return float(value.replace('₹', '').replace(',', '').strip())
                        except ValueError:
                            return None

                    stock = Stock(
                        ticker=row.get('ticker', '').strip(),
                        strategy=row.get('strategy', '').strip(),
                        trend_score=row.get('trend_score', '').strip(),
                        quality_score=parse_price(row.get('quality_score', '')),
                        value_score=parse_price(row.get('value_score', '')),
                        forensic_verdict=row.get('forensic_verdict', '').strip(),
                        action=row.get('action', '').strip(),
                        entry_zone_min=entry_zone_min,
                        entry_zone_max=entry_zone_max,
                        stop_loss=parse_price(row.get('stop_loss', '')),
                        target=parse_price(row.get('target', '')),
                        notes=row.get('notes', '').strip()
                    )

                    if stock.ticker:
                        self.stocks.append(stock)

                logger.info(f"Loaded {len(self.stocks)} stocks from {self.config_file}")
                return True

        except FileNotFoundError:
            logger.error(f"Config file not found: {self.config_file}")
            return False
        except Exception as e:
            logger.error(f"Error loading stocks: {str(e)}")
            return False

    def monitor_all(self) -> tuple[int, int]:
        """
        Monitor all stocks and trigger alerts

        Returns:
            Tuple of (alerts_count, errors_count)
        """
        if not self.stocks:
            logger.warning("No stocks loaded. Call load_stocks() first.")
            return 0, 0

        alerts = []
        errors_count = 0

        logger.info(f"Monitoring {len(self.stocks)} stocks...")

        for stock in self.stocks:
            try:
                # Fetch current price
                price = self.price_fetcher.get_price(stock.ticker_symbol)

                if price is None:
                    errors_count += 1
                    continue

                # Update stock data
                stock.current_price = price
                stock.last_checked = datetime.now()

                # Check alert conditions
                conditions = stock.get_alert_conditions(price)

                if conditions:
                    alert = Alert(
                        ticker=stock.ticker,
                        price=price,
                        conditions=conditions
                    )
                    alerts.append(alert)
                    stock.alert_triggered = True
                    stock.last_alert_time = datetime.now()

            except Exception as e:
                logger.error(f"Error monitoring {stock.ticker}: {str(e)}")
                errors_count += 1

        # Send all alerts
        if alerts:
            self.alerter.send_multiple_alerts(alerts)

        return len(alerts), errors_count

    def get_stock_status(self) -> str:
        """Get formatted status of all stocks"""
        from tabulate import tabulate

        if not self.stocks:
            return "No stocks loaded"

        headers = ['Ticker', 'Strategy', 'CMP', 'Entry Zone', 'Stop Loss', 'Target', 'Status']
        rows = []

        for stock in self.stocks:
            entry_zone = ''
            if stock.entry_zone_min and stock.entry_zone_max:
                if stock.entry_zone_min == stock.entry_zone_max:
                    entry_zone = f"₹{stock.entry_zone_min:.0f}"
                else:
                    entry_zone = f"₹{stock.entry_zone_min:.0f}-₹{stock.entry_zone_max:.0f}"

            cmp = f"₹{stock.current_price:.2f}" if stock.current_price else "---"
            stop_loss = f"₹{stock.stop_loss:.0f}" if stock.stop_loss else "---"
            target = f"₹{stock.target:.0f}" if stock.target else "---"

            # Status
            status = "⚪ Watching"
            if stock.current_price:
                if stock.hit_target(stock.current_price):
                    status = "🎯 Target Hit"
                elif stock.hit_stop_loss(stock.current_price):
                    status = "🛑 Stop Loss"
                elif stock.is_in_entry_zone(stock.current_price):
                    status = "✅ In Entry Zone"

            rows.append([
                stock.ticker,
                stock.strategy,
                cmp,
                entry_zone,
                stop_loss,
                target,
                status
            ])

        return tabulate(rows, headers=headers, tablefmt='grid')

    def save_state(self, filename: str = 'logs/monitor_state.csv'):
        """Save current state of all stocks"""
        try:
            Path('logs').mkdir(exist_ok=True)

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'ticker', 'current_price', 'last_checked', 'alert_triggered', 'last_alert_time'
                ])

                for stock in self.stocks:
                    writer.writerow([
                        stock.ticker,
                        stock.current_price or '',
                        stock.last_checked.isoformat() if stock.last_checked else '',
                        stock.alert_triggered,
                        stock.last_alert_time.isoformat() if stock.last_alert_time else ''
                    ])

            logger.info(f"State saved to {filename}")

        except Exception as e:
            logger.error(f"Failed to save state: {str(e)}")
