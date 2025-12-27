"""LLM-based news sentiment analyzer with support for free LLM providers"""
from typing import List, Dict, Optional
from services.news_fetcher import NewsArticle

class LLMNewsAnalyzer:
    """Analyzes news sentiment using LLM (with fallback to keyword-based)"""
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 huggingface_api_key: Optional[str] = None,
                 groq_api_key: Optional[str] = None,
                 gemini_api_key: Optional[str] = None,
                 llm_provider: str = "auto"):
        """
        Initialize LLM analyzer
        
        Args:
            openai_api_key: Optional OpenAI API key (paid)
            huggingface_api_key: Optional Hugging Face API key (free tier available)
            groq_api_key: Optional Groq API key (free tier available)
            gemini_api_key: Optional Google Gemini API key (free tier available)
            llm_provider: Provider to use - "auto" (tries free first), "huggingface", "groq", "gemini", "openai"
        """
        self.openai_key = openai_api_key
        self.huggingface_key = huggingface_api_key
        self.groq_key = groq_api_key
        self.gemini_key = gemini_api_key
        self.provider = llm_provider
        self.use_llm = any([huggingface_api_key, groq_api_key, gemini_api_key, openai_api_key])
    
    def analyze_sentiment_llm(self, articles: List[NewsArticle]) -> Dict:
        """
        Analyze news sentiment using ALL available LLM providers and aggregate results
        
        Args:
            articles: List of news articles to analyze
            
        Returns:
            Dictionary with aggregated sentiment analysis results from all working providers
        """
        print(f"\n🤖 LLM Analysis: Processing {len(articles)} articles")
        
        if not self.use_llm or not articles:
            print("⚠️  LLM not available or no articles - using keyword fallback")
            return self._fallback_keyword_analysis(articles)
        
        # Prepare prompt
        prompt = self._create_analysis_prompt(articles)
        print(f"📝 Created prompt with {len(articles)} articles (prompt length: {len(prompt)} chars)")
        
        # Define provider order and methods
        providers = []
        if self.provider == "auto":
            # Auto mode: try all available providers in order (free first)
            if self.gemini_key:
                providers.append(("gemini", self._try_gemini))
            if self.groq_key:
                providers.append(("groq", self._try_groq))
            if self.huggingface_key:
                providers.append(("huggingface", self._try_huggingface))
            if self.openai_key:
                providers.append(("openai", self._try_openai))
        else:
            # Specific provider mode: try specified provider first, then fallback to others
            provider_map = {
                "gemini": (self.gemini_key, self._try_gemini),
                "groq": (self.groq_key, self._try_groq),
                "huggingface": (self.huggingface_key, self._try_huggingface),
                "openai": (self.openai_key, self._try_openai)
            }
            
            # Add specified provider first
            if self.provider in provider_map:
                key, method = provider_map[self.provider]
                if key:
                    providers.append((self.provider, method))
            
            # Add other available providers as fallback
            for name, (key, method) in provider_map.items():
                if name != self.provider and key:
                    providers.append((name, method))
        
        # Try ALL providers and collect successful results
        successful_results = []
        successful_providers = []
        last_error = None
        
        print(f"🔄 Attempting to use {len(providers)} LLM provider(s): {', '.join([p[0] for p in providers])}")
        
        for provider_name, provider_method in providers:
            try:
                result = provider_method(prompt)
                if result and result.get('sentiment_score') is not None:
                    # Success - collect this result
                    successful_results.append(result)
                    successful_providers.append(provider_name)
                    print(f"✓ Successfully used {provider_name} for sentiment analysis")
                else:
                    # Provider returned None or invalid result
                    print(f"⚠ {provider_name} returned invalid result, skipping...")
            except Exception as e:
                # Provider failed - log and continue
                error_msg = str(e)
                print(f"✗ {provider_name} failed: {error_msg[:100]}... Skipping...")
                last_error = e
                continue
        
        # If we have successful results, aggregate them
        if successful_results:
            print(f"📊 Aggregating results from {len(successful_results)} working LLM provider(s): {', '.join(successful_providers)}")
            aggregated = self._aggregate_llm_results(successful_results, successful_providers)
            print(f"✅ Final aggregated sentiment: {aggregated.get('sentiment', 'unknown')}, Score: {aggregated.get('sentiment_score', 0):.2f}, Impact: {aggregated.get('impact', 'unknown')}")
            print(f"   Confidence: {aggregated.get('confidence', 0):.2f}, Themes: {len(aggregated.get('themes', []))} themes found")
            return aggregated
        
        # All providers failed - fallback to keyword analysis
        print(f"⚠️  All LLM providers failed. Falling back to keyword-based analysis for {len(articles)} articles")
        if last_error:
            print(f"   Last error: {str(last_error)[:200]}")
        fallback_result = self._fallback_keyword_analysis(articles)
        print(f"📊 Keyword analysis result: {fallback_result.get('sentiment', 'unknown')}, Score: {fallback_result.get('sentiment_score', 0):.2f}")
        return fallback_result
    
    def _create_analysis_prompt(self, articles: List[NewsArticle]) -> str:
        """Create the analysis prompt from articles with dates"""
        article_texts = []
        articles_processed = 0
        max_articles = 100  # Limit to avoid token limits
        
        for article in articles[:max_articles]:
            # Format date if available
            date_str = ""
            if article.published_date:
                try:
                    date_str = article.published_date.strftime("%Y-%m-%d")
                except:
                    pass
            
            text = f"Date: {date_str}\nTitle: {article.title}\nSummary: {article.summary[:200]}"
            article_texts.append(text)
            articles_processed += 1
        
        if len(articles) > max_articles:
            print(f"⚠️  Limited to {max_articles} articles in prompt (had {len(articles)} total) to avoid token limits")
        
        print(f"✅ Prepared {articles_processed} articles for LLM analysis")
        
        combined_text = "\n\n---\n\n".join(article_texts)
        
        return f"""Analyze the following news articles about a stock and provide:
1. Overall sentiment (positive, negative, or neutral) - consider the time range and trends
2. Key themes and topics - note any patterns over time
3. Potential impact on stock price (bullish, bearish, or neutral) - consider recent vs older news
4. Confidence level (0.0 to 1.0) - higher confidence if multiple recent articles show consistent sentiment

News Articles (with dates):
{combined_text}

Important: Consider the dates of articles. Recent news may have more impact than older news. 
Look for trends and patterns over time. If sentiment changed recently, note this in your analysis.

Provide your analysis in the following JSON format:
{{
    "sentiment": "positive|negative|neutral",
    "sentiment_score": 0.0-1.0,
    "themes": ["theme1", "theme2", ...],
    "impact": "bullish|bearish|neutral",
    "confidence": 0.0-1.0,
    "summary": "Brief summary of key points, including any time-based trends"
}}
dont use any other text than the JSON format.
the JSON format is required and must be followed exactly."""
    
    def _try_huggingface(self, prompt: str) -> Optional[Dict]:
        """Try Hugging Face Inference API (free tier)"""
        try:
            import requests
            
            # Using a good free model for sentiment analysis
            model = "mistralai/Mistral-7B-Instruct-v0.2"  # Free model
            
            headers = {
                "Authorization": f"Bearer {self.huggingface_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": f"You are a financial news analyst. {prompt}",
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.3,
                    "return_full_text": False
                }
            }
            
            # Use new router endpoint instead of deprecated api-inference endpoint
            response = requests.post(
                f"https://router.huggingface.co/models/{model}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get('generated_text', '')
                    return self._parse_llm_response(text, 'huggingface')
            else:
                # API returned error status
                error_msg = response.text[:200] if response.text else f"HTTP {response.status_code}"
                raise Exception(f"HTTP {response.status_code}: {error_msg}")
        except ImportError:
            raise ImportError("requests library not installed. Install with: pip install requests")
        except Exception as e:
            # Re-raise to trigger fallback to next provider
            raise Exception(f"Hugging Face API error: {str(e)}")
    
    def _try_groq(self, prompt: str) -> Optional[Dict]:
        """Try Groq API (free tier, very fast)"""
        try:
            from groq import Groq
            
            client = Groq(api_key=self.groq_key)
            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Free, fast model
                messages=[
                    {"role": "system", "content": "You are a financial news analyst. Analyze stock news sentiment accurately."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Check if response is valid
            if not response or not response.choices or len(response.choices) == 0:
                raise Exception("Groq API returned empty response")
            
            result_text = response.choices[0].message.content
            if not result_text:
                raise Exception("Groq API returned empty content")
            
            parsed_result = self._parse_llm_response(result_text, 'groq')
            if not parsed_result:
                raise Exception("Failed to parse Groq response")
            
            return parsed_result
        except ImportError:
            raise ImportError("Groq library not installed. Install with: pip install groq")
        except Exception as e:
            # Re-raise to trigger fallback to next provider
            raise Exception(f"Groq API error: {str(e)}")
    
    def _try_gemini(self, prompt: str) -> Optional[Dict]:
        """Try Google Gemini API (free tier)"""
        try:
            # Suppress deprecation warning for google.generativeai
            # Note: Migration to google.genai recommended in future
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=FutureWarning, module='google.generativeai')
                import google.generativeai as genai
            
            genai.configure(api_key=self.gemini_key)
            
            # Try model names in order of reliability (2025 models)
            # Note: gemini-1.5-pro and gemini-1.5-flash were retired in Sept 2025
            # Using current 2025 models: gemini-2.5-flash, gemini-2.5-pro
            # Also try gemini-pro as fallback for compatibility
            model_names = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-pro', 'gemini-1.5-flash-latest']
            last_error = None
            available_models_list = []
            
            # First, try to get available models to see what's actually available
            try:
                available_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        # Extract just the model name (remove full path)
                        model_id = m.name.split('/')[-1] if '/' in m.name else m.name
                        available_models.append(model_id)
                        available_models_list.append(model_id)
                
                # If we found available models, prioritize those
                if available_models:
                    # Reorder model_names to prioritize available ones
                    prioritized = [m for m in model_names if m in available_models]
                    # Add any other available models we haven't tried yet
                    other_available = [m for m in available_models if m not in model_names]
                    model_names = prioritized + [m for m in model_names if m not in prioritized] + other_available
            except Exception as e:
                # If listing models fails, continue with default order
                # This is fine - we'll try the models in our list
                pass
            
            full_prompt = f"""You are a financial news analyst. Analyze stock news sentiment accurately.

{prompt}"""
            
            # Try each model name - both creation and generation
            response = None
            for model_name in model_names:
                try:
                    model = genai.GenerativeModel(model_name)
                    
                    # Try to generate content with this model
                    response = model.generate_content(
                        full_prompt,
                        generation_config={
                            'temperature': 0.3,
                            'max_output_tokens': 500,
                        }
                    )
                    
                    # If we got here, both model creation and generation succeeded
                    break
                except Exception as e:
                    last_error = e
                    # If it's a 404, model not found, or v1beta error, try next model
                    error_str = str(e).lower()
                    if '404' in error_str or 'not found' in error_str or 'v1beta' in error_str:
                        continue
                    # For other errors during generation, also try next model
                    continue
            
            if response is None:
                error_msg = f"Could not use any Gemini model. Tried: {', '.join(model_names[:5])}"
                if available_models_list:
                    error_msg += f". Available models found: {', '.join(available_models_list[:5])}"
                if last_error:
                    error_msg += f". Last error: {str(last_error)}"
                raise Exception(error_msg)
            
            if not response or not hasattr(response, 'text') or not response.text:
                raise Exception("Gemini API returned empty response")
            
            result_text = response.text
            return self._parse_llm_response(result_text, 'gemini')
        except ImportError:
            raise ImportError("Google Generative AI library not installed. Install with: pip install google-generativeai")
        except Exception as e:
            # Re-raise to trigger fallback to next provider
            raise Exception(f"Gemini API error: {str(e)}")
    
    def _try_openai(self, prompt: str) -> Optional[Dict]:
        """Try OpenAI API (paid)"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial news analyst. Analyze stock news sentiment accurately."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            return self._parse_llm_response(result_text, 'openai')
        except ImportError:
            raise ImportError("OpenAI library not installed. Install with: pip install openai")
        except Exception as e:
            # Re-raise to trigger fallback to next provider
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _aggregate_llm_results(self, results: List[Dict], providers: List[str]) -> Dict:
        """
        Aggregate results from multiple LLM providers
        
        Args:
            results: List of result dictionaries from different providers
            providers: List of provider names that succeeded
            
        Returns:
            Aggregated result dictionary
        """
        if not results:
            return self._fallback_keyword_analysis([])
        
        # If only one result, return it with updated method field
        if len(results) == 1:
            result = results[0].copy()
            result['method'] = f'llm-{providers[0]}'
            return result
        
        # Aggregate sentiment scores (average)
        sentiment_scores = [r.get('sentiment_score', 0.5) for r in results]
        avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)
        
        # Determine overall sentiment (majority vote, or based on average score)
        sentiments = [r.get('sentiment', 'neutral') for r in results]
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        neutral_count = sentiments.count('neutral')
        
        if positive_count > negative_count and positive_count > neutral_count:
            overall_sentiment = 'positive'
        elif negative_count > positive_count and negative_count > neutral_count:
            overall_sentiment = 'negative'
        elif avg_sentiment_score > 0.6:
            overall_sentiment = 'positive'
        elif avg_sentiment_score < 0.4:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        # Aggregate impacts (majority vote)
        impacts = [r.get('impact', 'neutral') for r in results]
        bullish_count = impacts.count('bullish')
        bearish_count = impacts.count('bearish')
        neutral_impact_count = impacts.count('neutral')
        
        if bullish_count > bearish_count and bullish_count > neutral_impact_count:
            overall_impact = 'bullish'
        elif bearish_count > bullish_count and bearish_count > neutral_impact_count:
            overall_impact = 'bearish'
        else:
            overall_impact = 'neutral'
        
        # Combine themes (unique themes from all providers)
        all_themes = []
        for r in results:
            themes = r.get('themes', [])
            if isinstance(themes, list):
                all_themes.extend(themes)
        unique_themes = list(dict.fromkeys(all_themes))  # Preserve order, remove duplicates
        
        # Average confidence
        confidences = [r.get('confidence', 0.7) for r in results]
        avg_confidence = sum(confidences) / len(confidences)
        # Boost confidence slightly when multiple providers agree
        if len(results) > 1:
            avg_confidence = min(1.0, avg_confidence + 0.05 * (len(results) - 1))
        
        # Combine summaries (take the longest/most detailed one, or combine)
        summaries = [r.get('summary', '') for r in results if r.get('summary')]
        if summaries:
            # Use the longest summary, or combine unique points
            combined_summary = max(summaries, key=len)
            if len(summaries) > 1:
                combined_summary += f" (Consensus from {len(providers)} LLM providers)"
        else:
            combined_summary = f"Analysis from {len(providers)} LLM providers"
        
        # Create method string showing all providers
        providers_str = '+'.join(providers)
        
        return {
            'sentiment': overall_sentiment,
            'sentiment_score': max(0.0, min(1.0, avg_sentiment_score)),
            'themes': unique_themes[:10],  # Limit to top 10 themes
            'impact': overall_impact,
            'confidence': max(0.0, min(1.0, avg_confidence)),
            'summary': combined_summary,
            'method': f'llm-{providers_str}'
        }
    
    def _parse_llm_response(self, text: str, provider: str) -> Optional[Dict]:
        """Parse LLM response into structured format"""
        import json
        import re
        
        # Find JSON in response
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                
                # Convert to our format
                sentiment_score = result.get('sentiment_score', 0.5)
                if isinstance(sentiment_score, str):
                    try:
                        sentiment_score = float(sentiment_score)
                    except:
                        sentiment_score = 0.5
                
                if result.get('sentiment') == 'negative':
                    sentiment_score = 1.0 - sentiment_score
                
                return {
                    'sentiment': result.get('sentiment', 'neutral'),
                    'sentiment_score': max(0.0, min(1.0, sentiment_score)),
                    'themes': result.get('themes', []),
                    'impact': result.get('impact', 'neutral'),
                    'confidence': max(0.0, min(1.0, result.get('confidence', 0.7))),
                    'summary': result.get('summary', ''),
                    'method': f'llm-{provider}'
                }
            except json.JSONDecodeError:
                pass
        
        return None
    
    def _fallback_keyword_analysis(self, articles: List[NewsArticle]) -> Dict:
        """Fallback to keyword-based analysis"""
        from services.analyzers.constants import (
            POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS, NEWS_SENTIMENT_MULTIPLIER
        )
        
        positive_count = 0
        negative_count = 0
        
        for article in articles:
            text = f"{article.title} {article.summary}".lower()
            
            # Check for positive keywords
            for keyword in POSITIVE_KEYWORDS:
                if keyword in text:
                    positive_count += 1
                    break
            
            # Check for negative keywords
            for keyword in NEGATIVE_KEYWORDS:
                if keyword in text:
                    negative_count += 1
                    break
        
        # Calculate sentiment
        total = len(articles)
        if total == 0:
            return {
                'sentiment': 'neutral',
                'sentiment_score': 0.5,
                'themes': [],
                'impact': 'neutral',
                'confidence': 0.3,
                'summary': 'No articles to analyze',
                'method': 'keyword'
            }
        
        positive_ratio = positive_count / total
        negative_ratio = negative_count / total
        
        if positive_count > negative_count * NEWS_SENTIMENT_MULTIPLIER:
            sentiment = 'positive'
            sentiment_score = 0.5 + (positive_ratio * 0.3)
        elif negative_count > positive_count * NEWS_SENTIMENT_MULTIPLIER:
            sentiment = 'negative'
            sentiment_score = 0.5 - (negative_ratio * 0.3)
        else:
            sentiment = 'neutral'
            sentiment_score = 0.5
        
        return {
            'sentiment': sentiment,
            'sentiment_score': max(0.0, min(1.0, sentiment_score)),
            'themes': [],
            'impact': 'bullish' if sentiment == 'positive' else 'bearish' if sentiment == 'negative' else 'neutral',
            'confidence': 0.5 + (min(positive_count, negative_count) / total * 0.2),
            'summary': f'Keyword analysis: {positive_count} positive, {negative_count} negative articles',
            'method': 'keyword'
        }

