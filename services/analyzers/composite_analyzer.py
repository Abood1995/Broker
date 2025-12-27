from typing import Dict, List
from models.stock import Stock
from models.recommendation import Recommendation, RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, DEFAULT_CONFIDENCE, DEFAULT_NO_ANALYZERS_REASONING,
    COMPOSITE_DEFAULT_SCORE, COMPOSITE_DEFAULT_CONFIDENCE
)

class CompositeAnalyzer(BaseAnalyzer):
    """Composite analyzer that combines multiple analyzers (Composite Pattern)"""
    
    def __init__(self, analyzers: List[BaseAnalyzer], name: str = "Composite Analysis"):
        """
        Initialize composite analyzer
        
        Args:
            analyzers: List of analyzers to combine
            name: Name of the composite analyzer
        """
        super().__init__(name, weight=1.0)
        self.analyzers = analyzers
    
    def analyze(self, stock: Stock) -> Dict:
        """Combine results from all analyzers"""
        if not self.analyzers:
            return {
                'score': COMPOSITE_DEFAULT_SCORE,
                'reasoning': DEFAULT_NO_ANALYZERS_REASONING,
                'confidence': COMPOSITE_DEFAULT_CONFIDENCE,
                'recommendation_type': RecommendationType.HOLD
            }
        
        all_reasons = []
        weighted_score = 0.0
        total_weight = 0.0
        weighted_confidence = 0.0
        all_articles = []  # Collect articles from analyzers
        
        # Run all analyzers and combine results
        for analyzer in self.analyzers:
            try:
                result = analyzer.analyze(stock)
                score = result.get('score', DEFAULT_SCORE)
                reasoning = result.get('reasoning', '')
                confidence = result.get('confidence', DEFAULT_CONFIDENCE)
                
                # Collect articles if available (from NewsAnalyzer)
                if 'articles' in result and result['articles']:
                    article_count = len(result['articles'])
                    print(f"CompositeAnalyzer: Found {article_count} articles from {analyzer.name}")
                    all_articles.extend(result['articles'])
                
                # Weight the score and confidence
                weight = analyzer.weight
                weighted_score += score * weight
                weighted_confidence += confidence * weight
                total_weight += weight
                
                # Collect reasoning
                all_reasons.append(f"{analyzer.name}: {reasoning}")
            
            except Exception as e:
                all_reasons.append(f"{analyzer.name}: Error - {str(e)}")
        
        # Calculate weighted averages
        if total_weight > 0:
            final_score = weighted_score / total_weight
            final_confidence = weighted_confidence / total_weight
        else:
            final_score = COMPOSITE_DEFAULT_SCORE
            final_confidence = COMPOSITE_DEFAULT_CONFIDENCE
        
        # Determine final recommendation type
        recommendation_type = self.calculate_recommendation_type(final_score)
        
        # Remove duplicate articles (based on title and URL)
        unique_articles = []
        seen_keys = set()
        for article in all_articles:
            # Use title if available, otherwise use URL, otherwise use a combination
            if article.title and article.title.strip():
                title_key = article.title.lower().strip()
            elif article.url and article.url.strip():
                title_key = article.url.lower().strip()
            else:
                # If no title or URL, use source + summary (first 50 chars)
                summary_key = article.summary[:50].lower().strip() if article.summary else ""
                title_key = f"{article.source}_{summary_key}"
            
            # Create a unique key
            unique_key = title_key
            
            if unique_key not in seen_keys:
                unique_articles.append(article)
                seen_keys.add(unique_key)
        
        print(f"CompositeAnalyzer: Total unique articles collected: {len(unique_articles)} (from {len(all_articles)} total)")
        
        return {
            'score': final_score,
            'reasoning': " | ".join(all_reasons),
            'confidence': final_confidence,
            'recommendation_type': recommendation_type,
            'articles': unique_articles  # Include articles in result
        }
    
    def add_analyzer(self, analyzer: BaseAnalyzer):
        """Add an analyzer to the composite"""
        self.analyzers.append(analyzer)
    
    def remove_analyzer(self, analyzer: BaseAnalyzer):
        """Remove an analyzer from the composite"""
        if analyzer in self.analyzers:
            self.analyzers.remove(analyzer)
    
    def get_analyzer_count(self) -> int:
        """Get the number of analyzers in the composite"""
        return len(self.analyzers)

