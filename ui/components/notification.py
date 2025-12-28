"""Toast notification system"""
import tkinter as tk
from typing import Optional
from ui import constants
from ui.theme_manager import get_theme_manager

class Notification:
    """Toast-style notification widget"""
    
    def __init__(
        self,
        parent,
        message: str,
        notification_type: str = "info",  # "success", "error", "warning", "info"
        duration: int = None
    ):
        self.parent = parent
        self.message = message
        self.notification_type = notification_type
        self.duration = duration or constants.TOAST_DURATION
        self.theme_manager = get_theme_manager()
        
        # Create toplevel window
        self.window = tk.Toplevel(parent)
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        
        # Position in top-right corner
        self.position_window()
        
        # Create content
        self.create_widgets()
        
        # Auto-dismiss
        self.window.after(self.duration, self.dismiss)
    
    def position_window(self):
        """Position window in top-right corner"""
        self.window.update_idletasks()
        width = constants.TOAST_WIDTH
        height = constants.TOAST_HEIGHT
        
        # Get parent window position
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        
        x = parent_x + parent_width - width - constants.SPACE_MD
        y = parent_y + constants.SPACE_MD
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create notification content"""
        # Get colors based on type
        if self.notification_type == "success":
            bg_color = (
                constants.LIGHT_SUCCESS_LIGHT if self.theme_manager.current_theme == constants.THEME_LIGHT
                else constants.DARK_SUCCESS_LIGHT
            )
            icon_color = (
                constants.LIGHT_SUCCESS if self.theme_manager.current_theme == constants.THEME_LIGHT
                else constants.DARK_SUCCESS
            )
            icon = constants.ICON_SUCCESS
        elif self.notification_type == "error":
            bg_color = (
                constants.LIGHT_ERROR_LIGHT if self.theme_manager.current_theme == constants.THEME_LIGHT
                else constants.DARK_ERROR_LIGHT
            )
            icon_color = (
                constants.LIGHT_ERROR if self.theme_manager.current_theme == constants.THEME_LIGHT
                else constants.DARK_ERROR
            )
            icon = constants.ICON_ERROR
        elif self.notification_type == "warning":
            bg_color = (
                constants.LIGHT_WARNING_LIGHT if self.theme_manager.current_theme == constants.THEME_LIGHT
                else constants.DARK_WARNING_LIGHT
            )
            icon_color = (
                constants.LIGHT_WARNING if self.theme_manager.current_theme == constants.THEME_LIGHT
                else constants.DARK_WARNING
            )
            icon = constants.ICON_WARNING
        else:  # info
            bg_color = (
                constants.LIGHT_INFO_LIGHT if self.theme_manager.current_theme == constants.THEME_LIGHT
                else constants.DARK_INFO_LIGHT
            )
            icon_color = (
                constants.LIGHT_INFO if self.theme_manager.current_theme == constants.THEME_LIGHT
                else constants.DARK_INFO
            )
            icon = constants.ICON_INFO
        
        self.window.configure(bg=bg_color)
        
        # Container
        container = tk.Frame(
            self.window,
            bg=bg_color,
            relief=tk.FLAT
        )
        container.pack(fill=tk.BOTH, expand=True, padx=constants.TOAST_PADDING, pady=constants.TOAST_PADDING)
        
        # Icon
        icon_label = tk.Label(
            container,
            text=icon,
            font=constants.FONT_BODY_LARGE,
            bg=bg_color,
            fg=icon_color
        )
        icon_label.pack(side=tk.LEFT, padx=(0, constants.SPACE_SM))
        
        # Message
        message_label = tk.Label(
            container,
            text=self.message,
            font=constants.FONT_BODY,
            bg=bg_color,
            fg=self.theme_manager.get_text_primary(),
            wraplength=constants.TOAST_WIDTH - constants.TOAST_PADDING * 2 - 40,
            justify=tk.LEFT
        )
        message_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Close button
        close_btn = tk.Label(
            container,
            text="×",
            font=constants.FONT_H4,
            bg=bg_color,
            fg=self.theme_manager.get_text_secondary(),
            cursor="hand2"
        )
        close_btn.pack(side=tk.RIGHT, padx=(constants.SPACE_SM, 0))
        close_btn.bind("<Button-1>", lambda e: self.dismiss())
        close_btn.bind("<Enter>", lambda e: close_btn.config(fg=self.theme_manager.get_text_primary()))
        close_btn.bind("<Leave>", lambda e: close_btn.config(fg=self.theme_manager.get_text_secondary()))
    
    def dismiss(self):
        """Dismiss the notification"""
        if self.window.winfo_exists():
            self.window.destroy()

def show_notification(parent, message: str, notification_type: str = "info", duration: int = None):
    """Show a notification"""
    return Notification(parent, message, notification_type, duration)

