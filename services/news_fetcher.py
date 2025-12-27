"""News fetcher service that aggregates news from multiple sources"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import yfinance as yf
import re

class NewsArticle:
    """Represents a news article from any source"""
    def __init__(self, title: str, summary: str, source: str, url: str = "", 
                 published_date: Optional[datetime] = None):
        self.title = title
        self.summary = summary
        self.source = source
        self.url = url
        self.published_date = published_date or datetime.now()
    
    def __repr__(self):
        return f"NewsArticle(title='{self.title[:50]}...', source='{self.source}')"

class NewsFetcher:
    """Fetches news from multiple sources"""
    
    def __init__(self, newsapi_key: Optional[str] = None, alphavantage_key: Optional[str] = None):
        """
        Initialize news fetcher
        
        Args:
            newsapi_key: Optional NewsAPI key for additional news sources
            alphavantage_key: Optional Alpha Vantage key for financial news
        """
        self.newsapi_key = newsapi_key
        self.alphavantage_key = alphavantage_key
    
    def fetch_from_yfinance(self, symbol: str, max_articles: int = 50, 
                           days_back: int = 30) -> List[NewsArticle]:
        """Fetch news from Yahoo Finance"""
        articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            print(f"Yahoo Finance: Fetched {len(news) if news else 0} news items for {symbol}")
            
            if news:
                for item in news[:max_articles * 2]:  # Fetch more to filter by date
                    # Debug: print the structure of the first item
                    if len(articles) == 0:
                        print(f"Yahoo Finance news item structure: {list(item.keys())}")
                        print(f"Yahoo Finance news item sample: {item}")
                    
                    # Try different possible field names
                    title = item.get('title', '') or item.get('headline', '') or item.get('headlineText', '')
                    summary = item.get('summary', '') or item.get('description', '') or item.get('text', '') or title
                    publisher = item.get('publisher', '') or item.get('publisherName', '') or item.get('provider', '') or 'Yahoo Finance'
                    link = item.get('link', '') or item.get('url', '') or item.get('canonicalUrl', '')
                    
                    # Parse published date if available (try different field names)
                    pub_date = None
                    for date_field in ['providerPublishTime', 'pubDate', 'publishedAt', 'publishTime', 'date']:
                        if date_field in item:
                            try:
                                if isinstance(item[date_field], (int, float)):
                                    pub_date = datetime.fromtimestamp(item[date_field])
                                elif isinstance(item[date_field], str):
                                    # Try to parse ISO format or other formats
                                    try:
                                        pub_date = datetime.fromisoformat(item[date_field].replace('Z', '+00:00'))
                                    except:
                                        pass
                                break
                            except Exception as e:
                                print(f"Error parsing date field {date_field}: {e}")
                                continue
                    
                    # Filter by date range if we have a date
                    if pub_date and pub_date < cutoff_date:
                        continue
                    
                    # Ensure we have at least a title - try harder to get one
                    if not title or not title.strip():
                        # Try to extract from link or use summary
                        if summary and summary.strip():
                            title = summary[:100].strip()
                        elif link:
                            # Try to extract from URL
                            title = link.split('/')[-1].replace('-', ' ').replace('_', ' ')[:100]
                        else:
                            title = f"News about {symbol}"
                    
                    # Ensure summary exists
                    if not summary or not summary.strip():
                        summary = title
                    
                    # Ensure URL exists - construct from link or use a placeholder
                    if not link or not link.strip():
                        # Try to construct URL from other fields
                        if 'uuid' in item:
                            link = f"https://finance.yahoo.com/news/{item['uuid']}"
                        elif 'id' in item:
                            link = f"https://finance.yahoo.com/news/{item['id']}"
                        else:
                            link = f"https://finance.yahoo.com/quote/{symbol}/news"
                    
                    print(f"Creating article: title='{title[:50]}', source='{publisher}', has_url={bool(link)}")
                    
                    articles.append(NewsArticle(
                        title=title.strip(),
                        summary=summary[:500].strip() if summary else title.strip(),
                        source=f"{publisher} (via Yahoo Finance)",
                        url=link,
                        published_date=pub_date
                    ))
                    
                    if len(articles) >= max_articles:
                        break
        except Exception as e:
            print(f"Error fetching news from Yahoo Finance for {symbol}: {e}")
            import traceback
            traceback.print_exc()
        
        print(f"Yahoo Finance: Returning {len(articles)} articles for {symbol}")
        return articles
    
    def fetch_from_newsapi(self, symbol: str, max_articles: int = 50, 
                          days_back: int = 30) -> List[NewsArticle]:
        """Fetch news from NewsAPI (requires API key)"""
        articles = []
        
        if not self.newsapi_key:
            return articles
        
        try:
            import requests
            
            # Calculate date range
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            # Search for company name and symbol
            query = f"{symbol} OR {symbol.lower()}"
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': min(max_articles, 100),  # NewsAPI max is 100
                'from': from_date,
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('articles', [])[:max_articles]:
                    title = item.get('title', '')
                    description = item.get('description', '') or item.get('content', '') or title
                    source_name = item.get('source', {}).get('name', 'Unknown')
                    url_link = item.get('url', '')
                    
                    # Parse published date
                    pub_date = None
                    if item.get('publishedAt'):
                        try:
                            pub_date = datetime.fromisoformat(item['publishedAt'].replace('Z', '+00:00'))
                        except:
                            pass
                    
                    # Ensure title is not empty
                    final_title = title.strip() if title and title.strip() else (description[:100] if description else "News Article")
                    
                    articles.append(NewsArticle(
                        title=final_title,
                        summary=description[:500] if description else final_title,  # Limit summary length
                        source=f"{source_name} (via NewsAPI)",
                        url=url_link,
                        published_date=pub_date
                    ))
        except ImportError:
            print("requests library not installed. Install with: pip install requests")
        except Exception as e:
            print(f"Error fetching news from NewsAPI for {symbol}: {e}")
        
        return articles
    
    def fetch_from_alphavantage(self, symbol: str, max_articles: int = 50,
                               days_back: int = 30) -> List[NewsArticle]:
        """Fetch news from Alpha Vantage (requires API key)"""
        articles = []
        
        if not self.alphavantage_key:
            return articles
        
        try:
            import requests
            
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'NEWS_SENTIMENT',
                'tickers': symbol,
                'apikey': self.alphavantage_key,
                'limit': min(max_articles, 1000)  # Alpha Vantage max is 1000
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                feed = data.get('feed', [])
                
                cutoff_date = datetime.now() - timedelta(days=days_back)
                
                for item in feed[:max_articles * 2]:  # Fetch more to filter by date
                    title = item.get('title', '')
                    summary = item.get('summary', '') or title
                    source = item.get('source', 'Alpha Vantage')
                    url_link = item.get('url', '')
                    
                    # Parse published date
                    pub_date = None
                    if item.get('time_published'):
                        try:
                            # Format: YYYYMMDDTHHMMSS
                            time_str = item['time_published']
                            pub_date = datetime.strptime(time_str, '%Y%m%dT%H%M%S')
                        except:
                            pass
                    
                    # Filter by date range
                    if pub_date and pub_date < cutoff_date:
                        continue
                    
                    # Ensure title is not empty
                    final_title = title.strip() if title and title.strip() else (summary[:100] if summary else "News Article")
                    
                    articles.append(NewsArticle(
                        title=final_title,
                        summary=summary[:500] if summary else final_title,
                        source=f"{source} (via Alpha Vantage)",
                        url=url_link,
                        published_date=pub_date
                    ))
                    
                    if len(articles) >= max_articles:
                        break
        except ImportError:
            print("requests library not installed. Install with: pip install requests")
        except Exception as e:
            print(f"Error fetching news from Alpha Vantage for {symbol}: {e}")
        
        return articles
    
    def get_stock_sector_info(self, symbol: str) -> Dict[str, str]:
        """Get stock sector and industry information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'longName': info.get('longName', symbol)
            }
        except:
            return {'sector': '', 'industry': '', 'longName': symbol}
    
    def get_related_market_keywords(self, sector: str, industry: str) -> List[str]:
        """Get related market keywords based on sector/industry"""
        # Map sectors/industries to related market topics
        related_topics = {
            'energy': ['oil', 'gas', 'war', 'conflict', 'geopolitics', 'OPEC', 'crude', 'petroleum'],
            'oil': ['war', 'conflict', 'geopolitics', 'OPEC', 'crude', 'petroleum', 'energy'],
            'technology': ['tech', 'AI', 'innovation', 'semiconductors', 'chips', 'regulation'],
            'healthcare': ['health', 'FDA', 'drug', 'pharmaceutical', 'medical', 'regulation'],
            'financial': ['banking', 'interest rates', 'Fed', 'economy', 'inflation', 'monetary policy'],
            'consumer': ['consumer', 'retail', 'spending', 'economy', 'inflation'],
            'industrial': ['manufacturing', 'supply chain', 'trade', 'economy'],
            'materials': ['commodities', 'metals', 'mining', 'trade', 'economy'],
            'utilities': ['energy', 'regulation', 'infrastructure', 'climate'],
            'real estate': ['housing', 'interest rates', 'economy', 'Fed'],
            'telecommunications': ['5G', 'infrastructure', 'regulation', 'tech']
        }
        
        keywords = []
        sector_lower = sector.lower() if sector else ''
        industry_lower = industry.lower() if industry else ''
        
        # Check sector
        for key, topics in related_topics.items():
            if key in sector_lower or key in industry_lower:
                keywords.extend(topics)
        
        return list(set(keywords))  # Remove duplicates
    
    def fetch_related_market_news(self, keywords: List[str], max_articles: int = 50,
                                 days_back: int = 30) -> List[NewsArticle]:
        """Fetch news related to market topics (e.g., war news for oil stocks)"""
        articles = []
        
        if not keywords or not self.newsapi_key:
            return articles
        
        try:
            import requests
            
            # Create query from keywords
            query = ' OR '.join(keywords[:5])  # Limit to 5 keywords to avoid query too long
            
            # Calculate date range
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': min(max_articles, 100),
                'from': from_date,
                'apiKey': self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('articles', [])[:max_articles]:
                    title = item.get('title', '')
                    description = item.get('description', '') or item.get('content', '') or title
                    source_name = item.get('source', {}).get('name', 'Unknown')
                    url_link = item.get('url', '')
                    
                    # Parse published date
                    pub_date = None
                    if item.get('publishedAt'):
                        try:
                            pub_date = datetime.fromisoformat(item['publishedAt'].replace('Z', '+00:00'))
                        except:
                            pass
                    
                    # Ensure title is not empty
                    final_title = title.strip() if title and title.strip() else (description[:100] if description else "Related Market News")
                    
                    articles.append(NewsArticle(
                        title=final_title,
                        summary=description[:500] if description else final_title,
                        source=f"{source_name} (Related Market News)",
                        url=url_link,
                        published_date=pub_date
                    ))
        except Exception as e:
            print(f"Error fetching related market news: {e}")
        
        return articles
    
    def fetch_from_rss_feeds(self, symbol: str, max_articles: int = 50, 
                             days_back: int = 30) -> List[NewsArticle]:
        """Fetch news from RSS feeds (free, no API key required)"""
        articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # Financial news RSS feeds from multiple sources
        rss_feeds = [
            # Yahoo Finance RSS feeds
            f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US",
            # MarketWatch (via Google News RSS)
            f"https://news.google.com/rss/search?q={symbol}+site:marketwatch.com&hl=en-US&gl=US&ceid=US:en",
            # CNBC (via Google News RSS)
            f"https://news.google.com/rss/search?q={symbol}+site:cnbc.com&hl=en-US&gl=US&ceid=US:en",
            # Reuters Finance (via Google News RSS)
            f"https://news.google.com/rss/search?q={symbol}+site:reuters.com/finance&hl=en-US&gl=US&ceid=US:en",
            # Seeking Alpha
            f"https://seekingalpha.com/api/sa/combined/{symbol}.xml",
            # Benzinga (via Google News RSS)
            f"https://news.google.com/rss/search?q={symbol}+site:benzinga.com&hl=en-US&gl=US&ceid=US:en",
        ]
        
        try:
            import feedparser
            
            for feed_url in rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    if feed.bozo == 0:  # No parsing errors
                        for entry in feed.entries[:max_articles]:
                            title = entry.get('title', '')
                            summary = entry.get('summary', '') or entry.get('description', '') or title
                            link = entry.get('link', '')
                            
                            # Parse published date
                            pub_date = None
                            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                                try:
                                    pub_date = datetime(*entry.published_parsed[:6])
                                except:
                                    pass
                            elif hasattr(entry, 'published'):
                                try:
                                    from email.utils import parsedate_to_datetime
                                    pub_date = parsedate_to_datetime(entry.published)
                                except:
                                    pass
                            
                            # Filter by date
                            if pub_date and pub_date < cutoff_date:
                                continue
                            
                            if title and title.strip():
                                # Determine source name from feed URL
                                source_name = "RSS Feed"
                                if "yahoo.com" in feed_url or "finance.yahoo.com" in feed_url:
                                    source_name = "Yahoo Finance RSS"
                                elif "marketwatch.com" in feed_url or "marketwatch" in feed_url.lower():
                                    source_name = "MarketWatch"
                                elif "cnbc.com" in feed_url or "cnbc" in feed_url.lower():
                                    source_name = "CNBC"
                                elif "reuters.com" in feed_url or "reuters" in feed_url.lower():
                                    source_name = "Reuters"
                                elif "seekingalpha.com" in feed_url or "seekingalpha" in feed_url.lower():
                                    source_name = "Seeking Alpha"
                                elif "benzinga.com" in feed_url or "benzinga" in feed_url.lower():
                                    source_name = "Benzinga"
                                elif "ft.com" in feed_url or "financialtimes" in feed_url.lower():
                                    source_name = "Financial Times"
                                elif "bloomberg.com" in feed_url or "bloomberg" in feed_url.lower():
                                    source_name = "Bloomberg"
                                
                                articles.append(NewsArticle(
                                    title=title.strip(),
                                    summary=summary[:500].strip() if summary else title.strip(),
                                    source=source_name,
                                    url=link,
                                    published_date=pub_date
                                ))
                except Exception as e:
                    print(f"Error fetching RSS feed {feed_url}: {e}")
                    continue
        except ImportError:
            pass  # feedparser not installed, skip RSS feeds
        except Exception as e:
            print(f"Error fetching RSS feeds for {symbol}: {e}")
        
        return articles
    
    def fetch_from_google_news(self, symbol: str, max_articles: int = 50,
                               days_back: int = 30) -> List[NewsArticle]:
        """Fetch news from Google News search (free, no API key)"""
        articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        try:
            import feedparser
            
            # Multiple Google News queries for better coverage
            queries = [
                f"{symbol} stock",
                f"{symbol} shares",
            ]
            
            for query in queries:
                url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
                
                feed = feedparser.parse(url)
                
                if feed.bozo == 0:
                    for entry in feed.entries[:max_articles // len(queries)]:  # Distribute articles across queries
                        title = entry.get('title', '')
                        summary = entry.get('summary', '') or entry.get('description', '') or title
                        link = entry.get('link', '')
                        
                        # Parse published date
                        pub_date = None
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            try:
                                pub_date = datetime(*entry.published_parsed[:6])
                            except:
                                pass
                        
                        # Filter by date
                        if pub_date and pub_date < cutoff_date:
                            continue
                        
                        if title and title.strip():
                            articles.append(NewsArticle(
                                title=title.strip(),
                                summary=summary[:500].strip() if summary else title.strip(),
                                source="Google News",
                                url=link,
                                published_date=pub_date
                            ))
        except ImportError:
            pass  # feedparser not installed, skip Google News
        except Exception as e:
            print(f"Error fetching Google News for {symbol}: {e}")
        
        return articles
    
    def fetch_all_sources(self, symbol: str, max_articles_per_source: int = 50,
                         days_back: int = 30, include_related_market: bool = True) -> List[NewsArticle]:
        """
        Fetch news from all available sources and deduplicate
        
        Args:
            symbol: Stock symbol
            max_articles_per_source: Maximum articles to fetch from each source
            days_back: Number of days to look back for news
            include_related_market: Whether to include related market news (e.g., war news for oil)
            
        Returns:
            List of unique news articles sorted by date (newest first)
        """
        all_articles = []
        sources_used = []
        
        # Fetch from all sources (free sources first)
        print(f"\n=== Fetching news for {symbol} from multiple sources ===")
        
        # Free sources (no API key required)
        yf_articles = self.fetch_from_yfinance(symbol, max_articles_per_source, days_back)
        if yf_articles:
            all_articles.extend(yf_articles)
            sources_used.append(f"Yahoo Finance ({len(yf_articles)} articles)")
        
        rss_articles = self.fetch_from_rss_feeds(symbol, max_articles_per_source, days_back)
        if rss_articles:
            all_articles.extend(rss_articles)
            sources_used.append(f"RSS Feeds ({len(rss_articles)} articles)")
        
        google_articles = self.fetch_from_google_news(symbol, max_articles_per_source, days_back)
        if google_articles:
            all_articles.extend(google_articles)
            sources_used.append(f"Google News ({len(google_articles)} articles)")
        
        # API-based sources (require API keys)
        newsapi_articles = self.fetch_from_newsapi(symbol, max_articles_per_source, days_back)
        if newsapi_articles:
            all_articles.extend(newsapi_articles)
            sources_used.append(f"NewsAPI ({len(newsapi_articles)} articles)")
        
        alphavantage_articles = self.fetch_from_alphavantage(symbol, max_articles_per_source, days_back)
        if alphavantage_articles:
            all_articles.extend(alphavantage_articles)
            sources_used.append(f"Alpha Vantage ({len(alphavantage_articles)} articles)")
        
        # Fetch related market news if enabled
        if include_related_market:
            sector_info = self.get_stock_sector_info(symbol)
            keywords = self.get_related_market_keywords(
                sector_info.get('sector', ''),
                sector_info.get('industry', '')
            )
            if keywords:
                related_articles = self.fetch_related_market_news(
                    keywords, 
                    max_articles=max_articles_per_source // 2,  # Half the amount for related news
                    days_back=days_back
                )
                if related_articles:
                    all_articles.extend(related_articles)
                    sources_used.append(f"Related Market News ({len(related_articles)} articles)")
        
        print(f"Sources used: {', '.join(sources_used) if sources_used else 'None'}")
        
        # Deduplicate based on title similarity
        unique_articles = []
        seen_titles = set()
        
        for article in all_articles:
            # Normalize title for comparison
            title_lower = article.title.lower().strip()
            
            # Check if we've seen a similar title (simple deduplication)
            is_duplicate = False
            for seen_title in seen_titles:
                # If titles are very similar (80% overlap), consider duplicate
                if self._similarity(title_lower, seen_title) > 0.8:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_articles.append(article)
                seen_titles.add(title_lower)
        
        # Sort by date (newest first)
        unique_articles.sort(key=lambda x: x.published_date, reverse=True)
        
        return unique_articles
    
    def _similarity(self, str1: str, str2: str) -> float:
        """Calculate simple string similarity (0.0 to 1.0)"""
        if not str1 or not str2:
            return 0.0
        
        # Simple word overlap similarity
        words1 = set(str1.split())
        words2 = set(str2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0

