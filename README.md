# Meteor Analysis System - IMX678

A professional meteor detection and analysis application for IMX678 camera footage. Designed to detect meteor events, analyze light curves, classify meteor types, and provide comprehensive scientific data.

## Features

✨ **Core Functionality:**
- Automatic meteor event detection (start/end points)
- Light curve analysis with zoom capability (up to 10x)
- Motion analysis graphs with zoom (event-centered)
- Meteor type classification with confidence percentage
- Extended meteor types: Fireball, Fragmentation, Ordinary, Slow, and more
- MP4 video player with frame-accurate navigation

🎨 **User Interface:**
- **Setup Tab**: Configuration management and save/load
- **Player Tab**: Video player with keyframe navigation
- **Analysis Tab**: Event detection and type classification
- **Graphs Tab**: Light curve and motion analysis
- Resizable windows and panels
- Configuration persistence

📊 **Analysis Features:**
- Automatic start/end detection of meteor events
- Light intensity analysis
- Motion tracking and trajectory analysis
- Meteor classification:
  - Fireball (bright, slow decay)
  - Fragmentation (multiple peaks)
  - Ordinary (standard meteor)
  - Slow (extended brightness duration)
  - And additional recommended types
- Confidence percentage for classifications

📹 **Video Features:**
- MP4 video loading and playback
- Frame-by-frame navigation
- Keyframe jumping (click on graphs to navigate)
- Central zoom keeping detected event in focus

## Credits

**Designer**: Your Name  
**Project**: AstroBytes Meteor Analysis  
**Community**: [AstroBytes Facebook Group](https://www.facebook.com/groups/1400913928146353?locale=es_ES%2F)

## Installation

```bash
# Clone the repository
git clone https://github.com/Cubzilla470/Meteor.git
cd Meteor

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Requirements

- Python 3.8+
- PyQt5
- OpenCV (cv2)
- NumPy
- Matplotlib
- SciPy

## Usage

1. **Load Video**: Use Setup tab to configure and load MP4 files
2. **Detect Events**: Click "Analyze" to find meteor events
3. **View Analysis**: Check event details in Analysis tab
4. **Examine Graphs**: Zoom into light curve and motion graphs (up to 10x)
5. **Navigate Video**: Click on graphs or use keyframe navigation
6. **Save Configuration**: Save analysis settings for future use

## Architecture

- `main.py` - Application entry point
- `ui/` - User interface components
- `analysis/` - Meteor detection and analysis algorithms
- `video/` - Video processing and playback
- `config/` - Configuration management
- `data/` - Sample data and test files

## License

MIT License - Open for scientific use

---

*AstroBytes: Bringing Meteors into Focus*
