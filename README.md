# Stock Broker MVP - AI-Powered Stock Analysis & Recommendations

A comprehensive desktop application for stock market analysis and investment recommendations, powered by multiple AI/LLM providers and real-time news sentiment analysis.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Features

### Core Functionality
- **Multi-Stock Analysis**: Analyze multiple stocks simultaneously with comprehensive metrics
- **AI-Powered Sentiment Analysis**: Uses multiple LLM providers (Gemini, Groq, Hugging Face, OpenAI) for news sentiment analysis
- **Multiple News Sources**: Aggregates news from 10+ sources including Yahoo Finance, Google News, MarketWatch, CNBC, Reuters, and more
- **Interactive Charts**: Multiple chart types (Line, Candlestick, Volume, Combined) with customizable time periods
- **Real-Time Data**: Fetches live stock data, prices, and news articles
- **Comprehensive Analysis**: 9 different analysis strategies including:
  - Price Analysis
  - Volume Analysis
  - News Sentiment Analysis
  - Technical Strategy Analysis
  - Period-Based Analysis
  - Support/Resistance Analysis
  - Fundamental Analysis
  - Momentum Analysis
  - Volatility Analysis

### User Interface
- **Tabbed Interface**: Organized into Overview, Charts, Analysis, and News tabs
- **Interactive Stock Cards**: Visual display of key metrics and recommendations
- **Expandable Analysis Sections**: Detailed breakdown of analysis reasoning
- **Clickable News Articles**: Direct links to original news sources
- **Export Functionality**: Export analysis results to CSV or JSON
- **Keyboard Shortcuts**: Efficient navigation and operations
- **Responsive Design**: Modern, clean UI with proper layout management

## 📋 Requirements

- Python 3.8 or higher
- Internet connection for data fetching
- (Optional) API keys for enhanced features (see Configuration)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/broker.git
   cd broker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys** (Optional but recommended)
   ```bash
   cp config.example.py config.py
   # Edit config.py and add your API keys
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Basic Setup (No API Keys Required)
The application works out of the box with free data sources:
- Yahoo Finance (stock data and news)
- Google News RSS feeds
- Multiple financial news RSS feeds

### Enhanced Setup (With API Keys)

#### Free LLM Providers (Recommended)
Get free API keys from:
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **Groq**: https://console.groq.com/keys
- **Hugging Face**: https://huggingface.co/settings/tokens

#### Optional News APIs
- **NewsAPI**: https://newsapi.org/register (100 requests/day free)
- **Alpha Vantage**: https://www.alphavantage.co/support/#api-key (5 calls/min free)

#### Paid Option
- **OpenAI**: https://platform.openai.com/api-keys (pay-as-you-go)

Edit `config.py` and add your keys:
```python
# Free LLM Providers (recommended)
GEMINI_API_KEY = "your_gemini_key_here"
GROQ_API_KEY = "your_groq_key_here"
HUGGINGFACE_API_KEY = "your_huggingface_token_here"

# Optional News APIs
NEWSAPI_KEY = "your_newsapi_key_here"
ALPHAVANTAGE_KEY = "your_alphavantage_key_here"

# Paid LLM Provider (optional)
OPENAI_API_KEY = "your_openai_key_here"
```

## 📖 Usage

### Basic Usage

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Enter stock symbols**
   - Type stock symbols in the input field (comma-separated)
   - Example: `AAPL, MSFT, GOOGL, TSLA`
   - Use autocomplete for suggestions (Ctrl+F to focus)

3. **Analyze stocks**
   - Click "Analyze Stocks" or press Enter
   - Wait for analysis to complete (progress shown in console)

4. **View results**
   - **Overview Tab**: See all recommendations in a sortable table
   - **Charts Tab**: Interactive price charts with multiple types and time periods
   - **Analysis Tab**: Detailed breakdown of analysis reasoning
   - **News Tab**: Recent news articles with clickable links

### Advanced Features

- **Filter Results**: Use the dropdown to filter by recommendation type
- **Sort Table**: Click column headers to sort
- **Export Data**: Right-click on table or use Ctrl+E to export
- **View Details**: Click on any row to see detailed analysis
- **Keyboard Shortcuts**:
  - `Enter`: Analyze stocks
  - `Escape`: Clear selection
  - `Ctrl+F`: Focus search
  - `Ctrl+E`: Export results

## 🏗️ Project Structure

```
broker/
├── main.py                 # Application entry point
├── config.py              # Configuration (API keys, settings)
├── config.example.py      # Example configuration template
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── models/               # Data models
│   ├── stock.py         # Stock data model
│   └── recommendation.py # Recommendation model
│
├── services/            # Business logic
│   ├── analyzer.py     # Main analyzer coordinator
│   ├── data_fetcher.py # Stock data fetching
│   ├── news_fetcher.py # News aggregation from multiple sources
│   ├── llm_analyzer.py # LLM-based sentiment analysis
│   └── analyzers/      # Analysis strategies
│       ├── base_analyzer.py
│       ├── composite_analyzer.py
│       ├── news_analyzer.py
│       ├── price_analyzer.py
│       └── ... (other analyzers)
│
└── ui/                  # User interface
    ├── main_window.py   # Main application window
    ├── chart_widget.py  # Chart visualization
    ├── news_panel.py    # News display
    ├── stock_card.py    # Stock card component
    └── constants.py     # UI constants
```

## 🔍 Analysis Strategies

The application uses 9 different analysis strategies:

1. **Price Analysis**: Current price trends and changes
2. **Volume Analysis**: Trading volume patterns
3. **News Analysis**: Sentiment from multiple news sources (LLM-powered)
4. **Technical Strategy**: Technical indicators and patterns
5. **Period-Based Analysis**: Performance over different time periods
6. **Support/Resistance**: Key price levels
7. **Fundamental Analysis**: Financial metrics (P/E, market cap, etc.)
8. **Momentum Analysis**: Price momentum indicators
9. **Volatility Analysis**: Market volatility patterns

## 📰 News Sources

The application aggregates news from **10+ sources**:

### Free Sources (No API Key)
- Yahoo Finance
- Yahoo Finance RSS
- Google News
- MarketWatch (via RSS)
- CNBC (via RSS)
- Reuters (via RSS)
- Seeking Alpha (RSS)
- Benzinga (via RSS)
- Financial Times (via RSS)
- Bloomberg (via RSS)

### Optional API Sources
- NewsAPI (requires API key)
- Alpha Vantage (requires API key)
- Related Market News (uses NewsAPI if available)

## 🤖 LLM Integration

The application supports multiple LLM providers for sentiment analysis:

- **Auto Mode** (default): Tries free providers first (Gemini → Groq → Hugging Face), then OpenAI
- **Aggregation**: Combines results from all working providers for better accuracy
- **Fallback**: Uses keyword-based analysis if LLM is unavailable

### Supported Providers
- ✅ Google Gemini (Free tier)
- ✅ Groq (Free tier, very fast)
- ✅ Hugging Face (Free tier)
- ✅ OpenAI (Paid)

## 📊 Output Format

### Recommendation Types
- **STRONG BUY**: High confidence buy recommendation
- **BUY**: Positive recommendation
- **HOLD**: Neutral recommendation
- **SELL**: Negative recommendation
- **STRONG SELL**: High confidence sell recommendation

### Export Formats
- **CSV**: Spreadsheet-compatible format
- **JSON**: Structured data format

## 🐛 Troubleshooting

### No News Articles Showing
- Check internet connection
- Verify API keys are set correctly (if using API sources)
- Check console for error messages

### LLM Analysis Not Working
- Verify API keys are set in `config.py`
- Check console for provider-specific errors
- Application will fallback to keyword-based analysis

### Charts Not Loading
- Ensure `mplfinance` and `matplotlib` are installed
- Check console for data fetching errors

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **yfinance**: For stock data fetching
- **mplfinance**: For financial charting
- **LLM Providers**: Google Gemini, Groq, Hugging Face, OpenAI
- **News Sources**: All the financial news providers

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

## 🔮 Future Enhancements

- [ ] Dark mode theme
- [ ] Portfolio tracking
- [ ] Price alerts
- [ ] Historical backtesting
- [ ] More chart indicators
- [ ] Database storage for historical data
- [ ] Web version

---

**Note**: This is an MVP (Minimum Viable Product) for educational and research purposes. Always do your own research before making investment decisions.
