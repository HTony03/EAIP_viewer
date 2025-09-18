# EAIP Viewer Setup Guide

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HTony03/EAIP_viewer.git
   cd EAIP_viewer
   ```

2. **Install system dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt install python3-tk python3-pil python3-pil.imagetk

   # Or for other systems, ensure you have:
   # - Python 3.7+
   # - tkinter (usually included with Python)
   # - PIL/Pillow with ImageTk support
   ```

3. **Install Python packages:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python3 eaip_viewer.py
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

1. **"No module named 'tkinter'"**
   - Install python3-tk: `sudo apt install python3-tk`

2. **"cannot import name 'ImageTk'"**
   - Install PIL ImageTk: `sudo apt install python3-pil.imagetk`

3. **Charts not loading**
   - Ensure EAIP files are in supported formats (PNG, JPG, PDF, etc.)
   - Check file permissions
   - Verify directory structure

4. **External viewer not working**
   - Ensure you have appropriate viewers installed (PDF reader, image viewer)
   - Check system file associations

### Performance Tips

- For large EAIP archives, extraction may take time
- Image charts load faster than PDFs
- Search is case-insensitive and searches both names and filenames

## Development

### Running Tests

```bash
python3 -m unittest tests.test_eaip_handler -v
```

### Project Structure

```
EAIP_viewer/
├── src/                     # Source code
│   ├── main.py             # Main application
│   ├── eaip_handler.py     # EAIP data processing
│   ├── chart_viewer.py     # Chart display GUI
│   └── xpuipc_integration.py # Future X-Plane integration
├── tests/                   # Unit tests
├── eaip_viewer.py          # Launch script
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.