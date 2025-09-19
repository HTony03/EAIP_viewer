#!/usr/bin/env python3
"""
EAIP Handler - Handles loading and processing of EAIP data
Supports both ZIP files and unzipped directories
"""

import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
import xml.etree.ElementTree as ET


class EAIPHandler:
    def __init__(self):
        self.eaip_path: Optional[str] = None
        self.is_zip: bool = False
        self.temp_dir: Optional[str] = None
        self.charts: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}
        
    def load_eaip(self, path: str, is_zip: bool = True) -> bool:
        """Load EAIP data from ZIP file or directory"""
        try:
            self.cleanup()  # Clean up any previous data
            
            self.eaip_path = path
            self.is_zip = is_zip
            
            if is_zip:
                return self._load_from_zip(path)
            else:
                return self._load_from_directory(path)
                
        except Exception as e:
            print(f"Error loading EAIP: {e}")
            return False
            
    def _load_from_zip(self, zip_path: str) -> bool:
        """Load EAIP data from ZIP file"""
        if not os.path.exists(zip_path):
            print(f"ZIP file not found: {zip_path}")
            return False
            
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix="eaip_")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
                
            return self._process_eaip_directory(self.temp_dir)
            
        except zipfile.BadZipFile:
            print(f"Invalid ZIP file: {zip_path}")
            return False
        except Exception as e:
            print(f"Error extracting ZIP: {e}")
            return False
            
    def _load_from_directory(self, dir_path: str) -> bool:
        """Load EAIP data from directory"""
        if not os.path.isdir(dir_path):
            print(f"Directory not found: {dir_path}")
            return False
            
        return self._process_eaip_directory(dir_path)
        
    def _process_eaip_directory(self, base_path: str) -> bool:
        """Process EAIP directory structure and find charts"""
        try:
            self.charts = []
            self.metadata = {}
            
            # Look for common EAIP file patterns
            chart_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.gif', '.tif', '.tiff']
            
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    if file_ext in chart_extensions:
                        # Extract relative path from base
                        rel_path = os.path.relpath(file_path, base_path)
                        
                        chart_info = {
                            'name': os.path.splitext(file)[0],
                            'filename': file,
                            'path': file_path,
                            'relative_path': rel_path,
                            'type': file_ext[1:],  # Remove the dot
                            'size': os.path.getsize(file_path),
                            'category': self._categorize_chart(rel_path, file)
                        }
                        
                        self.charts.append(chart_info)
                        
            # Sort charts by category and name
            self.charts.sort(key=lambda x: (x['category'], x['name']))
            
            print(f"Found {len(self.charts)} charts in EAIP data")
            return len(self.charts) > 0
            
        except Exception as e:
            print(f"Error processing EAIP directory: {e}")
            return False
            
    def _categorize_chart(self, rel_path: str, filename: str) -> str:
        """Categorize chart based on path and filename"""
        path_lower = rel_path.lower()
        file_lower = filename.lower()
        
        # Common EAIP chart categories
        if any(x in path_lower for x in ['approach', 'app']):
            return 'Approach Charts'
        elif any(x in path_lower for x in ['departure', 'dep', 'sid']):
            return 'Departure Charts'
        elif any(x in path_lower for x in ['arrival', 'arr', 'star']):
            return 'Arrival Charts'
        elif any(x in path_lower for x in ['airport', 'ad']):
            return 'Airport Charts'
        elif any(x in path_lower for x in ['enroute', 'route']):
            return 'Enroute Charts'
        elif any(x in path_lower for x in ['general', 'gen']):
            return 'General'
        else:
            return 'Other'
            
    def get_charts(self) -> List[Dict[str, Any]]:
        """Get list of available charts"""
        return self.charts.copy()
        
    def get_charts_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get charts organized by category"""
        categories = {}
        for chart in self.charts:
            category = chart['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(chart)
        return categories
        
    def get_chart_path(self, chart: Dict[str, Any]) -> str:
        """Get the full path to a chart file"""
        return chart['path']
        
    def search_charts(self, query: str) -> List[Dict[str, Any]]:
        """Search charts by name or filename"""
        query_lower = query.lower()
        results = []
        
        for chart in self.charts:
            if (query_lower in chart['name'].lower() or 
                query_lower in chart['filename'].lower()):
                results.append(chart)
                
        return results
        
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None
            except Exception as e:
                print(f"Error cleaning up temp directory: {e}")
                
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()