# News Analyzer Guide

The News Analyzer has been significantly improved to provide better sentiment analysis from multiple sources with optional LLM support.

## Features

### 1. Multiple News Sources
The analyzer now fetches news from multiple sources:
- **Yahoo Finance** (default, no API key required)
- **NewsAPI** (optional, requires free API key)
- **Alpha Vantage** (optional, requires free API key)

### 2. Increased Article Coverage
- Analyzes up to **50 articles per source** (increased from 10)
- Automatically deduplicates articles from different sources
- Sorts articles by date (newest first)

### 3. LLM-Powered Sentiment Analysis (FREE Options Available!)
- **Free LLM Providers** (recommended):
  - **Google Gemini** - Free tier available, excellent quality
  - **Groq** - Free tier, very fast inference
  - **Hugging Face** - Free tier available, no credit card needed
- **Paid Option**:
  - **OpenAI GPT** - Pay-as-you-go
- Falls back to keyword-based analysis if LLM is not available
- Automatically tries free providers first, then paid
- Provides:
  - Overall sentiment (positive/negative/neutral)
  - Sentiment score (0.0 to 1.0)
  - Key themes and topics
  - Impact assessment (bullish/bearish/neutral)
  - Confidence level

## Setup

### Basic Setup (Yahoo Finance only)
No configuration needed! The analyzer works out of the box with Yahoo Finance.

### Enhanced Setup (Multiple Sources)

1. **Get API Keys** (all optional):
   - **NewsAPI**: https://newsapi.org/register (free tier: 100 requests/day)
   - **Alpha Vantage**: https://www.alphavantage.co/support/#api-key (free tier: 5 API calls/min)
   
   **Free LLM Providers** (recommended - try these first!):
   - **Google Gemini**: https://makersuite.google.com/app/apikey (free tier, excellent quality)
   - **Groq**: https://console.groq.com/keys (free tier, very fast)
   - **Hugging Face**: https://huggingface.co/settings/tokens (free tier, no credit card)
   
   **Paid LLM Provider**:
   - **OpenAI**: https://platform.openai.com/api-keys (pay-as-you-go)

2. **Configure API Keys**:
   Edit `config.py` and set your API keys:
   ```python
   NEWSAPI_KEY = "your_newsapi_key_here"
   ALPHAVANTAGE_KEY = "your_alphavantage_key_here"
   
   # Free LLM providers (recommended)
   GEMINI_API_KEY = "your_gemini_key_here"  # Get free key (recommended)
   GROQ_API_KEY = "your_groq_key_here"  # Get free key
   HUGGINGFACE_API_KEY = "your_huggingface_token_here"  # Get free token
   
   # Paid LLM provider
   OPENAI_API_KEY = "your_openai_key_here"  # Optional, paid
   
   # Provider preference: "auto" tries free first (Gemini → Groq → Hugging Face → OpenAI)
   # Or specify: "gemini", "groq", "huggingface", "openai"
   LLM_PROVIDER = "auto"
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How It Works

1. **News Fetching**:
   - Fetches news from all configured sources
   - Deduplicates articles based on title similarity
   - Combines and sorts by date

2. **Sentiment Analysis**:
   - If API keys are set: Tries free LLM providers first (Gemini → Groq → Hugging Face), then OpenAI
   - Falls back to keyword-based analysis if no LLM available
   - Analyzes up to 50 articles
   - Uses "auto" mode by default to prefer free providers (Gemini is tried first)

3. **Score Calculation**:
   - Considers news activity (number of articles)
   - Applies sentiment score (positive/negative)
   - Boosts confidence when using LLM
   - Boosts confidence when multiple sources are used

## Benefits

- **More Comprehensive**: Analyzes 50+ articles instead of 10
- **Better Coverage**: Multiple sources provide diverse perspectives
- **Smarter Analysis**: LLM understands context and nuance
- **Higher Confidence**: Multiple sources and LLM increase reliability
- **Automatic Fallback**: Works even without API keys

## Example Output

With LLM enabled:
```
High news activity (47 articles from multiple sources)
Sources: 3 different sources
Positive news sentiment (llm analysis)
Key themes: earnings growth, market expansion, product launch
Summary: Recent news indicates strong financial performance...
```

Without LLM (keyword-based):
```
High news activity (35 articles)
Sources: 2 different sources
Positive news sentiment (keyword analysis)
```

## Cost Considerations

- **Yahoo Finance**: Free, unlimited
- **NewsAPI**: Free tier: 100 requests/day
- **Alpha Vantage**: Free tier: 5 API calls/min, 500/day
- **Google Gemini**: Free tier available, excellent quality, no credit card needed
- **Groq**: Free tier available, very fast, no credit card needed
- **Hugging Face**: Free tier available, no credit card needed
- **OpenAI**: Pay-as-you-go (~$0.001-0.002 per analysis) - only used if free providers unavailable

## Troubleshooting

- **No news found**: Check if the stock symbol is correct
- **API errors**: Verify API keys are correct and not rate-limited
- **LLM not working**: 
  - Check Gemini, Groq, or Hugging Face API keys (free options)
  - If using OpenAI, check API key and account balance
  - System automatically falls back to keyword analysis if LLM fails
- **Slow performance**: Reduce `NEWS_ARTICLES_PER_SOURCE` in constants if needed
- **Free LLM rate limits**: Free tiers have rate limits; system will fallback gracefully to next provider

