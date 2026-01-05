"""
Technical indicators calculator (RSI, Moving Averages, etc.)
"""
import logging
import requests
from typing import Optional, Dict
import pandas as pd

logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """Calculate technical indicators for stocks"""

    def __init__(self):
        self.cache: Dict[str, Dict] = {}

    def _get_historical_data(self, ticker: str, period: str = '3mo') -> Optional[pd.DataFrame]:
        """Fetch historical price data from Yahoo Finance"""
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {'interval': '1d', 'range': period}
            headers = {'User-Agent': 'Mozilla/5.0'}

            response = requests.get(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()

            data = response.json()
            result = data.get('chart', {}).get('result', [])

            if not result or len(result) == 0:
                return None

            # Extract price data
            timestamps = result[0].get('timestamp', [])
            indicators = result[0].get('indicators', {}).get('quote', [])

            if not indicators or len(indicators) == 0:
                return None

            quote = indicators[0]
            closes = quote.get('close', [])
            highs = quote.get('high', [])
            lows = quote.get('low', [])

            # Create DataFrame
            df = pd.DataFrame({
                'timestamp': timestamps,
                'close': closes,
                'high': highs,
                'low': lows
            })

            # Remove rows with None values
            df = df.dropna()

            if df.empty:
                return None

            return df

        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {str(e)}")
            return None

    def calculate_rsi(self, ticker: str, period: int = 14) -> Optional[float]:
        """
        Calculate RSI (Relative Strength Index)

        Args:
            ticker: Stock ticker symbol
            period: RSI period (default 14 days)

        Returns:
            RSI value (0-100) or None if calculation fails
        """
        try:
            df = self._get_historical_data(ticker)

            if df is None or len(df) < period + 1:
                logger.warning(f"Insufficient data for RSI calculation: {ticker}")
                return None

            # Calculate price changes
            df['change'] = df['close'].diff()

            # Separate gains and losses
            df['gain'] = df['change'].apply(lambda x: x if x > 0 else 0)
            df['loss'] = df['change'].apply(lambda x: abs(x) if x < 0 else 0)

            # Calculate average gain and loss
            avg_gain = df['gain'].rolling(window=period).mean()
            avg_loss = df['loss'].rolling(window=period).mean()

            # Calculate RS and RSI
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            # Get the most recent RSI value
            current_rsi = rsi.iloc[-1]

            if pd.isna(current_rsi):
                return None

            logger.info(f"RSI for {ticker}: {current_rsi:.2f}")
            return float(current_rsi)

        except Exception as e:
            logger.error(f"Error calculating RSI for {ticker}: {str(e)}")
            return None

    def calculate_ma(self, ticker: str, period: int = 50) -> Optional[float]:
        """
        Calculate Moving Average

        Args:
            ticker: Stock ticker symbol
            period: MA period (default 50 days)

        Returns:
            Moving average value or None if calculation fails
        """
        try:
            df = self._get_historical_data(ticker)

            if df is None or len(df) < period:
                logger.warning(f"Insufficient data for MA calculation: {ticker}")
                return None

            # Calculate moving average
            ma = df['close'].rolling(window=period).mean()

            # Get the most recent MA value
            current_ma = ma.iloc[-1]

            if pd.isna(current_ma):
                return None

            logger.info(f"MA{period} for {ticker}: {current_ma:.2f}")
            return float(current_ma)

        except Exception as e:
            logger.error(f"Error calculating MA for {ticker}: {str(e)}")
            return None

    def get_all_indicators(self, ticker: str) -> Dict[str, Optional[float]]:
        """
        Get all technical indicators for a ticker

        Returns:
            Dictionary with RSI, MA20, MA50, MA200
        """
        return {
            'rsi': self.calculate_rsi(ticker),
            'ma20': self.calculate_ma(ticker, 20),
            'ma50': self.calculate_ma(ticker, 50),
            'ma200': self.calculate_ma(ticker, 200),
        }

    def check_price_vs_ma(self, current_price: float, ticker: str, ma_period: int = 50) -> Optional[str]:
        """
        Check if price is above or below moving average

        Returns:
            'above', 'below', or None
        """
        ma = self.calculate_ma(ticker, ma_period)

        if ma is None:
            return None

        if current_price > ma:
            return 'above'
        else:
            return 'below'
