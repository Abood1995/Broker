"""Chart controls for selecting chart type and period"""
import tkinter as tk
from tkinter import ttk
from ui import constants
from ui.theme_manager import get_theme_manager

class ChartControls(tk.Frame):
    """Control panel for chart type and period selection"""
    
    def __init__(self, parent, chart_widget=None, data_fetcher=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.theme_manager = get_theme_manager()
        bg = self.theme_manager.get_background()
        self.configure(bg=bg)
        self.chart_widget = chart_widget
        self.data_fetcher = data_fetcher
        self.current_symbol = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create modern control widgets"""
        bg = self.theme_manager.get_background()
        text_primary = self.theme_manager.get_text_primary()
        primary = self.theme_manager.get_primary()
        
        # Chart type selector
        type_frame = tk.Frame(self, bg=bg)
        type_frame.pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        
        tk.Label(
            type_frame,
            text="Chart Type:",
            font=constants.FONT_LABEL,
            bg=bg,
            fg=text_primary
        ).pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        
        self.chart_type_var = tk.StringVar(value=constants.CHART_TYPES[1])  # Default to Candlestick
        self.chart_type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.chart_type_var,
            values=constants.CHART_TYPES,
            state="readonly",
            width=18
        )
        self.chart_type_combo.pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        self.chart_type_combo.bind("<<ComboboxSelected>>", self.on_chart_type_change)
        
        # Period selector
        period_frame = tk.Frame(self, bg=bg)
        period_frame.pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        
        tk.Label(
            period_frame,
            text="Period:",
            font=constants.FONT_LABEL,
            bg=bg,
            fg=text_primary
        ).pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        
        self.period_var = tk.StringVar(value="3M")  # Default to 3 months
        self.period_combo = ttk.Combobox(
            period_frame,
            textvariable=self.period_var,
            values=list(constants.CHART_PERIODS.keys()),
            state="readonly",
            width=12
        )
        self.period_combo.pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        self.period_combo.bind("<<ComboboxSelected>>", self.on_period_change)
        
        # Modern refresh button
        refresh_btn = tk.Button(
            self,
            text=f"{constants.ICON_REFRESH} Refresh",
            command=self.refresh_chart,
            bg=primary,
            fg=constants.LIGHT_TEXT_PRIMARY if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_TEXT_PRIMARY,
            font=constants.FONT_BUTTON,
            padx=constants.BUTTON_PADX,
            pady=constants.BUTTON_PADY,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2"
        )
        refresh_btn.pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        
        # Button hover effects
        primary_hover = constants.LIGHT_PRIMARY_HOVER if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_PRIMARY_HOVER
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(bg=primary_hover))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(bg=primary))
    
    def set_symbol(self, symbol: str):
        """Set the current symbol and load chart"""
        self.current_symbol = symbol
        if symbol and self.chart_widget and self.data_fetcher:
            self.load_chart()
    
    def load_chart(self):
        """Load chart data and update display"""
        if not self.current_symbol:
            return
        
        chart_type = self.chart_type_var.get()
        period_key = self.period_var.get()
        period_value = constants.CHART_PERIODS.get(period_key, "3mo")
        
        # Fetch data
        if self.data_fetcher:
            data = self.data_fetcher.fetch_historical_data(self.current_symbol, period_value)
            if data is not None and self.chart_widget:
                self.chart_widget.update_chart(self.current_symbol, data, chart_type, period_key)
    
    def on_chart_type_change(self, event=None):
        """Handle chart type change"""
        if self.current_symbol:
            self.load_chart()
    
    def on_period_change(self, event=None):
        """Handle period change"""
        if self.current_symbol:
            self.load_chart()
    
    def refresh_chart(self):
        """Refresh the current chart"""
        if self.current_symbol:
            # Clear cache and reload
            if self.data_fetcher:
                self.data_fetcher.clear_cache()
            self.load_chart()

