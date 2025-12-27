# Setup Guide

This guide will help you set up the Stock Broker MVP application from scratch.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/broker.git
cd broker
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys (Optional)

```bash
# Copy the example config file
cp config.example.py config.py

# Edit config.py with your favorite text editor
# Add your API keys (see below for where to get them)
```

### 5. Run the Application

```bash
python main.py
```

## Getting API Keys

### Free LLM Providers (Recommended)

#### Google Gemini
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in `config.py`

#### Groq
1. Go to https://console.groq.com/keys
2. Sign up or sign in
3. Create a new API key
4. Copy the key and paste it in `config.py`

#### Hugging Face
1. Go to https://huggingface.co/settings/tokens
2. Sign up or sign in
3. Create a new token (read access is enough)
4. Copy the token and paste it in `config.py`

### Optional News APIs

#### NewsAPI
1. Go to https://newsapi.org/register
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier: 100 requests/day

#### Alpha Vantage
1. Go to https://www.alphavantage.co/support/#api-key
2. Fill out the form to get a free API key
3. Free tier: 5 API calls per minute

### Paid Option

#### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Sign up and add payment method
3. Create an API key
4. Pay-as-you-go pricing

## Configuration File Structure

Your `config.py` should look like this:

```python
# Free LLM Providers (recommended)
GEMINI_API_KEY = "your_key_here"
GROQ_API_KEY = "your_key_here"
HUGGINGFACE_API_KEY = "your_token_here"

# Optional News APIs
NEWSAPI_KEY = "your_key_here"  # or None
ALPHAVANTAGE_KEY = "your_key_here"  # or None

# Paid LLM Provider (optional)
OPENAI_API_KEY = None  # or "your_key_here"

# LLM Provider preference
LLM_PROVIDER = "auto"  # or "gemini", "groq", "huggingface", "openai"
```

## Troubleshooting

### Import Errors
If you get import errors, make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Key Errors
- Verify your API keys are correct
- Check if the API key has the right permissions
- Some free tiers have rate limits

### No News Articles
- Check your internet connection
- Verify NewsAPI/Alpha Vantage keys if using those sources
- The app works with free sources even without API keys

### LLM Not Working
- Verify at least one LLM API key is set
- Check console for error messages
- App will fallback to keyword-based analysis if LLM fails

## Next Steps

Once setup is complete:
1. Run `python main.py`
2. Enter stock symbols (e.g., "AAPL, MSFT, GOOGL")
3. Click "Analyze Stocks"
4. Explore the results in different tabs

Enjoy analyzing stocks! 📈

