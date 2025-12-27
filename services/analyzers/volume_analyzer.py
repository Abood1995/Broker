from typing import Dict
from models.stock import Stock
from models.recommendation import RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, MIN_SCORE, MAX_SCORE,
    VOLUME_HIGH_THRESHOLD, VOLUME_VERY_HIGH_THRESHOLD, VOLUME_LOW_THRESHOLD,
    VOLUME_CONFIDENCE, VOLUME_SCORE_VERY_HIGH, VOLUME_SCORE_HIGH, VOLUME_SCORE_LOW,
    VOLUME_SCORE_BULLISH_SIGNAL, VOLUME_SCORE_BEARISH_SIGNAL,
    VOLUME_PRICE_CHANGE_THRESHOLD
)

class VolumeAnalyzer(BaseAnalyzer):
    """Analyzer based on trading volume patterns"""
    
    def __init__(self, weight: float = 1.0):
        super().__init__("Volume Analysis", weight)
        self.high_volume_threshold = VOLUME_HIGH_THRESHOLD
        self.very_high_volume_threshold = VOLUME_VERY_HIGH_THRESHOLD
        self.low_volume_threshold = VOLUME_LOW_THRESHOLD
    
    def analyze(self, stock: Stock) -> Dict:
        """Analyze stock based on volume metrics"""
        score = DEFAULT_SCORE  # Start neutral
        reasons = []
        confidence = VOLUME_CONFIDENCE  # Volume alone is less reliable
        
        volume = stock.volume
        
        # High volume indicates strong interest
        if volume >= self.very_high_volume_threshold:
            score += VOLUME_SCORE_VERY_HIGH
            reasons.append(f"Very high trading volume ({volume:,}) - strong market interest")
        elif volume >= self.high_volume_threshold:
            score += VOLUME_SCORE_HIGH
            reasons.append(f"High trading volume ({volume:,}) - good liquidity")
        elif volume < self.low_volume_threshold:
            score += VOLUME_SCORE_LOW
            reasons.append(f"Low trading volume ({volume:,}) - limited liquidity")
        else:
            reasons.append(f"Moderate trading volume ({volume:,})")
        
        # Volume-price relationship (simplified - would need historical data for better analysis)
        # High volume with price increase = bullish
        # High volume with price decrease = bearish
        if volume >= self.high_volume_threshold:
            if stock.price_change_percent > VOLUME_PRICE_CHANGE_THRESHOLD:
                score += VOLUME_SCORE_BULLISH_SIGNAL
                reasons.append("High volume with price increase - bullish signal")
            elif stock.price_change_percent < -VOLUME_PRICE_CHANGE_THRESHOLD:
                score += VOLUME_SCORE_BEARISH_SIGNAL
                reasons.append("High volume with price decrease - bearish signal")
        
        # Normalize score
        score = max(MIN_SCORE, min(MAX_SCORE, score))
        
        recommendation_type = self.calculate_recommendation_type(score)
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons) if reasons else "No volume indicators",
            'confidence': confidence,
            'recommendation_type': recommendation_type
        }

