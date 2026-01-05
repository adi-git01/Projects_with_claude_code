"""
Stock data model for monitoring metrics and alerts
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime


@dataclass
class CustomCondition:
    """Represents a custom alert condition"""
    metric: str
    operator: str  # >, <, >=, <=, ==
    threshold: float
    description: str = ""

    def __str__(self) -> str:
        return f"{self.metric} {self.operator} {self.threshold}"


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
    custom_conditions: List[CustomCondition] = field(default_factory=list)

    # Runtime data
    current_price: Optional[float] = None
    last_checked: Optional[datetime] = None
    alert_triggered: bool = False
    last_alert_time: Optional[datetime] = None
    technical_indicators: Dict[str, Optional[float]] = field(default_factory=dict)
    custom_metrics: Dict[str, Optional[float]] = field(default_factory=dict)

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

    def check_custom_condition(self, condition: CustomCondition) -> tuple[bool, str]:
        """
        Check if a custom condition is met

        Returns:
            Tuple of (condition_met, alert_message)
        """
        # Check technical indicators
        if condition.metric in self.technical_indicators:
            value = self.technical_indicators[condition.metric]
            if value is None:
                return False, ""

            metric_name = condition.metric.upper()
            condition_met = self._evaluate_condition(value, condition.operator, condition.threshold)

            if condition_met:
                return True, f"{metric_name}={value:.2f} {condition.operator} {condition.threshold}"

        # Check custom metrics (commodity prices, forex, etc.)
        elif condition.metric in self.custom_metrics:
            value = self.custom_metrics[condition.metric]
            if value is None:
                return False, ""

            metric_name = condition.metric.replace('_', ' ').title()
            condition_met = self._evaluate_condition(value, condition.operator, condition.threshold)

            if condition_met:
                return True, f"{metric_name}={value:.2f} {condition.operator} {condition.threshold}"

        # Check price-based conditions
        elif condition.metric == 'price' and self.current_price:
            condition_met = self._evaluate_condition(self.current_price, condition.operator, condition.threshold)

            if condition_met:
                return True, f"Price ₹{self.current_price:.2f} {condition.operator} ₹{condition.threshold}"

        # Check fundamentals (PE ratio, market cap, etc.)
        elif condition.metric == 'pe_ratio' and self.quality_score:
            # Using quality_score as proxy for PE ratio
            condition_met = self._evaluate_condition(self.quality_score, condition.operator, condition.threshold)

            if condition_met:
                return True, f"PE Ratio {self.quality_score} {condition.operator} {condition.threshold}"

        return False, ""

    def _evaluate_condition(self, value: float, operator: str, threshold: float) -> bool:
        """Evaluate a comparison condition"""
        if operator == '>':
            return value > threshold
        elif operator == '<':
            return value < threshold
        elif operator == '>=':
            return value >= threshold
        elif operator == '<=':
            return value <= threshold
        elif operator == '==':
            return abs(value - threshold) < 0.01
        return False

    def get_alert_conditions(self, price: float) -> list[str]:
        """Get list of triggered alert conditions (ANY condition triggers alert)"""
        alerts = []

        # Standard price-based alerts
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

        # Check custom conditions (technical indicators, fundamentals, external metrics)
        for condition in self.custom_conditions:
            met, message = self.check_custom_condition(condition)
            if met:
                alerts.append(f"CUSTOM: {message}")

        return alerts

    def __str__(self) -> str:
        return f"{self.ticker} | {self.strategy} | Action: {self.action} | CMP: ₹{self.current_price}"
