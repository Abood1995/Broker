# Default stock symbols to analyze
DEFAULT_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA"]

# Analysis thresholds
MIN_VOLUME = 1000000
PE_RATIO_MIN = 10
PE_RATIO_MAX = 25
DIVIDEND_YIELD_THRESHOLD = 0.03

# UI Settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# News API Keys (Optional - set to None if not available)
# Get free API keys from:
# - NewsAPI: https://newsapi.org/register (free tier: 100 requests/day)
# - Alpha Vantage: https://www.alphavantage.co/support/#api-key (free tier: 5 calls/min)
# 
# Free LLM Providers (recommended):
# - Hugging Face: https://huggingface.co/settings/tokens (free tier available)
# - Groq: https://console.groq.com/keys (free tier, very fast)
# - Google Gemini: https://makersuite.google.com/app/apikey (free tier available)
# 
# Paid LLM Provider:
# - OpenAI: https://platform.openai.com/api-keys (pay-as-you-go)
NEWSAPI_KEY = None  # Set your NewsAPI key here
ALPHAVANTAGE_KEY = None  # Set your Alpha Vantage key here

# Free LLM Providers (recommended - try these first!)
HUGGINGFACE_API_KEY = None  # Get free token: https://huggingface.co/settings/tokens
GROQ_API_KEY = None  # Get free key: https://console.groq.com/keys
GEMINI_API_KEY = None  # Get free key: https://makersuite.google.com/app/apikey

# Paid LLM Provider
OPENAI_API_KEY = None  # Set your OpenAI API key here (paid service)

# LLM Provider preference: "auto" (tries free first), "huggingface", "groq", "gemini", "openai"
LLM_PROVIDER = "auto"

