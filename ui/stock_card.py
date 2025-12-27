"""Stock card component for displaying stock overview"""
import tkinter as tk
from tkinter import ttk
from models.stock import Stock
from models.recommendation import Recommendation
from ui.constants import (
    CARD_BACKGROUND, CARD_BORDER_COLOR, CARD_BORDER_WIDTH, CARD_PADDING,
    FONT_LABEL, FONT_LABEL_BOLD, FONT_HEADER,
    COLOR_TEXT_PRIMARY, COLOR_POSITIVE, COLOR_NEGATIVE, COLOR_NEUTRAL,
    RECOMMENDATION_COLORS, RECOMMENDATION_COLOR_DEFAULT,
    BACKGROUND_COLOR, DEFAULT_NA_VALUE, PROGRESS_BAR_LENGTH, PROGRESS_BAR_HEIGHT
)

class StockCard(tk.Frame):
    """Card widget displaying stock overview with key metrics"""
    
    def __init__(self, parent, stock: Stock, recommendation: Recommendation, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.stock = stock
        self.recommendation = recommendation
        self.configure(bg=CARD_BACKGROUND, relief=tk.RAISED, bd=CARD_BORDER_WIDTH)
        self.create_widgets()
    
    def create_widgets(self):
        """Create card content"""
        # Header with symbol and name
        header_frame = tk.Frame(self, bg=CARD_BACKGROUND)
        header_frame.pack(fill=tk.X, padx=CARD_PADDING, pady=(CARD_PADDING, 5))
        
        symbol_label = tk.Label(
            header_frame,
            text=self.stock.symbol,
            font=("Arial", 18, "bold"),
            bg=CARD_BACKGROUND,
            fg=COLOR_TEXT_PRIMARY
        )
        symbol_label.pack(side=tk.LEFT)
        
        name_label = tk.Label(
            header_frame,
            text=f" - {self.stock.name[:30]}{'...' if len(self.stock.name) > 30 else ''}",
            font=FONT_LABEL,
            bg=CARD_BACKGROUND,
            fg=COLOR_NEUTRAL
        )
        name_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Price section
        price_frame = tk.Frame(self, bg=CARD_BACKGROUND)
        price_frame.pack(fill=tk.X, padx=CARD_PADDING, pady=5)
        
        price_label = tk.Label(
            price_frame,
            text=f"${self.stock.current_price:.2f}",
            font=("Arial", 24, "bold"),
            bg=CARD_BACKGROUND,
            fg=COLOR_TEXT_PRIMARY
        )
        price_label.pack(side=tk.LEFT)
        
        # Price change with color and arrow
        change_color = COLOR_POSITIVE if self.stock.price_change_percent >= 0 else COLOR_NEGATIVE
        change_arrow = "↑" if self.stock.price_change_percent >= 0 else "↓"
        
        change_label = tk.Label(
            price_frame,
            text=f" {change_arrow} ${self.stock.price_change:.2f} ({self.stock.price_change_percent:+.2f}%)",
            font=("Arial", 14),
            bg=CARD_BACKGROUND,
            fg=change_color
        )
        change_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Metrics row
        metrics_frame = tk.Frame(self, bg=CARD_BACKGROUND)
        metrics_frame.pack(fill=tk.X, padx=CARD_PADDING, pady=5)
        
        # Volume
        volume_str = f"{self.stock.volume:,}" if self.stock.volume else DEFAULT_NA_VALUE
        self.create_metric(metrics_frame, "Volume", volume_str, 0)
        
        # Market Cap
        market_cap_str = f"${self.stock.market_cap/1e9:.2f}B" if self.stock.market_cap else DEFAULT_NA_VALUE
        self.create_metric(metrics_frame, "Market Cap", market_cap_str, 1)
        
        # P/E Ratio
        pe_str = f"{self.stock.pe_ratio:.2f}" if self.stock.pe_ratio else DEFAULT_NA_VALUE
        self.create_metric(metrics_frame, "P/E Ratio", pe_str, 2)
        
        # Recommendation badge
        rec_frame = tk.Frame(self, bg=CARD_BACKGROUND)
        rec_frame.pack(fill=tk.X, padx=CARD_PADDING, pady=5)
        
        rec_type = self.recommendation.recommendation_type.value
        rec_color = RECOMMENDATION_COLORS.get(rec_type, RECOMMENDATION_COLOR_DEFAULT)
        
        rec_label = tk.Label(
            rec_frame,
            text=rec_type,
            font=("Arial", 12, "bold"),
            bg=rec_color,
            fg=COLOR_TEXT_PRIMARY,
            padx=10,
            pady=5,
            relief=tk.RAISED,
            bd=2
        )
        rec_label.pack(side=tk.LEFT)
        
        # Confidence score with progress bar
        confidence_frame = tk.Frame(self, bg=CARD_BACKGROUND)
        confidence_frame.pack(fill=tk.X, padx=CARD_PADDING, pady=5)
        
        tk.Label(
            confidence_frame,
            text="Confidence:",
            font=FONT_LABEL,
            bg=CARD_BACKGROUND
        ).pack(side=tk.LEFT)
        
        confidence_value = self.recommendation.confidence_score
        confidence_label = tk.Label(
            confidence_frame,
            text=f"{confidence_value:.1%}",
            font=FONT_LABEL_BOLD,
            bg=CARD_BACKGROUND,
            fg=COLOR_TEXT_PRIMARY
        )
        confidence_label.pack(side=tk.LEFT, padx=(5, 10))
        
        # Progress bar
        progress_canvas = tk.Canvas(
            confidence_frame,
            width=PROGRESS_BAR_LENGTH,
            height=PROGRESS_BAR_HEIGHT,
            bg=CARD_BACKGROUND,
            highlightthickness=0
        )
        progress_canvas.pack(side=tk.LEFT)
        
        # Draw progress bar
        progress_width = int(PROGRESS_BAR_LENGTH * confidence_value)
        progress_color = COLOR_POSITIVE if confidence_value > 0.6 else COLOR_NEUTRAL if confidence_value > 0.4 else COLOR_NEGATIVE
        
        progress_canvas.create_rectangle(
            0, 0, progress_width, PROGRESS_BAR_HEIGHT,
            fill=progress_color, outline=COLOR_NEUTRAL, width=1
        )
        
        # Target price
        if self.recommendation.target_price:
            target_frame = tk.Frame(self, bg=CARD_BACKGROUND)
            target_frame.pack(fill=tk.X, padx=CARD_PADDING, pady=(5, CARD_PADDING))
            
            tk.Label(
                target_frame,
                text="Target Price:",
                font=FONT_LABEL,
                bg=CARD_BACKGROUND
            ).pack(side=tk.LEFT)
            
            tk.Label(
                target_frame,
                text=f"${self.recommendation.target_price:.2f}",
                font=FONT_LABEL_BOLD,
                bg=CARD_BACKGROUND,
                fg=COLOR_TEXT_PRIMARY
            ).pack(side=tk.LEFT, padx=(5, 0))
    
    def create_metric(self, parent, label, value, column):
        """Create a metric label"""
        metric_frame = tk.Frame(parent, bg=CARD_BACKGROUND)
        metric_frame.grid(row=0, column=column, padx=10, sticky="w")
        
        tk.Label(
            metric_frame,
            text=label + ":",
            font=FONT_LABEL,
            bg=CARD_BACKGROUND,
            fg=COLOR_NEUTRAL
        ).pack(anchor=tk.W)
        
        tk.Label(
            metric_frame,
            text=value,
            font=FONT_LABEL_BOLD,
            bg=CARD_BACKGROUND,
            fg=COLOR_TEXT_PRIMARY
        ).pack(anchor=tk.W)

