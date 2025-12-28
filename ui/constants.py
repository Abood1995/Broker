"""UI constants and configuration values for the broker application"""

# ============================================================================
# DESIGN SYSTEM - Modern UI/UX Constants
# ============================================================================

# Window Configuration
WINDOW_TITLE = "Stock Broker MVP - Recommendations"
WINDOW_GEOMETRY = "1400x900"
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 700

# ============================================================================
# TYPOGRAPHY SYSTEM
# ============================================================================

# Font Stack (system fonts for better performance)
FONT_FAMILY_PRIMARY = ("Segoe UI", "Helvetica Neue", "Arial", "sans-serif")
FONT_FAMILY_MONO = ("Consolas", "Monaco", "Courier New", "monospace")

# Typography Scale
FONT_H1 = (FONT_FAMILY_PRIMARY[0], 32, "bold")  # Main header
FONT_H2 = (FONT_FAMILY_PRIMARY[0], 24, "bold")  # Section headers
FONT_H3 = (FONT_FAMILY_PRIMARY[0], 20, "bold")  # Subsection headers
FONT_H4 = (FONT_FAMILY_PRIMARY[0], 16, "bold")  # Card titles
FONT_H5 = (FONT_FAMILY_PRIMARY[0], 14, "bold")  # Small headers
FONT_H6 = (FONT_FAMILY_PRIMARY[0], 12, "bold")  # Tiny headers

FONT_BODY_LARGE = (FONT_FAMILY_PRIMARY[0], 14, "normal")
FONT_BODY = (FONT_FAMILY_PRIMARY[0], 12, "normal")
FONT_BODY_SMALL = (FONT_FAMILY_PRIMARY[0], 11, "normal")
FONT_CAPTION = (FONT_FAMILY_PRIMARY[0], 10, "normal")

FONT_BUTTON = (FONT_FAMILY_PRIMARY[0], 12, "bold")
FONT_BUTTON_SMALL = (FONT_FAMILY_PRIMARY[0], 11, "bold")

FONT_LABEL = (FONT_FAMILY_PRIMARY[0], 12, "normal")
FONT_LABEL_BOLD = (FONT_FAMILY_PRIMARY[0], 12, "bold")
FONT_LABEL_SMALL = (FONT_FAMILY_PRIMARY[0], 10, "normal")

FONT_ENTRY = (FONT_FAMILY_PRIMARY[0], 12, "normal")
FONT_DETAILS = (FONT_FAMILY_MONO[0], 11, "normal")
FONT_CODE = (FONT_FAMILY_MONO[0], 10, "normal")

# Legacy font mappings (for backward compatibility)
FONT_HEADER = FONT_H2
FONT_ANALYZERS_LABEL = (FONT_FAMILY_PRIMARY[0], 10, "italic")

# ============================================================================
# SPACING SYSTEM (8px base unit)
# ============================================================================

SPACE_XS = 4   # 0.5 units
SPACE_SM = 8   # 1 unit
SPACE_MD = 16  # 2 units
SPACE_LG = 24  # 3 units
SPACE_XL = 32  # 4 units
SPACE_2XL = 48 # 6 units
SPACE_3XL = 64 # 8 units

# Padding Constants
PADDING_HEADER = SPACE_XL
PADDING_INPUT = SPACE_MD
PADDING_WIDGET = SPACE_SM
PADDING_FRAME = SPACE_LG
PADDING_DETAILS_LABEL = (SPACE_SM + SPACE_XS, SPACE_XS)
PADDING_DETAILS_TEXT = (0, SPACE_LG)
PADDING_CARD = SPACE_MD
PADDING_BUTTON_X = SPACE_LG
PADDING_BUTTON_Y = SPACE_SM + SPACE_XS

# Button Padding
BUTTON_PADX = PADDING_BUTTON_X
BUTTON_PADY = PADDING_BUTTON_Y

# ============================================================================
# COLOR SYSTEM - Light Theme
# ============================================================================

# Base Colors
LIGHT_BACKGROUND = "#FFFFFF"
LIGHT_BACKGROUND_SECONDARY = "#F8F9FA"
LIGHT_BACKGROUND_TERTIARY = "#F1F3F5"
LIGHT_SURFACE = "#FFFFFF"
LIGHT_SURFACE_ELEVATED = "#FFFFFF"

# Text Colors
LIGHT_TEXT_PRIMARY = "#111827"
LIGHT_TEXT_SECONDARY = "#6B7280"
LIGHT_TEXT_TERTIARY = "#9CA3AF"
LIGHT_TEXT_DISABLED = "#D1D5DB"

# Semantic Colors
LIGHT_PRIMARY = "#2563EB"
LIGHT_PRIMARY_HOVER = "#1D4ED8"
LIGHT_PRIMARY_ACTIVE = "#1E40AF"
LIGHT_PRIMARY_LIGHT = "#DBEAFE"

LIGHT_SUCCESS = "#10B981"
LIGHT_SUCCESS_HOVER = "#059669"
LIGHT_SUCCESS_LIGHT = "#D1FAE5"

LIGHT_WARNING = "#F59E0B"
LIGHT_WARNING_HOVER = "#D97706"
LIGHT_WARNING_LIGHT = "#FEF3C7"

LIGHT_ERROR = "#EF4444"
LIGHT_ERROR_HOVER = "#DC2626"
LIGHT_ERROR_LIGHT = "#FEE2E2"

LIGHT_INFO = "#3B82F6"
LIGHT_INFO_HOVER = "#2563EB"
LIGHT_INFO_LIGHT = "#DBEAFE"

# Border Colors
LIGHT_BORDER = "#E5E7EB"
LIGHT_BORDER_LIGHT = "#F3F4F6"
LIGHT_BORDER_DARK = "#D1D5DB"

# Chart Colors
LIGHT_CHART_UP = "#10B981"
LIGHT_CHART_DOWN = "#EF4444"
LIGHT_CHART_NEUTRAL = "#6B7280"
LIGHT_CHART_GRID = "#F3F4F6"
LIGHT_CHART_BACKGROUND = "#FFFFFF"

# ============================================================================
# COLOR SYSTEM - Dark Theme
# ============================================================================

# Base Colors
DARK_BACKGROUND = "#111827"
DARK_BACKGROUND_SECONDARY = "#1F2937"
DARK_BACKGROUND_TERTIARY = "#374151"
DARK_SURFACE = "#1F2937"
DARK_SURFACE_ELEVATED = "#374151"

# Text Colors
DARK_TEXT_PRIMARY = "#F9FAFB"
DARK_TEXT_SECONDARY = "#D1D5DB"
DARK_TEXT_TERTIARY = "#9CA3AF"
DARK_TEXT_DISABLED = "#6B7280"

# Semantic Colors
DARK_PRIMARY = "#3B82F6"
DARK_PRIMARY_HOVER = "#2563EB"
DARK_PRIMARY_ACTIVE = "#1E40AF"
DARK_PRIMARY_LIGHT = "#1E3A8A"

DARK_SUCCESS = "#34D399"
DARK_SUCCESS_HOVER = "#10B981"
DARK_SUCCESS_LIGHT = "#065F46"

DARK_WARNING = "#FBBF24"
DARK_WARNING_HOVER = "#F59E0B"
DARK_WARNING_LIGHT = "#78350F"

DARK_ERROR = "#F87171"
DARK_ERROR_HOVER = "#EF4444"
DARK_ERROR_LIGHT = "#7F1D1D"

DARK_INFO = "#60A5FA"
DARK_INFO_HOVER = "#3B82F6"
DARK_INFO_LIGHT = "#1E3A8A"

# Border Colors
DARK_BORDER = "#374151"
DARK_BORDER_LIGHT = "#4B5563"
DARK_BORDER_DARK = "#1F2937"

# Chart Colors
DARK_CHART_UP = "#34D399"
DARK_CHART_DOWN = "#F87171"
DARK_CHART_NEUTRAL = "#9CA3AF"
DARK_CHART_GRID = "#374151"
DARK_CHART_BACKGROUND = "#1F2937"

# ============================================================================
# CURRENT THEME (Default to Light)
# ============================================================================

THEME_LIGHT = "light"
THEME_DARK = "dark"
CURRENT_THEME = THEME_LIGHT

# Initialize theme manager on import to load saved preference
try:
    from ui.theme_manager import get_theme_manager
    _tm = get_theme_manager()
    CURRENT_THEME = _tm.current_theme
except:
    pass  # Fallback to default if theme manager not available yet

# Theme-aware color getters (will be used by theme manager)
def get_background():
    return LIGHT_BACKGROUND if CURRENT_THEME == THEME_LIGHT else DARK_BACKGROUND

def get_background_secondary():
    return LIGHT_BACKGROUND_SECONDARY if CURRENT_THEME == THEME_LIGHT else DARK_BACKGROUND_SECONDARY

def get_text_primary():
    return LIGHT_TEXT_PRIMARY if CURRENT_THEME == THEME_LIGHT else DARK_TEXT_PRIMARY

def get_text_secondary():
    return LIGHT_TEXT_SECONDARY if CURRENT_THEME == THEME_LIGHT else DARK_TEXT_SECONDARY

def get_primary():
    return LIGHT_PRIMARY if CURRENT_THEME == THEME_LIGHT else DARK_PRIMARY

def get_success():
    return LIGHT_SUCCESS if CURRENT_THEME == THEME_LIGHT else DARK_SUCCESS

def get_warning():
    return LIGHT_WARNING if CURRENT_THEME == THEME_LIGHT else DARK_WARNING

def get_error():
    return LIGHT_ERROR if CURRENT_THEME == THEME_LIGHT else DARK_ERROR

# Legacy color mappings (for backward compatibility)
BACKGROUND_COLOR = LIGHT_BACKGROUND_SECONDARY
COLOR_TEXT_PRIMARY = LIGHT_TEXT_PRIMARY
COLOR_BUTTON_BG = LIGHT_PRIMARY
COLOR_BUTTON_FG = LIGHT_TEXT_PRIMARY
COLOR_ANALYZERS_LABEL = LIGHT_TEXT_TERTIARY
COLOR_POSITIVE = LIGHT_SUCCESS
COLOR_NEGATIVE = LIGHT_ERROR
COLOR_NEUTRAL = LIGHT_TEXT_SECONDARY
COLOR_CARD_HEADER = LIGHT_BACKGROUND_TERTIARY
COLOR_BORDER = LIGHT_BORDER

# ============================================================================
# RECOMMENDATION COLORS (Enhanced)
# ============================================================================

# Light Theme Recommendation Colors
RECOMMENDATION_COLORS_LIGHT = {
    "STRONG BUY": "#D1FAE5",      # Light green
    "BUY": "#DBEAFE",              # Light blue
    "HOLD": "#FEF3C7",             # Light yellow
    "SELL": "#FEE2E2",             # Light red
    "STRONG SELL": "#FECACA"       # Light red (darker)
}

RECOMMENDATION_COLORS_DARK = {
    "STRONG BUY": "#065F46",       # Dark green
    "BUY": "#1E3A8A",              # Dark blue
    "HOLD": "#78350F",              # Dark yellow
    "SELL": "#7F1D1D",              # Dark red
    "STRONG SELL": "#991B1B"        # Dark red (darker)
}

RECOMMENDATION_TEXT_COLORS_LIGHT = {
    "STRONG BUY": "#065F46",
    "BUY": "#1E40AF",
    "HOLD": "#92400E",
    "SELL": "#991B1B",
    "STRONG SELL": "#7F1D1D"
}

RECOMMENDATION_TEXT_COLORS_DARK = {
    "STRONG BUY": "#34D399",
    "BUY": "#60A5FA",
    "HOLD": "#FBBF24",
    "SELL": "#F87171",
    "STRONG SELL": "#EF4444"
}

# Current recommendation colors (based on theme)
RECOMMENDATION_COLORS = RECOMMENDATION_COLORS_LIGHT
RECOMMENDATION_TEXT_COLORS = RECOMMENDATION_TEXT_COLORS_LIGHT
RECOMMENDATION_COLOR_DEFAULT = LIGHT_SURFACE

# ============================================================================
# ELEVATION & SHADOWS
# ============================================================================

# Shadow definitions (for cards and elevated surfaces)
SHADOW_SM = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
SHADOW_MD = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
SHADOW_LG = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
SHADOW_XL = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"

# Note: Tkinter doesn't support CSS shadows directly, but we can use relief and colors
# to simulate depth. These are documented for reference.

# ============================================================================
# CARD STYLING (Enhanced)
# ============================================================================

CARD_BACKGROUND = LIGHT_SURFACE
CARD_BACKGROUND_DARK = DARK_SURFACE
CARD_BORDER_COLOR = LIGHT_BORDER
CARD_BORDER_COLOR_DARK = DARK_BORDER
CARD_BORDER_WIDTH = 1
CARD_PADDING = PADDING_CARD
CARD_CORNER_RADIUS = 8  # Increased for modern look
CARD_ELEVATION = 1  # Visual elevation level

# ============================================================================
# BUTTON STYLING
# ============================================================================

BUTTON_RADIUS = 6
BUTTON_HEIGHT = 36
BUTTON_HEIGHT_SMALL = 32
BUTTON_TRANSITION_DURATION = 150  # ms (for hover effects)

# ============================================================================
# INPUT STYLING
# ============================================================================

INPUT_HEIGHT = 36
INPUT_BORDER_RADIUS = 6
INPUT_FOCUS_BORDER_WIDTH = 2

# ============================================================================
# TEXT LABELS
# ============================================================================

TEXT_HEADER = "Stock Recommendation Broker"
TEXT_SYMBOLS_LABEL = "Stock Symbols (comma-separated):"
TEXT_BUTTON_ANALYZE = "Analyze Stocks"
TEXT_DETAILS_LABEL = "Recommendation Details:"
TEXT_ACTIVE_ANALYZERS_PREFIX = "Active Analyzers: "
TEXT_NO_ANALYZERS = "No analyzers active"
TEXT_DETAILS_HEADER = "RECOMMENDATION DETAILS"

# ============================================================================
# DEFAULT VALUES
# ============================================================================

DEFAULT_SYMBOLS = "AAPL, MSFT, GOOGL, TSLA, AMZN"
DEFAULT_NA_VALUE = "N/A"

# ============================================================================
# COMMON STOCK SYMBOLS FOR AUTOCOMPLETE
# ============================================================================

COMMON_STOCK_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "TSLA", "NVDA", "JPM", "V",
    "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS", "BAC", "ADBE", "CRM",
    "NFLX", "PYPL", "INTC", "CMCSA", "PFE", "CSCO", "KO", "PEP", "TMO", "ABT",
    "COST", "AVGO", "NKE", "MRK", "TXN", "QCOM", "ACN", "HON", "DHR", "LIN",
    "VZ", "AMGN", "PM", "NEE", "RTX", "LOW", "UPS", "SPGI", "INTU", "CAT",
    "AXP", "SBUX", "GS", "BLK", "ADP", "TJX", "SYK", "ZTS", "GE", "DE"
]

# ============================================================================
# TABLE/TREEVIEW CONFIGURATION
# ============================================================================

TREEVIEW_COLUMNS = ("Symbol", "Name", "Price", "Change %", "Recommendation", "Confidence", "Target Price")
TREEVIEW_COLUMN_WIDTH = 140  # Increased for better readability
TREEVIEW_HEIGHT = 15
TREEVIEW_ROW_HEIGHT = 32  # Increased for better spacing
TREEVIEW_ALTERNATE_COLOR_LIGHT = "#F9FAFB"
TREEVIEW_ALTERNATE_COLOR_DARK = "#1F2937"
TREEVIEW_HOVER_COLOR_LIGHT = "#F3F4F6"
TREEVIEW_HOVER_COLOR_DARK = "#374151"
TREEVIEW_SELECTED_COLOR_LIGHT = "#DBEAFE"
TREEVIEW_SELECTED_COLOR_DARK = "#1E3A8A"

# ============================================================================
# WIDGET DIMENSIONS
# ============================================================================

ENTRY_WIDTH = 45  # Increased
DETAILS_TEXT_WIDTH = 100
DETAILS_TEXT_HEIGHT = 10  # Increased
NAME_TRUNCATE_LENGTH = 25  # Increased

# ============================================================================
# MESSAGES
# ============================================================================

MESSAGE_WARNING_TITLE = "Warning"
MESSAGE_NO_SYMBOLS = "Please enter stock symbols"
MESSAGE_ANALYZING = "Analyzing {count} stocks...\n\n"
MESSAGE_ANALYSIS_COMPLETE = "Analysis complete! Found {count} recommendations.\n\n"
MESSAGE_CLICK_FOR_DETAILS = "Click on a row to see detailed reasoning.\n"

# ============================================================================
# DETAILS DISPLAY
# ============================================================================

DETAILS_SEPARATOR_LENGTH = 60
DETAILS_SEPARATOR = "=" * DETAILS_SEPARATOR_LENGTH

# ============================================================================
# TAB CONFIGURATION
# ============================================================================

TAB_NAMES = ["Overview", "Charts", "Analysis", "News"]
TAB_OVERVIEW = 0
TAB_CHARTS = 1
TAB_ANALYSIS = 2
TAB_NEWS = 3

# Tab styling
TAB_PADDING = (SPACE_MD, SPACE_SM)
TAB_ACTIVE_COLOR_LIGHT = LIGHT_PRIMARY
TAB_ACTIVE_COLOR_DARK = DARK_PRIMARY
TAB_INACTIVE_COLOR_LIGHT = LIGHT_TEXT_SECONDARY
TAB_INACTIVE_COLOR_DARK = DARK_TEXT_SECONDARY

# ============================================================================
# CHART CONFIGURATION
# ============================================================================

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
CHART_WIDTH = 14  # Increased
CHART_HEIGHT = 7  # Increased
CHART_DPI = 100

# Chart styling
CHART_FONT_SIZE = 10
CHART_TITLE_SIZE = 14
CHART_GRID_ALPHA = 0.3
CHART_LINE_WIDTH = 1.5

# ============================================================================
# PROGRESS BAR
# ============================================================================

PROGRESS_BAR_LENGTH = 250  # Increased
PROGRESS_BAR_HEIGHT = 24   # Increased
PROGRESS_BAR_RADIUS = 4

# ============================================================================
# LOADING INDICATORS
# ============================================================================

LOADING_SPINNER_SIZE = 40
LOADING_SPINNER_COLOR_LIGHT = LIGHT_PRIMARY
LOADING_SPINNER_COLOR_DARK = DARK_PRIMARY

# ============================================================================
# NOTIFICATIONS/TOASTS
# ============================================================================

TOAST_DURATION = 3000  # ms
TOAST_WIDTH = 350
TOAST_HEIGHT = 60
TOAST_PADDING = SPACE_MD
TOAST_RADIUS = 8

# ============================================================================
# ICONS & SYMBOLS (Unicode)
# ============================================================================

ICON_UP = "▲"
ICON_DOWN = "▼"
ICON_NEUTRAL = "●"
ICON_LOADING = "⟳"
ICON_SUCCESS = "✓"
ICON_ERROR = "✕"
ICON_WARNING = "⚠"
ICON_INFO = "ℹ"
ICON_EXPORT = "📥"
ICON_REFRESH = "↻"
ICON_CHART = "📊"
ICON_NEWS = "📰"
ICON_ANALYSIS = "📈"
ICON_SETTINGS = "⚙"
ICON_THEME_LIGHT = "☀"
ICON_THEME_DARK = "🌙"
ICON_EXPAND = "▶"
ICON_COLLAPSE = "▼"

