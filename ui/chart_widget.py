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
from ui.constants import (
    CHART_WIDTH, CHART_HEIGHT, CHART_DPI, BACKGROUND_COLOR
)

class ChartWidget(tk.Frame):
    """Widget for displaying stock price charts"""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg=BACKGROUND_COLOR)
        self.current_data = None
        self.current_symbol = None
        self.current_chart_type = "Candlestick"
        self.current_period = "3mo"
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(CHART_WIDTH, CHART_HEIGHT), dpi=CHART_DPI, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Placeholder text
        self.show_placeholder()
    
    def show_placeholder(self):
        """Show placeholder message when no data"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.text(0.5, 0.5, 'Select a stock to view chart', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=14, color='gray')
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
        """Draw a simple line chart of closing prices"""
        ax = self.fig.add_subplot(111)
        ax.plot(data.index, data['Close'], linewidth=2, color='#3498db')
        ax.set_title(f'{symbol} - Price Chart ({self.current_period})', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
    
    def _draw_candlestick_chart(self, data: pd.DataFrame, symbol: str):
        """Draw a candlestick chart"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # Sample data if too many points for performance
        if len(data) > 100:
            data = data.iloc[::len(data)//100]  # Sample to ~100 points
        
        # Draw candlesticks
        for i, (idx, row) in enumerate(data.iterrows()):
            color = '#28a745' if row['Close'] >= row['Open'] else '#dc3545'
            # High-Low line (wick)
            ax.plot([i, i], [row['Low'], row['High']], color='black', linewidth=0.5, zorder=1)
            # Open-Close body
            body_height = abs(row['Close'] - row['Open'])
            if body_height < 0.01:  # Doji - very small body
                body_height = 0.01
            body_bottom = min(row['Open'], row['Close'])
            rect = mpatches.Rectangle(
                (i - 0.3, body_bottom), 0.6, body_height,
                facecolor=color, edgecolor='black', linewidth=0.5, zorder=2
            )
            ax.add_patch(rect)
        
        # Set x-axis labels
        ax.set_xticks(range(0, len(data), max(1, len(data)//10)))
        ax.set_xticklabels([data.index[i].strftime('%Y-%m-%d') if i < len(data) else '' 
                            for i in range(0, len(data), max(1, len(data)//10))], rotation=45)
        
        ax.set_title(f'{symbol} - Candlestick Chart ({self.current_period})', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
    
    def _draw_volume_chart(self, data: pd.DataFrame, symbol: str):
        """Draw a volume chart"""
        ax = self.fig.add_subplot(111)
        colors = ['green' if data.loc[idx, 'Close'] >= data.loc[idx, 'Open'] else 'red' 
                  for idx in data.index]
        ax.bar(data.index, data['Volume'], color=colors, alpha=0.6)
        ax.set_title(f'{symbol} - Volume Chart ({self.current_period})', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Volume')
        ax.grid(True, alpha=0.3)
        self.fig.autofmt_xdate()
        self.fig.tight_layout()
    
    def _draw_combined_chart(self, data: pd.DataFrame, symbol: str):
        """Draw combined candlestick and volume chart"""
        # Sample data if too many points
        if len(data) > 100:
            data = data.iloc[::len(data)//100]
        
        # Create two subplots
        ax1 = self.fig.add_subplot(211)
        ax2 = self.fig.add_subplot(212)
        
        # Candlestick on top
        for i, (idx, row) in enumerate(data.iterrows()):
            color = '#28a745' if row['Close'] >= row['Open'] else '#dc3545'
            ax1.plot([i, i], [row['Low'], row['High']], color='black', linewidth=0.5, zorder=1)
            body_height = abs(row['Close'] - row['Open'])
            if body_height < 0.01:
                body_height = 0.01
            body_bottom = min(row['Open'], row['Close'])
            rect = mpatches.Rectangle(
                (i - 0.3, body_bottom), 0.6, body_height,
                facecolor=color, edgecolor='black', linewidth=0.5, zorder=2
            )
            ax1.add_patch(rect)
        
        ax1.set_title(f'{symbol} - Price & Volume ({self.current_period})', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price ($)')
        ax1.grid(True, alpha=0.3)
        
        # Volume on bottom
        colors = ['#28a745' if data.iloc[i]['Close'] >= data.iloc[i]['Open'] else '#dc3545' 
                  for i in range(len(data))]
        ax2.bar(range(len(data)), data['Volume'], color=colors, alpha=0.6)
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Volume')
        ax2.grid(True, alpha=0.3)
        
        # Set x-axis labels for both
        tick_positions = range(0, len(data), max(1, len(data)//10))
        tick_labels = [data.index[i].strftime('%Y-%m-%d') if i < len(data) else '' 
                       for i in tick_positions]
        ax1.set_xticks(tick_positions)
        ax1.set_xticklabels(tick_labels, rotation=45)
        ax2.set_xticks(tick_positions)
        ax2.set_xticklabels(tick_labels, rotation=45)
        
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

