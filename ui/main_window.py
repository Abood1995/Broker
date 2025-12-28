import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import csv
import json
from typing import List, Optional
from datetime import datetime
from models.recommendation import Recommendation
from services.analyzer import StockAnalyzer
from services.chart_data_fetcher import ChartDataFetcher
from ui.chart_widget import ChartWidget
from ui.chart_controls import ChartControls
from ui.news_panel import NewsPanel
from ui.tooltip import ToolTip
from services.news_fetcher import NewsFetcher
from ui.theme_manager import get_theme_manager
from ui.components import StatCard, LoadingWidget, show_notification, StockSelector
from ui import constants

class MainWindow:
    """Main GUI window for the broker application with tabbed interface"""
    
    def __init__(self, root: tk.Tk, analyzer: StockAnalyzer):
        self.root = root
        self.analyzer = analyzer
        self.current_recommendations = []
        self.selected_recommendation = None
        self.chart_data_fetcher = ChartDataFetcher()
        self.theme_manager = get_theme_manager()
        self.loading_widget = None
        
        # Initialize news fetcher with API keys from config if available
        try:
            from config import NEWSAPI_KEY, ALPHAVANTAGE_KEY
            self.news_fetcher = NewsFetcher(
                newsapi_key=NEWSAPI_KEY,
                alphavantage_key=ALPHAVANTAGE_KEY
            )
        except:
            self.news_fetcher = NewsFetcher()
        
        # Register theme change callback
        self.theme_manager.register_callback(self.on_theme_change)
        
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title(constants.WINDOW_TITLE)
        self.root.geometry(constants.WINDOW_GEOMETRY)
        self.root.minsize(constants.WINDOW_MIN_WIDTH, constants.WINDOW_MIN_HEIGHT)
        bg = self.theme_manager.get_background()
        self.root.configure(bg=bg)
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def on_theme_change(self, theme: str):
        """Handle theme change"""
        bg = self.theme_manager.get_background()
        self.root.configure(bg=bg)
        self.apply_theme_to_widgets()
    
    def apply_theme_to_widgets(self):
        """Apply theme to all widgets"""
        # This will be called recursively for all widgets
        bg = self.theme_manager.get_background()
        self._apply_theme_recursive(self.root, bg)
    
    def _apply_theme_recursive(self, widget, bg):
        """Recursively apply theme to widgets"""
        try:
            if isinstance(widget, (tk.Frame, tk.Label, tk.Button)):
                widget.configure(bg=bg)
        except:
            pass
        for child in widget.winfo_children():
            self._apply_theme_recursive(child, bg)
    
    def create_widgets(self):
        """Create and layout all GUI widgets with tabbed interface"""
        bg = self.theme_manager.get_background()
        text_primary = self.theme_manager.get_text_primary()
        text_secondary = self.theme_manager.get_text_secondary()
        primary = self.theme_manager.get_primary()
        
        # Header frame with title and theme toggle
        header_frame = tk.Frame(self.root, bg=bg)
        header_frame.grid(row=0, column=0, pady=constants.PADDING_HEADER, padx=constants.PADDING_FRAME, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Header title
        header = tk.Label(
            header_frame,
            text=constants.TEXT_HEADER,
            font=constants.FONT_H1,
            bg=bg,
            fg=text_primary
        )
        header.grid(row=0, column=0, sticky="w")
        
        # Theme toggle button
        theme_icon = constants.ICON_THEME_DARK if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.ICON_THEME_LIGHT
        self.theme_btn = tk.Button(
            header_frame,
            text=theme_icon,
            command=self.toggle_theme,
            bg=bg,
            fg=text_secondary,
            font=constants.FONT_BODY_LARGE,
            relief=tk.FLAT,
            bd=0,
            padx=constants.SPACE_SM,
            pady=constants.SPACE_XS,
            cursor="hand2"
        )
        self.theme_btn.grid(row=0, column=1, sticky="e")
        self.theme_btn.bind("<Enter>", lambda e: self.theme_btn.config(bg=self.theme_manager.get_surface()))
        self.theme_btn.bind("<Leave>", lambda e: self.theme_btn.config(bg=bg))
        ToolTip(self.theme_btn, "Toggle light/dark theme")
        
        # Collapsible stock selection frame
        selection_container = tk.Frame(self.root, bg=bg)
        selection_container.grid(row=1, column=0, pady=constants.PADDING_INPUT, padx=constants.PADDING_FRAME, sticky="ew")
        selection_container.grid_columnconfigure(0, weight=1)
        
        # Collapsible header
        selection_header = tk.Frame(selection_container, bg=bg, relief=tk.FLAT, bd=1, highlightbackground=self.theme_manager.get_border(), highlightthickness=1)
        selection_header.grid(row=0, column=0, sticky="ew")
        selection_header.grid_columnconfigure(1, weight=1)
        
        # Expand/collapse indicator
        self.selection_expand_icon = tk.Label(
            selection_header,
            text=constants.ICON_COLLAPSE,
            font=constants.FONT_BODY,
            bg=bg,
            fg=text_secondary,
            cursor="hand2"
        )
        self.selection_expand_icon.grid(row=0, column=0, padx=constants.SPACE_SM, pady=constants.SPACE_SM)
        
        # Header label
        header_label = tk.Label(
            selection_header,
            text="📊 Stock Selection",
            font=constants.FONT_LABEL_BOLD,
            bg=bg,
            fg=text_primary,
            cursor="hand2"
        )
        header_label.grid(row=0, column=1, sticky="w", padx=constants.SPACE_SM, pady=constants.SPACE_SM)
        
        # Stock selection content (initially visible)
        self.selection_content = tk.Frame(selection_container, bg=bg)
        self.selection_content.grid(row=1, column=0, sticky="ew")
        self.selection_content.grid_columnconfigure(0, weight=1)
        
        # Create notebook for selection methods
        selection_notebook = ttk.Notebook(self.selection_content)
        selection_notebook.grid(row=0, column=0, sticky="ew")
        
        # Visual Stock Selector Tab
        visual_frame = tk.Frame(selection_notebook, bg=bg)
        selection_notebook.add(visual_frame, text="📊 Quick Select")
        visual_frame.grid_rowconfigure(0, weight=1)
        visual_frame.grid_columnconfigure(0, weight=1)
        
        # Create stock selector with fixed height
        self.stock_selector = StockSelector(
            visual_frame,
            on_selection_change=self.on_stock_selection_change
        )
        self.stock_selector.pack(fill=tk.BOTH, expand=True, padx=constants.SPACE_SM, pady=constants.SPACE_SM)
        
        # Manual Entry Tab
        manual_frame = tk.Frame(selection_notebook, bg=bg)
        selection_notebook.add(manual_frame, text="⌨️ Manual Entry")
        manual_frame.grid_columnconfigure(1, weight=1)
        
        # Manual input frame
        input_frame = tk.Frame(manual_frame, bg=bg)
        input_frame.grid(row=0, column=0, columnspan=3, pady=constants.PADDING_INPUT, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        
        tk.Label(
            input_frame,
            text=constants.TEXT_SYMBOLS_LABEL,
            font=constants.FONT_LABEL,
            bg=bg,
            fg=text_primary
        ).grid(row=0, column=0, padx=constants.PADDING_WIDGET, sticky="w")
        
        # Modern input styling
        from ui.constants import COMMON_STOCK_SYMBOLS
        self.symbol_entry = ttk.Combobox(
            input_frame,
            width=constants.ENTRY_WIDTH,
            font=constants.FONT_ENTRY,
            values=COMMON_STOCK_SYMBOLS
        )
        self.symbol_entry.grid(row=0, column=1, padx=constants.PADDING_WIDGET, sticky="ew")
        self.symbol_entry.insert(0, constants.DEFAULT_SYMBOLS)
        self.symbol_entry.bind('<KeyRelease>', self.on_symbol_entry_change)
        
        # Add tooltips
        ToolTip(self.symbol_entry, "Enter stock symbols separated by commas. Use autocomplete for suggestions.")
        
        # Toggle selection panel
        self.selection_expanded = True
        def toggle_selection_panel(event=None):
            if self.selection_expanded:
                self.selection_content.grid_remove()
                self.selection_expand_icon.config(text=constants.ICON_EXPAND)
                self.selection_expanded = False
            else:
                self.selection_content.grid()
                self.selection_expand_icon.config(text=constants.ICON_COLLAPSE)
                self.selection_expanded = True
            self.root.update_idletasks()
        
        self.selection_expand_icon.bind("<Button-1>", toggle_selection_panel)
        header_label.bind("<Button-1>", toggle_selection_panel)
        
        # Action buttons frame
        action_frame = tk.Frame(self.root, bg=bg)
        action_frame.grid(row=2, column=0, pady=constants.PADDING_INPUT, padx=constants.PADDING_FRAME, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)
        
        # Analyze button
        self.analyze_btn = tk.Button(
            action_frame,
            text=f"{constants.ICON_ANALYSIS} {constants.TEXT_BUTTON_ANALYZE}",
            command=self.analyze_stocks,
            bg=primary,
            fg=constants.LIGHT_TEXT_PRIMARY if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_TEXT_PRIMARY,
            font=constants.FONT_BUTTON,
            padx=constants.BUTTON_PADX,
            pady=constants.BUTTON_PADY,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2"
        )
        self.analyze_btn.pack(side=tk.LEFT)
        
        # Button hover effects
        primary_hover = constants.LIGHT_PRIMARY_HOVER if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_PRIMARY_HOVER
        self.analyze_btn.bind("<Enter>", lambda e: self.analyze_btn.config(bg=primary_hover))
        self.analyze_btn.bind("<Leave>", lambda e: self.analyze_btn.config(bg=primary))
        
        ToolTip(self.analyze_btn, "Analyze the selected stocks (Press Enter)")
        
        # Selected stocks display
        self.selected_stocks_label = tk.Label(
            action_frame,
            text="",
            font=constants.FONT_BODY_SMALL,
            bg=bg,
            fg=text_secondary
        )
        self.selected_stocks_label.pack(side=tk.LEFT, padx=constants.SPACE_MD)
        
        # Active analyzers label
        self.analyzers_label = tk.Label(
            action_frame,
            text="",
            font=constants.FONT_ANALYZERS_LABEL,
            bg=bg,
            fg=text_secondary
        )
        self.analyzers_label.pack(side=tk.RIGHT)
        self.update_analyzers_label()
        
        # Create notebook for tabs with modern styling
        style = ttk.Style()
        style.theme_use('clam')
        # Configure notebook style
        style.configure('TNotebook', background=bg, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[constants.SPACE_MD, constants.SPACE_SM])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=3, column=0, padx=constants.PADDING_FRAME, pady=constants.PADDING_INPUT, sticky="nsew")
        
        # Create tabs
        self.create_overview_tab()
        self.create_charts_tab()
        self.create_analysis_tab()
        self.create_news_tab()
        
        # Bind selection event for tree
        if hasattr(self, 'tree'):
            self.tree.bind("<<TreeviewSelect>>", self.on_select)
            # Context menu
            self.context_menu = tk.Menu(self.root, tearoff=0)
            self.context_menu.add_command(label="View Details", command=self.view_selected_details)
            self.context_menu.add_command(label="Export Selected", command=self.export_selected)
            self.tree.bind("<Button-3>", self.show_context_menu)  # Right-click
        
        # Export button with modern styling
        export_frame = tk.Frame(self.root, bg=bg)
        export_frame.grid(row=4, column=0, pady=constants.PADDING_INPUT)
        
        success_color = constants.LIGHT_SUCCESS if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_SUCCESS
        success_hover = constants.LIGHT_SUCCESS_HOVER if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_SUCCESS_HOVER
        
        export_btn = tk.Button(
            export_frame,
            text=f"{constants.ICON_EXPORT} Export Results",
            command=self.export_results,
            bg=success_color,
            fg=constants.LIGHT_TEXT_PRIMARY if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.DARK_TEXT_PRIMARY,
            font=constants.FONT_BUTTON,
            padx=constants.BUTTON_PADX,
            pady=constants.BUTTON_PADY,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2"
        )
        export_btn.pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        export_btn.bind("<Enter>", lambda e: export_btn.config(bg=success_hover))
        export_btn.bind("<Leave>", lambda e: export_btn.config(bg=success_color))
        ToolTip(export_btn, "Export analysis results to CSV or JSON (Ctrl+E)")
        
        # Bind keyboard shortcuts
        self.root.bind('<Return>', lambda e: self.analyze_stocks())
        self.root.bind('<Escape>', lambda e: self.clear_selection())
        self.root.bind('<Control-f>', lambda e: self.symbol_entry.focus())
        self.root.bind('<Control-e>', lambda e: self.export_results())
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.theme_manager.toggle_theme()
        theme_icon = constants.ICON_THEME_DARK if self.theme_manager.current_theme == constants.THEME_LIGHT else constants.ICON_THEME_LIGHT
        self.theme_btn.config(text=theme_icon)
    
    def on_symbol_entry_change(self, event):
        """Handle autocomplete for symbol entry and sync with visual selector"""
        value = self.symbol_entry.get().upper()
        if value:
            # Filter symbols that start with the entered text
            filtered = [s for s in COMMON_STOCK_SYMBOLS if s.startswith(value)]
            if filtered:
                self.symbol_entry['values'] = filtered
            else:
                self.symbol_entry['values'] = COMMON_STOCK_SYMBOLS
            
            # Update visual selector if symbols are entered
            if hasattr(self, 'stock_selector'):
                symbols = [s.strip().upper() for s in value.split(",") if s.strip()]
                # Only update if symbols are valid and match known stocks
                from ui.components.stock_selector import STOCK_DEFINITIONS
                valid_symbols = [s for s in symbols if s in STOCK_DEFINITIONS]
                if valid_symbols:
                    self.stock_selector.set_selected_symbols(valid_symbols)
        else:
            self.symbol_entry['values'] = COMMON_STOCK_SYMBOLS
            # Clear visual selector if entry is cleared
            if hasattr(self, 'stock_selector'):
                self.stock_selector.clear_all()
    
    def create_overview_tab(self):
        """Create the Overview tab with results table and details"""
        bg = self.theme_manager.get_background()
        overview_frame = tk.Frame(self.notebook, bg=bg)
        self.notebook.add(overview_frame, text=constants.TAB_NAMES[0])
        overview_frame.grid_rowconfigure(2, weight=1)
        overview_frame.grid_columnconfigure(0, weight=1)
        
        # Modern dashboard frame with stat cards
        dashboard_frame = tk.Frame(overview_frame, bg=bg)
        dashboard_frame.grid(row=0, column=0, padx=constants.PADDING_FRAME, pady=(constants.PADDING_INPUT, constants.SPACE_MD), sticky="ew")
        dashboard_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="stat")
        
        self.dashboard_frame = dashboard_frame
        
        # Filter frame with modern styling
        filter_frame = tk.Frame(overview_frame, bg=bg)
        filter_frame.grid(row=1, column=0, padx=constants.PADDING_FRAME, pady=(constants.SPACE_SM, constants.SPACE_MD), sticky="ew")
        
        text_primary = self.theme_manager.get_text_primary()
        tk.Label(
            filter_frame,
            text="Filter by Recommendation:",
            font=constants.FONT_LABEL,
            bg=bg,
            fg=text_primary
        ).pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"],
            state="readonly",
            width=18
        )
        filter_combo.pack(side=tk.LEFT, padx=constants.PADDING_WIDGET)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Results frame with treeview
        results_frame = tk.Frame(overview_frame, bg=bg)
        results_frame.grid(row=2, column=0, padx=constants.PADDING_FRAME, pady=constants.PADDING_INPUT, sticky="nsew")
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Modern treeview styling
        style = ttk.Style()
        style.configure("Treeview", 
                       background=self.theme_manager.get_surface(),
                       foreground=text_primary,
                       fieldbackground=self.theme_manager.get_surface(),
                       rowheight=constants.TREEVIEW_ROW_HEIGHT,
                       font=constants.FONT_BODY)
        style.configure("Treeview.Heading",
                       background=self.theme_manager.get_surface(),
                       foreground=text_primary,
                       font=constants.FONT_LABEL_BOLD)
        style.map("Treeview",
                 background=[("selected", self.theme_manager.get_treeview_selected())],
                 foreground=[("selected", text_primary)])
        
        # Treeview for recommendations
        self.tree = ttk.Treeview(results_frame, columns=constants.TREEVIEW_COLUMNS, show="headings", height=constants.TREEVIEW_HEIGHT)
        
        self.sort_column = None
        self.sort_reverse = False
        
        for col in constants.TREEVIEW_COLUMNS:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=constants.TREEVIEW_COLUMN_WIDTH, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Details section with modern styling
        details_frame = tk.Frame(overview_frame, bg=bg)
        details_frame.grid(row=3, column=0, padx=constants.PADDING_FRAME, pady=constants.PADDING_INPUT, sticky="ew")
        details_frame.grid_columnconfigure(0, weight=1)
        
        details_label = tk.Label(
            details_frame,
            text=constants.TEXT_DETAILS_LABEL,
            font=constants.FONT_LABEL_BOLD,
            bg=bg,
            fg=text_primary
        )
        details_label.grid(row=0, column=0, pady=constants.PADDING_DETAILS_LABEL, sticky="w")
        
        surface = self.theme_manager.get_surface()
        border = self.theme_manager.get_border()
        self.details_text = scrolledtext.ScrolledText(
            details_frame,
            width=constants.DETAILS_TEXT_WIDTH,
            height=constants.DETAILS_TEXT_HEIGHT,
            font=constants.FONT_DETAILS,
            wrap=tk.WORD,
            bg=surface,
            fg=text_primary,
            relief=tk.FLAT,
            bd=1,
            highlightbackground=border,
            highlightcolor=self.theme_manager.get_primary(),
            highlightthickness=1
        )
        self.details_text.grid(row=1, column=0, sticky="ew")
    
    def create_charts_tab(self):
        """Create the Charts tab with chart widget and controls"""
        bg = self.theme_manager.get_background()
        charts_frame = tk.Frame(self.notebook, bg=bg)
        self.notebook.add(charts_frame, text=constants.TAB_NAMES[1])
        charts_frame.grid_rowconfigure(1, weight=1)
        charts_frame.grid_columnconfigure(0, weight=1)
        
        # Chart controls at top
        self.chart_controls = ChartControls(
            charts_frame,
            data_fetcher=self.chart_data_fetcher
        )
        self.chart_controls.grid(row=0, column=0, padx=constants.PADDING_FRAME, pady=constants.PADDING_INPUT, sticky="ew")
        
        # Chart widget
        self.chart_widget = ChartWidget(charts_frame)
        self.chart_widget.grid(row=1, column=0, padx=constants.PADDING_FRAME, pady=constants.PADDING_INPUT, sticky="nsew")
        
        # Connect controls to chart widget
        self.chart_controls.chart_widget = self.chart_widget
        
        # Store reference
        self.charts_frame = charts_frame
    
    def create_analysis_tab(self):
        """Create the Analysis tab with expandable sections"""
        bg = self.theme_manager.get_background()
        analysis_frame = tk.Frame(self.notebook, bg=bg)
        self.notebook.add(analysis_frame, text=constants.TAB_NAMES[2])
        analysis_frame.grid_rowconfigure(0, weight=1)
        analysis_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollable frame for analysis sections
        canvas = tk.Canvas(analysis_frame, bg=bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=bg)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Placeholder
        placeholder = tk.Label(
            scrollable_frame,
            text="Select a stock to view detailed analysis breakdown",
            font=constants.FONT_LABEL,
            bg=bg,
            fg=self.theme_manager.get_text_secondary()
        )
        placeholder.pack(pady=50)
        
        # Store references
        self.analysis_frame = scrollable_frame
        self.analysis_canvas = canvas
    
    def create_news_tab(self):
        """Create the News tab with news panel"""
        bg = self.theme_manager.get_background()
        news_frame = tk.Frame(self.notebook, bg=bg)
        self.notebook.add(news_frame, text=constants.TAB_NAMES[3])
        news_frame.grid_rowconfigure(0, weight=1)
        news_frame.grid_columnconfigure(0, weight=1)
        
        # News panel
        self.news_panel = NewsPanel(news_frame)
        self.news_panel.pack(fill=tk.BOTH, expand=True, padx=constants.PADDING_FRAME, pady=constants.PADDING_INPUT)
        
        # Store reference
        self.news_frame = news_frame
    
    def update_analyzers_label(self):
        """Update the label showing active analyzers"""
        active_analyzers = self.analyzer.get_active_analyzers()
        if active_analyzers:
            analyzers_text = f"{constants.TEXT_ACTIVE_ANALYZERS_PREFIX}{', '.join(active_analyzers)}"
            self.analyzers_label.config(text=analyzers_text)
        else:
            self.analyzers_label.config(text=constants.TEXT_NO_ANALYZERS)
    
    def on_stock_selection_change(self, selected_symbols: List[str]):
        """Handle stock selection change from visual selector"""
        if selected_symbols:
            symbols_str = ", ".join(selected_symbols)
            self.selected_stocks_label.config(
                text=f"Selected: {symbols_str} ({len(selected_symbols)} stocks)",
                fg=self.theme_manager.get_text_primary()
            )
            # Also update manual entry field
            self.symbol_entry.delete(0, tk.END)
            self.symbol_entry.insert(0, symbols_str)
        else:
            self.selected_stocks_label.config(text="", fg=self.theme_manager.get_text_secondary())
    
    def analyze_stocks(self):
        """Analyze stocks and display recommendations"""
        # Get symbols from either visual selector or manual entry
        symbols = []
        
        # Check visual selector first
        if hasattr(self, 'stock_selector'):
            selected = self.stock_selector.get_selected_symbols()
            if selected:
                symbols = selected
        
        # Fallback to manual entry if no visual selection
        if not symbols:
            symbols_str = self.symbol_entry.get().strip()
            if not symbols_str:
                show_notification(self.root, constants.MESSAGE_NO_SYMBOLS, "warning")
                return
            symbols = [s.strip().upper() for s in symbols_str.split(",")]
        
        if not symbols:
            show_notification(self.root, constants.MESSAGE_NO_SYMBOLS, "warning")
            return
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.details_text.delete(1.0, tk.END)
        
        # Show loading indicator
        bg = self.theme_manager.get_background()
        loading_frame = tk.Frame(self.root, bg=bg)
        loading_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        loading_label = tk.Label(
            loading_frame,
            text=f"{constants.MESSAGE_ANALYZING.format(count=len(symbols))}Please wait...",
            font=constants.FONT_BODY_LARGE,
            bg=bg,
            fg=self.theme_manager.get_text_primary()
        )
        loading_label.pack(pady=constants.SPACE_MD)
        
        self.loading_widget = LoadingWidget(loading_frame)
        self.loading_widget.pack()
        self.loading_widget.start()
        
        self.root.update()
        
        # Disable analyze button during analysis
        if hasattr(self, 'analyze_btn'):
            self.analyze_btn.config(state=tk.DISABLED, cursor="wait")
        
        try:
            # Get recommendations
            self.current_recommendations = self.analyzer.analyze_multiple_stocks(symbols)
            
            # Remove loading indicator
            if self.loading_widget:
                self.loading_widget.stop()
                self.loading_widget.destroy()
            loading_frame.destroy()
            
            if not self.current_recommendations:
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, "No recommendations found. Please check the stock symbols and try again.")
                show_notification(self.root, "No recommendations were generated. Please verify the stock symbols are correct.", "warning")
                return
            
            # Populate tree
            for rec in self.current_recommendations:
                stock = rec.stock
                
                item = self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        stock.symbol,
                        stock.name[:constants.NAME_TRUNCATE_LENGTH] + "..." if len(stock.name) > constants.NAME_TRUNCATE_LENGTH else stock.name,
                        f"${stock.current_price:.2f}",
                        f"{stock.price_change_percent:+.2f}%",
                        rec.recommendation_type.value,
                        f"{rec.confidence_score:.1%}",
                        f"${rec.target_price:.2f}" if rec.target_price else constants.DEFAULT_NA_VALUE
                    ),
                    tags=(rec.recommendation_type.value,)
                )
            
            # Configure tags for colors
            for rec_type, color in constants.RECOMMENDATION_COLORS.items():
                self.tree.tag_configure(rec_type, background=color)
            
            # Update dashboard
            self.update_dashboard()
            
            # Update details
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, constants.MESSAGE_ANALYSIS_COMPLETE.format(count=len(self.current_recommendations)))
            self.details_text.insert(tk.END, constants.MESSAGE_CLICK_FOR_DETAILS)
            
            # Show success notification
            show_notification(self.root, f"Analysis complete! Found {len(self.current_recommendations)} recommendations.", "success")
        
        except Exception as e:
            # Remove loading indicator
            if self.loading_widget:
                self.loading_widget.stop()
                self.loading_widget.destroy()
            loading_frame.destroy()
            
            error_msg = f"Error analyzing stocks: {str(e)}"
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Error: {error_msg}\n\nPlease check your internet connection and try again.")
            show_notification(self.root, f"Analysis failed: {error_msg}", "error")
        
        finally:
            # Re-enable analyze button
            if hasattr(self, 'analyze_btn'):
                self.analyze_btn.config(state=tk.NORMAL, cursor="hand2")
    
    def clear_selection(self):
        """Clear current selection"""
        self.tree.selection_remove(self.tree.selection())
        self.selected_recommendation = None
    
    def on_select(self, event):
        """Handle tree selection event"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        symbol = item['values'][0]
        
        # Find the recommendation from current recommendations
        rec = None
        for r in self.current_recommendations:
            if r.stock.symbol == symbol:
                rec = r
                break
        
        if rec:
            self.selected_recommendation = rec
            self.display_recommendation_details(rec)
            # Trigger chart and news updates (will be implemented later)
            self.update_charts_tab(rec)
            self.update_news_tab(rec)
            self.update_analysis_tab(rec)
    
    def display_recommendation_details(self, rec: Recommendation):
        """Display detailed recommendation information"""
        stock = rec.stock
        self.details_text.delete(1.0, tk.END)
        
        market_cap_str = f"${stock.market_cap/1e9:.2f}B" if stock.market_cap else constants.DEFAULT_NA_VALUE
        pe_ratio_str = f"{stock.pe_ratio:.2f}" if stock.pe_ratio else constants.DEFAULT_NA_VALUE
        dividend_yield_str = f"{stock.dividend_yield*100:.2f}%" if stock.dividend_yield else constants.DEFAULT_NA_VALUE
        target_price_str = f"${rec.target_price:.2f}" if rec.target_price else constants.DEFAULT_NA_VALUE
        
        details = f"""
{constants.DETAILS_SEPARATOR}
{constants.TEXT_DETAILS_HEADER}
{constants.DETAILS_SEPARATOR}

Stock: {stock.symbol} - {stock.name}
Current Price: ${stock.current_price:.2f}
Previous Close: ${stock.previous_close:.2f}
Price Change: ${stock.price_change:.2f} ({stock.price_change_percent:+.2f}%)
Volume: {stock.volume:,}

Recommendation: {rec.recommendation_type.value}
Confidence Score: {rec.confidence_score:.1%}
Target Price: {target_price_str}

Reasoning:
{rec.reasoning}

Additional Metrics:
- Market Cap: {market_cap_str}
- P/E Ratio: {pe_ratio_str}
- Dividend Yield: {dividend_yield_str}
"""
        self.details_text.insert(tk.END, details)
    
    def update_charts_tab(self, rec: Recommendation):
        """Update charts tab when stock is selected"""
        if rec and self.chart_controls:
            self.chart_controls.set_symbol(rec.stock.symbol)
    
    def update_news_tab(self, rec: Recommendation):
        """Update news tab when stock is selected"""
        if not rec:
            print("update_news_tab: No recommendation provided")
            return
            
        if not self.news_panel:
            print("update_news_tab: News panel not initialized")
            return
        
        print(f"update_news_tab: Updating news for {rec.stock.symbol}")
        print(f"update_news_tab: Articles in recommendation: {len(rec.articles) if rec.articles else 0}")
        print(f"update_news_tab: Articles: {rec.articles}")
        # Always try to fetch fresh news, but use stored articles if available and not empty
        articles_to_display = []
        
        # First, try to use articles from recommendation
        if rec.articles and len(rec.articles) > 0:
            print(f"Using {len(rec.articles)} articles from recommendation")
            articles_to_display = rec.articles
        else:
            # Fetch news if not already stored or if stored articles are empty
            print(f"Fetching fresh news for {rec.stock.symbol}")
            if self.news_fetcher:
                try:
                    articles_to_display = self.news_fetcher.fetch_all_sources(
                        rec.stock.symbol,
                        max_articles_per_source=50,
                        days_back=30,
                        include_related_market=True
                    )
                    print(f"Fetched {len(articles_to_display)} articles from news fetcher")
                    # Update the recommendation with fetched articles for future use
                    rec.articles = articles_to_display
                except Exception as e:
                    print(f"Error fetching news: {e}")
                    import traceback
                    traceback.print_exc()
                    articles_to_display = []
            else:
                print("News fetcher not available")
                articles_to_display = []
        
        # Display articles
        print(f"Displaying {len(articles_to_display)} articles in news panel")
        self.news_panel.display_articles(articles_to_display)
    
    def update_analysis_tab(self, rec: Recommendation):
        """Update analysis tab with expandable sections"""
        if not rec or not hasattr(self, 'analysis_frame'):
            return
        
        # Clear existing content
        for widget in self.analysis_frame.winfo_children():
            widget.destroy()
        
        # Parse reasoning to extract sections
        reasoning = rec.reasoning
        sections = self.parse_reasoning_sections(reasoning)
        
        # Create expandable sections
        for section_name, section_content in sections.items():
            self.create_expandable_section(section_name, section_content)
        
        # Update canvas scroll region
        self.analysis_canvas.update_idletasks()
        self.analysis_canvas.configure(scrollregion=self.analysis_canvas.bbox("all"))
    
    def parse_reasoning_sections(self, reasoning: str) -> dict:
        """Parse reasoning text into sections"""
        sections = {}
        
        # Split by common section markers
        section_markers = [
            "Price Analysis:", "Volume Analysis:", "News Analysis:",
            "Technical Strategy Analysis:", "Period-Based Analysis:",
            "Support/Resistance Analysis:", "Fundamental Analysis:",
            "Momentum Analysis:", "Volatility Analysis:"
        ]
        
        current_section = "Overview"
        current_content = []
        
        lines = reasoning.split(";")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts with a section marker
            found_section = False
            for marker in section_markers:
                if line.startswith(marker):
                    # Save previous section
                    if current_content:
                        sections[current_section] = " | ".join(current_content)
                    # Start new section
                    current_section = marker.replace(":", "")
                    current_content = [line.replace(marker, "").strip()]
                    found_section = True
                    break
            
            if not found_section:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = " | ".join(current_content)
        
        # If no sections found, put everything in Overview
        if not sections:
            sections["Overview"] = reasoning
        
        return sections
    
    def create_expandable_section(self, title: str, content: str):
        """Create an expandable section with modern styling"""
        bg = self.theme_manager.get_background()
        surface = self.theme_manager.get_surface()
        text_primary = self.theme_manager.get_text_primary()
        text_secondary = self.theme_manager.get_text_secondary()
        border = self.theme_manager.get_border()
        
        # Section header (clickable)
        header_frame = tk.Frame(self.analysis_frame, bg=surface, relief=tk.FLAT, bd=1, highlightbackground=border)
        header_frame.pack(fill=tk.X, padx=constants.SPACE_MD, pady=constants.SPACE_SM)
        
        # Expand/collapse indicator
        indicator = tk.Label(
            header_frame,
            text=constants.ICON_EXPAND,
            font=constants.FONT_BODY,
            bg=surface,
            fg=text_secondary,
            cursor="hand2"
        )
        indicator.pack(side=tk.LEFT, padx=constants.SPACE_SM)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text=title,
            font=constants.FONT_LABEL_BOLD,
            bg=surface,
            fg=text_primary,
            cursor="hand2"
        )
        title_label.pack(side=tk.LEFT, padx=constants.SPACE_SM)
        
        # Content frame (initially hidden)
        content_frame = tk.Frame(self.analysis_frame, bg=bg, relief=tk.FLAT, bd=0)
        
        content_text = tk.Label(
            content_frame,
            text=content,
            font=constants.FONT_BODY,
            bg=bg,
            fg=text_primary,
            wraplength=1000,
            justify=tk.LEFT,
            anchor=tk.W
        )
        content_text.pack(anchor=tk.W, padx=constants.SPACE_LG, pady=constants.SPACE_MD)
        
        # Initially hide content
        content_frame.pack_forget()
        is_expanded = [False]
        
        def toggle_section():
            if is_expanded[0]:
                content_frame.pack_forget()
                indicator.config(text=constants.ICON_EXPAND)
                is_expanded[0] = False
            else:
                content_frame.pack(fill=tk.X, padx=constants.SPACE_MD, pady=(0, constants.SPACE_SM), before=header_frame)
                indicator.config(text=constants.ICON_COLLAPSE)
                is_expanded[0] = True
            self.analysis_canvas.update_idletasks()
            self.analysis_canvas.configure(scrollregion=self.analysis_canvas.bbox("all"))
        
        title_label.bind("<Button-1>", lambda e: toggle_section())
        indicator.bind("<Button-1>", lambda e: toggle_section())
        
        # Hover effects
        def on_enter(e):
            header_frame.config(bg=self.theme_manager.get_surface())
        def on_leave(e):
            header_frame.config(bg=surface)
        header_frame.bind("<Enter>", on_enter)
        header_frame.bind("<Leave>", on_leave)
    
    def export_results(self):
        """Export analysis results to CSV or JSON"""
        if not self.current_recommendations:
            messagebox.showwarning("No Data", "No results to export. Please analyze stocks first.")
            return
        
        # Ask user for file format
        file_types = [
            ("CSV files", "*.csv"),
            ("JSON files", "*.json"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=file_types,
            title="Export Analysis Results"
        )
        
        if not filename:
            return
        
        try:
            if filename.endswith('.csv'):
                self.export_to_csv(filename)
            elif filename.endswith('.json'):
                self.export_to_json(filename)
            else:
                messagebox.showerror("Invalid Format", "Please select CSV or JSON format.")
                return
            
            messagebox.showinfo("Export Successful", f"Results exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting results: {str(e)}")
    
    def export_to_csv(self, filename: str):
        """Export results to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Header
            writer.writerow([
                'Symbol', 'Name', 'Price', 'Change %', 'Recommendation',
                'Confidence', 'Target Price', 'Market Cap', 'P/E Ratio',
                'Dividend Yield', 'Volume', 'Reasoning'
            ])
            # Data
            for rec in self.current_recommendations:
                stock = rec.stock
                market_cap = f"${stock.market_cap/1e9:.2f}B" if stock.market_cap else "N/A"
                pe_ratio = f"{stock.pe_ratio:.2f}" if stock.pe_ratio else "N/A"
                div_yield = f"{stock.dividend_yield*100:.2f}%" if stock.dividend_yield else "N/A"
                target_price = f"${rec.target_price:.2f}" if rec.target_price else "N/A"
                
                writer.writerow([
                    stock.symbol,
                    stock.name,
                    f"${stock.current_price:.2f}",
                    f"{stock.price_change_percent:+.2f}%",
                    rec.recommendation_type.value,
                    f"{rec.confidence_score:.1%}",
                    target_price,
                    market_cap,
                    pe_ratio,
                    div_yield,
                    stock.volume,
                    rec.reasoning.replace('\n', ' ').replace(';', ' | ')
                ])
    
    def export_to_json(self, filename: str):
        """Export results to JSON"""
        data = {
            'export_date': str(datetime.now()),
            'total_stocks': len(self.current_recommendations),
            'recommendations': []
        }
        
        for rec in self.current_recommendations:
            stock = rec.stock
            data['recommendations'].append({
                'symbol': stock.symbol,
                'name': stock.name,
                'current_price': stock.current_price,
                'previous_close': stock.previous_close,
                'price_change': stock.price_change,
                'price_change_percent': stock.price_change_percent,
                'volume': stock.volume,
                'market_cap': stock.market_cap,
                'pe_ratio': stock.pe_ratio,
                'dividend_yield': stock.dividend_yield,
                'recommendation': rec.recommendation_type.value,
                'confidence_score': rec.confidence_score,
                'target_price': rec.target_price,
                'reasoning': rec.reasoning
            })
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    def update_dashboard(self):
        """Update summary dashboard with aggregate statistics using modern stat cards"""
        if not hasattr(self, 'dashboard_frame') or not self.current_recommendations:
            return
        
        # Clear existing dashboard widgets
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        
        # Calculate statistics
        total_stocks = len(self.current_recommendations)
        avg_confidence = sum(r.confidence_score for r in self.current_recommendations) / total_stocks if total_stocks > 0 else 0
        
        # Count recommendations
        rec_counts = {}
        for rec in self.current_recommendations:
            rec_type = rec.recommendation_type.value
            rec_counts[rec_type] = rec_counts.get(rec_type, 0) + 1
        
        buy_count = rec_counts.get("STRONG BUY", 0) + rec_counts.get("BUY", 0)
        sell_count = rec_counts.get("STRONG SELL", 0) + rec_counts.get("SELL", 0)
        
        # Create modern stat cards
        stats = [
            StatCard(
                self.dashboard_frame,
                "Total Stocks",
                str(total_stocks),
                icon=constants.ICON_CHART
            ),
            StatCard(
                self.dashboard_frame,
                "Avg Confidence",
                f"{avg_confidence:.1%}",
                icon=constants.ICON_ANALYSIS
            ),
            StatCard(
                self.dashboard_frame,
                "Buy Signals",
                str(buy_count),
                icon=constants.ICON_UP,
                trend="up" if buy_count > 0 else None
            ),
            StatCard(
                self.dashboard_frame,
                "Sell Signals",
                str(sell_count),
                icon=constants.ICON_DOWN,
                trend="down" if sell_count > 0 else None
            )
        ]
        
        for i, stat_card in enumerate(stats):
            stat_card.grid(row=0, column=i, padx=constants.SPACE_SM, sticky="ew")
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def view_selected_details(self):
        """View details of selected item"""
        selection = self.tree.selection()
        if selection:
            self.on_select(None)
    
    def export_selected(self):
        """Export selected stock to CSV"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a stock to export.")
            return
        
        item = self.tree.item(selection[0])
        symbol = item['values'][0]
        
        # Find recommendation
        rec = None
        for r in self.current_recommendations:
            if r.stock.symbol == symbol:
                rec = r
                break
        
        if not rec:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title=f"Export {symbol}",
            initialfile=f"{symbol}_analysis.csv"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Field', 'Value'])
                    stock = rec.stock
                    writer.writerow(['Symbol', stock.symbol])
                    writer.writerow(['Name', stock.name])
                    writer.writerow(['Price', f"${stock.current_price:.2f}"])
                    writer.writerow(['Change %', f"{stock.price_change_percent:+.2f}%"])
                    writer.writerow(['Recommendation', rec.recommendation_type.value])
                    writer.writerow(['Confidence', f"{rec.confidence_score:.1%}"])
                    writer.writerow(['Target Price', f"${rec.target_price:.2f}" if rec.target_price else "N/A"])
                    writer.writerow(['Reasoning', rec.reasoning])
                
                messagebox.showinfo("Export Successful", f"{symbol} data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting: {str(e)}")
    
    def sort_treeview(self, col):
        """Sort treeview by column"""
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Determine sort type
        try:
            # Try numeric sort
            items.sort(key=lambda t: float(t[0].replace('$', '').replace('%', '').replace(',', '')), reverse=self.sort_reverse if col == self.sort_column else False)
        except ValueError:
            # String sort
            items.sort(key=lambda t: t[0], reverse=self.sort_reverse if col == self.sort_column else False)
        
        # Rearrange items
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        # Toggle reverse if same column
        if col == self.sort_column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        
        # Update heading to show sort direction
        for c in constants.TREEVIEW_COLUMNS:
            heading_text = c
            if c == col:
                heading_text += " ↑" if not self.sort_reverse else " ↓"
            self.tree.heading(c, text=heading_text)
    
    def apply_filters(self):
        """Apply filters to treeview"""
        filter_value = self.filter_var.get()
        
        if filter_value == "All":
            # Show all items
            for item in self.tree.get_children():
                self.tree.item(item, tags=(self.tree.item(item)['tags'][0],))
        else:
            # Hide items that don't match
            for item in self.tree.get_children():
                tags = self.tree.item(item)['tags']
                if tags and tags[0] == filter_value:
                    self.tree.item(item, tags=tags)
                else:
                    self.tree.item(item, tags=('hidden',))
                    self.tree.detach(item)
