"""Chart controls for selecting chart type and period"""
import tkinter as tk
from tkinter import ttk
from ui.constants import (
    FONT_LABEL, BACKGROUND_COLOR, COLOR_BUTTON_BG, COLOR_BUTTON_FG,
    FONT_BUTTON, CHART_TYPES, CHART_PERIODS, PADDING_WIDGET
)

class ChartControls(tk.Frame):
    """Control panel for chart type and period selection"""
    
    def __init__(self, parent, chart_widget=None, data_fetcher=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg=BACKGROUND_COLOR)
        self.chart_widget = chart_widget
        self.data_fetcher = data_fetcher
        self.current_symbol = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create control widgets"""
        # Chart type selector
        type_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        type_frame.pack(side=tk.LEFT, padx=PADDING_WIDGET)
        
        tk.Label(
            type_frame,
            text="Chart Type:",
            font=FONT_LABEL,
            bg=BACKGROUND_COLOR
        ).pack(side=tk.LEFT, padx=PADDING_WIDGET)
        
        self.chart_type_var = tk.StringVar(value=CHART_TYPES[1])  # Default to Candlestick
        self.chart_type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.chart_type_var,
            values=CHART_TYPES,
            state="readonly",
            width=15
        )
        self.chart_type_combo.pack(side=tk.LEFT, padx=PADDING_WIDGET)
        self.chart_type_combo.bind("<<ComboboxSelected>>", self.on_chart_type_change)
        
        # Period selector
        period_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        period_frame.pack(side=tk.LEFT, padx=PADDING_WIDGET)
        
        tk.Label(
            period_frame,
            text="Period:",
            font=FONT_LABEL,
            bg=BACKGROUND_COLOR
        ).pack(side=tk.LEFT, padx=PADDING_WIDGET)
        
        self.period_var = tk.StringVar(value="3M")  # Default to 3 months
        self.period_combo = ttk.Combobox(
            period_frame,
            textvariable=self.period_var,
            values=list(CHART_PERIODS.keys()),
            state="readonly",
            width=10
        )
        self.period_combo.pack(side=tk.LEFT, padx=PADDING_WIDGET)
        self.period_combo.bind("<<ComboboxSelected>>", self.on_period_change)
        
        # Refresh button
        refresh_btn = tk.Button(
            self,
            text="Refresh",
            command=self.refresh_chart,
            bg=COLOR_BUTTON_BG,
            fg=COLOR_BUTTON_FG,
            font=FONT_BUTTON,
            padx=10,
            pady=5
        )
        refresh_btn.pack(side=tk.LEFT, padx=PADDING_WIDGET)
    
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
        period_value = CHART_PERIODS.get(period_key, "3mo")
        
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

