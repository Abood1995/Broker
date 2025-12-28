"""Theme manager for light/dark mode switching"""
import os
import json
import tkinter as tk
from typing import Callable, List, Optional
from ui import constants

class ThemeManager:
    """Manages theme switching and persistence"""
    
    SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".broker_theme.json")
    
    def __init__(self):
        self.current_theme = self.load_theme()
        self._callbacks: List[Callable[[str], None]] = []
        self._widgets: List[tk.Widget] = []
    
    def load_theme(self) -> str:
        """Load theme preference from file"""
        try:
            if os.path.exists(self.SETTINGS_FILE):
                with open(self.SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    theme = data.get('theme', constants.THEME_LIGHT)
                    if theme in [constants.THEME_LIGHT, constants.THEME_DARK]:
                        return theme
        except Exception:
            pass
        return constants.THEME_LIGHT
    
    def save_theme(self, theme: str):
        """Save theme preference to file"""
        try:
            data = {'theme': theme}
            with open(self.SETTINGS_FILE, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass
    
    def set_theme(self, theme: str):
        """Set the current theme and update all registered widgets"""
        if theme not in [constants.THEME_LIGHT, constants.THEME_DARK]:
            return
        
        self.current_theme = theme
        constants.CURRENT_THEME = theme
        
        # Update recommendation colors based on theme
        if theme == constants.THEME_LIGHT:
            constants.RECOMMENDATION_COLORS = constants.RECOMMENDATION_COLORS_LIGHT
            constants.RECOMMENDATION_TEXT_COLORS = constants.RECOMMENDATION_TEXT_COLORS_LIGHT
            constants.RECOMMENDATION_COLOR_DEFAULT = constants.LIGHT_SURFACE
        else:
            constants.RECOMMENDATION_COLORS = constants.RECOMMENDATION_COLORS_DARK
            constants.RECOMMENDATION_TEXT_COLORS = constants.RECOMMENDATION_TEXT_COLORS_DARK
            constants.RECOMMENDATION_COLOR_DEFAULT = constants.DARK_SURFACE
        
        # Save preference
        self.save_theme(theme)
        
        # Notify callbacks
        for callback in self._callbacks:
            try:
                callback(theme)
            except Exception:
                pass
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = constants.THEME_DARK if self.current_theme == constants.THEME_LIGHT else constants.THEME_LIGHT
        self.set_theme(new_theme)
    
    def register_callback(self, callback: Callable[[str], None]):
        """Register a callback to be called when theme changes"""
        if callback not in self._callbacks:
            self._callbacks.append(callback)
    
    def unregister_callback(self, callback: Callable[[str], None]):
        """Unregister a callback"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def get_background(self) -> str:
        """Get current background color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_BACKGROUND_SECONDARY
        return constants.DARK_BACKGROUND_SECONDARY
    
    def get_background_secondary(self) -> str:
        """Get current secondary background color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_BACKGROUND_TERTIARY
        return constants.DARK_BACKGROUND_TERTIARY
    
    def get_surface(self) -> str:
        """Get current surface color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_SURFACE
        return constants.DARK_SURFACE
    
    def get_text_primary(self) -> str:
        """Get current primary text color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_TEXT_PRIMARY
        return constants.DARK_TEXT_PRIMARY
    
    def get_text_secondary(self) -> str:
        """Get current secondary text color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_TEXT_SECONDARY
        return constants.DARK_TEXT_SECONDARY
    
    def get_primary(self) -> str:
        """Get current primary color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_PRIMARY
        return constants.DARK_PRIMARY
    
    def get_border(self) -> str:
        """Get current border color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_BORDER
        return constants.DARK_BORDER
    
    def get_card_background(self) -> str:
        """Get current card background color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_SURFACE
        return constants.DARK_SURFACE
    
    def get_chart_background(self) -> str:
        """Get current chart background color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_CHART_BACKGROUND
        return constants.DARK_CHART_BACKGROUND
    
    def get_chart_grid(self) -> str:
        """Get current chart grid color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_CHART_GRID
        return constants.DARK_CHART_GRID
    
    def get_chart_up(self) -> str:
        """Get current chart up color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_CHART_UP
        return constants.DARK_CHART_UP
    
    def get_chart_down(self) -> str:
        """Get current chart down color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.LIGHT_CHART_DOWN
        return constants.DARK_CHART_DOWN
    
    def get_treeview_alternate(self) -> str:
        """Get current treeview alternate row color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.TREEVIEW_ALTERNATE_COLOR_LIGHT
        return constants.TREEVIEW_ALTERNATE_COLOR_DARK
    
    def get_treeview_hover(self) -> str:
        """Get current treeview hover color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.TREEVIEW_HOVER_COLOR_LIGHT
        return constants.TREEVIEW_HOVER_COLOR_DARK
    
    def get_treeview_selected(self) -> str:
        """Get current treeview selected color"""
        if self.current_theme == constants.THEME_LIGHT:
            return constants.TREEVIEW_SELECTED_COLOR_LIGHT
        return constants.TREEVIEW_SELECTED_COLOR_DARK

# Global theme manager instance
_theme_manager: Optional[ThemeManager] = None

def get_theme_manager() -> ThemeManager:
    """Get the global theme manager instance"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager

