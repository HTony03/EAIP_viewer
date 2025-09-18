#!/usr/bin/env python3
"""
EAIP Viewer - A local aviation chart viewer for CAAC EAIP
Similar to ChartFox application functionality
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from eaip_handler import EAIPHandler
from chart_viewer import ChartViewer


class EAIPViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EAIP Viewer - CAAC Aviation Charts")
        self.root.geometry("1200x800")
        
        # Initialize handlers
        self.eaip_handler = EAIPHandler()
        self.chart_viewer = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="EAIP Data Source")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(file_frame, text="Select EAIP ZIP File", 
                  command=self.select_zip_file).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="Select EAIP Directory", 
                  command=self.select_directory).pack(side=tk.LEFT, padx=5, pady=5)
        
        self.source_label = ttk.Label(file_frame, text="No EAIP source selected")
        self.source_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Chart viewer frame
        self.viewer_frame = ttk.LabelFrame(main_frame, text="Chart Viewer")
        self.viewer_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select an EAIP source to begin")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def select_zip_file(self):
        """Select an EAIP ZIP file"""
        filetypes = [
            ("ZIP files", "*.zip"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select EAIP ZIP File",
            filetypes=filetypes
        )
        
        if filename:
            self.load_eaip_source(filename, is_zip=True)
            
    def select_directory(self):
        """Select an EAIP directory"""
        dirname = filedialog.askdirectory(
            title="Select EAIP Directory"
        )
        
        if dirname:
            self.load_eaip_source(dirname, is_zip=False)
            
    def load_eaip_source(self, path, is_zip=True):
        """Load EAIP data from the selected source"""
        try:
            self.status_var.set("Loading EAIP data...")
            self.root.update()
            
            success = self.eaip_handler.load_eaip(path, is_zip=is_zip)
            
            if success:
                self.source_label.config(text=f"Loaded: {os.path.basename(path)}")
                self.status_var.set("EAIP data loaded successfully")
                
                # Initialize chart viewer
                self.chart_viewer = ChartViewer(self.viewer_frame, self.eaip_handler)
                self.status_var.set("Ready - EAIP charts available")
            else:
                messagebox.showerror("Error", "Failed to load EAIP data")
                self.status_var.set("Error loading EAIP data")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading EAIP: {str(e)}")
            self.status_var.set("Error loading EAIP data")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = EAIPViewerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()