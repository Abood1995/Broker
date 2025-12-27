# Design Patterns Used in Broker MVP

## Strategy Pattern

The application uses the **Strategy Pattern** to implement multiple analysis strategies. This allows us to easily add, remove, or modify different analysis approaches without changing the core application logic.

### Structure

```
BaseAnalyzer (Abstract)
    ├── PriceAnalyzer
    ├── VolumeAnalyzer
    ├── NewsAnalyzer
    └── TechnicalStrategyAnalyzer
```

### Benefits

1. **Open/Closed Principle**: Open for extension (new analyzers), closed for modification
2. **Single Responsibility**: Each analyzer focuses on one analysis method
3. **Easy Testing**: Each analyzer can be tested independently
4. **Flexibility**: Analyzers can be enabled/disabled or weighted differently

## Composite Pattern

The **Composite Pattern** is used to combine multiple analyzers into a single unified analysis.

### Implementation

- `CompositeAnalyzer` combines results from multiple `BaseAnalyzer` instances
- Weighted averaging of scores and confidence levels
- Aggregated reasoning from all analyzers

### Benefits

1. **Unified Interface**: Treat multiple analyzers as a single analyzer
2. **Weighted Analysis**: Different analyzers can have different weights
3. **Dynamic Composition**: Add/remove analyzers at runtime

## Usage Example

```python
from services.analyzers import PriceAnalyzer, VolumeAnalyzer, NewsAnalyzer, CompositeAnalyzer

# Create individual analyzers with weights
price_analyzer = PriceAnalyzer(weight=1.5)  # Higher weight for price
volume_analyzer = VolumeAnalyzer(weight=1.0)
news_analyzer = NewsAnalyzer(weight=0.8)    # Lower weight for news

# Combine them
composite = CompositeAnalyzer([
    price_analyzer,
    volume_analyzer,
    news_analyzer
])

# Use the composite analyzer
result = composite.analyze(stock)
```

## Analyzer Details

### PriceAnalyzer
- **Focus**: Price movements, momentum, P/E ratios
- **Weight**: Default 1.0
- **Confidence**: 0.7 (price data is reliable)

### VolumeAnalyzer
- **Focus**: Trading volume patterns, liquidity
- **Weight**: Default 1.0
- **Confidence**: 0.6 (volume alone is less reliable)

### NewsAnalyzer
- **Focus**: News sentiment, recent news activity
- **Weight**: Default 1.0
- **Confidence**: 0.5 (news sentiment can be volatile)

### TechnicalStrategyAnalyzer
- **Focus**: Technical indicators (RSI, Moving Averages, Support/Resistance)
- **Weight**: Default 1.0
- **Confidence**: 0.65 (technical analysis has moderate reliability)

### PeriodBasedAnalyzer
- **Focus**: Multi-timeframe performance (1 week, 1 month, 3 months, 6 months)
- **Weight**: Default 1.2 (higher weight for consensus analysis)
- **Confidence**: 0.7
- **Special Feature**: Combines recommendations across periods (e.g., "Week: BUY, Month: BUY → Overall: BUY")

### SupportResistanceAnalyzer
- **Focus**: Historical support and resistance levels
- **Weight**: Default 1.1 (higher weight for key levels)
- **Confidence**: 0.65
- **Special Feature**: Identifies price floors/ceilings from historical data

### FundamentalAnalyzer
- **Focus**: Financial metrics (P/E, P/B, debt, margins, growth)
- **Weight**: Default 1.0
- **Confidence**: 0.6

### MomentumAnalyzer
- **Focus**: Price momentum across short/medium/long-term
- **Weight**: Default 1.0
- **Confidence**: 0.7

### VolatilityAnalyzer
- **Focus**: Risk assessment and volatility patterns
- **Weight**: Default 0.8 (lower weight, more for risk info)
- **Confidence**: 0.65

## Adding New Analyzers

To add a new analyzer:

1. Create a new class inheriting from `BaseAnalyzer`
2. Implement the `analyze()` method
3. Return a dictionary with: `score`, `reasoning`, `confidence`, `recommendation_type`
4. Add it to the `CompositeAnalyzer` or configure it in `StockAnalyzer`

Example:

```python
class CustomAnalyzer(BaseAnalyzer):
    def __init__(self, weight: float = 1.0):
        super().__init__("Custom Analysis", weight)
    
    def analyze(self, stock: Stock) -> Dict:
        score = 0.5
        reasons = []
        confidence = 0.6
        
        # Your analysis logic here
        
        return {
            'score': score,
            'reasoning': "; ".join(reasons),
            'confidence': confidence,
            'recommendation_type': self.calculate_recommendation_type(score)
        }
```

## Configuration

You can configure which analyzers to use and their weights:

```python
analyzer = StockAnalyzer(
    data_fetcher,
    use_price=True,
    use_volume=True,
    use_news=True,
    use_technical=True,
    analyzer_weights={
        'price': 1.5,      # Emphasize price analysis
        'volume': 1.0,
        'news': 0.8,       # Reduce news weight
        'technical': 1.2   # Increase technical weight
    }
)
```

