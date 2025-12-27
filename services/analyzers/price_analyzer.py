from typing import Dict
from models.stock import Stock
from models.recommendation import RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, MIN_SCORE, MAX_SCORE,
    PRICE_MOMENTUM_THRESHOLD, PRICE_PE_RATIO_MIN, PRICE_PE_RATIO_MAX, PRICE_PE_RATIO_HIGH,
    PRICE_CONFIDENCE, PRICE_SCORE_STRONG_POSITIVE, PRICE_SCORE_POSITIVE,
    PRICE_SCORE_STRONG_NEGATIVE, PRICE_SCORE_NEGATIVE, PRICE_SCORE_REASONABLE_VALUATION,
    PRICE_SCORE_UNDERVALUED, PRICE_SCORE_OVERVALUED, PRICE_SCORE_SIGNIFICANT_INCREASE,
    PRICE_SCORE_SIGNIFICANT_DECREASE, PRICE_CHANGE_THRESHOLD,
    PRICE_MULTIPLIER_HIGH, PRICE_MULTIPLIER_LOW
)

class PriceAnalyzer(BaseAnalyzer):
    """Analyzer based on price movements and momentum"""
    
    def __init__(self, weight: float = 1.0):
        super().__init__("Price Analysis", weight)
        self.momentum_threshold = PRICE_MOMENTUM_THRESHOLD
        self.pe_ratio_min = PRICE_PE_RATIO_MIN
        self.pe_ratio_max = PRICE_PE_RATIO_MAX
        self.pe_ratio_high = PRICE_PE_RATIO_HIGH
    
    def analyze(self, stock: Stock) -> Dict:
        """Analyze stock based on price metrics"""
        score = DEFAULT_SCORE  # Start neutral
        reasons = []
        confidence = PRICE_CONFIDENCE  # Price data is usually reliable
        
        # Price momentum analysis
        price_change_pct = stock.price_change_percent
        
        if price_change_pct > self.momentum_threshold:
            score += PRICE_SCORE_STRONG_POSITIVE
            reasons.append(f"Strong positive momentum (+{price_change_pct:.2f}%)")
        elif price_change_pct > PRICE_CHANGE_THRESHOLD:
            score += PRICE_SCORE_POSITIVE
            reasons.append(f"Positive momentum (+{price_change_pct:.2f}%)")
        elif price_change_pct < -self.momentum_threshold:
            score += PRICE_SCORE_STRONG_NEGATIVE
            reasons.append(f"Strong negative momentum ({price_change_pct:.2f}%)")
        elif price_change_pct < -PRICE_CHANGE_THRESHOLD:
            score += PRICE_SCORE_NEGATIVE
            reasons.append(f"Negative momentum ({price_change_pct:.2f}%)")
        else:
            reasons.append("Price stability")
        
        # P/E Ratio analysis (valuation)
        if stock.pe_ratio:
            if self.pe_ratio_min <= stock.pe_ratio <= self.pe_ratio_max:
                score += PRICE_SCORE_REASONABLE_VALUATION
                reasons.append(f"Reasonable valuation (P/E: {stock.pe_ratio:.2f})")
            elif stock.pe_ratio < self.pe_ratio_min:
                score += PRICE_SCORE_UNDERVALUED
                reasons.append(f"Undervalued (P/E: {stock.pe_ratio:.2f})")
            elif stock.pe_ratio > self.pe_ratio_high:
                score += PRICE_SCORE_OVERVALUED
                reasons.append(f"Overvalued (P/E: {stock.pe_ratio:.2f})")
            else:
                reasons.append(f"Moderate valuation (P/E: {stock.pe_ratio:.2f})")
        
        # Price relative to previous close
        if stock.current_price > stock.previous_close * PRICE_MULTIPLIER_HIGH:
            score += PRICE_SCORE_SIGNIFICANT_INCREASE
            reasons.append("Significant price increase from previous close")
        elif stock.current_price < stock.previous_close * PRICE_MULTIPLIER_LOW:
            score += PRICE_SCORE_SIGNIFICANT_DECREASE
            reasons.append("Significant price decrease from previous close")
        
        # Normalize score
        score = max(MIN_SCORE, min(MAX_SCORE, score))
        
        recommendation_type = self.calculate_recommendation_type(score)
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons) if reasons else "No price indicators",
            'confidence': confidence,
            'recommendation_type': recommendation_type
        }

