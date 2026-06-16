# Air Drawing 🎨

Draw in mid-air using hand gestures! This is a real-time hand gesture-based drawing application that uses computer vision to detect your hand and convert your movements into digital art.

## Features ✨

- **Real-time Hand Tracking**: Uses MediaPipe for accurate hand pose detection
- **Gesture-based Drawing**: 
  - Index finger extended = Draw
  - Two or more fingers = Eraser
- **Color Palette**: Choose from 8 different colors
- **Adjustable Brush Size**: Control line thickness
- **Clear Canvas**: Quick keyboard command to clear
- **Save Drawings**: Export your artwork as PNG images
- **FPS Counter**: Monitor performance
- **Hand Landmarks Visualization**: Toggle landmark visibility

## Requirements 📋

- Python 3.7+
- Webcam/Camera
- OpenCV
- MediaPipe
- NumPy
- Pillow

## Installation 🔧

1. Clone the repository:
```bash
git clone https://github.com/SnehaKumariArya/air-drawing.git
cd air-drawing
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage 🚀

1. Run the application:
```bash
python air_drawing.py
```

2. Allow access to your camera when prompted

3. Use hand gestures to draw:
   - **Raise index finger only** → Draw
   - **Raise two or more fingers** → Erase
   - **Close hand/no fingers** → Idle (no drawing)

### Keyboard Controls ⌨️

| Key | Action |
|-----|--------|
| `1-8` | Change color (8 colors available) |
| `+` / `-` | Increase/decrease brush size |
| `C` | Clear canvas |
| `S` | Save drawing |
| `L` | Toggle hand landmarks visibility |
| `Q` | Quit application |

## How It Works 🔍

### Architecture

The application consists of modular components:

- **`hand_detector.py`**: Hand tracking using MediaPipe
  - Detects 21 hand landmarks
  - Identifies finger positions and gestures
  - Tracks hand movement in real-time

- **`drawing_canvas.py`**: Canvas management
  - Stores drawing state
  - Renders lines and eraser strokes
  - Saves finished drawings

- **`ui_overlay.py`**: User interface
  - Displays instructions and status
  - Shows color palette
  - Renders hand landmarks
  - FPS counter

- **`air_drawing.py`**: Main application
  - Orchestrates all components
  - Handles user input
  - Manages drawing modes
  - Controls frame processing

- **`config.py`**: Configuration
  - Tunable parameters
  - Color definitions
  - Threshold values
  - UI settings

### Drawing Mode Detection

The application uses finger counting to determine drawing mode:

```
Raised Fingers | Mode
--- | ---
0 | Idle (no drawing)
1 | Drawing (index finger)
2+ | Eraser (multiple fingers)
```

### Gesture Recognition

Fingers are detected as "raised" by comparing their tip position with their PIP (Proximal Interphalangeal) joint:
- If tip is above PIP → Finger is raised
- If tip is below PIP → Finger is down

## Configuration 🎯

Edit `config.py` to customize:

- **Screen dimensions**: `SCREEN_WIDTH`, `SCREEN_HEIGHT`
- **Drawing thickness**: `DRAWING_THICKNESS`, `ERASER_THICKNESS`
- **Colors**: Add/modify in `COLORS` dictionary
- **Hand detection sensitivity**: `MIN_DETECTION_CONFIDENCE`, `MIN_TRACKING_CONFIDENCE`
- **Smoothing factor**: `SMOOTH_FACTOR` (0-1, higher = smoother)

### Example: Change Default Color

```python
# In config.py
DEFAULT_COLOR = 'red'  # Change from 'blue' to 'red'
```

### Example: Add New Color

```python
# In config.py - COLORS dictionary
COLORS = {
    # ... existing colors ...
    'orange': (0, 165, 255),  # BGR format
}
```

## Troubleshooting 🐛

### Camera not detected
- Ensure camera is properly connected
- Check camera permissions
- Try changing camera index in `air_drawing.py` (default is 0)

### Hand not detected
- Ensure good lighting
- Move hand slowly and deliberately
- Keep hand fully visible in frame
- Adjust `MIN_DETECTION_CONFIDENCE` in `config.py` (lower = more sensitive)

### Low FPS / Slow performance
- Close other applications
- Reduce `SCREEN_WIDTH` and `SCREEN_HEIGHT`
- Disable hand landmarks visualization (press `L`)
- Check camera resolution settings

### Drawings not saving
- Ensure `drawings/` directory exists (auto-created)
- Check file permissions
- Ensure sufficient disk space

## Tips for Best Results 💡

1. **Lighting**: Use well-lit environments for accurate hand detection
2. **Distance**: Position hand 20-40cm from camera
3. **Movement**: Draw slowly for smoother lines
4. **Gestures**: Raise fingers clearly to switch modes
5. **Stability**: Keep hand steady while drawing

## Performance Optimization ⚡

- Target FPS: 30 fps
- Hand detection runs at each frame
- Drawing operations are optimized with OpenCV's line antialiasing
- Consider reducing resolution for resource-constrained devices

## Future Enhancements 🚀

- [ ] Multi-hand drawing support
- [ ] Undo/Redo functionality
- [ ] Preset brush styles
- [ ] Drawing filters and effects
- [ ] Gesture shortcuts
- [ ] Recording video of drawing process
- [ ] Touch support for mobile devices

## File Structure 📁

```
air-drawing/
├── air_drawing.py          # Main application
├── hand_detector.py        # Hand detection module
├── drawing_canvas.py       # Canvas management
├── ui_overlay.py           # UI rendering
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── drawings/              # Output directory for saved drawings
```

## Credits 🙏

- Built with [MediaPipe](https://mediapipe.dev/) by Google
- Uses [OpenCV](https://opencv.org/) for image processing
- Inspired by gesture-based drawing applications

## License 📄

This project is open source and available under the MIT License.

## Contributing 🤝

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## Support 💬

If you encounter issues or have questions, please:
1. Check the troubleshooting section
2. Review the code comments
3. Check existing issues
4. Create a new issue with details

Enjoy drawing in the air! 🎨✨
