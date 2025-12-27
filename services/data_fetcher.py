import yfinance as yf
from typing import List, Optional
from models.stock import Stock

class DataFetcher:
    """Fetches stock data from external sources"""
    
    def __init__(self):
        self.cache = {}  # Simple in-memory cache
    
    def fetch_stock(self, symbol: str) -> Optional[Stock]:
        """Fetch data for a single stock"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            previous_close = info.get('previousClose', current_price)
            
            return Stock(
                symbol=symbol.upper(),
                name=info.get('longName', symbol),
                current_price=float(current_price),
                previous_close=float(previous_close),
                volume=int(hist['Volume'].iloc[-1]),
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('trailingPE'),
                dividend_yield=info.get('dividendYield')
            )
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def fetch_multiple_stocks(self, symbols: List[str]) -> List[Stock]:
        """Fetch data for multiple stocks"""
        stocks = []
        for symbol in symbols:
            stock = self.fetch_stock(symbol)
            if stock:
                stocks.append(stock)
        return stocks

