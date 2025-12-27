"""Service for fetching historical stock price data for charts"""
import yfinance as yf
from typing import Optional
import pandas as pd
from datetime import datetime

class ChartDataFetcher:
    """Fetches historical OHLCV data for stock charts"""
    
    def __init__(self):
        """Initialize the chart data fetcher"""
        self.cache = {}  # Simple cache to avoid redundant API calls
    
    def fetch_historical_data(self, symbol: str, period: str = "3mo") -> Optional[pd.DataFrame]:
        """
        Fetch historical OHLCV data for a stock
        
        Args:
            symbol: Stock symbol (e.g., "AAPL")
            period: Time period - "1d", "5d", "1mo", "3mo", "6mo", "1y", "max"
            
        Returns:
            DataFrame with columns: Open, High, Low, Close, Volume
            Returns None if error occurs
        """
        cache_key = f"{symbol}_{period}"
        
        # Check cache (simple implementation - could add TTL)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                print(f"No historical data available for {symbol} with period {period}")
                return None
            
            # Ensure we have the required columns
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in hist.columns for col in required_columns):
                print(f"Missing required columns in data for {symbol}")
                return None
            
            # Cache the result
            self.cache[cache_key] = hist
            
            return hist
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return None
    
    def clear_cache(self):
        """Clear the data cache"""
        self.cache.clear()
    
    def get_available_periods(self) -> dict:
        """Get mapping of period names to yfinance period values"""
        return {
            "1D": "1d",
            "1W": "5d",
            "1M": "1mo",
            "3M": "3mo",
            "6M": "6mo",
            "1Y": "1y",
            "All": "max"
        }

