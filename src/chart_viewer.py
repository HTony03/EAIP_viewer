#!/usr/bin/env python3
"""
Chart Viewer - GUI component for displaying aviation charts
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
import subprocess
import platform
from typing import Optional, Dict, Any, List


class ChartViewer:
    def __init__(self, parent_frame: ttk.Frame, eaip_handler):
        self.parent_frame = parent_frame
        self.eaip_handler = eaip_handler
        self.current_chart: Optional[Dict[str, Any]] = None
        
        self.setup_ui()
        self.load_chart_list()
        
    def setup_ui(self):
        """Setup the chart viewer UI"""
        # Create horizontal paned window
        paned = ttk.PanedWindow(self.parent_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Chart list
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Search frame
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        # Chart tree view
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.chart_tree = ttk.Treeview(tree_frame, columns=('Type', 'Size'), show='tree headings')
        self.chart_tree.heading('#0', text='Chart Name')
        self.chart_tree.heading('Type', text='Type')
        self.chart_tree.heading('Size', text='Size')
        
        # Configure column widths
        self.chart_tree.column('#0', width=200)
        self.chart_tree.column('Type', width=60)
        self.chart_tree.column('Size', width=80)
        
        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.chart_tree.yview)
        self.chart_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.chart_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click event
        self.chart_tree.bind('<Double-1>', self.on_chart_select)
        
        # Right panel - Chart display
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)
        
        # Chart info frame
        info_frame = ttk.Frame(right_frame)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.chart_info_var = tk.StringVar()
        self.chart_info_var.set("Select a chart to view")
        ttk.Label(info_frame, textvariable=self.chart_info_var).pack(side=tk.LEFT)
        
        # Buttons frame
        button_frame = ttk.Frame(info_frame)
        button_frame.pack(side=tk.RIGHT)
        
        self.open_button = ttk.Button(button_frame, text="Open in External Viewer", 
                                     command=self.open_external, state=tk.DISABLED)
        self.open_button.pack(side=tk.RIGHT, padx=5)
        
        # Chart display area
        display_frame = ttk.Frame(right_frame)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas for image display
        self.canvas = tk.Canvas(display_frame, bg='white')
        
        # Scrollbars for canvas
        v_scroll = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scroll = ttk.Scrollbar(display_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Pack scrollbars and canvas
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind canvas events for zooming
        self.canvas.bind('<MouseWheel>', self.on_mouse_wheel)
        self.canvas.bind('<Button-4>', self.on_mouse_wheel)
        self.canvas.bind('<Button-5>', self.on_mouse_wheel)
        
        # Image variables
        self.image = None
        self.photo_image = None
        self.zoom_factor = 1.0
        
    def load_chart_list(self):
        """Load charts into the tree view"""
        # Clear existing items
        for item in self.chart_tree.get_children():
            self.chart_tree.delete(item)
            
        # Get charts by category
        charts_by_category = self.eaip_handler.get_charts_by_category()
        
        for category, charts in charts_by_category.items():
            # Add category as parent node
            category_id = self.chart_tree.insert('', 'end', text=category, values=('', ''))
            
            # Add charts under category
            for chart in charts:
                size_kb = chart['size'] // 1024
                size_str = f"{size_kb} KB" if size_kb < 1024 else f"{size_kb // 1024} MB"
                
                chart_id = self.chart_tree.insert(
                    category_id, 'end', 
                    text=chart['name'],
                    values=(chart['type'].upper(), size_str),
                    tags=('chart',)
                )
                
                # Store chart data with the tree item
                self.chart_tree.set(chart_id, 'chart_data', chart)
                
        # Expand all categories
        for item in self.chart_tree.get_children():
            self.chart_tree.item(item, open=True)
            
    def on_search(self, event=None):
        """Handle search input"""
        query = self.search_var.get().strip()
        
        if not query:
            self.load_chart_list()
            return
            
        # Clear existing items
        for item in self.chart_tree.get_children():
            self.chart_tree.delete(item)
            
        # Search charts
        matching_charts = self.eaip_handler.search_charts(query)
        
        if matching_charts:
            # Add search results
            search_id = self.chart_tree.insert('', 'end', text=f"Search Results ({len(matching_charts)})", values=('', ''))
            
            for chart in matching_charts:
                size_kb = chart['size'] // 1024
                size_str = f"{size_kb} KB" if size_kb < 1024 else f"{size_kb // 1024} MB"
                
                chart_id = self.chart_tree.insert(
                    search_id, 'end',
                    text=chart['name'],
                    values=(chart['type'].upper(), size_str),
                    tags=('chart',)
                )
                
                self.chart_tree.set(chart_id, 'chart_data', chart)
                
            self.chart_tree.item(search_id, open=True)
            
    def on_chart_select(self, event=None):
        """Handle chart selection"""
        selection = self.chart_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        tags = self.chart_tree.item(item, 'tags')
        
        if 'chart' in tags:
            # Get chart data
            chart_data = self.chart_tree.set(item, 'chart_data')
            if chart_data:
                self.display_chart(chart_data)
                
    def display_chart(self, chart: Dict[str, Any]):
        """Display the selected chart"""
        try:
            self.current_chart = chart
            chart_path = self.eaip_handler.get_chart_path(chart)
            
            # Update info
            info_text = f"Chart: {chart['name']} | Type: {chart['type'].upper()} | Size: {chart['size'] // 1024} KB"
            self.chart_info_var.set(info_text)
            
            # Enable external viewer button
            self.open_button.config(state=tk.NORMAL)
            
            # Try to display image if it's an image file
            if chart['type'].lower() in ['png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff']:
                self.display_image(chart_path)
            else:
                # For PDFs and other formats, show placeholder
                self.show_placeholder(f"Chart: {chart['name']}\\nType: {chart['type'].upper()}\\n\\nDouble-click 'Open in External Viewer' to view this chart")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying chart: {str(e)}")
            
    def display_image(self, image_path: str):
        """Display an image in the canvas"""
        try:
            # Load image
            self.image = Image.open(image_path)
            self.zoom_factor = 1.0
            
            # Calculate initial zoom to fit canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                img_width, img_height = self.image.size
                zoom_x = canvas_width / img_width
                zoom_y = canvas_height / img_height
                self.zoom_factor = min(zoom_x, zoom_y, 1.0)  # Don't zoom in beyond 100%
                
            self.update_image_display()
            
        except Exception as e:
            self.show_placeholder(f"Error loading image: {str(e)}")
            
    def update_image_display(self):
        """Update the image display with current zoom"""
        if not self.image:
            return
            
        try:
            # Calculate new size
            orig_width, orig_height = self.image.size
            new_width = int(orig_width * self.zoom_factor)
            new_height = int(orig_height * self.zoom_factor)
            
            # Resize image
            resized_image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(resized_image)
            
            # Clear canvas and add image
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
            
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            self.show_placeholder(f"Error displaying image: {str(e)}")
            
    def show_placeholder(self, text: str):
        """Show placeholder text in canvas"""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=text,
            justify=tk.CENTER,
            font=('Arial', 12)
        )
        
    def on_mouse_wheel(self, event):
        """Handle mouse wheel for zooming"""
        if not self.image:
            return
            
        # Determine zoom direction
        if event.delta > 0 or event.num == 4:
            zoom_delta = 1.1
        else:
            zoom_delta = 0.9
            
        # Apply zoom
        new_zoom = self.zoom_factor * zoom_delta
        
        # Limit zoom range
        if 0.1 <= new_zoom <= 5.0:
            self.zoom_factor = new_zoom
            self.update_image_display()
            
    def open_external(self):
        """Open chart in external viewer"""
        if not self.current_chart:
            return
            
        try:
            chart_path = self.eaip_handler.get_chart_path(self.current_chart)
            
            # Open with default system application
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', chart_path])
            elif platform.system() == 'Windows':  # Windows
                os.startfile(chart_path)
            else:  # Linux
                subprocess.call(['xdg-open', chart_path])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error opening chart externally: {str(e)}")