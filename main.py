from ui.main_window import MainWindow
from services.data_fetcher import DataFetcher
from services.analyzer import StockAnalyzer
import tkinter as tk

class BrokerApp:
    """Main application class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.data_fetcher = DataFetcher()
        self.analyzer = StockAnalyzer(self.data_fetcher)
        self.main_window = MainWindow(self.root, self.analyzer)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BrokerApp()
    app.run()

