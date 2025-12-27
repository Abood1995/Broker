from abc import ABC, abstractmethod
from typing import Dict, List
from models.stock import Stock
from models.recommendation import Recommendation, RecommendationType
from services.analyzers.constants import (
    SCORE_STRONG_BUY_THRESHOLD, SCORE_BUY_THRESHOLD, SCORE_HOLD_THRESHOLD,
    SCORE_SELL_THRESHOLD, TARGET_PRICE_MULTIPLIER, DEFAULT_SCORE,
    DEFAULT_CONFIDENCE, DEFAULT_REASONING
)

class BaseAnalyzer(ABC):
    """Abstract base class for all stock analyzers (Strategy Pattern)"""
    
    def __init__(self, name: str, weight: float = 1.0):
        """
        Initialize the analyzer
        
        Args:
            name: Name of the analyzer strategy
            weight: Weight of this analyzer in composite analysis (default: 1.0)
        """
        self.name = name
        self.weight = weight
    
    @abstractmethod
    def analyze(self, stock: Stock) -> Dict:
        """
        Analyze a stock and return analysis results
        
        Args:
            stock: Stock to analyze
            
        Returns:
            Dictionary containing:
                - score: float (0.0 to 1.0) - analysis score
                - reasoning: str - explanation of the analysis
                - confidence: float (0.0 to 1.0) - confidence in the analysis
                - recommendation_type: RecommendationType - suggested recommendation
        """
        pass
    
    def calculate_recommendation_type(self, score: float) -> RecommendationType:
        """Convert score to recommendation type"""
        if score >= SCORE_STRONG_BUY_THRESHOLD:
            return RecommendationType.STRONG_BUY
        elif score >= SCORE_BUY_THRESHOLD:
            return RecommendationType.BUY
        elif score >= SCORE_HOLD_THRESHOLD:
            return RecommendationType.HOLD
        elif score >= SCORE_SELL_THRESHOLD:
            return RecommendationType.SELL
        else:
            return RecommendationType.STRONG_SELL
    
    def create_recommendation(self, stock: Stock, analysis_result: Dict) -> Recommendation:
        """Create a Recommendation object from analysis results"""
        score = analysis_result.get('score', DEFAULT_SCORE)
        reasoning = analysis_result.get('reasoning', DEFAULT_REASONING)
        confidence = analysis_result.get('confidence', DEFAULT_CONFIDENCE)
        recommendation_type = analysis_result.get('recommendation_type', 
                                                  self.calculate_recommendation_type(score))
        articles = analysis_result.get('articles', [])  # Get articles from analysis result
        
        # Calculate target price for buy recommendations
        target_price = None
        if recommendation_type in [RecommendationType.BUY, RecommendationType.STRONG_BUY]:
            target_price = stock.current_price * TARGET_PRICE_MULTIPLIER
        
        # For composite analyzer, don't add prefix as it already includes analyzer names
        if self.name == "Composite Analysis":
            final_reasoning = reasoning
        else:
            final_reasoning = f"[{self.name}] {reasoning}"
        
        return Recommendation(
            stock=stock,
            recommendation_type=recommendation_type,
            confidence_score=confidence,
            reasoning=final_reasoning,
            target_price=target_price,
            articles=articles  # Include articles in recommendation
        )
    
    def __str__(self):
        return f"{self.name} (weight: {self.weight})"

