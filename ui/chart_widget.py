"""Chart widget for displaying stock price charts"""
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import pandas as pd
from typing import Optional
from ui import constants
from ui.theme_manager import get_theme_manager

class ChartWidget(tk.Frame):
    """Widget for displaying stock price charts"""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.theme_manager = get_theme_manager()
        bg = self.theme_manager.get_background()
        self.configure(bg=bg)
        self.current_data = None
        self.current_symbol = None
        self.current_chart_type = "Candlestick"
        self.current_period = "3mo"
        
        # Create matplotlib figure with theme-aware background
        chart_bg = self.theme_manager.get_chart_background()
        self.fig = Figure(figsize=(constants.CHART_WIDTH, constants.CHART_HEIGHT), 
                         dpi=constants.CHART_DPI, 
                         facecolor=chart_bg)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Placeholder text
        self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder message when no data"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        chart_bg = self.theme_manager.get_chart_background()
        text_color = self.theme_manager.get_text_secondary()
        ax.set_facecolor(chart_bg)
        ax.text(0.5, 0.5, 'Select a stock to view chart', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, 
                fontsize=constants.CHART_TITLE_SIZE, 
                color=text_color)
        ax.axis('off')
        self.canvas.draw()
    
    def update_chart(self, symbol: str, data: pd.DataFrame, chart_type: str = "Candlestick", period: str = "3mo"):
        """
        Update the chart with new data
        
        Args:
            symbol: Stock symbol
            data: DataFrame with OHLCV data
            chart_type: Type of chart ("Line", "Candlestick", "Volume", "Combined")
            period: Time period for display
        """
        if data is None or data.empty:
            self.show_placeholder()
            return
        
        self.current_data = data
        self.current_symbol = symbol
        self.current_chart_type = chart_type
        self.current_period = period
        
        try:
            self.fig.clear()
            
            if chart_type == "Line":
                self._draw_line_chart(data, symbol)
            elif chart_type == "Candlestick":
                self._draw_candlestick_chart(data, symbol)
            elif chart_type == "Volume":
                self._draw_volume_chart(data, symbol)
            elif chart_type == "Combined":
                self._draw_combined_chart(data, symbol)
            else:
                self._draw_candlestick_chart(data, symbol)  # Default
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating chart: {e}")
            self.show_placeholder()
    
    def _draw_line_chart(self, data: pd.DataFrame, symbol: str):
        """Draw a simple line chart of closing prices with modern styling"""
        ax = self.fig.add_subplot(111)
        chart_bg = self.theme_manager.get_chart_background()
        text_color = self.theme_manager.get_text_primary()
        grid_color = self.theme_manager.get_chart_grid()
        primary_color = self.theme_manager.get_primary()
        
        ax.set_facecolor(chart_bg)
        self.fig.patch.set_facecolor(chart_bg)
        
        ax.plot(data.index, data['Close'], linewidth=constants.CHART_LINE_WIDTH, color=primary_color)
        ax.set_title(f'{symbol} - Price Chart ({self.current_period})', 
                    fontsize=constants.CHART_TITLE_SIZE, 
                    fontweight='bold',
                    color=text_color)
        ax.set_xlabel('Date', color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax.set_ylabel('Price ($)', color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax.tick_params(colors=text_color, labelsize=constants.CHART_FONT_SIZE)
        ax.grid(True, alpha=constants.CHART_GRID_ALPHA, color=grid_color)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['top'].set_color(text_color)
        ax.spines['right'].set_color(text_color)
        ax.spines['left'].set_color(text_color)
        self.fig.tight_layout()
    
    def _draw_candlestick_chart(self, data: pd.DataFrame, symbol: str):
        """Draw a candlestick chart with modern styling"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        chart_bg = self.theme_manager.get_chart_background()
        text_color = self.theme_manager.get_text_primary()
        grid_color = self.theme_manager.get_chart_grid()
        chart_up = self.theme_manager.get_chart_up()
        chart_down = self.theme_manager.get_chart_down()
        
        ax.set_facecolor(chart_bg)
        self.fig.patch.set_facecolor(chart_bg)
        
        # Sample data if too many points for performance
        if len(data) > 100:
            data = data.iloc[::len(data)//100]  # Sample to ~100 points
        
        # Draw candlesticks
        for i, (idx, row) in enumerate(data.iterrows()):
            color = chart_up if row['Close'] >= row['Open'] else chart_down
            wick_color = text_color
            # High-Low line (wick)
            ax.plot([i, i], [row['Low'], row['High']], color=wick_color, linewidth=0.5, zorder=1, alpha=0.7)
            # Open-Close body
            body_height = abs(row['Close'] - row['Open'])
            if body_height < 0.01:  # Doji - very small body
                body_height = 0.01
            body_bottom = min(row['Open'], row['Close'])
            rect = mpatches.Rectangle(
                (i - 0.3, body_bottom), 0.6, body_height,
                facecolor=color, edgecolor=wick_color, linewidth=0.5, zorder=2, alpha=0.8
            )
            ax.add_patch(rect)
        
        # Set x-axis labels
        ax.set_xticks(range(0, len(data), max(1, len(data)//10)))
        ax.set_xticklabels([data.index[i].strftime('%Y-%m-%d') if i < len(data) else '' 
                            for i in range(0, len(data), max(1, len(data)//10))], 
                          rotation=45, color=text_color, fontsize=constants.CHART_FONT_SIZE)
        
        ax.set_title(f'{symbol} - Candlestick Chart ({self.current_period})', 
                    fontsize=constants.CHART_TITLE_SIZE, 
                    fontweight='bold',
                    color=text_color)
        ax.set_xlabel('Date', color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax.set_ylabel('Price ($)', color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax.tick_params(colors=text_color, labelsize=constants.CHART_FONT_SIZE)
        ax.grid(True, alpha=constants.CHART_GRID_ALPHA, color=grid_color)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['top'].set_color(text_color)
        ax.spines['right'].set_color(text_color)
        ax.spines['left'].set_color(text_color)
        self.fig.tight_layout()
    
    def _draw_volume_chart(self, data: pd.DataFrame, symbol: str):
        """Draw a volume chart with modern styling"""
        ax = self.fig.add_subplot(111)
        
        chart_bg = self.theme_manager.get_chart_background()
        text_color = self.theme_manager.get_text_primary()
        grid_color = self.theme_manager.get_chart_grid()
        chart_up = self.theme_manager.get_chart_up()
        chart_down = self.theme_manager.get_chart_down()
        
        ax.set_facecolor(chart_bg)
        self.fig.patch.set_facecolor(chart_bg)
        
        colors = [chart_up if data.loc[idx, 'Close'] >= data.loc[idx, 'Open'] else chart_down 
                  for idx in data.index]
        ax.bar(data.index, data['Volume'], color=colors, alpha=0.6)
        ax.set_title(f'{symbol} - Volume Chart ({self.current_period})', 
                    fontsize=constants.CHART_TITLE_SIZE, 
                    fontweight='bold',
                    color=text_color)
        ax.set_xlabel('Date', color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax.set_ylabel('Volume', color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax.tick_params(colors=text_color, labelsize=constants.CHART_FONT_SIZE)
        ax.grid(True, alpha=constants.CHART_GRID_ALPHA, color=grid_color)
        ax.spines['bottom'].set_color(text_color)
        ax.spines['top'].set_color(text_color)
        ax.spines['right'].set_color(text_color)
        ax.spines['left'].set_color(text_color)
        self.fig.autofmt_xdate()
        self.fig.tight_layout()
    
    def _draw_combined_chart(self, data: pd.DataFrame, symbol: str):
        """Draw combined candlestick and volume chart with modern styling"""
        chart_bg = self.theme_manager.get_chart_background()
        text_color = self.theme_manager.get_text_primary()
        grid_color = self.theme_manager.get_chart_grid()
        chart_up = self.theme_manager.get_chart_up()
        chart_down = self.theme_manager.get_chart_down()
        
        self.fig.patch.set_facecolor(chart_bg)
        
        # Sample data if too many points
        if len(data) > 100:
            data = data.iloc[::len(data)//100]
        
        # Create two subplots
        ax1 = self.fig.add_subplot(211)
        ax2 = self.fig.add_subplot(212)
        
        ax1.set_facecolor(chart_bg)
        ax2.set_facecolor(chart_bg)
        
        # Candlestick on top
        for i, (idx, row) in enumerate(data.iterrows()):
            color = chart_up if row['Close'] >= row['Open'] else chart_down
            wick_color = text_color
            ax1.plot([i, i], [row['Low'], row['High']], color=wick_color, linewidth=0.5, zorder=1, alpha=0.7)
            body_height = abs(row['Close'] - row['Open'])
            if body_height < 0.01:
                body_height = 0.01
            body_bottom = min(row['Open'], row['Close'])
            rect = mpatches.Rectangle(
                (i - 0.3, body_bottom), 0.6, body_height,
                facecolor=color, edgecolor=wick_color, linewidth=0.5, zorder=2, alpha=0.8
            )
            ax1.add_patch(rect)
        
        ax1.set_title(f'{symbol} - Price & Volume ({self.current_period})', 
                     fontsize=constants.CHART_TITLE_SIZE, 
                     fontweight='bold',
                     color=text_color)
        ax1.set_ylabel('Price ($)', color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax1.tick_params(colors=text_color, labelsize=constants.CHART_FONT_SIZE)
        ax1.grid(True, alpha=constants.CHART_GRID_ALPHA, color=grid_color)
        ax1.spines['bottom'].set_color(text_color)
        ax1.spines['top'].set_color(text_color)
        ax1.spines['right'].set_color(text_color)
        ax1.spines['left'].set_color(text_color)
        
        # Volume on bottom
        colors = [chart_up if data.iloc[i]['Close'] >= data.iloc[i]['Open'] else chart_down 
                  for i in range(len(data))]
        ax2.bar(range(len(data)), data['Volume'], color=colors, alpha=0.6)
        ax2.set_xlabel('Date', color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax2.set_ylabel('Volume', color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax2.tick_params(colors=text_color, labelsize=constants.CHART_FONT_SIZE)
        ax2.grid(True, alpha=constants.CHART_GRID_ALPHA, color=grid_color)
        ax2.spines['bottom'].set_color(text_color)
        ax2.spines['top'].set_color(text_color)
        ax2.spines['right'].set_color(text_color)
        ax2.spines['left'].set_color(text_color)
        
        # Set x-axis labels for both
        tick_positions = range(0, len(data), max(1, len(data)//10))
        tick_labels = [data.index[i].strftime('%Y-%m-%d') if i < len(data) else '' 
                       for i in tick_positions]
        ax1.set_xticks(tick_positions)
        ax1.set_xticklabels(tick_labels, rotation=45, color=text_color, fontsize=constants.CHART_FONT_SIZE)
        ax2.set_xticks(tick_positions)
        ax2.set_xticklabels(tick_labels, rotation=45, color=text_color, fontsize=constants.CHART_FONT_SIZE)
        
        self.fig.tight_layout()
    
    def refresh(self):
        """Refresh the current chart"""
        if self.current_data is not None and self.current_symbol:
            self.update_chart(
                self.current_symbol,
                self.current_data,
                self.current_chart_type,
                self.current_period
            )

