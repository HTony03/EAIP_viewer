#!/usr/bin/env python3
"""
EAIP Viewer - A local aviation chart viewer for CAAC EAIP
Similar to ChartFox application functionality

Built with PySide6 (Qt6) for modern, cross-platform GUI
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QGroupBox, QPushButton, QLabel, 
                               QStatusBar, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from eaip_handler import EAIPHandler
from chart_viewer import ChartViewer


class EAIPLoadThread(QThread):
    """Thread for loading EAIP data without blocking UI"""
    finished = Signal(bool)
    progress = Signal(str)
    
    def __init__(self, eaip_handler, path, is_zip):
        super().__init__()
        self.eaip_handler = eaip_handler
        self.path = path
        self.is_zip = is_zip
        
    def run(self):
        try:
            self.progress.emit("Loading EAIP data...")
            success = self.eaip_handler.load_eaip(self.path, is_zip=self.is_zip)
            self.finished.emit(success)
        except Exception as e:
            print(f"Error loading EAIP: {e}")
            self.finished.emit(False)


class EAIPViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EAIP Viewer - CAAC Aviation Charts (Qt6)")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize handlers
        self.eaip_handler = EAIPHandler()
        self.chart_viewer = None
        self.load_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # File selection group
        file_group = QGroupBox("EAIP Data Source")
        file_layout = QHBoxLayout()
        
        # File selection buttons
        self.zip_button = QPushButton("Select EAIP ZIP File")
        self.zip_button.clicked.connect(self.select_zip_file)
        file_layout.addWidget(self.zip_button)
        
        self.dir_button = QPushButton("Select EAIP Directory")
        self.dir_button.clicked.connect(self.select_directory)
        file_layout.addWidget(self.dir_button)
        
        # Source label
        self.source_label = QLabel("No EAIP source selected")
        file_layout.addWidget(self.source_label)
        
        file_layout.addStretch()
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # Chart viewer group
        self.viewer_group = QGroupBox("Chart Viewer")
        self.viewer_layout = QVBoxLayout()
        self.viewer_group.setLayout(self.viewer_layout)
        main_layout.addWidget(self.viewer_group)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Select an EAIP source to begin")
        
    def select_zip_file(self):
        """Select an EAIP ZIP file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select EAIP ZIP File",
            "",
            "ZIP files (*.zip);;All files (*.*)"
        )
        
        if filename:
            self.load_eaip_source(filename, is_zip=True)
            
    def select_directory(self):
        """Select an EAIP directory"""
        dirname = QFileDialog.getExistingDirectory(
            self,
            "Select EAIP Directory"
        )
        
        if dirname:
            self.load_eaip_source(dirname, is_zip=False)
            
    def load_eaip_source(self, path, is_zip=True):
        """Load EAIP data from the selected source"""
        try:
            # Disable buttons during loading
            self.zip_button.setEnabled(False)
            self.dir_button.setEnabled(False)
            
            # Start loading thread
            self.load_thread = EAIPLoadThread(self.eaip_handler, path, is_zip)
            self.load_thread.progress.connect(self.update_status)
            self.load_thread.finished.connect(lambda success: self.on_load_finished(success, path))
            self.load_thread.start()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading EAIP: {str(e)}")
            self.status_bar.showMessage("Error loading EAIP data")
            self.zip_button.setEnabled(True)
            self.dir_button.setEnabled(True)
            
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.showMessage(message)
        
    def on_load_finished(self, success, path):
        """Handle completion of EAIP loading"""
        # Re-enable buttons
        self.zip_button.setEnabled(True)
        self.dir_button.setEnabled(True)
        
        if success:
            self.source_label.setText(f"Loaded: {os.path.basename(path)}")
            self.status_bar.showMessage("EAIP data loaded successfully")
            
            # Initialize chart viewer
            if self.chart_viewer:
                # Remove existing chart viewer
                self.viewer_layout.removeWidget(self.chart_viewer)
                self.chart_viewer.deleteLater()
                
            self.chart_viewer = ChartViewer(self.eaip_handler)
            self.viewer_layout.addWidget(self.chart_viewer)
            self.status_bar.showMessage("Ready - EAIP charts available")
        else:
            QMessageBox.critical(self, "Error", "Failed to load EAIP data")
            self.status_bar.showMessage("Error loading EAIP data")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("EAIP Viewer")
    app.setApplicationVersion("2.0")
    app.setApplicationDisplayName("EAIP Viewer - Qt6")
    
    window = EAIPViewerApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()