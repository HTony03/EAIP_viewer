# EAIP Viewer

A local aviation chart viewer for CAAC EAIP (Electronic Aeronautical Information Publication), providing a similar experience to ChartFox application.

## Features

- **Multi-format Support**: Read both ZIP files and unzipped EAIP directories
- **Chart Categories**: Organize charts by type (Approach, Departure, Arrival, Airport, Enroute, etc.)
- **Search Functionality**: Quickly find charts by name or filename
- **Image Viewer**: Built-in image viewer with zoom capabilities
- **External Viewer**: Open charts in external applications (PDF viewers, image viewers)
- **Future Ready**: Prepared for XPUIPC integration to display airplane location on maps

## Installation

1. Clone this repository:
```bash
git clone https://github.com/HTony03/EAIP_viewer.git
cd EAIP_viewer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python eaip_viewer.py
```

### Loading EAIP Data

1. **From ZIP file**: Click "Select EAIP ZIP File" and choose your EAIP ZIP archive
2. **From Directory**: Click "Select EAIP Directory" and choose an unzipped EAIP folder

### Viewing Charts

1. After loading EAIP data, charts will appear in the left panel organized by category
2. Use the search box to quickly find specific charts
3. Double-click on a chart to view it
4. For image files (PNG, JPG, etc.), use mouse wheel to zoom
5. Click "Open in External Viewer" to open charts in your default system application

## Supported File Types

- **Images**: PNG, JPG, JPEG, GIF, TIF, TIFF
- **Documents**: PDF (opens in external viewer)
- **Other**: Any file type can be opened in external applications

## Chart Categories

The application automatically categorizes charts based on their location and filename:

- **Approach Charts**: Instrument approach procedures
- **Departure Charts**: Standard Instrument Departures (SID)
- **Arrival Charts**: Standard Terminal Arrival Routes (STAR)
- **Airport Charts**: Airport layout and ground movement charts
- **Enroute Charts**: Navigation charts for enroute flight
- **General**: General information charts
- **Other**: Uncategorized charts

## Future Development

- XPUIPC integration for real-time aircraft position display
- Map overlay functionality
- Flight planning integration
- Chart annotation capabilities

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- Pillow (PIL) for image handling
- See `requirements.txt` for complete list

## License

MIT License - see LICENSE file for details.