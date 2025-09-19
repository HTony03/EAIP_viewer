#!/usr/bin/env python3
"""
Chart Viewer - GUI component for displaying aviation charts using PySide6
"""

import os
import subprocess
import platform
from typing import Optional, Dict, Any, List

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
                               QTreeWidget, QTreeWidgetItem, QLineEdit, QLabel, 
                               QPushButton, QScrollArea, QMessageBox, QFrame)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QPainter, QFont

from PIL import Image


class ImageViewer(QLabel):
    """Custom image viewer widget with zoom capabilities"""
    
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("QLabel { background-color: white; }")
        self.setMinimumSize(400, 300)
        
        # Image properties
        self.original_pixmap = None
        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        
    def set_image(self, image_path: str):
        """Load and display an image"""
        try:
            # Load image using PIL first to handle various formats
            pil_image = Image.open(image_path)
            
            # Convert PIL image to Qt format
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
                
            # Convert to bytes and then to QPixmap
            import io
            byte_array = io.BytesIO()
            pil_image.save(byte_array, format='PNG')
            byte_array.seek(0)
            
            self.original_pixmap = QPixmap()
            self.original_pixmap.loadFromData(byte_array.getvalue())
            
            # Reset zoom and display
            self.zoom_factor = 1.0
            self.fit_to_window()
            
        except Exception as e:
            self.show_placeholder(f"Error loading image: {str(e)}")
            
    def show_placeholder(self, text: str):
        """Show placeholder text"""
        self.original_pixmap = None
        self.setText(text)
        
    def fit_to_window(self):
        """Fit image to current widget size"""
        if not self.original_pixmap:
            return
            
        # Calculate zoom to fit widget
        widget_size = self.size()
        pixmap_size = self.original_pixmap.size()
        
        if widget_size.width() > 0 and widget_size.height() > 0:
            zoom_x = widget_size.width() / pixmap_size.width()
            zoom_y = widget_size.height() / pixmap_size.height()
            self.zoom_factor = min(zoom_x, zoom_y, 1.0)  # Don't zoom in beyond 100%
            
        self.update_display()
        
    def zoom_in(self):
        """Zoom in by 10%"""
        new_zoom = self.zoom_factor * 1.1
        if new_zoom <= self.max_zoom:
            self.zoom_factor = new_zoom
            self.update_display()
            
    def zoom_out(self):
        """Zoom out by 10%"""
        new_zoom = self.zoom_factor * 0.9
        if new_zoom >= self.min_zoom:
            self.zoom_factor = new_zoom
            self.update_display()
            
    def update_display(self):
        """Update the displayed image with current zoom"""
        if not self.original_pixmap:
            return
            
        # Scale pixmap
        new_size = self.original_pixmap.size() * self.zoom_factor
        scaled_pixmap = self.original_pixmap.scaled(
            new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        
        self.setPixmap(scaled_pixmap)
        self.setText("")  # Clear any text
        
    def wheelEvent(self, event):
        """Handle mouse wheel for zooming"""
        if self.original_pixmap:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        super().wheelEvent(event)
        
    def resizeEvent(self, event):
        """Handle widget resize"""
        if self.original_pixmap and event.oldSize().width() > 0:
            # Only auto-fit if we're at the initial zoom
            if abs(self.zoom_factor - 1.0) < 0.1:
                self.fit_to_window()
        super().resizeEvent(event)


class ChartViewer(QWidget):
    """Main chart viewer widget"""
    
    def __init__(self, eaip_handler):
        super().__init__()
        self.eaip_handler = eaip_handler
        self.current_chart: Optional[Dict[str, Any]] = None
        
        self.setup_ui()
        self.load_chart_list()
        
    def setup_ui(self):
        """Setup the chart viewer UI"""
        # Main horizontal layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Chart list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(350)
        left_panel.setMinimumWidth(250)
        
        # Search section
        search_label = QLabel("Search:")
        left_layout.addWidget(search_label)
        
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Type to search charts...")
        self.search_entry.textChanged.connect(self.on_search)
        left_layout.addWidget(self.search_entry)
        
        # Chart tree
        self.chart_tree = QTreeWidget()
        self.chart_tree.setHeaderLabels(["Chart Name", "Type", "Size"])
        self.chart_tree.setColumnWidth(0, 200)
        self.chart_tree.setColumnWidth(1, 60)
        self.chart_tree.setColumnWidth(2, 80)
        self.chart_tree.itemDoubleClicked.connect(self.on_chart_select)
        left_layout.addWidget(self.chart_tree)
        
        splitter.addWidget(left_panel)
        
        # Right panel - Chart display
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        
        # Chart info and controls
        info_layout = QHBoxLayout()
        
        self.chart_info_label = QLabel("Select a chart to view")
        info_layout.addWidget(self.chart_info_label)
        
        info_layout.addStretch()
        
        self.external_button = QPushButton("Open in External Viewer")
        self.external_button.setEnabled(False)
        self.external_button.clicked.connect(self.open_external)
        info_layout.addWidget(self.external_button)
        
        right_layout.addLayout(info_layout)
        
        # Image viewer in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(Qt.AlignCenter)
        
        self.image_viewer = ImageViewer()
        scroll_area.setWidget(self.image_viewer)
        right_layout.addWidget(scroll_area)
        
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([300, 900])
        
    def load_chart_list(self):
        """Load charts into the tree view"""
        self.chart_tree.clear()
        
        # Get charts by category
        charts_by_category = self.eaip_handler.get_charts_by_category()
        
        for category, charts in charts_by_category.items():
            # Add category as parent item
            category_item = QTreeWidgetItem([category, "", ""])
            category_item.setFont(0, QFont("", -1, QFont.Bold))
            self.chart_tree.addTopLevelItem(category_item)
            
            # Add charts under category
            for chart in charts:
                size_kb = chart['size'] // 1024
                size_str = f"{size_kb} KB" if size_kb < 1024 else f"{size_kb // 1024} MB"
                
                chart_item = QTreeWidgetItem([
                    chart['name'],
                    chart['type'].upper(),
                    size_str
                ])
                
                # Store chart data
                chart_item.setData(0, Qt.UserRole, chart)
                category_item.addChild(chart_item)
                
        # Expand all categories
        self.chart_tree.expandAll()
        
    def on_search(self):
        """Handle search input"""
        query = self.search_entry.text().strip()
        
        if not query:
            self.load_chart_list()
            return
            
        # Clear tree
        self.chart_tree.clear()
        
        # Search charts
        matching_charts = self.eaip_handler.search_charts(query)
        
        if matching_charts:
            # Add search results
            search_item = QTreeWidgetItem([f"Search Results ({len(matching_charts)})", "", ""])
            search_item.setFont(0, QFont("", -1, QFont.Bold))
            self.chart_tree.addTopLevelItem(search_item)
            
            for chart in matching_charts:
                size_kb = chart['size'] // 1024
                size_str = f"{size_kb} KB" if size_kb < 1024 else f"{size_kb // 1024} MB"
                
                chart_item = QTreeWidgetItem([
                    chart['name'],
                    chart['type'].upper(),
                    size_str
                ])
                
                chart_item.setData(0, Qt.UserRole, chart)
                search_item.addChild(chart_item)
                
            self.chart_tree.expandAll()
            
    def on_chart_select(self, item, column):
        """Handle chart selection"""
        chart_data = item.data(0, Qt.UserRole)
        if chart_data:
            self.display_chart(chart_data)
            
    def display_chart(self, chart: Dict[str, Any]):
        """Display the selected chart"""
        try:
            self.current_chart = chart
            chart_path = self.eaip_handler.get_chart_path(chart)
            
            # Update info
            info_text = f"Chart: {chart['name']} | Type: {chart['type'].upper()} | Size: {chart['size'] // 1024} KB"
            self.chart_info_label.setText(info_text)
            
            # Enable external viewer button
            self.external_button.setEnabled(True)
            
            # Try to display image if it's an image file
            if chart['type'].lower() in ['png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff']:
                self.image_viewer.set_image(chart_path)
            else:
                # For PDFs and other formats, show placeholder
                self.image_viewer.show_placeholder(
                    f"Chart: {chart['name']}\nType: {chart['type'].upper()}\n\n"
                    f"Click 'Open in External Viewer' to view this chart"
                )
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error displaying chart: {str(e)}")
            
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
            QMessageBox.critical(self, "Error", f"Error opening chart externally: {str(e)}")