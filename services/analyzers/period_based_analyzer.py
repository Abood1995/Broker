from typing import Dict, List
from models.stock import Stock
from models.recommendation import RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, MIN_SCORE, MAX_SCORE,
    PERIOD_BASED_CONFIDENCE, PERIOD_BASED_CONFIDENCE_ERROR,
    PERIODS_CONFIG, PERIOD_CHANGE_STRONG_POSITIVE, PERIOD_CHANGE_POSITIVE,
    PERIOD_CHANGE_NEGATIVE, PERIOD_CHANGE_STRONG_NEGATIVE,
    PERIOD_SCORE_STRONG_POSITIVE, PERIOD_SCORE_POSITIVE, PERIOD_SCORE_SLIGHTLY_POSITIVE,
    PERIOD_SCORE_SLIGHTLY_NEGATIVE, PERIOD_SCORE_NEGATIVE, PERIOD_SCORE_STRONG_NEGATIVE,
    PERIOD_REC_BUY, PERIOD_REC_HOLD, PERIOD_REC_SELL,
    CONSENSUS_BUY_COUNT_STRONG, CONSENSUS_BUY_COUNT_MODERATE,
    CONSENSUS_SELL_COUNT_STRONG, CONSENSUS_SELL_COUNT_MODERATE,
    CONSENSUS_SCORE_STRONG_BUY, CONSENSUS_SCORE_BUY,
    CONSENSUS_SCORE_STRONG_SELL, CONSENSUS_SCORE_SELL
)
import yfinance as yf

class PeriodBasedAnalyzer(BaseAnalyzer):
    """Analyzer that evaluates stock performance across multiple time periods"""
    
    def __init__(self, weight: float = 1.0):
        super().__init__("Period-Based Analysis", weight)
        self.periods = PERIODS_CONFIG
    
    def analyze(self, stock: Stock) -> Dict:
        """Analyze stock across multiple time periods and combine results"""
        score = DEFAULT_SCORE  # Start neutral
        reasons = []
        confidence = PERIOD_BASED_CONFIDENCE
        period_recommendations = []
        
        try:
            ticker = yf.Ticker(stock.symbol)
            current_price = stock.current_price
            
            total_weight = 0.0
            weighted_score = 0.0
            
            for period_key, period_info in self.periods.items():
                try:
                    hist = ticker.history(period=period_info['period'])
                    
                    if hist.empty or len(hist) < 2:
                        continue
                    
                    period_start_price = hist['Close'].iloc[0]
                    period_end_price = hist['Close'].iloc[-1]
                    period_change = ((period_end_price - period_start_price) / period_start_price) * 100
                    
                    # Score based on period performance
                    period_score = DEFAULT_SCORE
                    if period_change > PERIOD_CHANGE_STRONG_POSITIVE:
                        period_score = PERIOD_SCORE_STRONG_POSITIVE
                        period_rec = PERIOD_REC_BUY
                    elif period_change > PERIOD_CHANGE_POSITIVE:
                        period_score = PERIOD_SCORE_POSITIVE
                        period_rec = PERIOD_REC_BUY
                    elif period_change > 0:
                        period_score = PERIOD_SCORE_SLIGHTLY_POSITIVE
                        period_rec = PERIOD_REC_HOLD
                    elif period_change > PERIOD_CHANGE_NEGATIVE:
                        period_score = PERIOD_SCORE_SLIGHTLY_NEGATIVE
                        period_rec = PERIOD_REC_HOLD
                    elif period_change > PERIOD_CHANGE_STRONG_NEGATIVE:
                        period_score = PERIOD_SCORE_NEGATIVE
                        period_rec = PERIOD_REC_SELL
                    else:
                        period_score = PERIOD_SCORE_STRONG_NEGATIVE
                        period_rec = PERIOD_REC_SELL
                    
                    # Weight the period score
                    period_weight = period_info['weight']
                    weighted_score += period_score * period_weight
                    total_weight += period_weight
                    
                    period_recommendations.append(
                        f"{period_info['name']}: {period_rec} ({period_change:+.2f}%)"
                    )
                    reasons.append(
                        f"{period_info['name']}: {period_change:+.2f}% change"
                    )
                
                except Exception as e:
                    reasons.append(f"Error analyzing {period_info['name']}: {str(e)}")
            
            # Calculate weighted average score
            if total_weight > 0:
                score = weighted_score / total_weight
            
            # Determine consensus recommendation
            buy_count = sum(1 for rec in period_recommendations if PERIOD_REC_BUY in rec)
            sell_count = sum(1 for rec in period_recommendations if PERIOD_REC_SELL in rec)
            hold_count = sum(1 for rec in period_recommendations if PERIOD_REC_HOLD in rec)
            
            if buy_count >= CONSENSUS_BUY_COUNT_STRONG:
                score = max(score, CONSENSUS_SCORE_STRONG_BUY)
                reasons.append(f"Strong buy consensus across periods ({buy_count} buy, {hold_count} hold, {sell_count} sell)")
            elif buy_count >= CONSENSUS_BUY_COUNT_MODERATE and sell_count == 0:
                score = max(score, CONSENSUS_SCORE_BUY)
                reasons.append(f"Buy consensus ({buy_count} buy, {hold_count} hold)")
            elif sell_count >= CONSENSUS_SELL_COUNT_STRONG:
                score = min(score, CONSENSUS_SCORE_STRONG_SELL)
                reasons.append(f"Strong sell consensus ({buy_count} buy, {hold_count} hold, {sell_count} sell)")
            elif sell_count >= CONSENSUS_SELL_COUNT_MODERATE and buy_count == 0:
                score = min(score, CONSENSUS_SCORE_SELL)
                reasons.append(f"Sell consensus ({hold_count} hold, {sell_count} sell)")
            
            # Add period summary
            if period_recommendations:
                reasons.insert(0, f"Period Recommendations: {', '.join(period_recommendations)}")
        
        except Exception as e:
            reasons.append(f"Error in period-based analysis: {str(e)}")
            confidence = PERIOD_BASED_CONFIDENCE_ERROR
        
        # Normalize score
        score = max(MIN_SCORE, min(MAX_SCORE, score))
        
        recommendation_type = self.calculate_recommendation_type(score)
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons) if reasons else "No period-based indicators",
            'confidence': confidence,
            'recommendation_type': recommendation_type
        }

