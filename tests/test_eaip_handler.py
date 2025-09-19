"""
Tests for EAIP Viewer functionality
"""

import unittest
import tempfile
import os
import shutil
from PIL import Image
import sys

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from eaip_handler import EAIPHandler


class TestEAIPHandler(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.handler = EAIPHandler()
        
        # Create test directory structure
        os.makedirs(os.path.join(self.test_dir, 'approach'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'departure'), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, 'airport'), exist_ok=True)
        
        # Create test images
        img = Image.new('RGB', (100, 100), color='white')
        img.save(os.path.join(self.test_dir, 'approach', 'test_approach.png'))
        img.save(os.path.join(self.test_dir, 'departure', 'test_departure.png'))
        img.save(os.path.join(self.test_dir, 'airport', 'test_airport.png'))
        
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        self.handler.cleanup()
        
    def test_load_directory(self):
        """Test loading EAIP from directory"""
        success = self.handler.load_eaip(self.test_dir, is_zip=False)
        self.assertTrue(success)
        
        charts = self.handler.get_charts()
        self.assertEqual(len(charts), 3)
        
    def test_chart_categorization(self):
        """Test chart categorization"""
        self.handler.load_eaip(self.test_dir, is_zip=False)
        categories = self.handler.get_charts_by_category()
        
        self.assertIn('Approach Charts', categories)
        self.assertIn('Departure Charts', categories)
        self.assertIn('Airport Charts', categories)
        
    def test_search_charts(self):
        """Test chart search functionality"""
        self.handler.load_eaip(self.test_dir, is_zip=False)
        
        results = self.handler.search_charts('approach')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'test_approach')
        
    def test_invalid_directory(self):
        """Test handling of invalid directory"""
        success = self.handler.load_eaip('/nonexistent/path', is_zip=False)
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()