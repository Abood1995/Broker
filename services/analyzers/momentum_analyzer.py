from typing import Dict
from models.stock import Stock
from models.recommendation import RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, MIN_SCORE, MAX_SCORE,
    MOMENTUM_HISTORY_PERIOD, MOMENTUM_MIN_DATA_LENGTH,
    MOMENTUM_CONFIDENCE, MOMENTUM_CONFIDENCE_INSUFFICIENT_DATA, MOMENTUM_CONFIDENCE_ERROR,
    MOMENTUM_PERIOD_5D, MOMENTUM_PERIOD_20D, MOMENTUM_PERIOD_60D,
    MOMENTUM_5D_STRONG_POSITIVE, MOMENTUM_5D_POSITIVE, MOMENTUM_5D_STRONG_NEGATIVE, MOMENTUM_5D_NEGATIVE,
    MOMENTUM_SCORE_5D_STRONG_POSITIVE, MOMENTUM_SCORE_5D_POSITIVE,
    MOMENTUM_SCORE_5D_STRONG_NEGATIVE, MOMENTUM_SCORE_5D_NEGATIVE,
    MOMENTUM_20D_STRONG_POSITIVE, MOMENTUM_20D_POSITIVE, MOMENTUM_20D_STRONG_NEGATIVE, MOMENTUM_20D_NEGATIVE,
    MOMENTUM_SCORE_20D_STRONG_POSITIVE, MOMENTUM_SCORE_20D_POSITIVE,
    MOMENTUM_SCORE_20D_STRONG_NEGATIVE, MOMENTUM_SCORE_20D_NEGATIVE,
    MOMENTUM_60D_STRONG_POSITIVE, MOMENTUM_60D_POSITIVE, MOMENTUM_60D_STRONG_NEGATIVE, MOMENTUM_60D_NEGATIVE,
    MOMENTUM_SCORE_60D_STRONG_POSITIVE, MOMENTUM_SCORE_60D_POSITIVE,
    MOMENTUM_SCORE_60D_STRONG_NEGATIVE, MOMENTUM_SCORE_60D_NEGATIVE,
    MOMENTUM_SCORE_CONSISTENT_POSITIVE, MOMENTUM_SCORE_CONSISTENT_NEGATIVE,
    MOMENTUM_SCORE_ACCELERATING, MOMENTUM_SCORE_DECELERATING
)
import yfinance as yf
import numpy as np

class MomentumAnalyzer(BaseAnalyzer):
    """Analyzer based on price momentum across different timeframes"""
    
    def __init__(self, weight: float = 1.0):
        super().__init__("Momentum Analysis", weight)
    
    def calculate_momentum(self, prices: list, period: int) -> float:
        """Calculate momentum as percentage change over period"""
        if len(prices) < period + 1:
            return 0.0
        return ((prices[-1] - prices[-period-1]) / prices[-period-1]) * 100
    
    def analyze(self, stock: Stock) -> Dict:
        """Analyze stock based on momentum indicators"""
        score = DEFAULT_SCORE  # Start neutral
        reasons = []
        confidence = MOMENTUM_CONFIDENCE
        
        try:
            ticker = yf.Ticker(stock.symbol)
            hist = ticker.history(period=MOMENTUM_HISTORY_PERIOD)
            
            if hist.empty or len(hist) < MOMENTUM_MIN_DATA_LENGTH:
                reasons.append("Insufficient data for momentum analysis")
                confidence = MOMENTUM_CONFIDENCE_INSUFFICIENT_DATA
            else:
                prices = hist['Close'].tolist()
                
                # Calculate momentum for different periods
                momentum_5d = self.calculate_momentum(prices, MOMENTUM_PERIOD_5D)
                momentum_20d = self.calculate_momentum(prices, MOMENTUM_PERIOD_20D)
                momentum_60d = self.calculate_momentum(prices, MOMENTUM_PERIOD_60D)
                
                # Short-term momentum (5 days)
                if momentum_5d > MOMENTUM_5D_STRONG_POSITIVE:
                    score += MOMENTUM_SCORE_5D_STRONG_POSITIVE
                    reasons.append(f"Strong short-term momentum (+{momentum_5d:.2f}% in 5 days)")
                elif momentum_5d > MOMENTUM_5D_POSITIVE:
                    score += MOMENTUM_SCORE_5D_POSITIVE
                    reasons.append(f"Positive short-term momentum (+{momentum_5d:.2f}% in 5 days)")
                elif momentum_5d < MOMENTUM_5D_STRONG_NEGATIVE:
                    score += MOMENTUM_SCORE_5D_STRONG_NEGATIVE
                    reasons.append(f"Negative short-term momentum ({momentum_5d:.2f}% in 5 days)")
                elif momentum_5d < MOMENTUM_5D_NEGATIVE:
                    score += MOMENTUM_SCORE_5D_NEGATIVE
                    reasons.append(f"Weak short-term momentum ({momentum_5d:.2f}% in 5 days)")
                
                # Medium-term momentum (20 days)
                if momentum_20d > MOMENTUM_20D_STRONG_POSITIVE:
                    score += MOMENTUM_SCORE_20D_STRONG_POSITIVE
                    reasons.append(f"Strong medium-term momentum (+{momentum_20d:.2f}% in 20 days)")
                elif momentum_20d > MOMENTUM_20D_POSITIVE:
                    score += MOMENTUM_SCORE_20D_POSITIVE
                    reasons.append(f"Positive medium-term momentum (+{momentum_20d:.2f}% in 20 days)")
                elif momentum_20d < MOMENTUM_20D_STRONG_NEGATIVE:
                    score += MOMENTUM_SCORE_20D_STRONG_NEGATIVE
                    reasons.append(f"Negative medium-term momentum ({momentum_20d:.2f}% in 20 days)")
                elif momentum_20d < MOMENTUM_20D_NEGATIVE:
                    score += MOMENTUM_SCORE_20D_NEGATIVE
                    reasons.append(f"Weak medium-term momentum ({momentum_20d:.2f}% in 20 days)")
                
                # Long-term momentum (60 days)
                if momentum_60d > MOMENTUM_60D_STRONG_POSITIVE:
                    score += MOMENTUM_SCORE_60D_STRONG_POSITIVE
                    reasons.append(f"Strong long-term momentum (+{momentum_60d:.2f}% in 60 days)")
                elif momentum_60d > MOMENTUM_60D_POSITIVE:
                    score += MOMENTUM_SCORE_60D_POSITIVE
                    reasons.append(f"Positive long-term momentum (+{momentum_60d:.2f}% in 60 days)")
                elif momentum_60d < MOMENTUM_60D_STRONG_NEGATIVE:
                    score += MOMENTUM_SCORE_60D_STRONG_NEGATIVE
                    reasons.append(f"Negative long-term momentum ({momentum_60d:.2f}% in 60 days)")
                elif momentum_60d < MOMENTUM_60D_NEGATIVE:
                    score += MOMENTUM_SCORE_60D_NEGATIVE
                    reasons.append(f"Weak long-term momentum ({momentum_60d:.2f}% in 60 days)")
                
                # Momentum consistency (all timeframes aligned)
                if (momentum_5d > 0 and momentum_20d > 0 and momentum_60d > 0):
                    score += MOMENTUM_SCORE_CONSISTENT_POSITIVE
                    reasons.append("Consistent positive momentum across all timeframes")
                elif (momentum_5d < 0 and momentum_20d < 0 and momentum_60d < 0):
                    score += MOMENTUM_SCORE_CONSISTENT_NEGATIVE
                    reasons.append("Consistent negative momentum across all timeframes")
                
                # Momentum acceleration/deceleration
                if momentum_5d > momentum_20d > momentum_60d:
                    score += MOMENTUM_SCORE_ACCELERATING
                    reasons.append("Momentum accelerating - bullish signal")
                elif momentum_5d < momentum_20d < momentum_60d:
                    score += MOMENTUM_SCORE_DECELERATING
                    reasons.append("Momentum decelerating - bearish signal")
        
        except Exception as e:
            reasons.append(f"Error in momentum analysis: {str(e)}")
            confidence = MOMENTUM_CONFIDENCE_ERROR
        
        # Normalize score
        score = max(MIN_SCORE, min(MAX_SCORE, score))
        
        recommendation_type = self.calculate_recommendation_type(score)
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons) if reasons else "No momentum indicators",
            'confidence': confidence,
            'recommendation_type': recommendation_type
        }

