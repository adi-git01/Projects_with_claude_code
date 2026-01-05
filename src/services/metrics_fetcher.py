"""
Custom metrics fetcher for external data (commodities, forex, indices)
"""
import logging
import requests
from typing import Optional, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class MetricsFetcher:
    """Fetches custom metrics like commodity prices, forex rates, indices"""

    def __init__(self):
        self.cache: Dict[str, tuple[float, datetime]] = {}
        self.cache_duration_seconds = 300  # Cache for 5 minutes

    def _get_yahoo_price(self, symbol: str) -> Optional[float]:
        """Fetch price from Yahoo Finance for any symbol"""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {'interval': '1d', 'range': '1d'}
            headers = {'User-Agent': 'Mozilla/5.0'}

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            result = data.get('chart', {}).get('result', [])

            if result and len(result) > 0:
                meta = result[0].get('meta', {})
                price = meta.get('regularMarketPrice')

                if price is None:
                    indicators = result[0].get('indicators', {}).get('quote', [])
                    if indicators and len(indicators) > 0:
                        closes = indicators[0].get('close', [])
                        if closes:
                            price = closes[-1]

                if price:
                    return float(price)

            return None

        except Exception as e:
            logger.debug(f"Error fetching {symbol}: {str(e)}")
            return None

    def get_metric(self, metric_name: str) -> Optional[float]:
        """
        Get value for a custom metric

        Supported metrics:
        - aluminum_lme: Aluminum LME price (USD/tonne)
        - copper_lme: Copper LME price
        - crude_oil: Crude oil price
        - gold: Gold price
        - silver: Silver price
        - usd_inr: USD to INR exchange rate
        - nifty50: Nifty 50 index
        - Any Yahoo Finance symbol

        Args:
            metric_name: Name of the metric

        Returns:
            Current value or None if fetch fails
        """
        # Check cache first
        if metric_name in self.cache:
            cached_value, cached_time = self.cache[metric_name]
            age = (datetime.now() - cached_time).total_seconds()
            if age < self.cache_duration_seconds:
                logger.debug(f"Using cached value for {metric_name}: {cached_value}")
                return cached_value

        # Map common metric names to Yahoo Finance symbols
        symbol_map = {
            'aluminum_lme': 'ALI=F',      # Aluminum futures
            'copper_lme': 'HG=F',         # Copper futures
            'crude_oil': 'CL=F',          # Crude oil futures
            'gold': 'GC=F',               # Gold futures
            'silver': 'SI=F',             # Silver futures
            'usd_inr': 'USDINR=X',        # USD/INR forex
            'nifty50': '^NSEI',           # Nifty 50
            'sensex': '^BSESN',           # BSE Sensex
            'dow': '^DJI',                # Dow Jones
            'sp500': '^GSPC',             # S&P 500
            'nasdaq': '^IXIC',            # NASDAQ
            'natural_gas': 'NG=F',        # Natural gas
            'zinc': 'ZN=F',               # Zinc futures
        }

        # Get Yahoo Finance symbol
        symbol = symbol_map.get(metric_name.lower(), metric_name)

        # Fetch the price
        value = self._get_yahoo_price(symbol)

        if value:
            self.cache[metric_name] = (value, datetime.now())
            logger.info(f"Fetched {metric_name}: {value}")
            return value
        else:
            logger.warning(f"No data available for {metric_name}")
            return None

    def get_multiple_metrics(self, metric_names: list[str]) -> Dict[str, Optional[float]]:
        """Get multiple metrics at once"""
        results = {}
        for metric_name in metric_names:
            results[metric_name] = self.get_metric(metric_name)
        return results

    def clear_cache(self):
        """Clear the metrics cache"""
        self.cache.clear()
        logger.info("Metrics cache cleared")
