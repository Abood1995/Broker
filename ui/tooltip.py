"""Tooltip widget for showing help text with modern styling"""
import tkinter as tk
from ui import constants
from ui.theme_manager import get_theme_manager

class ToolTip:
    """Create a modern tooltip for a given widget with theme support"""
    
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.theme_manager = get_theme_manager()
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.leave)
        self.widget.bind('<ButtonPress>', self.leave)
        self.widget.bind('<FocusIn>', self.enter)  # Show on focus for accessibility
        self.widget.bind('<FocusOut>', self.leave)
    
    def enter(self, event=None):
        self.schedule()
    
    def leave(self, event=None):
        self.unschedule()
        self.hidetip()
    
    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)
    
    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    
    def showtip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        # Creates a toplevel window with theme-aware styling
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        
        # Theme-aware colors
        if self.theme_manager.current_theme == constants.THEME_LIGHT:
            bg_color = constants.LIGHT_SURFACE_ELEVATED
            fg_color = constants.LIGHT_TEXT_PRIMARY
            border_color = constants.LIGHT_BORDER
        else:
            bg_color = constants.DARK_SURFACE_ELEVATED
            fg_color = constants.DARK_TEXT_PRIMARY
            border_color = constants.DARK_BORDER
        
        label = tk.Label(
            tw, 
            text=self.text, 
            justify=tk.LEFT,
            background=bg_color, 
            foreground=fg_color,
            relief=tk.SOLID, 
            borderwidth=1,
            highlightbackground=border_color,
            highlightthickness=1,
            font=constants.FONT_CAPTION, 
            wraplength=300,
            padx=constants.SPACE_SM,
            pady=constants.SPACE_XS
        )
        label.pack(ipadx=1)
    
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

