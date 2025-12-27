from typing import List, Optional
from models.stock import Stock
from models.recommendation import Recommendation
from services.data_fetcher import DataFetcher
from services.analyzers.composite_analyzer import CompositeAnalyzer
from services.analyzers.price_analyzer import PriceAnalyzer
from services.analyzers.volume_analyzer import VolumeAnalyzer
from services.analyzers.news_analyzer import NewsAnalyzer
from services.analyzers.technical_strategy_analyzer import TechnicalStrategyAnalyzer
from services.analyzers.period_based_analyzer import PeriodBasedAnalyzer
from services.analyzers.support_resistance_analyzer import SupportResistanceAnalyzer
from services.analyzers.fundamental_analyzer import FundamentalAnalyzer
from services.analyzers.momentum_analyzer import MomentumAnalyzer
from services.analyzers.volatility_analyzer import VolatilityAnalyzer
import config

class StockAnalyzer:
    """Main analyzer that coordinates multiple analysis strategies"""
    
    def __init__(self, data_fetcher: DataFetcher, 
                 use_price: bool = True,
                 use_volume: bool = True,
                 use_news: bool = True,
                 use_technical: bool = True,
                 use_period: bool = True,
                 use_support_resistance: bool = True,
                 use_fundamental: bool = True,
                 use_momentum: bool = True,
                 use_volatility: bool = True,
                 analyzer_weights: Optional[dict] = None):
        """
        Initialize the stock analyzer with configurable strategies
        
        Args:
            data_fetcher: Data fetcher service
            use_price: Enable price-based analysis
            use_volume: Enable volume-based analysis
            use_news: Enable news-based analysis
            use_technical: Enable technical strategy analysis
            use_period: Enable period-based analysis (week, month, quarter)
            use_support_resistance: Enable support/resistance analysis
            use_fundamental: Enable fundamental analysis
            use_momentum: Enable momentum analysis
            use_volatility: Enable volatility analysis
            analyzer_weights: Dictionary of analyzer weights (e.g., {'price': 1.5, 'news': 0.8})
        """
        self.data_fetcher = data_fetcher
        
        # Create analyzers based on configuration
        analyzers = []
        
        if use_price:
            weight = analyzer_weights.get('price', 1.0) if analyzer_weights else 1.0
            analyzers.append(PriceAnalyzer(weight=weight))
        
        if use_volume:
            weight = analyzer_weights.get('volume', 1.0) if analyzer_weights else 1.0
            analyzers.append(VolumeAnalyzer(weight=weight))
        
        if use_news:
            weight = analyzer_weights.get('news', 1.0) if analyzer_weights else 1.0
            analyzers.append(NewsAnalyzer(
                weight=weight,
                newsapi_key=config.NEWSAPI_KEY,
                alphavantage_key=config.ALPHAVANTAGE_KEY,
                openai_api_key=config.OPENAI_API_KEY,
                huggingface_api_key=config.HUGGINGFACE_API_KEY,
                groq_api_key=config.GROQ_API_KEY,
                gemini_api_key=config.GEMINI_API_KEY,
                llm_provider=config.LLM_PROVIDER
            ))
        
        if use_technical:
            weight = analyzer_weights.get('technical', 1.0) if analyzer_weights else 1.0
            analyzers.append(TechnicalStrategyAnalyzer(weight=weight))
        
        if use_period:
            weight = analyzer_weights.get('period', 1.2) if analyzer_weights else 1.2
            analyzers.append(PeriodBasedAnalyzer(weight=weight))
        
        if use_support_resistance:
            weight = analyzer_weights.get('support_resistance', 1.1) if analyzer_weights else 1.1
            analyzers.append(SupportResistanceAnalyzer(weight=weight))
        
        if use_fundamental:
            weight = analyzer_weights.get('fundamental', 1.0) if analyzer_weights else 1.0
            analyzers.append(FundamentalAnalyzer(weight=weight))
        
        if use_momentum:
            weight = analyzer_weights.get('momentum', 1.0) if analyzer_weights else 1.0
            analyzers.append(MomentumAnalyzer(weight=weight))
        
        if use_volatility:
            weight = analyzer_weights.get('volatility', 0.8) if analyzer_weights else 0.8
            analyzers.append(VolatilityAnalyzer(weight=weight))
        
        # Create composite analyzer
        self.composite_analyzer = CompositeAnalyzer(analyzers)
    
    def analyze_stock(self, stock: Stock) -> Recommendation:
        """Analyze a stock using all configured analyzers"""
        analysis_result = self.composite_analyzer.analyze(stock)
        return self.composite_analyzer.create_recommendation(stock, analysis_result)
    
    def analyze_multiple_stocks(self, symbols: List[str]) -> List[Recommendation]:
        """Analyze multiple stocks and return recommendations"""
        stocks = self.data_fetcher.fetch_multiple_stocks(symbols)
        recommendations = []
        for stock in stocks:
            rec = self.analyze_stock(stock)
            recommendations.append(rec)
        return sorted(recommendations, key=lambda x: x.confidence_score, reverse=True)
    
    def get_active_analyzers(self) -> List[str]:
        """Get list of active analyzer names"""
        return [analyzer.name for analyzer in self.composite_analyzer.analyzers]

