"""Stat card component for displaying metrics"""
import tkinter as tk
from typing import Optional
from ui import constants
from ui.theme_manager import get_theme_manager

class StatCard(tk.Frame):
    """Modern stat card widget for displaying metrics"""
    
    def __init__(
        self,
        parent,
        label: str,
        value: str,
        icon: Optional[str] = None,
        trend: Optional[str] = None,
        trend_value: Optional[str] = None,
        *args,
        **kwargs
    ):
        super().__init__(parent, *args, **kwargs)
        self.theme_manager = get_theme_manager()
        self.label = label
        self.value = value
        self.icon = icon
        self.trend = trend  # "up", "down", or None
        self.trend_value = trend_value
        
        self.configure(
            bg=self.theme_manager.get_card_background(),
            relief=tk.FLAT,
            bd=0
        )
        
        self.create_widgets()
        self.apply_theme()
    
    def create_widgets(self):
        """Create card content"""
        # Main container with padding
        container = tk.Frame(self, bg=self.theme_manager.get_card_background())
        container.pack(fill=tk.BOTH, expand=True, padx=constants.SPACE_MD, pady=constants.SPACE_MD)
        
        # Header row (icon + label)
        header_frame = tk.Frame(container, bg=self.theme_manager.get_card_background())
        header_frame.pack(fill=tk.X, pady=(0, constants.SPACE_SM))
        
        if self.icon:
            icon_label = tk.Label(
                header_frame,
                text=self.icon,
                font=constants.FONT_BODY_LARGE,
                bg=self.theme_manager.get_card_background(),
                fg=self.theme_manager.get_text_secondary()
            )
            icon_label.pack(side=tk.LEFT, padx=(0, constants.SPACE_XS))
        
        label_widget = tk.Label(
            header_frame,
            text=self.label,
            font=constants.FONT_LABEL_SMALL,
            bg=self.theme_manager.get_card_background(),
            fg=self.theme_manager.get_text_secondary()
        )
        label_widget.pack(side=tk.LEFT)
        
        # Value row
        value_frame = tk.Frame(container, bg=self.theme_manager.get_card_background())
        value_frame.pack(fill=tk.X)
        
        value_label = tk.Label(
            value_frame,
            text=self.value,
            font=constants.FONT_H3,
            bg=self.theme_manager.get_card_background(),
            fg=self.theme_manager.get_text_primary()
        )
        value_label.pack(side=tk.LEFT)
        
        # Trend indicator
        if self.trend and self.trend_value:
            trend_color = (
                constants.LIGHT_SUCCESS if self.trend == "up" else constants.LIGHT_ERROR
                if self.theme_manager.current_theme == constants.THEME_LIGHT
                else constants.DARK_SUCCESS if self.trend == "up" else constants.DARK_ERROR
            )
            trend_icon = constants.ICON_UP if self.trend == "up" else constants.ICON_DOWN
            
            trend_frame = tk.Frame(value_frame, bg=self.theme_manager.get_card_background())
            trend_frame.pack(side=tk.LEFT, padx=(constants.SPACE_SM, 0))
            
            trend_icon_label = tk.Label(
                trend_frame,
                text=trend_icon,
                font=constants.FONT_BODY,
                bg=self.theme_manager.get_card_background(),
                fg=trend_color
            )
            trend_icon_label.pack(side=tk.LEFT)
            
            trend_label = tk.Label(
                trend_frame,
                text=self.trend_value,
                font=constants.FONT_BODY_SMALL,
                bg=self.theme_manager.get_card_background(),
                fg=trend_color
            )
            trend_label.pack(side=tk.LEFT, padx=(constants.SPACE_XS, 0))
    
    def apply_theme(self):
        """Apply current theme to the card"""
        bg = self.theme_manager.get_card_background()
        self.configure(bg=bg)
        for widget in self.winfo_children():
            self._apply_theme_recursive(widget, bg)
    
    def _apply_theme_recursive(self, widget, bg):
        """Recursively apply theme to widgets"""
        if isinstance(widget, tk.Frame):
            widget.configure(bg=bg)
        elif isinstance(widget, tk.Label):
            widget.configure(bg=bg)
        for child in widget.winfo_children():
            self._apply_theme_recursive(child, bg)
    
    def update_value(self, value: str, trend: Optional[str] = None, trend_value: Optional[str] = None):
        """Update the displayed value"""
        self.value = value
        self.trend = trend
        self.trend_value = trend_value
        # Recreate widgets
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.apply_theme()

