"""UI constants and configuration values for the broker application"""

# Window Configuration
WINDOW_TITLE = "Stock Broker MVP - Recommendations"
WINDOW_GEOMETRY = "1400x900"
BACKGROUND_COLOR = "#f0f0f0"

# Fonts
FONT_HEADER = ("Arial", 20, "bold")
FONT_LABEL = ("Arial", 12)
FONT_LABEL_BOLD = ("Arial", 12, "bold")
FONT_ENTRY = ("Arial", 11)
FONT_BUTTON = ("Arial", 11, "bold")
FONT_ANALYZERS_LABEL = ("Arial", 9, "italic")
FONT_DETAILS = ("Consolas", 10)

# Colors
COLOR_TEXT_PRIMARY = "#2c3e50"
COLOR_BUTTON_BG = "#3498db"
COLOR_BUTTON_FG = "white"
COLOR_ANALYZERS_LABEL = "#7f8c8d"

# Recommendation Type Colors
RECOMMENDATION_COLORS = {
    "STRONG BUY": "#d4edda",
    "BUY": "#d1ecf1",
    "HOLD": "#fff3cd",
    "SELL": "#f8d7da",
    "STRONG SELL": "#f5c6cb"
}
RECOMMENDATION_COLOR_DEFAULT = "#ffffff"

# Text Labels
TEXT_HEADER = "Stock Recommendation Broker"
TEXT_SYMBOLS_LABEL = "Stock Symbols (comma-separated):"
TEXT_BUTTON_ANALYZE = "Analyze Stocks"
TEXT_DETAILS_LABEL = "Recommendation Details:"
TEXT_ACTIVE_ANALYZERS_PREFIX = "Active Analyzers: "
TEXT_NO_ANALYZERS = "No analyzers active"
TEXT_DETAILS_HEADER = "RECOMMENDATION DETAILS"

# Default Values
DEFAULT_SYMBOLS = "AAPL, MSFT, GOOGL, TSLA, AMZN"
DEFAULT_NA_VALUE = "N/A"

# Common Stock Symbols for Autocomplete
COMMON_STOCK_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "TSLA", "NVDA", "JPM", "V",
    "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS", "BAC", "ADBE", "CRM",
    "NFLX", "PYPL", "INTC", "CMCSA", "PFE", "CSCO", "KO", "PEP", "TMO", "ABT",
    "COST", "AVGO", "NKE", "MRK", "TXN", "QCOM", "ACN", "HON", "DHR", "LIN",
    "VZ", "AMGN", "PM", "NEE", "RTX", "LOW", "UPS", "SPGI", "INTU", "CAT",
    "AXP", "SBUX", "GS", "BLK", "ADP", "TJX", "SYK", "ZTS", "GE", "DE"
]

# Treeview Configuration
TREEVIEW_COLUMNS = ("Symbol", "Name", "Price", "Change %", "Recommendation", "Confidence", "Target Price")
TREEVIEW_COLUMN_WIDTH = 120
TREEVIEW_HEIGHT = 15

# Widget Dimensions
ENTRY_WIDTH = 40
DETAILS_TEXT_WIDTH = 100
DETAILS_TEXT_HEIGHT = 8
NAME_TRUNCATE_LENGTH = 20

# Padding and Spacing
PADDING_HEADER = 20
PADDING_INPUT = 10
PADDING_WIDGET = 5
PADDING_FRAME = 20
PADDING_DETAILS_LABEL = (10, 5)
PADDING_DETAILS_TEXT = (0, 20)

# Button Padding
BUTTON_PADX = 20
BUTTON_PADY = 5

# Messages
MESSAGE_WARNING_TITLE = "Warning"
MESSAGE_NO_SYMBOLS = "Please enter stock symbols"
MESSAGE_ANALYZING = "Analyzing {count} stocks...\n\n"
MESSAGE_ANALYSIS_COMPLETE = "Analysis complete! Found {count} recommendations.\n\n"
MESSAGE_CLICK_FOR_DETAILS = "Click on a row to see detailed reasoning.\n"

# Details Display
DETAILS_SEPARATOR_LENGTH = 60
DETAILS_SEPARATOR = "=" * DETAILS_SEPARATOR_LENGTH

# Tab Configuration
TAB_NAMES = ["Overview", "Charts", "Analysis", "News"]
TAB_OVERVIEW = 0
TAB_CHARTS = 1
TAB_ANALYSIS = 2
TAB_NEWS = 3

# Card Styling
CARD_BACKGROUND = "#ffffff"
CARD_BORDER_COLOR = "#d0d0d0"
CARD_BORDER_WIDTH = 1
CARD_PADDING = 15
CARD_CORNER_RADIUS = 5

# Chart Configuration
CHART_DEFAULT_PERIOD = "3mo"
CHART_PERIODS = {
    "1D": "1d",
    "1W": "5d",
    "1M": "1mo",
    "3M": "3mo",
    "6M": "6mo",
    "1Y": "1y",
    "All": "max"
}
CHART_TYPES = ["Line", "Candlestick", "Volume", "Combined"]
CHART_WIDTH = 12
CHART_HEIGHT = 6
CHART_DPI = 100

# Color Palette Extensions
COLOR_POSITIVE = "#28a745"
COLOR_NEGATIVE = "#dc3545"
COLOR_NEUTRAL = "#6c757d"
COLOR_CARD_HEADER = "#f8f9fa"
COLOR_BORDER = "#dee2e6"

# Progress Bar
PROGRESS_BAR_LENGTH = 200
PROGRESS_BAR_HEIGHT = 20

# Theme Support
THEME_LIGHT = "light"
THEME_DARK = "dark"
CURRENT_THEME = THEME_LIGHT

# Dark Theme Colors (for future use)
DARK_BACKGROUND = "#1e1e1e"
DARK_TEXT = "#ffffff"
DARK_CARD_BG = "#2d2d2d"

