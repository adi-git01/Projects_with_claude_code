"""
Stock data model for monitoring metrics and alerts
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Stock:
    """Represents a stock with its trading metrics and strategy"""

    ticker: str
    strategy: str
    trend_score: str
    quality_score: Optional[float]
    value_score: Optional[float]
    forensic_verdict: str
    action: str
    entry_zone_min: Optional[float]
    entry_zone_max: Optional[float]
    stop_loss: Optional[float]
    target: Optional[float]
    notes: str = ""

    # Runtime data
    current_price: Optional[float] = None
    last_checked: Optional[datetime] = None
    alert_triggered: bool = False
    last_alert_time: Optional[datetime] = None

    @property
    def ticker_symbol(self) -> str:
        """Get the ticker symbol with .NS suffix for NSE stocks"""
        if not self.ticker.endswith('.NS'):
            return f"{self.ticker}.NS"
        return self.ticker

    def is_in_entry_zone(self, price: float) -> bool:
        """Check if current price is in entry zone"""
        if self.entry_zone_min is None or self.entry_zone_max is None:
            return False
        return self.entry_zone_min <= price <= self.entry_zone_max

    def is_below_entry_zone(self, price: float) -> bool:
        """Check if price is below entry zone"""
        if self.entry_zone_min is None:
            return False
        return price < self.entry_zone_min

    def is_above_entry_zone(self, price: float) -> bool:
        """Check if price is above entry zone"""
        if self.entry_zone_max is None:
            return False
        return price > self.entry_zone_max

    def hit_stop_loss(self, price: float) -> bool:
        """Check if stop loss is hit"""
        if self.stop_loss is None:
            return False
        return price <= self.stop_loss

    def hit_target(self, price: float) -> bool:
        """Check if target is hit"""
        if self.target is None:
            return False
        return price >= self.target

    def get_alert_conditions(self, price: float) -> list[str]:
        """Get list of triggered alert conditions"""
        alerts = []

        if self.is_in_entry_zone(price):
            alerts.append(f"IN ENTRY ZONE (₹{self.entry_zone_min}-₹{self.entry_zone_max})")

        if self.hit_stop_loss(price):
            alerts.append(f"STOP LOSS HIT (₹{self.stop_loss})")

        if self.hit_target(price):
            alerts.append(f"TARGET REACHED (₹{self.target})")

        # Price distance from entry zone
        if self.entry_zone_min and price < self.entry_zone_min:
            diff_pct = ((self.entry_zone_min - price) / price) * 100
            if diff_pct <= 5:  # Within 5% of entry
                alerts.append(f"NEAR ENTRY ZONE (₹{price:.2f}, {diff_pct:.1f}% below)")

        return alerts

    def __str__(self) -> str:
        return f"{self.ticker} | {self.strategy} | Action: {self.action} | CMP: ₹{self.current_price}"
