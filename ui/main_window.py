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
from ui.constants import (
    WINDOW_TITLE, WINDOW_GEOMETRY, BACKGROUND_COLOR,
    FONT_HEADER, FONT_LABEL, FONT_LABEL_BOLD, FONT_ENTRY, FONT_BUTTON, FONT_ANALYZERS_LABEL, FONT_DETAILS,
    COLOR_TEXT_PRIMARY, COLOR_BUTTON_BG, COLOR_BUTTON_FG, COLOR_ANALYZERS_LABEL,
    COLOR_POSITIVE, COLOR_NEGATIVE, COLOR_NEUTRAL,
    RECOMMENDATION_COLORS, RECOMMENDATION_COLOR_DEFAULT,
    TEXT_HEADER, TEXT_SYMBOLS_LABEL, TEXT_BUTTON_ANALYZE, TEXT_DETAILS_LABEL,
    TEXT_ACTIVE_ANALYZERS_PREFIX, TEXT_NO_ANALYZERS, TEXT_DETAILS_HEADER,
    DEFAULT_SYMBOLS, DEFAULT_NA_VALUE,
    TREEVIEW_COLUMNS, TREEVIEW_COLUMN_WIDTH, TREEVIEW_HEIGHT,
    ENTRY_WIDTH, DETAILS_TEXT_WIDTH, DETAILS_TEXT_HEIGHT, NAME_TRUNCATE_LENGTH,
    PADDING_HEADER, PADDING_INPUT, PADDING_WIDGET, PADDING_FRAME,
    PADDING_DETAILS_LABEL, PADDING_DETAILS_TEXT,
    BUTTON_PADX, BUTTON_PADY,
    MESSAGE_WARNING_TITLE, MESSAGE_NO_SYMBOLS, MESSAGE_ANALYZING,
    MESSAGE_ANALYSIS_COMPLETE, MESSAGE_CLICK_FOR_DETAILS,
    DETAILS_SEPARATOR, TAB_NAMES, COMMON_STOCK_SYMBOLS
)

class MainWindow:
    """Main GUI window for the broker application with tabbed interface"""
    
    def __init__(self, root: tk.Tk, analyzer: StockAnalyzer):
        self.root = root
        self.analyzer = analyzer
        self.current_recommendations = []
        self.selected_recommendation = None
        self.chart_data_fetcher = ChartDataFetcher()
        # Initialize news fetcher with API keys from config if available
        try:
            from config import NEWSAPI_KEY, ALPHAVANTAGE_KEY
            self.news_fetcher = NewsFetcher(
                newsapi_key=NEWSAPI_KEY,
                alphavantage_key=ALPHAVANTAGE_KEY
            )
        except:
            self.news_fetcher = NewsFetcher()
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.configure(bg=BACKGROUND_COLOR)
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        """Create and layout all GUI widgets with tabbed interface"""
        # Header
        header = tk.Label(
            self.root,
            text=TEXT_HEADER,
            font=FONT_HEADER,
            bg=BACKGROUND_COLOR,
            fg=COLOR_TEXT_PRIMARY
        )
        header.grid(row=0, column=0, pady=PADDING_HEADER, sticky="ew")
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        input_frame.grid(row=1, column=0, pady=PADDING_INPUT, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        
        tk.Label(
            input_frame,
            text=TEXT_SYMBOLS_LABEL,
            font=FONT_LABEL,
            bg=BACKGROUND_COLOR
        ).grid(row=0, column=0, padx=PADDING_WIDGET, sticky="w")
        
        # Use Combobox for autocomplete
        from ui.constants import COMMON_STOCK_SYMBOLS
        self.symbol_entry = ttk.Combobox(
            input_frame,
            width=ENTRY_WIDTH,
            font=FONT_ENTRY,
            values=COMMON_STOCK_SYMBOLS
        )
        self.symbol_entry.grid(row=0, column=1, padx=PADDING_WIDGET, sticky="ew")
        self.symbol_entry.insert(0, DEFAULT_SYMBOLS)
        self.symbol_entry.bind('<KeyRelease>', self.on_symbol_entry_change)
        
        self.analyze_btn = tk.Button(
            input_frame,
            text=TEXT_BUTTON_ANALYZE,
            command=self.analyze_stocks,
            bg=COLOR_BUTTON_BG,
            fg=COLOR_BUTTON_FG,
            font=FONT_BUTTON,
            padx=BUTTON_PADX,
            pady=BUTTON_PADY
        )
        self.analyze_btn.grid(row=0, column=2, padx=PADDING_WIDGET)
        
        # Add tooltips
        ToolTip(self.symbol_entry, "Enter stock symbols separated by commas. Use autocomplete for suggestions.")
        ToolTip(self.analyze_btn, "Analyze the entered stocks (Press Enter)")
        
        # Active analyzers label
        self.analyzers_label = tk.Label(
            input_frame,
            text="",
            font=FONT_ANALYZERS_LABEL,
            bg=BACKGROUND_COLOR,
            fg=COLOR_ANALYZERS_LABEL
        )
        self.analyzers_label.grid(row=1, column=0, columnspan=3, pady=(PADDING_WIDGET, 0))
        self.update_analyzers_label()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=2, column=0, padx=PADDING_FRAME, pady=PADDING_INPUT, sticky="nsew")
        
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
        
        # Export button
        export_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        export_frame.grid(row=3, column=0, pady=PADDING_INPUT)
        
        export_btn = tk.Button(
            export_frame,
            text="Export Results",
            command=self.export_results,
            bg="#27ae60",
            fg="white",
            font=FONT_BUTTON,
            padx=15,
            pady=5
        )
        export_btn.pack(side=tk.LEFT, padx=PADDING_WIDGET)
        ToolTip(export_btn, "Export analysis results to CSV or JSON (Ctrl+E)")
        
        # Bind keyboard shortcuts
        self.root.bind('<Return>', lambda e: self.analyze_stocks())
        self.root.bind('<Escape>', lambda e: self.clear_selection())
        self.root.bind('<Control-f>', lambda e: self.symbol_entry.focus())
        self.root.bind('<Control-e>', lambda e: self.export_results())
    
    def on_symbol_entry_change(self, event):
        """Handle autocomplete for symbol entry"""
        value = self.symbol_entry.get().upper()
        if value:
            # Filter symbols that start with the entered text
            filtered = [s for s in COMMON_STOCK_SYMBOLS if s.startswith(value)]
            if filtered:
                self.symbol_entry['values'] = filtered
            else:
                self.symbol_entry['values'] = COMMON_STOCK_SYMBOLS
        else:
            self.symbol_entry['values'] = COMMON_STOCK_SYMBOLS
    
    def create_overview_tab(self):
        """Create the Overview tab with results table and details"""
        overview_frame = tk.Frame(self.notebook, bg=BACKGROUND_COLOR)
        self.notebook.add(overview_frame, text=TAB_NAMES[0])
        overview_frame.grid_rowconfigure(2, weight=1)
        overview_frame.grid_columnconfigure(0, weight=1)
        
        # Dashboard frame
        dashboard_frame = tk.Frame(overview_frame, bg=BACKGROUND_COLOR, relief=tk.RAISED, bd=1)
        dashboard_frame.grid(row=0, column=0, padx=PADDING_FRAME, pady=(PADDING_INPUT, 5), sticky="ew")
        dashboard_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.dashboard_frame = dashboard_frame
        
        # Filter frame
        filter_frame = tk.Frame(overview_frame, bg=BACKGROUND_COLOR)
        filter_frame.grid(row=1, column=0, padx=PADDING_FRAME, pady=(5, 0), sticky="ew")
        
        tk.Label(
            filter_frame,
            text="Filter by Recommendation:",
            font=FONT_LABEL,
            bg=BACKGROUND_COLOR
        ).pack(side=tk.LEFT, padx=PADDING_WIDGET)
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"],
            state="readonly",
            width=15
        )
        filter_combo.pack(side=tk.LEFT, padx=PADDING_WIDGET)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())
        
        # Results frame with treeview
        results_frame = tk.Frame(overview_frame, bg=BACKGROUND_COLOR)
        results_frame.grid(row=2, column=0, padx=PADDING_FRAME, pady=PADDING_INPUT, sticky="nsew")
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview for recommendations
        self.tree = ttk.Treeview(results_frame, columns=TREEVIEW_COLUMNS, show="headings", height=TREEVIEW_HEIGHT)
        
        self.sort_column = None
        self.sort_reverse = False
        
        for col in TREEVIEW_COLUMNS:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=TREEVIEW_COLUMN_WIDTH, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Details section
        details_frame = tk.Frame(overview_frame, bg=BACKGROUND_COLOR)
        details_frame.grid(row=3, column=0, padx=PADDING_FRAME, pady=PADDING_INPUT, sticky="ew")
        details_frame.grid_columnconfigure(0, weight=1)
        
        details_label = tk.Label(
            details_frame,
            text=TEXT_DETAILS_LABEL,
            font=FONT_LABEL_BOLD,
            bg=BACKGROUND_COLOR
        )
        details_label.grid(row=0, column=0, pady=PADDING_DETAILS_LABEL, sticky="w")
        
        self.details_text = scrolledtext.ScrolledText(
            details_frame,
            width=DETAILS_TEXT_WIDTH,
            height=DETAILS_TEXT_HEIGHT,
            font=FONT_DETAILS,
            wrap=tk.WORD
        )
        self.details_text.grid(row=1, column=0, sticky="ew")
    
    def create_charts_tab(self):
        """Create the Charts tab with chart widget and controls"""
        charts_frame = tk.Frame(self.notebook, bg=BACKGROUND_COLOR)
        self.notebook.add(charts_frame, text=TAB_NAMES[1])
        charts_frame.grid_rowconfigure(1, weight=1)
        charts_frame.grid_columnconfigure(0, weight=1)
        
        # Chart controls at top
        self.chart_controls = ChartControls(
            charts_frame,
            data_fetcher=self.chart_data_fetcher
        )
        self.chart_controls.grid(row=0, column=0, padx=PADDING_FRAME, pady=PADDING_INPUT, sticky="ew")
        
        # Chart widget
        self.chart_widget = ChartWidget(charts_frame)
        self.chart_widget.grid(row=1, column=0, padx=PADDING_FRAME, pady=PADDING_INPUT, sticky="nsew")
        
        # Connect controls to chart widget
        self.chart_controls.chart_widget = self.chart_widget
        
        # Store reference
        self.charts_frame = charts_frame
    
    def create_analysis_tab(self):
        """Create the Analysis tab with expandable sections"""
        analysis_frame = tk.Frame(self.notebook, bg=BACKGROUND_COLOR)
        self.notebook.add(analysis_frame, text=TAB_NAMES[2])
        analysis_frame.grid_rowconfigure(0, weight=1)
        analysis_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollable frame for analysis sections
        canvas = tk.Canvas(analysis_frame, bg=BACKGROUND_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BACKGROUND_COLOR)
        
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
            font=FONT_LABEL,
            bg=BACKGROUND_COLOR,
            fg=COLOR_ANALYZERS_LABEL
        )
        placeholder.pack(pady=50)
        
        # Store references
        self.analysis_frame = scrollable_frame
        self.analysis_canvas = canvas
    
    def create_news_tab(self):
        """Create the News tab with news panel"""
        news_frame = tk.Frame(self.notebook, bg=BACKGROUND_COLOR)
        self.notebook.add(news_frame, text=TAB_NAMES[3])
        news_frame.grid_rowconfigure(0, weight=1)
        news_frame.grid_columnconfigure(0, weight=1)
        
        # News panel
        self.news_panel = NewsPanel(news_frame)
        self.news_panel.pack(fill=tk.BOTH, expand=True, padx=PADDING_FRAME, pady=PADDING_INPUT)
        
        # Store reference
        self.news_frame = news_frame
    
    def update_analyzers_label(self):
        """Update the label showing active analyzers"""
        active_analyzers = self.analyzer.get_active_analyzers()
        if active_analyzers:
            analyzers_text = f"{TEXT_ACTIVE_ANALYZERS_PREFIX}{', '.join(active_analyzers)}"
            self.analyzers_label.config(text=analyzers_text)
        else:
            self.analyzers_label.config(text=TEXT_NO_ANALYZERS)
    
    def analyze_stocks(self):
        """Analyze stocks and display recommendations"""
        symbols_str = self.symbol_entry.get().strip()
        if not symbols_str:
            messagebox.showwarning(MESSAGE_WARNING_TITLE, MESSAGE_NO_SYMBOLS)
            return
        
        symbols = [s.strip().upper() for s in symbols_str.split(",")]
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.details_text.delete(1.0, tk.END)
        
        # Show loading message with progress
        self.details_text.insert(tk.END, MESSAGE_ANALYZING.format(count=len(symbols)))
        self.details_text.insert(tk.END, "Please wait...\n")
        self.root.update()
        
        # Disable analyze button during analysis
        if hasattr(self, 'analyze_btn'):
            self.analyze_btn.config(state=tk.DISABLED)
        
        try:
            # Get recommendations
            self.current_recommendations = self.analyzer.analyze_multiple_stocks(symbols)
            
            if not self.current_recommendations:
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, "No recommendations found. Please check the stock symbols and try again.")
                messagebox.showinfo("No Results", "No recommendations were generated. Please verify the stock symbols are correct.")
                return
            
            # Populate tree
            for rec in self.current_recommendations:
                stock = rec.stock
                
                item = self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        stock.symbol,
                        stock.name[:NAME_TRUNCATE_LENGTH] + "..." if len(stock.name) > NAME_TRUNCATE_LENGTH else stock.name,
                        f"${stock.current_price:.2f}",
                        f"{stock.price_change_percent:+.2f}%",
                        rec.recommendation_type.value,
                        f"{rec.confidence_score:.1%}",
                        f"${rec.target_price:.2f}" if rec.target_price else DEFAULT_NA_VALUE
                    ),
                    tags=(rec.recommendation_type.value,)
                )
            
            # Configure tags for colors
            for rec_type, color in RECOMMENDATION_COLORS.items():
                self.tree.tag_configure(rec_type, background=color)
            
                # Update dashboard
                self.update_dashboard()
                
                # Update details
                self.details_text.delete(1.0, tk.END)
                self.details_text.insert(tk.END, MESSAGE_ANALYSIS_COMPLETE.format(count=len(self.current_recommendations)))
                self.details_text.insert(tk.END, MESSAGE_CLICK_FOR_DETAILS)
        
        except Exception as e:
            error_msg = f"Error analyzing stocks: {str(e)}"
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, f"Error: {error_msg}\n\nPlease check your internet connection and try again.")
            messagebox.showerror("Analysis Error", f"An error occurred while analyzing stocks:\n\n{error_msg}\n\nPlease try again.")
        
        finally:
            # Re-enable analyze button
            if hasattr(self, 'analyze_btn'):
                self.analyze_btn.config(state=tk.NORMAL)
    
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
        
        market_cap_str = f"${stock.market_cap/1e9:.2f}B" if stock.market_cap else DEFAULT_NA_VALUE
        pe_ratio_str = f"{stock.pe_ratio:.2f}" if stock.pe_ratio else DEFAULT_NA_VALUE
        dividend_yield_str = f"{stock.dividend_yield*100:.2f}%" if stock.dividend_yield else DEFAULT_NA_VALUE
        target_price_str = f"${rec.target_price:.2f}" if rec.target_price else DEFAULT_NA_VALUE
        
        details = f"""
{DETAILS_SEPARATOR}
{TEXT_DETAILS_HEADER}
{DETAILS_SEPARATOR}

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
        """Create an expandable section"""
        # Section header (clickable)
        header_frame = tk.Frame(self.analysis_frame, bg=BACKGROUND_COLOR)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Expand/collapse indicator
        indicator = tk.Label(
            header_frame,
            text="▶",
            font=("Arial", 10),
            bg=BACKGROUND_COLOR,
            fg=COLOR_TEXT_PRIMARY
        )
        indicator.pack(side=tk.LEFT, padx=5)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text=title,
            font=FONT_LABEL_BOLD,
            bg=BACKGROUND_COLOR,
            fg=COLOR_TEXT_PRIMARY,
            cursor="hand2"
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Content frame (initially hidden)
        content_frame = tk.Frame(self.analysis_frame, bg="#f8f8f8", relief=tk.SUNKEN, bd=1)
        content_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        content_text = tk.Label(
            content_frame,
            text=content,
            font=FONT_LABEL,
            bg="#f8f8f8",
            fg=COLOR_TEXT_PRIMARY,
            wraplength=1000,
            justify=tk.LEFT,
            anchor=tk.W
        )
        content_text.pack(anchor=tk.W, padx=15, pady=10)
        
        # Initially hide content
        content_frame.pack_forget()
        is_expanded = [False]
        
        def toggle_section():
            if is_expanded[0]:
                content_frame.pack_forget()
                indicator.config(text="▶")
                is_expanded[0] = False
            else:
                content_frame.pack(fill=tk.X, padx=10, pady=(0, 5), before=header_frame)
                indicator.config(text="▼")
                is_expanded[0] = True
            self.analysis_canvas.update_idletasks()
            self.analysis_canvas.configure(scrollregion=self.analysis_canvas.bbox("all"))
        
        title_label.bind("<Button-1>", lambda e: toggle_section())
        indicator.bind("<Button-1>", lambda e: toggle_section())
    
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
        """Update summary dashboard with aggregate statistics"""
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
        
        # Create dashboard widgets
        stats = [
            ("Total Stocks", str(total_stocks)),
            ("Avg Confidence", f"{avg_confidence:.1%}"),
            ("Buy Signals", str(rec_counts.get("STRONG BUY", 0) + rec_counts.get("BUY", 0))),
            ("Sell Signals", str(rec_counts.get("STRONG SELL", 0) + rec_counts.get("SELL", 0)))
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = tk.Frame(self.dashboard_frame, bg="#ffffff", relief=tk.RAISED, bd=1)
            stat_frame.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            
            tk.Label(
                stat_frame,
                text=label,
                font=("Arial", 9),
                bg="#ffffff",
                fg=COLOR_NEUTRAL
            ).pack()
            
            tk.Label(
                stat_frame,
                text=value,
                font=("Arial", 16, "bold"),
                bg="#ffffff",
                fg=COLOR_TEXT_PRIMARY
            ).pack()
    
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
        for c in TREEVIEW_COLUMNS:
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
