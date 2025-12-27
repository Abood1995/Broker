# Stock Analyzers Guide

This document describes all available analyzers in the Broker MVP application.

## Available Analyzers

### 1. Price Analyzer
**Focus**: Price movements, momentum, and valuation metrics
- Analyzes price change percentage
- Evaluates P/E ratios
- Compares current price to previous close
- **Confidence**: 0.7 (price data is reliable)

### 2. Volume Analyzer
**Focus**: Trading volume patterns and liquidity
- High volume indicates strong market interest
- Volume-price relationship analysis
- Liquidity assessment
- **Confidence**: 0.6 (volume alone is less reliable)

### 3. News Analyzer
**Focus**: News sentiment and recent news activity
- Analyzes news count and recency
- Keyword-based sentiment analysis
- Positive/negative news ratio
- **Confidence**: 0.5 (news sentiment can be volatile)

### 4. Technical Strategy Analyzer
**Focus**: Technical indicators and trading strategies
- RSI (Relative Strength Index)
- Moving Averages (Golden Cross/Death Cross)
- Support/Resistance levels (basic)
- **Confidence**: 0.65 (technical analysis has moderate reliability)

### 5. Period-Based Analyzer ⭐ NEW
**Focus**: Multi-timeframe performance analysis
- Analyzes performance across multiple periods:
  - 1 Week (20% weight)
  - 1 Month (30% weight)
  - 3 Months (30% weight)
  - 6 Months (20% weight)
- Combines period recommendations (e.g., "Week: BUY, Month: BUY, Quarter: HOLD")
- Consensus-based scoring
- **Confidence**: 0.7

**Example Output**:
```
Period Recommendations: 1 Week: BUY (+3.2%), 1 Month: BUY (+5.1%), 
3 Months: HOLD (+1.2%), 6 Months: BUY (+8.5%)
Strong buy consensus across periods (3 buy, 1 hold, 0 sell)
```

### 6. Support/Resistance Analyzer ⭐ NEW
**Focus**: Historical price levels and key support/resistance zones
- Identifies support and resistance levels from historical data
- Analyzes current price position relative to S/R levels
- Risk/reward ratio calculation
- **Confidence**: 0.65

**Features**:
- Finds support levels (price floors where stock tends to bounce)
- Finds resistance levels (price ceilings where stock tends to reject)
- Analyzes proximity to these levels
- Calculates favorable entry/exit points

**Example Output**:
```
Support: $145.50 | Resistance: $165.20 | Current: $150.30
Near strong support at $145.50 (3.3% away) - potential bounce
Favorable risk/reward ratio (2.5:1)
```

### 7. Fundamental Analyzer ⭐ NEW
**Focus**: Financial metrics and company fundamentals
- P/E Ratio analysis
- Price-to-Book (P/B) ratio
- Debt-to-Equity ratio
- Profit margins
- Revenue growth
- Earnings growth
- Dividend yield
- Market capitalization
- **Confidence**: 0.6

**Example Output**:
```
Attractive P/E ratio (18.5)
Low debt-to-equity (35.2) - strong balance sheet
Strong profit margin (22.5%)
Strong revenue growth (25.3%)
```

### 8. Momentum Analyzer ⭐ NEW
**Focus**: Price momentum across different timeframes
- Short-term momentum (5 days)
- Medium-term momentum (20 days)
- Long-term momentum (60 days)
- Momentum consistency across timeframes
- Momentum acceleration/deceleration
- **Confidence**: 0.7

**Example Output**:
```
Strong short-term momentum (+4.2% in 5 days)
Positive medium-term momentum (+6.8% in 20 days)
Strong long-term momentum (+12.5% in 60 days)
Consistent positive momentum across all timeframes
Momentum accelerating - bullish signal
```

### 9. Volatility Analyzer ⭐ NEW
**Focus**: Risk assessment and volatility patterns
- Annualized volatility calculation
- Volatility trend analysis
- Price range assessment
- Risk level evaluation
- **Confidence**: 0.65

**Example Output**:
```
Moderate volatility (24.5%) - balanced risk/reward
Volatility decreasing - stabilizing trend
Tight trading range (18.2%) - consolidation
```

## How Period-Based Analysis Works

The Period-Based Analyzer evaluates stock performance across multiple timeframes and combines the results:

1. **Individual Period Analysis**: Each period (1 week, 1 month, 3 months, 6 months) gets a recommendation
2. **Weighted Scoring**: Periods are weighted (recent periods slightly less, medium-term more)
3. **Consensus Building**: If multiple periods show "BUY", the overall score increases
4. **Combined Recommendation**: Final recommendation considers all periods

**Example Scenario**:
- Week: BUY (+3%)
- Month: BUY (+5%)
- Quarter: HOLD (+1%)
- 6 Months: BUY (+8%)

**Result**: Strong buy consensus (3 buy, 1 hold) → Higher confidence in BUY recommendation

## How Support/Resistance Analysis Works

The Support/Resistance Analyzer identifies key price levels from historical data:

1. **Level Identification**: Finds local minima (support) and maxima (resistance) in price history
2. **Clustering**: Groups similar price levels together (within 2% tolerance)
3. **Touch Count**: Requires at least 2 touches to validate a level
4. **Position Analysis**: Evaluates current price relative to nearest support/resistance
5. **Risk/Reward**: Calculates potential upside vs downside

**Trading Signals**:
- **Near Support**: Potential bounce → BUY signal
- **Near Resistance**: Potential rejection → SELL signal
- **Between Levels**: Neutral, wait for breakout

## Configuration

You can enable/disable analyzers and adjust their weights:

```python
analyzer = StockAnalyzer(
    data_fetcher,
    use_price=True,
    use_volume=True,
    use_news=True,
    use_technical=True,
    use_period=True,              # Enable period-based analysis
    use_support_resistance=True,   # Enable S/R analysis
    use_fundamental=True,         # Enable fundamental analysis
    use_momentum=True,            # Enable momentum analysis
    use_volatility=True,          # Enable volatility analysis
    analyzer_weights={
        'price': 1.0,
        'volume': 1.0,
        'news': 0.8,
        'technical': 1.0,
        'period': 1.2,            # Higher weight for period analysis
        'support_resistance': 1.1, # Higher weight for S/R
        'fundamental': 1.0,
        'momentum': 1.0,
        'volatility': 0.8         # Lower weight (risk assessment)
    }
)
```

## Default Configuration

By default, all analyzers are enabled with these weights:
- Price: 1.0
- Volume: 1.0
- News: 1.0
- Technical: 1.0
- Period: 1.2 (slightly higher)
- Support/Resistance: 1.1 (slightly higher)
- Fundamental: 1.0
- Momentum: 1.0
- Volatility: 0.8 (slightly lower, as it's more about risk)

## Best Practices

1. **For Day Trading**: Focus on Price, Volume, Momentum, and Support/Resistance
2. **For Swing Trading**: Include Period-Based and Technical analyzers
3. **For Long-term Investing**: Emphasize Fundamental, Period-Based, and Volatility analyzers
4. **For News-Driven Stocks**: Increase News Analyzer weight
5. **For Technical Trading**: Increase Technical Strategy and Support/Resistance weights

## Adding Custom Analyzers

See `DESIGN_PATTERNS.md` for instructions on creating custom analyzers.

