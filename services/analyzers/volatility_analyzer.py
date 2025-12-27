from typing import Dict
from models.stock import Stock
from models.recommendation import RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, MIN_SCORE, MAX_SCORE,
    VOLATILITY_LOW_THRESHOLD, VOLATILITY_HIGH_THRESHOLD,
    VOLATILITY_HISTORY_PERIOD, VOLATILITY_MIN_DATA_LENGTH, VOLATILITY_MIN_DATA_LENGTH_TREND,
    VOLATILITY_CONFIDENCE, VOLATILITY_CONFIDENCE_INSUFFICIENT_DATA, VOLATILITY_CONFIDENCE_ERROR,
    TRADING_DAYS_PER_YEAR, VOLATILITY_TREND_DECREASING, VOLATILITY_TREND_INCREASING,
    VOLATILITY_SCORE_LOW, VOLATILITY_SCORE_HIGH, VOLATILITY_SCORE_DECREASING,
    VOLATILITY_SCORE_INCREASING, VOLATILITY_SCORE_TIGHT_RANGE, VOLATILITY_SCORE_WIDE_RANGE,
    VOLATILITY_RANGE_TIGHT, VOLATILITY_RANGE_WIDE, VOLATILITY_RECENT_PERIOD
)
import yfinance as yf
import numpy as np

class VolatilityAnalyzer(BaseAnalyzer):
    """Analyzer based on volatility and risk assessment"""
    
    def __init__(self, weight: float = 1.0):
        super().__init__("Volatility Analysis", weight)
        self.low_volatility_threshold = VOLATILITY_LOW_THRESHOLD
        self.high_volatility_threshold = VOLATILITY_HIGH_THRESHOLD
    
    def calculate_volatility(self, prices: list) -> float:
        """Calculate annualized volatility"""
        if len(prices) < 2:
            return 0.0
        
        returns = []
        for i in range(1, len(prices)):
            daily_return = (prices[i] - prices[i-1]) / prices[i-1]
            returns.append(daily_return)
        
        if not returns:
            return 0.0
        
        # Calculate standard deviation of returns
        std_dev = np.std(returns)
        
        # Annualize (assuming 252 trading days)
        annualized_vol = std_dev * np.sqrt(TRADING_DAYS_PER_YEAR)
        
        return annualized_vol
    
    def analyze(self, stock: Stock) -> Dict:
        """Analyze stock based on volatility metrics"""
        score = DEFAULT_SCORE  # Start neutral (volatility is neutral, risk assessment)
        reasons = []
        confidence = VOLATILITY_CONFIDENCE
        
        try:
            ticker = yf.Ticker(stock.symbol)
            hist = ticker.history(period=VOLATILITY_HISTORY_PERIOD)
            
            if hist.empty or len(hist) < VOLATILITY_MIN_DATA_LENGTH:
                reasons.append("Insufficient data for volatility analysis")
                confidence = VOLATILITY_CONFIDENCE_INSUFFICIENT_DATA
            else:
                prices = hist['Close'].tolist()
                volatility = self.calculate_volatility(prices)
                
                # Volatility assessment
                if volatility < self.low_volatility_threshold:
                    score += VOLATILITY_SCORE_LOW
                    reasons.append(
                        f"Low volatility ({volatility*100:.2f}%) - stable price action, lower risk"
                    )
                elif volatility > self.high_volatility_threshold:
                    score += VOLATILITY_SCORE_HIGH
                    reasons.append(
                        f"High volatility ({volatility*100:.2f}%) - increased risk, potential for large swings"
                    )
                else:
                    reasons.append(
                        f"Moderate volatility ({volatility*100:.2f}%) - balanced risk/reward"
                    )
                
                # Recent volatility trend
                if len(prices) >= VOLATILITY_MIN_DATA_LENGTH_TREND:
                    recent_vol = self.calculate_volatility(prices[-VOLATILITY_RECENT_PERIOD:])
                    earlier_vol = self.calculate_volatility(prices[-VOLATILITY_MIN_DATA_LENGTH_TREND:-VOLATILITY_RECENT_PERIOD])
                    
                    if recent_vol < earlier_vol * VOLATILITY_TREND_DECREASING:
                        score += VOLATILITY_SCORE_DECREASING
                        reasons.append("Volatility decreasing - stabilizing trend")
                    elif recent_vol > earlier_vol * VOLATILITY_TREND_INCREASING:
                        score += VOLATILITY_SCORE_INCREASING
                        reasons.append("Volatility increasing - uncertainty rising")
                
                # Price range analysis
                price_range = max(prices) - min(prices)
                avg_price = sum(prices) / len(prices)
                range_percent = (price_range / avg_price) * 100
                
                if range_percent < VOLATILITY_RANGE_TIGHT:
                    score += VOLATILITY_SCORE_TIGHT_RANGE
                    reasons.append(f"Tight trading range ({range_percent:.2f}%) - consolidation")
                elif range_percent > VOLATILITY_RANGE_WIDE:
                    score += VOLATILITY_SCORE_WIDE_RANGE
                    reasons.append(f"Wide trading range ({range_percent:.2f}%) - high uncertainty")
        
        except Exception as e:
            reasons.append(f"Error in volatility analysis: {str(e)}")
            confidence = VOLATILITY_CONFIDENCE_ERROR
        
        # Normalize score
        score = max(MIN_SCORE, min(MAX_SCORE, score))
        
        recommendation_type = self.calculate_recommendation_type(score)
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons) if reasons else "No volatility indicators",
            'confidence': confidence,
            'recommendation_type': recommendation_type
        }

