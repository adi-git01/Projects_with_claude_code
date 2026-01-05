"""
Stock price fetching service using Yahoo Finance
Supports both yfinance library and direct API fallback
"""
from typing import Optional, Dict
from datetime import datetime
import logging
import requests

# Try importing yfinance, but make it optional
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

logger = logging.getLogger(__name__)


class PriceFetcher:
    """Fetches real-time stock prices from Yahoo Finance"""

    def __init__(self):
        self.cache: Dict[str, tuple[float, datetime]] = {}
        self.cache_duration_seconds = 60  # Cache for 1 minute

    def _get_price_from_api(self, ticker: str) -> Optional[float]:
        """Fallback method using Yahoo Finance API directly"""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
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
                    # Try from quote data
                    indicators = result[0].get('indicators', {}).get('quote', [])
                    if indicators and len(indicators) > 0:
                        closes = indicators[0].get('close', [])
                        if closes:
                            price = closes[-1]

                if price:
                    return float(price)

            return None

        except Exception as e:
            logger.debug(f"API fallback error for {ticker}: {str(e)}")
            return None

    def get_price(self, ticker: str) -> Optional[float]:
        """
        Get current price for a ticker

        Args:
            ticker: Stock ticker symbol (e.g., 'SARDA.NS')

        Returns:
            Current price or None if fetch fails
        """
        try:
            # Check cache first
            if ticker in self.cache:
                cached_price, cached_time = self.cache[ticker]
                age = (datetime.now() - cached_time).total_seconds()
                if age < self.cache_duration_seconds:
                    logger.debug(f"Using cached price for {ticker}: ₹{cached_price}")
                    return cached_price

            price = None

            # Try yfinance if available
            if YFINANCE_AVAILABLE:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info

                    # Try different price fields
                    for field in ['currentPrice', 'regularMarketPrice', 'previousClose']:
                        if field in info and info[field]:
                            price = float(info[field])
                            break

                    if price is None:
                        # Fallback to history
                        hist = stock.history(period='1d')
                        if not hist.empty:
                            price = float(hist['Close'].iloc[-1])
                except Exception as e:
                    logger.debug(f"yfinance error for {ticker}: {str(e)}")

            # Fallback to direct API if yfinance failed or unavailable
            if price is None:
                logger.info(f"Using direct API for {ticker}")
                price = self._get_price_from_api(ticker)

            if price:
                self.cache[ticker] = (price, datetime.now())
                logger.info(f"Fetched price for {ticker}: ₹{price:.2f}")
                return price
            else:
                logger.warning(f"No price data available for {ticker}")
                return None

        except Exception as e:
            logger.error(f"Error fetching price for {ticker}: {str(e)}")
            return None

    def get_multiple_prices(self, tickers: list[str]) -> Dict[str, Optional[float]]:
        """
        Get prices for multiple tickers

        Args:
            tickers: List of ticker symbols

        Returns:
            Dictionary mapping ticker to price
        """
        prices = {}
        for ticker in tickers:
            prices[ticker] = self.get_price(ticker)
        return prices

    def clear_cache(self):
        """Clear the price cache"""
        self.cache.clear()
        logger.info("Price cache cleared")
