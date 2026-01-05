"""
Alert service for stock monitoring notifications
"""
import logging
from datetime import datetime
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

logger = logging.getLogger(__name__)


class Alert:
    """Represents an alert event"""

    def __init__(self, ticker: str, price: float, conditions: List[str], timestamp: datetime = None):
        self.ticker = ticker
        self.price = price
        self.conditions = conditions
        self.timestamp = timestamp or datetime.now()

    def __str__(self) -> str:
        conditions_str = " | ".join(self.conditions)
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.ticker} @ ₹{self.price:.2f} - {conditions_str}"


class Alerter:
    """Handles various types of alerts and notifications"""

    def __init__(self):
        self.enable_email = os.getenv('ENABLE_EMAIL_ALERTS', 'false').lower() == 'true'
        self.email_from = os.getenv('EMAIL_FROM')
        self.email_to = os.getenv('EMAIL_TO')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.alert_log_file = 'logs/alerts.log'

    def send_alert(self, alert: Alert):
        """
        Send alert through all configured channels

        Args:
            alert: Alert object to send
        """
        # Console alert (always enabled)
        self._console_alert(alert)

        # File log (always enabled)
        self._log_alert(alert)

        # Email alert (if enabled)
        if self.enable_email:
            self._email_alert(alert)

    def send_multiple_alerts(self, alerts: List[Alert]):
        """Send multiple alerts"""
        if not alerts:
            return

        print(f"\n{Fore.YELLOW}{'='*80}")
        print(f"{Fore.YELLOW}ALERTS TRIGGERED: {len(alerts)} stock(s)")
        print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")

        for alert in alerts:
            self.send_alert(alert)

    def _console_alert(self, alert: Alert):
        """Print alert to console with colors"""
        color = Fore.GREEN

        # Choose color based on alert type
        if any('STOP LOSS' in cond for cond in alert.conditions):
            color = Fore.RED
        elif any('TARGET' in cond for cond in alert.conditions):
            color = Fore.GREEN
        elif any('ENTRY ZONE' in cond for cond in alert.conditions):
            color = Fore.CYAN

        print(f"{color}🔔 {alert}{Style.RESET_ALL}")

    def _log_alert(self, alert: Alert):
        """Write alert to log file"""
        try:
            os.makedirs(os.path.dirname(self.alert_log_file), exist_ok=True)
            with open(self.alert_log_file, 'a') as f:
                f.write(str(alert) + '\n')
        except Exception as e:
            logger.error(f"Failed to write alert to log: {str(e)}")

    def _email_alert(self, alert: Alert):
        """Send alert via email"""
        if not all([self.email_from, self.email_to, self.email_password]):
            logger.warning("Email credentials not configured")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = self.email_to
            msg['Subject'] = f"Stock Alert: {alert.ticker} - {', '.join(alert.conditions)}"

            body = f"""
Stock Alert Triggered!

Ticker: {alert.ticker}
Current Price: ₹{alert.price:.2f}
Conditions:
{chr(10).join('  - ' + cond for cond in alert.conditions)}

Timestamp: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

---
Automated Stock Monitor
            """

            msg.attach(MIMEText(body, 'plain'))

            # Send email using Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_from, self.email_password)
            server.send_message(msg)
            server.quit()

            logger.info(f"Email alert sent for {alert.ticker}")

        except Exception as e:
            logger.error(f"Failed to send email alert: {str(e)}")

    def send_summary(self, total_stocks: int, alerts_count: int, errors_count: int):
        """Send monitoring summary"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{Fore.BLUE}{'─'*80}")
        print(f"Monitoring Summary - {timestamp}")
        print(f"{'─'*80}")
        print(f"Total Stocks: {total_stocks}")
        print(f"Alerts Triggered: {Fore.YELLOW}{alerts_count}{Style.RESET_ALL}")
        print(f"Errors: {Fore.RED if errors_count > 0 else Fore.GREEN}{errors_count}{Style.RESET_ALL}")
        print(f"{'─'*80}{Style.RESET_ALL}\n")
