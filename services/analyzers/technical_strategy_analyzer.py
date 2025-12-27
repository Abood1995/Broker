from typing import Dict, List
from models.stock import Stock
from models.recommendation import RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, MIN_SCORE, MAX_SCORE,
    RSI_PERIOD, SMA_SHORT, SMA_LONG, TECHNICAL_HISTORY_PERIOD,
    TECHNICAL_MIN_DATA_LENGTH, TECHNICAL_CONFIDENCE, TECHNICAL_CONFIDENCE_INSUFFICIENT_DATA,
    TECHNICAL_CONFIDENCE_ERROR, RSI_OVERSOLD, RSI_OVERBOUGHT, RSI_NEUTRAL_LOW, RSI_NEUTRAL_HIGH,
    TECHNICAL_SCORE_OVERSOLD, TECHNICAL_SCORE_OVERBOUGHT, TECHNICAL_SCORE_NEUTRAL_RSI,
    TECHNICAL_SCORE_GOLDEN_CROSS, TECHNICAL_SCORE_DEATH_CROSS, TECHNICAL_SCORE_ABOVE_MA,
    TECHNICAL_SCORE_BELOW_MA, TECHNICAL_SCORE_NEAR_HIGHS, TECHNICAL_SCORE_NEAR_LOWS,
    TECHNICAL_RECENT_PERIOD
)
from utils.indicators import TechnicalIndicators
import yfinance as yf

class TechnicalStrategyAnalyzer(BaseAnalyzer):
    """Analyzer based on technical indicators and trading strategies"""
    
    def __init__(self, weight: float = 1.0):
        super().__init__("Technical Strategy Analysis", weight)
        self.indicators = TechnicalIndicators()
        self.rsi_period = RSI_PERIOD
        self.sma_short = SMA_SHORT
        self.sma_long = SMA_LONG
    
    def analyze(self, stock: Stock) -> Dict:
        """Analyze stock based on technical indicators"""
        score = DEFAULT_SCORE  # Start neutral
        reasons = []
        confidence = TECHNICAL_CONFIDENCE  # Technical analysis has moderate reliability
        
        try:
            ticker = yf.Ticker(stock.symbol)
            hist = ticker.history(period=TECHNICAL_HISTORY_PERIOD)  # Get 3 months of data
            
            if hist.empty or len(hist) < TECHNICAL_MIN_DATA_LENGTH:
                reasons.append("Insufficient historical data for technical analysis")
                confidence = TECHNICAL_CONFIDENCE_INSUFFICIENT_DATA
            else:
                prices = hist['Close'].tolist()
                
                # RSI Analysis
                rsi = self.indicators.calculate_rsi(prices, self.rsi_period)
                if rsi < RSI_OVERSOLD:
                    score += TECHNICAL_SCORE_OVERSOLD
                    reasons.append(f"Oversold condition (RSI: {rsi:.2f}) - potential buy signal")
                elif rsi > RSI_OVERBOUGHT:
                    score += TECHNICAL_SCORE_OVERBOUGHT
                    reasons.append(f"Overbought condition (RSI: {rsi:.2f}) - potential sell signal")
                elif RSI_NEUTRAL_LOW <= rsi <= RSI_NEUTRAL_HIGH:
                    score += TECHNICAL_SCORE_NEUTRAL_RSI
                    reasons.append(f"Neutral RSI ({rsi:.2f}) - stable momentum")
                else:
                    reasons.append(f"RSI: {rsi:.2f}")
                
                # Moving Average Analysis
                if len(prices) >= self.sma_long:
                    sma_short = self.indicators.calculate_sma(prices, self.sma_short)
                    sma_long = self.indicators.calculate_sma(prices, self.sma_long)
                    current_price = prices[-1]
                    
                    # Golden Cross / Death Cross
                    if sma_short > sma_long:
                        score += TECHNICAL_SCORE_GOLDEN_CROSS
                        reasons.append(f"Golden Cross (SMA{self.sma_short} > SMA{self.sma_long}) - bullish trend")
                    elif sma_short < sma_long:
                        score += TECHNICAL_SCORE_DEATH_CROSS
                        reasons.append(f"Death Cross (SMA{self.sma_short} < SMA{self.sma_long}) - bearish trend")
                    
                    # Price relative to moving averages
                    if current_price > sma_short > sma_long:
                        score += TECHNICAL_SCORE_ABOVE_MA
                        reasons.append("Price above both moving averages - strong uptrend")
                    elif current_price < sma_short < sma_long:
                        score += TECHNICAL_SCORE_BELOW_MA
                        reasons.append("Price below both moving averages - strong downtrend")
                
                # Support/Resistance levels (simplified)
                recent_high = max(prices[-TECHNICAL_RECENT_PERIOD:])
                recent_low = min(prices[-TECHNICAL_RECENT_PERIOD:])
                current_price = prices[-1]
                
                if current_price > (recent_high + recent_low) / 2:
                    score += TECHNICAL_SCORE_NEAR_HIGHS
                    reasons.append("Price near recent highs - bullish momentum")
                elif current_price < (recent_high + recent_low) / 2:
                    score += TECHNICAL_SCORE_NEAR_LOWS
                    reasons.append("Price near recent lows - bearish pressure")
        
        except Exception as e:
            reasons.append(f"Error in technical analysis: {str(e)}")
            confidence = TECHNICAL_CONFIDENCE_ERROR
        
        # Normalize score
        score = max(MIN_SCORE, min(MAX_SCORE, score))
        
        recommendation_type = self.calculate_recommendation_type(score)
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons) if reasons else "No technical indicators",
            'confidence': confidence,
            'recommendation_type': recommendation_type
        }

