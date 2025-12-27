"""News panel component for displaying news articles"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List
from services.news_fetcher import NewsArticle
from ui.constants import (
    BACKGROUND_COLOR, FONT_LABEL, FONT_LABEL_BOLD, COLOR_TEXT_PRIMARY,
    COLOR_POSITIVE, COLOR_NEGATIVE, COLOR_NEUTRAL, PADDING_WIDGET, CARD_PADDING
)
import webbrowser

class NewsPanel(tk.Frame):
    """Panel for displaying news articles"""
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(bg=BACKGROUND_COLOR)
        self.articles = []
        self.create_widgets()
    
    def create_widgets(self):
        """Create news panel widgets"""
        # Header frame with title and refresh button
        header_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        header_frame.pack(fill=tk.X, pady=PADDING_WIDGET)
        
        header = tk.Label(
            header_frame,
            text="Recent News Articles",
            font=("Arial", 14, "bold"),
            bg=BACKGROUND_COLOR,
            fg=COLOR_TEXT_PRIMARY
        )
        header.pack(side=tk.LEFT, padx=PADDING_WIDGET)
        
        # Scrollable frame for articles
        canvas_frame = tk.Frame(self, bg=BACKGROUND_COLOR)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg=BACKGROUND_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BACKGROUND_COLOR)
        
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
    
    def display_articles(self, articles: List[NewsArticle]):
        """Display news articles in the panel"""
        # Ensure articles is a list
        if articles is None:
            articles = []
        elif not isinstance(articles, list):
            articles = list(articles) if hasattr(articles, '__iter__') else []
        
        self.articles = articles
        
        print(f"NewsPanel.display_articles: Received {len(self.articles)} articles")
        if len(self.articles) > 0:
            print(f"NewsPanel.display_articles: First article title: {self.articles[0].title[:50] if self.articles[0].title else 'No title'}")
        
        # Clear existing articles
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.articles or len(self.articles) == 0:
            no_news_label = tk.Label(
                self.scrollable_frame,
                text="No news articles available for this stock.\n\nArticles may not have been fetched during analysis.\nTry analyzing the stock again.",
                font=FONT_LABEL,
                bg=BACKGROUND_COLOR,
                fg=COLOR_NEUTRAL,
                justify=tk.CENTER
            )
            no_news_label.pack(pady=20)
            self.scrollable_frame.update_idletasks()
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            return
        
        # Display each article (limit to 50 for performance)
        article_count = min(len(self.articles), 50)
        print(f"NewsPanel.display_articles: Creating {article_count} article cards")
        for i, article in enumerate(self.articles[:article_count]):
            try:
                self.create_article_card(article, i)
            except Exception as e:
                print(f"Error creating article card {i}: {e}")
                import traceback
                traceback.print_exc()
        
        # Update canvas scroll region after all widgets are created
        self.scrollable_frame.update_idletasks()
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        print(f"NewsPanel.display_articles: Finished displaying articles")
    
    def create_article_card(self, article: NewsArticle, index: int):
        """Create a card for a single article"""
        card = tk.Frame(
            self.scrollable_frame,
            bg="#ffffff",
            relief=tk.RAISED,
            bd=1
        )
        card.pack(fill=tk.X, padx=10, pady=5)
        
        # Store URL for click handlers (fix closure issue)
        article_url = article.url if article.url and article.url.strip() else None
        
        # Date
        date_str = ""
        date_label = None
        if article.published_date:
            try:
                date_str = article.published_date.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = "Date unknown"
        
        if date_str:
            date_label = tk.Label(
                card,
                text=date_str,
                font=("Arial", 9),
                bg="#ffffff",
                fg=COLOR_NEUTRAL,
                cursor="hand2" if article_url else "arrow"
            )
            date_label.pack(anchor=tk.W, padx=CARD_PADDING, pady=(CARD_PADDING, 0))
        
        # Create click handler function that captures the URL properly
        def create_click_handler(url):
            """Create a click handler that properly captures the URL"""
            def handler(event=None):
                try:
                    print(f"Opening article URL: {url}")
                    webbrowser.open(url)
                except Exception as e:
                    print(f"Error opening URL: {e}")
                    import traceback
                    traceback.print_exc()
            return handler
        
        # Title (clickable if URL available) - Make sure title exists
        title_text = article.title if article.title else "No title available"
        if not title_text or title_text.strip() == "":
            title_text = "Untitled Article"
        
        title_label = tk.Label(
            card,
            text=title_text,
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#0066cc" if article_url else COLOR_TEXT_PRIMARY,
            wraplength=800,
            justify=tk.LEFT,
            cursor="hand2" if article_url else "arrow"
        )
        title_label.pack(anchor=tk.W, padx=CARD_PADDING, pady=(2, 0))
        
        # Make entire card and all elements clickable if URL exists
        if article_url:
            click_handler = create_click_handler(article_url)
            
            # Bind click to title label
            title_label.bind("<Button-1>", click_handler)
            title_label.bind("<Enter>", lambda e, lbl=title_label: lbl.config(fg="#0052a3", underline=True))
            title_label.bind("<Leave>", lambda e, lbl=title_label: lbl.config(fg="#0066cc", underline=False))
            
            # Make entire card clickable
            card.bind("<Button-1>", click_handler)
            card.config(cursor="hand2")
            
            # Store click handler for binding to other elements
            card._click_handler = click_handler
        
        # Source
        source_label = tk.Label(
            card,
            text=f"Source: {article.source}",
            font=("Arial", 9),
            bg="#ffffff",
            fg=COLOR_NEUTRAL,
            cursor="hand2" if article_url else "arrow"
        )
        source_label.pack(anchor=tk.W, padx=CARD_PADDING, pady=(2, 0))
        
        # Make source clickable if URL exists
        if article_url and hasattr(card, '_click_handler'):
            source_label.bind("<Button-1>", card._click_handler)
        
        # Summary
        if article.summary and article.summary.strip():
            summary_text = article.summary[:300] + "..." if len(article.summary) > 300 else article.summary
            summary_label = tk.Label(
                card,
                text=summary_text,
                font=("Arial", 10),
                bg="#ffffff",
                fg=COLOR_TEXT_PRIMARY,
                wraplength=800,
                justify=tk.LEFT,
                cursor="hand2" if article_url else "arrow"
            )
            summary_label.pack(anchor=tk.W, padx=CARD_PADDING, pady=(5, CARD_PADDING))
            
            # Make summary clickable if URL exists
            if article_url and hasattr(card, '_click_handler'):
                summary_label.bind("<Button-1>", card._click_handler)
        else:
            # If no summary, add some padding
            tk.Frame(card, height=5, bg="#ffffff").pack()
        
        # Add visual indicator for clickable articles
        if article_url:
            # Add a subtle hover effect to the card
            def on_card_enter(e):
                card.config(bg="#f5f5f5", relief=tk.SUNKEN)
            def on_card_leave(e):
                card.config(bg="#ffffff", relief=tk.RAISED)
            
            card.bind("<Enter>", on_card_enter)
            card.bind("<Leave>", on_card_leave)
            
            # Also make date label clickable if it exists
            if date_label and hasattr(card, '_click_handler'):
                date_label.bind("<Button-1>", card._click_handler)
        
        # Separator
        separator = tk.Frame(card, height=1, bg="#e0e0e0")
        separator.pack(fill=tk.X, padx=CARD_PADDING, pady=(0, CARD_PADDING))

