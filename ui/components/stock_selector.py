"""Visual stock selector component with icons and names"""
import tkinter as tk
from typing import List, Set, Callable
from ui import constants
from ui.theme_manager import get_theme_manager
from ui.tooltip import ToolTip

# Stock definitions with icons and names
STOCK_DEFINITIONS = {
    # Tech Stocks
    "AAPL": {"name": "Apple Inc.", "icon": "🍎", "category": "Technology"},
    "MSFT": {"name": "Microsoft Corporation", "icon": "💻", "category": "Technology"},
    "GOOGL": {"name": "Alphabet Inc.", "icon": "🔍", "category": "Technology"},
    "AMZN": {"name": "Amazon.com Inc.", "icon": "📦", "category": "E-commerce"},
    "META": {"name": "Meta Platforms Inc.", "icon": "👤", "category": "Social Media"},
    "TSLA": {"name": "Tesla Inc.", "icon": "🚗", "category": "Automotive"},
    "NVDA": {"name": "NVIDIA Corporation", "icon": "🎮", "category": "Technology"},
    "NFLX": {"name": "Netflix Inc.", "icon": "🎬", "category": "Entertainment"},
    
    # Finance
    "JPM": {"name": "JPMorgan Chase & Co.", "icon": "🏦", "category": "Finance"},
    "BAC": {"name": "Bank of America Corp.", "icon": "🏦", "category": "Finance"},
    "GS": {"name": "Goldman Sachs Group Inc.", "icon": "💼", "category": "Finance"},
    "V": {"name": "Visa Inc.", "icon": "💳", "category": "Finance"},
    "MA": {"name": "Mastercard Inc.", "icon": "💳", "category": "Finance"},
    
    # Consumer
    "WMT": {"name": "Walmart Inc.", "icon": "🛒", "category": "Retail"},
    "COST": {"name": "Costco Wholesale Corp.", "icon": "🛍️", "category": "Retail"},
    "SBUX": {"name": "Starbucks Corporation", "icon": "☕", "category": "Food & Beverage"},
    "NKE": {"name": "Nike Inc.", "icon": "👟", "category": "Apparel"},
    
    # Healthcare
    "JNJ": {"name": "Johnson & Johnson", "icon": "💊", "category": "Healthcare"},
    "PFE": {"name": "Pfizer Inc.", "icon": "💉", "category": "Healthcare"},
    "UNH": {"name": "UnitedHealth Group Inc.", "icon": "🏥", "category": "Healthcare"},
    
    # Energy & Commodities
    "XOM": {"name": "Exxon Mobil Corporation", "icon": "⛽", "category": "Energy"},
    "CVX": {"name": "Chevron Corporation", "icon": "🛢️", "category": "Energy"},
    
    # Commodities (ETFs and futures proxies)
    "GLD": {"name": "SPDR Gold Trust", "icon": "🥇", "category": "Commodities"},
    "SLV": {"name": "iShares Silver Trust", "icon": "🥈", "category": "Commodities"},
    "USO": {"name": "United States Oil Fund (WTI Crude Oil)", "icon": "🛢️", "category": "Commodities"},
    "UCO": {"name": "ProShares Ultra Bloomberg Crude Oil (2x Leveraged WTI)", "icon": "🛢️", "category": "Commodities"},
    "BNO": {"name": "United States Brent Oil Fund (Brent Crude)", "icon": "🛢️", "category": "Commodities"},
    "UNG": {"name": "United States Natural Gas Fund", "icon": "⛽", "category": "Commodities"},
    "DBA": {"name": "Invesco DB Agriculture Fund", "icon": "🌾", "category": "Commodities"},
    
    # Additional popular stocks
    "DIS": {"name": "The Walt Disney Company", "icon": "🏰", "category": "Entertainment"},
    "HD": {"name": "The Home Depot Inc.", "icon": "🔨", "category": "Retail"},
    "PG": {"name": "Procter & Gamble Co.", "icon": "🧴", "category": "Consumer Goods"},
    "KO": {"name": "The Coca-Cola Company", "icon": "🥤", "category": "Food & Beverage"},
    "PEP": {"name": "PepsiCo Inc.", "icon": "🥤", "category": "Food & Beverage"},
    "ADBE": {"name": "Adobe Inc.", "icon": "🎨", "category": "Technology"},
    "CRM": {"name": "Salesforce Inc.", "icon": "☁️", "category": "Technology"},
    "INTC": {"name": "Intel Corporation", "icon": "💾", "category": "Technology"},
    "AMD": {"name": "Advanced Micro Devices", "icon": "⚡", "category": "Technology"},
    "PYPL": {"name": "PayPal Holdings Inc.", "icon": "💸", "category": "Finance"},
    "SQ": {"name": "Block Inc. (Square)", "icon": "📱", "category": "Finance"},
    
    # More Commodities
    "DBC": {"name": "Invesco DB Commodity Index", "icon": "📊", "category": "Commodities"},
    "PDBC": {"name": "Invesco Optimum Yield Diversified", "icon": "🌍", "category": "Commodities"},
    "GSG": {"name": "iShares S&P GSCI Commodity", "icon": "📈", "category": "Commodities"},
    
    # Crypto-related (if available as stocks/ETFs)
    "COIN": {"name": "Coinbase Global Inc.", "icon": "₿", "category": "Finance"},
    "MSTR": {"name": "MicroStrategy Inc.", "icon": "₿", "category": "Technology"},
}

class StockSelector(tk.Frame):
    """Visual stock selector with buttons showing icons and names"""
    
    def __init__(self, parent, on_selection_change: Callable[[List[str]], None] = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.theme_manager = get_theme_manager()
        self.on_selection_change = on_selection_change
        self.selected_symbols: Set[str] = set()
        self.stock_buttons = {}
        
        bg = self.theme_manager.get_background()
        self.configure(bg=bg)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the stock selector interface"""
        bg = self.theme_manager.get_background()
        text_primary = self.theme_manager.get_text_primary()
        text_secondary = self.theme_manager.get_text_secondary()
        
        # Header
        header_frame = tk.Frame(self, bg=bg)
        header_frame.pack(fill=tk.X, pady=(0, constants.SPACE_MD))
        
        tk.Label(
            header_frame,
            text="Select Stocks to Analyze",
            font=constants.FONT_H4,
            bg=bg,
            fg=text_primary
        ).pack(side=tk.LEFT)
        
        # Clear selection button
        clear_btn = tk.Button(
            header_frame,
            text="Clear All",
            command=self.clear_all,
            bg=bg,
            fg=text_secondary,
            font=constants.FONT_BODY_SMALL,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=constants.SPACE_SM,
            pady=constants.SPACE_XS
        )
        clear_btn.pack(side=tk.RIGHT)
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(fg=text_primary))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(fg=text_secondary))
        
        # Search filter
        search_frame = tk.Frame(self, bg=bg)
        search_frame.pack(fill=tk.X, pady=(0, constants.SPACE_SM))
        
        tk.Label(
            search_frame,
            text="🔍 Search:",
            font=constants.FONT_LABEL_SMALL,
            bg=bg,
            fg=text_secondary
        ).pack(side=tk.LEFT, padx=constants.SPACE_SM)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=constants.FONT_BODY_SMALL,
            width=30
        )
        search_entry.pack(side=tk.LEFT, padx=constants.SPACE_SM)
        ToolTip(search_entry, "Filter stocks by name or symbol")
        
        self.search_filter = ""
        
        # Scrollable frame for stock buttons with max height
        canvas_frame = tk.Frame(self, bg=bg)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg=bg, highlightthickness=0, height=250)  # Reduced height
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=bg)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scrollable_frame = scrollable_frame
        self.canvas = canvas
        
        # Store original categories for filtering
        self.all_categories = {}
        for symbol, info in STOCK_DEFINITIONS.items():
            category = info["category"]
            if category not in self.all_categories:
                self.all_categories[category] = []
            self.all_categories[category].append((symbol, info))
        
        self.create_category_sections()
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_category_sections(self):
        """Create category sections with optional filtering"""
        # Clear existing sections
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Filter categories based on search
        filtered_categories = {}
        search_lower = self.search_filter.lower()
        
        for category, stocks in self.all_categories.items():
            filtered_stocks = []
            for symbol, info in stocks:
                if (not search_lower or 
                    search_lower in symbol.lower() or 
                    search_lower in info["name"].lower() or
                    search_lower in category.lower()):
                    filtered_stocks.append((symbol, info))
            
            if filtered_stocks:
                filtered_categories[category] = filtered_stocks
        
        # Create category sections
        for category in sorted(filtered_categories.keys()):
            self.create_category_section(self.scrollable_frame, category, filtered_categories[category])
        
        # Update canvas scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_search_change(self, *args):
        """Handle search filter change"""
        self.search_filter = self.search_var.get()
        self.create_category_sections()
    
    def create_category_section(self, parent, category: str, stocks: List[tuple]):
        """Create a section for a category of stocks"""
        bg = self.theme_manager.get_background()
        text_primary = self.theme_manager.get_text_primary()
        text_secondary = self.theme_manager.get_text_secondary()
        
        # Category header
        category_frame = tk.Frame(parent, bg=bg)
        category_frame.pack(fill=tk.X, padx=constants.SPACE_MD, pady=(constants.SPACE_LG, constants.SPACE_SM))
        
        tk.Label(
            category_frame,
            text=category,
            font=constants.FONT_LABEL_BOLD,
            bg=bg,
            fg=text_secondary
        ).pack(anchor=tk.W)
        
        # Stock buttons grid
        buttons_frame = tk.Frame(parent, bg=bg)
        buttons_frame.pack(fill=tk.X, padx=constants.SPACE_MD, pady=(0, constants.SPACE_MD))
        
        # Create buttons in a grid (3 columns)
        for i, (symbol, info) in enumerate(stocks):
            row = i // 3
            col = i % 3
            
            self.create_stock_button(buttons_frame, symbol, info, row, col)
    
    def create_stock_button(self, parent, symbol: str, info: dict, row: int, col: int):
        """Create a stock selection button"""
        surface = self.theme_manager.get_surface()
        border = self.theme_manager.get_border()
        text_primary = self.theme_manager.get_text_primary()
        text_secondary = self.theme_manager.get_text_secondary()
        primary = self.theme_manager.get_primary()
        
        # Button frame
        btn_frame = tk.Frame(
            parent,
            bg=surface,
            relief=tk.FLAT,
            bd=1,
            highlightbackground=border,
            highlightthickness=1
        )
        btn_frame.grid(row=row, column=col, padx=constants.SPACE_SM, pady=constants.SPACE_SM, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        # Content frame
        content_frame = tk.Frame(btn_frame, bg=surface)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=constants.SPACE_MD, pady=constants.SPACE_SM)
        
        # Icon and symbol
        icon_frame = tk.Frame(content_frame, bg=surface)
        icon_frame.pack(fill=tk.X, pady=(0, constants.SPACE_XS))
        
        icon_label = tk.Label(
            icon_frame,
            text=info["icon"],
            font=constants.FONT_BODY_LARGE,
            bg=surface,
            fg=text_primary
        )
        icon_label.pack(side=tk.LEFT)
        
        symbol_label = tk.Label(
            icon_frame,
            text=symbol,
            font=constants.FONT_LABEL_BOLD,
            bg=surface,
            fg=text_primary
        )
        symbol_label.pack(side=tk.LEFT, padx=(constants.SPACE_XS, 0))
        
        # Company name
        name_label = tk.Label(
            content_frame,
            text=info["name"],
            font=constants.FONT_BODY_SMALL,
            bg=surface,
            fg=text_secondary,
            wraplength=200,
            justify=tk.LEFT
        )
        name_label.pack(anchor=tk.W)
        
        # Store references
        btn_frame.symbol = symbol
        btn_frame.icon_label = icon_label
        btn_frame.symbol_label = symbol_label
        btn_frame.name_label = name_label
        
        # Selection indicator
        indicator = tk.Frame(btn_frame, bg=surface, height=3)
        indicator.pack(fill=tk.X, side=tk.BOTTOM)
        btn_frame.indicator = indicator
        
        # Click handler
        def toggle_selection(event=None):
            if symbol in self.selected_symbols:
                self.deselect_stock(btn_frame, symbol)
            else:
                self.select_stock(btn_frame, symbol)
        
        # Make entire button clickable
        for widget in [btn_frame, content_frame, icon_frame, icon_label, symbol_label, name_label]:
            widget.bind("<Button-1>", toggle_selection)
            widget.config(cursor="hand2")
        
        # Hover effects
        hover_bg = self.theme_manager.get_background_secondary()
        def on_enter(e):
            if symbol not in self.selected_symbols:
                btn_frame.config(bg=hover_bg, highlightbackground=primary)
                for w in [content_frame, icon_frame, icon_label, symbol_label, name_label]:
                    w.config(bg=hover_bg)
        
        def on_leave(e):
            if symbol not in self.selected_symbols:
                btn_frame.config(bg=surface, highlightbackground=border)
                for w in [content_frame, icon_frame, icon_label, symbol_label, name_label]:
                    w.config(bg=surface)
        
        btn_frame.bind("<Enter>", on_enter)
        btn_frame.bind("<Leave>", on_leave)
        
        self.stock_buttons[symbol] = btn_frame
    
    def select_stock(self, btn_frame, symbol: str):
        """Select a stock"""
        self.selected_symbols.add(symbol)
        
        primary = self.theme_manager.get_primary()
        primary_light = constants.LIGHT_PRIMARY_LIGHT if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_PRIMARY_LIGHT
        text_primary = self.theme_manager.get_text_primary()
        
        # Update button appearance
        btn_frame.config(bg=primary_light, highlightbackground=primary, highlightthickness=2)
        btn_frame.indicator.config(bg=primary)
        
        # Update all child widgets
        content_frame = btn_frame.winfo_children()[0]
        for w in [content_frame, btn_frame.icon_label, btn_frame.symbol_label, btn_frame.name_label]:
            if hasattr(w, 'config'):
                try:
                    w.config(bg=primary_light)
                except:
                    pass
        
        # Notify callback
        if self.on_selection_change:
            self.on_selection_change(list(self.selected_symbols))
    
    def deselect_stock(self, btn_frame, symbol: str):
        """Deselect a stock"""
        self.selected_symbols.discard(symbol)
        
        surface = self.theme_manager.get_surface()
        border = self.theme_manager.get_border()
        
        # Update button appearance
        btn_frame.config(bg=surface, highlightbackground=border, highlightthickness=1)
        btn_frame.indicator.config(bg=surface)
        
        # Update all child widgets
        content_frame = btn_frame.winfo_children()[0]
        for w in [content_frame, btn_frame.icon_label, btn_frame.symbol_label, btn_frame.name_label]:
            if hasattr(w, 'config'):
                try:
                    w.config(bg=surface)
                except:
                    pass
        
        # Notify callback
        if self.on_selection_change:
            self.on_selection_change(list(self.selected_symbols))
    
    def clear_all(self):
        """Clear all selections"""
        for symbol in list(self.selected_symbols):
            if symbol in self.stock_buttons:
                self.deselect_stock(self.stock_buttons[symbol], symbol)
    
    def get_selected_symbols(self) -> List[str]:
        """Get list of selected symbols"""
        return list(self.selected_symbols)
    
    def set_selected_symbols(self, symbols: List[str]):
        """Set selected symbols programmatically"""
        self.clear_all()
        for symbol in symbols:
            if symbol in self.stock_buttons:
                self.select_stock(self.stock_buttons[symbol], symbol)

