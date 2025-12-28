"""Stock card component for displaying stock overview"""
import tkinter as tk
from tkinter import ttk
from models.stock import Stock
from models.recommendation import Recommendation
from ui import constants
from ui.theme_manager import get_theme_manager

class StockCard(tk.Frame):
    """Card widget displaying stock overview with key metrics"""
    
    def __init__(self, parent, stock: Stock, recommendation: Recommendation, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.stock = stock
        self.recommendation = recommendation
        self.theme_manager = get_theme_manager()
        
        surface = self.theme_manager.get_surface()
        border = self.theme_manager.get_border()
        self.configure(
            bg=surface, 
            relief=tk.FLAT, 
            bd=constants.CARD_BORDER_WIDTH,
            highlightbackground=border,
            highlightthickness=1
        )
        self.create_widgets()
    
    def create_widgets(self):
        """Create modern card content"""
        surface = self.theme_manager.get_surface()
        text_primary = self.theme_manager.get_text_primary()
        text_secondary = self.theme_manager.get_text_secondary()
        border = self.theme_manager.get_border()
        
        # Header with symbol and name
        header_frame = tk.Frame(self, bg=surface)
        header_frame.pack(fill=tk.X, padx=constants.CARD_PADDING, pady=(constants.CARD_PADDING, constants.SPACE_SM))
        
        symbol_label = tk.Label(
            header_frame,
            text=f"{constants.ICON_CHART} {self.stock.symbol}",
            font=constants.FONT_H3,
            bg=surface,
            fg=text_primary
        )
        symbol_label.pack(side=tk.LEFT)
        
        name_label = tk.Label(
            header_frame,
            text=f" - {self.stock.name[:30]}{'...' if len(self.stock.name) > 30 else ''}",
            font=constants.FONT_BODY,
            bg=surface,
            fg=text_secondary
        )
        name_label.pack(side=tk.LEFT, padx=(constants.SPACE_XS, 0))
        
        # Price section
        price_frame = tk.Frame(self, bg=surface)
        price_frame.pack(fill=tk.X, padx=constants.CARD_PADDING, pady=constants.SPACE_SM)
        
        price_label = tk.Label(
            price_frame,
            text=f"${self.stock.current_price:.2f}",
            font=constants.FONT_H1,
            bg=surface,
            fg=text_primary
        )
        price_label.pack(side=tk.LEFT)
        
        # Price change with color and arrow
        if self.stock.price_change_percent >= 0:
            change_color = constants.LIGHT_SUCCESS if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_SUCCESS
            change_arrow = constants.ICON_UP
        else:
            change_color = constants.LIGHT_ERROR if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_ERROR
            change_arrow = constants.ICON_DOWN
        
        change_label = tk.Label(
            price_frame,
            text=f" {change_arrow} ${self.stock.price_change:.2f} ({self.stock.price_change_percent:+.2f}%)",
            font=constants.FONT_BODY_LARGE,
            bg=surface,
            fg=change_color
        )
        change_label.pack(side=tk.LEFT, padx=(constants.SPACE_SM, 0))
        
        # Metrics row with icons
        metrics_frame = tk.Frame(self, bg=surface)
        metrics_frame.pack(fill=tk.X, padx=constants.CARD_PADDING, pady=constants.SPACE_SM)
        
        # Volume
        volume_str = f"{self.stock.volume:,}" if self.stock.volume else constants.DEFAULT_NA_VALUE
        self.create_metric(metrics_frame, "📊 Volume", volume_str, 0)
        
        # Market Cap
        market_cap_str = f"${self.stock.market_cap/1e9:.2f}B" if self.stock.market_cap else constants.DEFAULT_NA_VALUE
        self.create_metric(metrics_frame, "💰 Market Cap", market_cap_str, 1)
        
        # P/E Ratio
        pe_str = f"{self.stock.pe_ratio:.2f}" if self.stock.pe_ratio else constants.DEFAULT_NA_VALUE
        self.create_metric(metrics_frame, "📈 P/E Ratio", pe_str, 2)
        
        # Recommendation badge with modern styling
        rec_frame = tk.Frame(self, bg=surface)
        rec_frame.pack(fill=tk.X, padx=constants.CARD_PADDING, pady=constants.SPACE_SM)
        
        rec_type = self.recommendation.recommendation_type.value
        rec_color = constants.RECOMMENDATION_COLORS.get(rec_type, constants.RECOMMENDATION_COLOR_DEFAULT)
        rec_text_color = constants.RECOMMENDATION_TEXT_COLORS.get(rec_type, text_primary)
        
        rec_label = tk.Label(
            rec_frame,
            text=rec_type,
            font=constants.FONT_LABEL_BOLD,
            bg=rec_color,
            fg=rec_text_color,
            padx=constants.SPACE_MD,
            pady=constants.SPACE_SM,
            relief=tk.FLAT,
            bd=0
        )
        rec_label.pack(side=tk.LEFT)
        
        # Confidence score with progress bar
        confidence_frame = tk.Frame(self, bg=surface)
        confidence_frame.pack(fill=tk.X, padx=constants.CARD_PADDING, pady=constants.SPACE_SM)
        
        tk.Label(
            confidence_frame,
            text="Confidence:",
            font=constants.FONT_LABEL,
            bg=surface,
            fg=text_secondary
        ).pack(side=tk.LEFT)
        
        confidence_value = self.recommendation.confidence_score
        confidence_label = tk.Label(
            confidence_frame,
            text=f"{confidence_value:.1%}",
            font=constants.FONT_LABEL_BOLD,
            bg=surface,
            fg=text_primary
        )
        confidence_label.pack(side=tk.LEFT, padx=(constants.SPACE_XS, constants.SPACE_SM))
        
        # Modern progress bar
        progress_canvas = tk.Canvas(
            confidence_frame,
            width=constants.PROGRESS_BAR_LENGTH,
            height=constants.PROGRESS_BAR_HEIGHT,
            bg=surface,
            highlightthickness=0
        )
        progress_canvas.pack(side=tk.LEFT)
        
        # Draw progress bar with rounded corners effect
        progress_width = int(constants.PROGRESS_BAR_LENGTH * confidence_value)
        if confidence_value > 0.6:
            progress_color = constants.LIGHT_SUCCESS if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_SUCCESS
        elif confidence_value > 0.4:
            progress_color = constants.LIGHT_WARNING if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_WARNING
        else:
            progress_color = constants.LIGHT_ERROR if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_ERROR
        
        progress_canvas.create_rectangle(
            0, 0, progress_width, constants.PROGRESS_BAR_HEIGHT,
            fill=progress_color, outline=border, width=1
        )
        
        # Target price
        if self.recommendation.target_price:
            target_frame = tk.Frame(self, bg=surface)
            target_frame.pack(fill=tk.X, padx=constants.CARD_PADDING, pady=(constants.SPACE_SM, constants.CARD_PADDING))
            
            tk.Label(
                target_frame,
                text="🎯 Target Price:",
                font=constants.FONT_LABEL,
                bg=surface,
                fg=text_secondary
            ).pack(side=tk.LEFT)
            
            tk.Label(
                target_frame,
                text=f"${self.recommendation.target_price:.2f}",
                font=constants.FONT_LABEL_BOLD,
                bg=surface,
                fg=text_primary
            ).pack(side=tk.LEFT, padx=(constants.SPACE_XS, 0))
        
        # Add hover effect
        hover_bg = self.theme_manager.get_background_secondary()
        def on_enter(e):
            self.config(bg=hover_bg, highlightbackground=self.theme_manager.get_primary())
        def on_leave(e):
            self.config(bg=surface, highlightbackground=border)
        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
    
    def create_metric(self, parent, label, value, column):
        """Create a modern metric label"""
        surface = self.theme_manager.get_surface()
        text_primary = self.theme_manager.get_text_primary()
        text_secondary = self.theme_manager.get_text_secondary()
        
        metric_frame = tk.Frame(parent, bg=surface)
        metric_frame.grid(row=0, column=column, padx=constants.SPACE_SM, sticky="w")
        
        tk.Label(
            metric_frame,
            text=label + ":",
            font=constants.FONT_CAPTION,
            bg=surface,
            fg=text_secondary
        ).pack(anchor=tk.W)
        
        tk.Label(
            metric_frame,
            text=value,
            font=constants.FONT_LABEL_BOLD,
            bg=surface,
            fg=text_primary
        ).pack(anchor=tk.W)

