from typing import Dict, List, Optional
from models.stock import Stock
from models.recommendation import RecommendationType
from services.analyzers.base_analyzer import BaseAnalyzer
from services.analyzers.constants import (
    DEFAULT_SCORE, DEFAULT_CONFIDENCE, MIN_SCORE, MAX_SCORE,
    NEWS_COUNT_THRESHOLD, NEWS_ARTICLES_TO_CHECK, NEWS_ARTICLES_PER_SOURCE,
    NEWS_SENTIMENT_MULTIPLIER, NEWS_CONFIDENCE_BASE, NEWS_CONFIDENCE_NO_NEWS,
    NEWS_CONFIDENCE_MAX, NEWS_CONFIDENCE_ERROR, NEWS_SCORE_HIGH_ACTIVITY,
    NEWS_SCORE_POSITIVE_SENTIMENT, NEWS_SCORE_NEGATIVE_SENTIMENT,
    NEWS_CONFIDENCE_CALCULATION_DIVISOR, NEWS_LLM_CONFIDENCE_BOOST
)
from services.news_fetcher import NewsFetcher
from services.llm_analyzer import LLMNewsAnalyzer

class NewsAnalyzer(BaseAnalyzer):
    """Analyzer based on news sentiment and recent news from multiple sources"""
    
    def __init__(self, weight: float = 1.0, 
                 newsapi_key: Optional[str] = None,
                 alphavantage_key: Optional[str] = None,
                 openai_api_key: Optional[str] = None,
                 huggingface_api_key: Optional[str] = None,
                 groq_api_key: Optional[str] = None,
                 gemini_api_key: Optional[str] = None,
                 llm_provider: str = "auto"):
        """
        Initialize news analyzer
        
        Args:
            weight: Weight of this analyzer in composite analysis
            newsapi_key: Optional NewsAPI key for additional news sources
            alphavantage_key: Optional Alpha Vantage key for financial news
            openai_api_key: Optional OpenAI API key for LLM-based sentiment analysis (paid)
            huggingface_api_key: Optional Hugging Face API key for free LLM analysis
            groq_api_key: Optional Groq API key for free LLM analysis (very fast)
            gemini_api_key: Optional Google Gemini API key for free LLM analysis
            llm_provider: LLM provider to use - "auto" (tries free first), "gemini", "groq", "huggingface", "openai"
        """
        super().__init__("News Analysis", weight)
        self.news_count_threshold = NEWS_COUNT_THRESHOLD
        self.news_fetcher = NewsFetcher(
            newsapi_key=newsapi_key,
            alphavantage_key=alphavantage_key
        )
        self.llm_analyzer = LLMNewsAnalyzer(
            openai_api_key=openai_api_key,
            huggingface_api_key=huggingface_api_key,
            groq_api_key=groq_api_key,
            gemini_api_key=gemini_api_key,
            llm_provider=llm_provider
        )
    
    def analyze(self, stock: Stock) -> Dict:
        """Analyze stock based on news sentiment from multiple sources"""
        score = DEFAULT_SCORE  # Start neutral
        reasons = []
        confidence = NEWS_CONFIDENCE_BASE  # News sentiment can be volatile
        
        try:
            # Fetch news from all available sources with date range and related market news
            from services.analyzers.constants import RECENT_NEWS_DAYS, NEWS_RELATED_MARKET_ARTICLES
            articles = self.news_fetcher.fetch_all_sources(
                stock.symbol, 
                max_articles_per_source=NEWS_ARTICLES_PER_SOURCE,
                days_back=RECENT_NEWS_DAYS,
                include_related_market=True
            )
            
            if not articles:
                reasons.append("No recent news available from any source")
                confidence = NEWS_CONFIDENCE_NO_NEWS
                print(f"No recent news available for {stock.symbol}")
            else:
                news_count = len(articles)
                
                # Analyze news count
                if news_count >= self.news_count_threshold:
                    score += NEWS_SCORE_HIGH_ACTIVITY
                    reasons.append(f"High news activity ({news_count} articles from multiple sources)")
                elif news_count > 0:
                    reasons.append(f"Moderate news activity ({news_count} articles)")
                
                # Get sources used
                sources = set(article.source for article in articles)
                reasons.append(f"Sources: {len(sources)} different sources")
                
                # Use LLM for sentiment analysis if available, otherwise fallback to keywords
                # Analyze up to NEWS_ARTICLES_TO_CHECK articles (currently 100)
                articles_to_analyze = articles[:NEWS_ARTICLES_TO_CHECK]
                print(f"📊 Sending {len(articles_to_analyze)} articles to LLM for sentiment analysis (out of {len(articles)} total articles)")
                if len(articles) > NEWS_ARTICLES_TO_CHECK:
                    print(f"⚠️  Note: {len(articles) - NEWS_ARTICLES_TO_CHECK} articles will not be analyzed by LLM (limit: {NEWS_ARTICLES_TO_CHECK})")
                
                sentiment_result = self.llm_analyzer.analyze_sentiment_llm(articles_to_analyze)
                
                # Apply sentiment to score
                sentiment_score = sentiment_result.get('sentiment_score', 0.5)
                sentiment = sentiment_result.get('sentiment', 'neutral')
                impact = sentiment_result.get('impact', 'neutral')
                method = sentiment_result.get('method', 'keyword')
                
                # Adjust score based on sentiment
                if sentiment == 'positive' or impact == 'bullish':
                    score += NEWS_SCORE_POSITIVE_SENTIMENT
                    reasons.append(f"Positive news sentiment ({method} analysis)")
                elif sentiment == 'negative' or impact == 'bearish':
                    score += NEWS_SCORE_NEGATIVE_SENTIMENT
                    reasons.append(f"Negative news sentiment ({method} analysis)")
                else:
                    reasons.append(f"Neutral news sentiment ({method} analysis)")
                
                # Add themes if available from LLM
                themes = sentiment_result.get('themes', [])
                if themes:
                    reasons.append(f"Key themes: {', '.join(themes[:3])}")
                
                # Add summary if available
                summary = sentiment_result.get('summary', '')
                if summary:
                    reasons.append(f"Summary: {summary[:100]}")
                
                # Calculate confidence
                base_confidence = min(
                    NEWS_CONFIDENCE_MAX, 
                    NEWS_CONFIDENCE_BASE + (news_count / NEWS_CONFIDENCE_CALCULATION_DIVISOR)
                )
                
                # Boost confidence if using LLM (check if method starts with 'llm')
                if method.startswith('llm'):
                    # Additional boost if multiple LLM providers were used
                    provider_count = method.count('+') + 1 if '+' in method else 1
                    llm_boost = NEWS_LLM_CONFIDENCE_BOOST * (1 + 0.1 * (provider_count - 1))
                    confidence = min(NEWS_CONFIDENCE_MAX, base_confidence + llm_boost)
                else:
                    confidence = base_confidence
                
                # Additional confidence boost for multiple sources
                if len(sources) > 1:
                    confidence = min(NEWS_CONFIDENCE_MAX, confidence + 0.05)
        
        except Exception as e:
            reasons.append(f"Error fetching news: {str(e)}")
            confidence = NEWS_CONFIDENCE_ERROR
        
        # Normalize score
        score = max(MIN_SCORE, min(MAX_SCORE, score))
        
        recommendation_type = self.calculate_recommendation_type(score)
        
        # Ensure articles list exists
        if 'articles' not in locals():
            articles = []
        
        print(f"NewsAnalyzer.analyze: Returning {len(articles)} articles for {stock.symbol}")
        if len(articles) > 0:
            print(f"NewsAnalyzer.analyze: First article: {articles[0].title[:50] if articles[0].title else 'No title'}")
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons) if reasons else "No news indicators",
            'confidence': confidence,
            'recommendation_type': recommendation_type,
            'articles': articles  # Store articles for UI
        }

