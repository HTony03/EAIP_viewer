#!/usr/bin/env python3
"""
EAIP Viewer Launch Script
"""

import sys
import os

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

from main import main

if __name__ == "__main__":
    main()