"""Loading spinner widget"""
import tkinter as tk
from typing import Optional
from ui import constants
from ui.theme_manager import get_theme_manager

class LoadingWidget(tk.Canvas):
    """Animated loading spinner widget"""
    
    def __init__(self, parent, size: int = None, *args, **kwargs):
        size = size or constants.LOADING_SPINNER_SIZE
        super().__init__(
            parent,
            width=size,
            height=size,
            highlightthickness=0,
            bg=parent.cget('bg') if hasattr(parent, 'cget') else constants.get_background(),
            *args,
            **kwargs
        )
        self.size = size
        self.theme_manager = get_theme_manager()
        self.angle = 0
        self.animation_id = None
        self.is_animating = False
        self.create_spinner()
    
    def create_spinner(self):
        """Create the spinner arcs"""
        self.delete("all")
        center = self.size // 2
        radius = (self.size - 4) // 2
        
        # Create 8 arcs for smooth animation
        for i in range(8):
            start_angle = (self.angle + i * 45) % 360
            extent = 30
            
            # Calculate opacity (fade effect)
            opacity = 1.0 - (i * 0.12)
            if opacity < 0.1:
                opacity = 0.1
            
            # Get color with opacity
            color = self.theme_manager.get_primary()
            # Convert hex to RGB and apply opacity
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            r = int(r * opacity)
            g = int(g * opacity)
            b = int(b * opacity)
            color_with_opacity = f"#{r:02x}{g:02x}{b:02x}"
            
            self.create_arc(
                center - radius,
                center - radius,
                center + radius,
                center + radius,
                start=start_angle,
                extent=extent,
                outline=color_with_opacity,
                width=3,
                style=tk.ARC
            )
    
    def animate(self):
        """Animate the spinner"""
        if not self.is_animating:
            return
        
        self.angle = (self.angle + 10) % 360
        self.create_spinner()
        self.animation_id = self.after(50, self.animate)
    
    def start(self):
        """Start the animation"""
        if not self.is_animating:
            self.is_animating = True
            self.animate()
    
    def stop(self):
        """Stop the animation"""
        self.is_animating = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None
        self.delete("all")
    
    def destroy(self):
        """Clean up on destroy"""
        self.stop()
        super().destroy()

