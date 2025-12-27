from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Any
from models.stock import Stock

class RecommendationType(Enum):
    STRONG_BUY = "STRONG BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG SELL"

@dataclass
class Recommendation:
    """Represents a stock recommendation"""
    stock: Stock
    recommendation_type: RecommendationType
    confidence_score: float  # 0.0 to 1.0
    reasoning: str
    target_price: Optional[float] = None
    articles: List[Any] = field(default_factory=list)  # News articles for this stock
    
    def __str__(self):
        return f"{self.stock.symbol}: {self.recommendation_type.value} (Confidence: {self.confidence_score:.1%})"

