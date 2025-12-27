from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Stock:
    """Represents a stock with its key metrics"""
    symbol: str
    name: str
    current_price: float
    previous_close: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    @property
    def price_change(self) -> float:
        """Calculate price change from previous close"""
        return self.current_price - self.previous_close
    
    @property
    def price_change_percent(self) -> float:
        """Calculate percentage change"""
        if self.previous_close == 0:
            return 0.0
        return (self.price_change / self.previous_close) * 100
    
    def __str__(self):
        return f"{self.symbol}: ${self.current_price:.2f} ({self.price_change_percent:+.2f}%)"

