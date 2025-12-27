from typing import Dict
from models.stock import Stock
from models.recommendation import RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, MIN_SCORE, MAX_SCORE,
    FUNDAMENTAL_CONFIDENCE, FUNDAMENTAL_CONFIDENCE_ERROR,
    PE_RATIO_MIN, PE_RATIO_MAX, PE_RATIO_HIGH,
    FUNDAMENTAL_SCORE_PE_ATTRACTIVE, FUNDAMENTAL_SCORE_PE_VERY_LOW, FUNDAMENTAL_SCORE_PE_HIGH,
    PB_RATIO_LOW, PB_RATIO_REASONABLE, PB_RATIO_HIGH,
    FUNDAMENTAL_SCORE_PB_LOW, FUNDAMENTAL_SCORE_PB_REASONABLE, FUNDAMENTAL_SCORE_PB_HIGH,
    DEBT_TO_EQUITY_LOW, DEBT_TO_EQUITY_HIGH,
    FUNDAMENTAL_SCORE_DEBT_LOW, FUNDAMENTAL_SCORE_DEBT_HIGH,
    PROFIT_MARGIN_STRONG, PROFIT_MARGIN_GOOD,
    FUNDAMENTAL_SCORE_MARGIN_STRONG, FUNDAMENTAL_SCORE_MARGIN_GOOD, FUNDAMENTAL_SCORE_MARGIN_NEGATIVE,
    REVENUE_GROWTH_STRONG, REVENUE_GROWTH_GOOD, REVENUE_GROWTH_DECLINING,
    FUNDAMENTAL_SCORE_REVENUE_STRONG, FUNDAMENTAL_SCORE_REVENUE_GOOD, FUNDAMENTAL_SCORE_REVENUE_DECLINING,
    EARNINGS_GROWTH_STRONG, EARNINGS_GROWTH_GOOD, EARNINGS_GROWTH_DECLINING,
    FUNDAMENTAL_SCORE_EARNINGS_STRONG, FUNDAMENTAL_SCORE_EARNINGS_GOOD, FUNDAMENTAL_SCORE_EARNINGS_DECLINING,
    DIVIDEND_YIELD_ATTRACTIVE, DIVIDEND_YIELD_MODERATE,
    FUNDAMENTAL_SCORE_DIVIDEND_ATTRACTIVE, FUNDAMENTAL_SCORE_DIVIDEND_MODERATE,
    MARKET_CAP_LARGE, FUNDAMENTAL_SCORE_LARGE_CAP
)
import yfinance as yf

class FundamentalAnalyzer(BaseAnalyzer):
    """Analyzer based on fundamental financial metrics"""
    
    def __init__(self, weight: float = 1.0):
        super().__init__("Fundamental Analysis", weight)
    
    def analyze(self, stock: Stock) -> Dict:
        """Analyze stock based on fundamental metrics"""
        score = DEFAULT_SCORE  # Start neutral
        reasons = []
        confidence = FUNDAMENTAL_CONFIDENCE
        
        try:
            ticker = yf.Ticker(stock.symbol)
            info = ticker.info
            
            # P/E Ratio analysis
            pe_ratio = info.get('trailingPE') or info.get('forwardPE')
            if pe_ratio:
                if PE_RATIO_MIN <= pe_ratio <= PE_RATIO_MAX:
                    score += FUNDAMENTAL_SCORE_PE_ATTRACTIVE
                    reasons.append(f"Attractive P/E ratio ({pe_ratio:.2f})")
                elif pe_ratio < PE_RATIO_MIN:
                    score += FUNDAMENTAL_SCORE_PE_VERY_LOW
                    reasons.append(f"Very low P/E ratio ({pe_ratio:.2f}) - potentially undervalued")
                elif pe_ratio > PE_RATIO_HIGH:
                    score += FUNDAMENTAL_SCORE_PE_HIGH
                    reasons.append(f"High P/E ratio ({pe_ratio:.2f}) - potentially overvalued")
            
            # Price-to-Book ratio
            pb_ratio = info.get('priceToBook')
            if pb_ratio:
                if pb_ratio < PB_RATIO_LOW:
                    score += FUNDAMENTAL_SCORE_PB_LOW
                    reasons.append(f"Low P/B ratio ({pb_ratio:.2f}) - trading below book value")
                elif pb_ratio < PB_RATIO_REASONABLE:
                    score += FUNDAMENTAL_SCORE_PB_REASONABLE
                    reasons.append(f"Reasonable P/B ratio ({pb_ratio:.2f})")
                elif pb_ratio > PB_RATIO_HIGH:
                    score += FUNDAMENTAL_SCORE_PB_HIGH
                    reasons.append(f"High P/B ratio ({pb_ratio:.2f})")
            
            # Debt-to-Equity
            debt_to_equity = info.get('debtToEquity')
            if debt_to_equity:
                if debt_to_equity < DEBT_TO_EQUITY_LOW:
                    score += FUNDAMENTAL_SCORE_DEBT_LOW
                    reasons.append(f"Low debt-to-equity ({debt_to_equity:.2f}) - strong balance sheet")
                elif debt_to_equity > DEBT_TO_EQUITY_HIGH:
                    score += FUNDAMENTAL_SCORE_DEBT_HIGH
                    reasons.append(f"High debt-to-equity ({debt_to_equity:.2f}) - financial risk")
            
            # Profit margins
            profit_margin = info.get('profitMargins')
            if profit_margin:
                if profit_margin > PROFIT_MARGIN_STRONG:
                    score += FUNDAMENTAL_SCORE_MARGIN_STRONG
                    reasons.append(f"Strong profit margin ({profit_margin*100:.2f}%)")
                elif profit_margin > PROFIT_MARGIN_GOOD:
                    score += FUNDAMENTAL_SCORE_MARGIN_GOOD
                    reasons.append(f"Good profit margin ({profit_margin*100:.2f}%)")
                elif profit_margin < 0:
                    score += FUNDAMENTAL_SCORE_MARGIN_NEGATIVE
                    reasons.append(f"Negative profit margin ({profit_margin*100:.2f}%)")
            
            # Revenue growth
            revenue_growth = info.get('revenueGrowth')
            if revenue_growth:
                if revenue_growth > REVENUE_GROWTH_STRONG:
                    score += FUNDAMENTAL_SCORE_REVENUE_STRONG
                    reasons.append(f"Strong revenue growth ({revenue_growth*100:.2f}%)")
                elif revenue_growth > REVENUE_GROWTH_GOOD:
                    score += FUNDAMENTAL_SCORE_REVENUE_GOOD
                    reasons.append(f"Good revenue growth ({revenue_growth*100:.2f}%)")
                elif revenue_growth < REVENUE_GROWTH_DECLINING:
                    score += FUNDAMENTAL_SCORE_REVENUE_DECLINING
                    reasons.append(f"Declining revenue ({revenue_growth*100:.2f}%)")
            
            # Earnings growth
            earnings_growth = info.get('earningsGrowth')
            if earnings_growth:
                if earnings_growth > EARNINGS_GROWTH_STRONG:
                    score += FUNDAMENTAL_SCORE_EARNINGS_STRONG
                    reasons.append(f"Strong earnings growth ({earnings_growth*100:.2f}%)")
                elif earnings_growth > EARNINGS_GROWTH_GOOD:
                    score += FUNDAMENTAL_SCORE_EARNINGS_GOOD
                    reasons.append(f"Positive earnings growth ({earnings_growth*100:.2f}%)")
                elif earnings_growth < EARNINGS_GROWTH_DECLINING:
                    score += FUNDAMENTAL_SCORE_EARNINGS_DECLINING
                    reasons.append(f"Declining earnings ({earnings_growth*100:.2f}%)")
            
            # Dividend yield
            dividend_yield = info.get('dividendYield')
            if dividend_yield and dividend_yield > 0:
                if dividend_yield > DIVIDEND_YIELD_ATTRACTIVE:
                    score += FUNDAMENTAL_SCORE_DIVIDEND_ATTRACTIVE
                    reasons.append(f"Attractive dividend yield ({dividend_yield*100:.2f}%)")
                elif dividend_yield > DIVIDEND_YIELD_MODERATE:
                    score += FUNDAMENTAL_SCORE_DIVIDEND_MODERATE
                    reasons.append(f"Moderate dividend yield ({dividend_yield*100:.2f}%)")
            
            # Market cap category
            market_cap = info.get('marketCap')
            if market_cap:
                if market_cap > MARKET_CAP_LARGE:
                    score += FUNDAMENTAL_SCORE_LARGE_CAP
                    reasons.append("Large-cap stock - established company")
        
        except Exception as e:
            reasons.append(f"Error fetching fundamental data: {str(e)}")
            confidence = FUNDAMENTAL_CONFIDENCE_ERROR
        
        # Normalize score
        score = max(MIN_SCORE, min(MAX_SCORE, score))
        
        recommendation_type = self.calculate_recommendation_type(score)
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons) if reasons else "No fundamental indicators",
            'confidence': confidence,
            'recommendation_type': recommendation_type
        }

