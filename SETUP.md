# EAIP Viewer Setup Guide

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HTony03/EAIP_viewer.git
   cd EAIP_viewer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: The application now uses PySide6 (Qt6) for a modern GUI experience.

3. **Run the application:**
   ```bash
   python eaip_viewer.py
   ```

## Usage Instructions

### Loading EAIP Data

The application supports two methods for loading CAAC EAIP data:

1. **ZIP File**: Click "Select EAIP ZIP File" and choose your downloaded EAIP ZIP archive
2. **Directory**: Click "Select EAIP Directory" and choose an extracted EAIP folder

### Supported File Types

- **Images**: PNG, JPG, JPEG, GIF, TIF, TIFF (displayed in built-in viewer)
- **PDFs**: Opened in external PDF viewer
- **Other**: Any file type can be opened in external applications

### Chart Categories

Charts are automatically organized into categories based on their file paths:

- **Approach Charts**: Instrument approach procedures
- **Departure Charts**: Standard Instrument Departures (SID)
- **Arrival Charts**: Standard Terminal Arrival Routes (STAR)  
- **Airport Charts**: Airport diagrams and ground movement charts
- **Enroute Charts**: Navigation charts for enroute phases
- **General**: Information and reference charts
- **Other**: Uncategorized charts

### Viewing Charts

1. **Browse**: Use the tree view on the left to browse charts by category
2. **Search**: Type in the search box to find specific charts by name
3. **View**: Double-click a chart to display it in the viewer
4. **Zoom**: Use mouse wheel to zoom in/out on image charts
5. **External**: Click "Open in External Viewer" for full-screen viewing

## Qt6 Features

### Modern Interface Benefits

- **Native Look**: Professional appearance on Windows, macOS, and Linux
- **High-DPI Support**: Perfect scaling on high-resolution displays
- **Smooth Performance**: Hardware-accelerated rendering
- **Responsive UI**: Non-blocking data loading with progress feedback
- **Better File Dialogs**: Native system file selection dialogs

### Enhanced Image Viewer

- **Smooth Zooming**: Mouse wheel zoom with proper scaling
- **Scroll Support**: Navigate large charts with automatic scrollbars
- **Auto-fit**: Charts automatically fit to window size
- **Quality Rendering**: High-quality image scaling with Qt's rendering engine

## Future Features

### XPUIPC Integration (Planned)

The application includes infrastructure for future X-Plane integration:

- Real-time aircraft position overlay on charts
- Automatic chart selection based on flight phase
- Flight path visualization
- Approach and departure procedure guidance

To enable this feature when implemented:
1. Install X-Plane with XPUIPC plugin
2. The application will detect and connect automatically
3. Aircraft position will appear as overlay on relevant charts

## Troubleshooting

### Common Issues

1. **"No module named 'PySide6'"**
   - Install PySide6: `pip install PySide6`
   - Or install all requirements: `pip install -r requirements.txt`

2. **Charts not loading**
   - Ensure EAIP files are in supported formats (PNG, JPG, PDF, etc.)
   - Check file permissions
   - Verify directory structure

3. **External viewer not working**
   - Ensure you have appropriate viewers installed (PDF reader, image viewer)
   - Check system file associations

4. **UI scaling issues on high-DPI displays**
   - Qt6 automatically handles high-DPI scaling
   - If issues persist, try setting environment variable: `QT_AUTO_SCREEN_SCALE_FACTOR=1`

### Performance Tips

- For large EAIP archives, extraction may take time (loading happens in background thread)
- Image charts load faster than PDFs
- Search is case-insensitive and searches both names and filenames
- Qt6 provides better memory management for large chart files

## Development

### Running Tests

```bash
python -m unittest tests.test_eaip_handler -v
```

### Project Structure

```
EAIP_viewer/
├── src/                     # Source code
│   ├── main.py             # Main Qt6 application
│   ├── eaip_handler.py     # EAIP data processing
│   ├── chart_viewer.py     # Qt6-based chart display GUI
│   └── xpuipc_integration.py # Future X-Plane integration
├── tests/                   # Unit tests
├── eaip_viewer.py          # Launch script
├── requirements.txt        # Python dependencies (includes PySide6)
└── README.md              # Documentation
```

### Qt6 Architecture

The application uses modern Qt6 patterns:
- **QMainWindow**: Main application window with menu bar and status bar
- **QTreeWidget**: Chart list with search and categorization
- **Custom ImageViewer**: QLabel-based image viewer with zoom capabilities
- **QThread**: Background loading to keep UI responsive
- **Signal/Slot**: Event handling for user interactions

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.