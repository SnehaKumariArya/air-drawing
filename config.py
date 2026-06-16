"""Configuration settings for Air Drawing application."""

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Drawing settings
DRAWING_THICKNESS = 3
ERASER_THICKNESS = 30
SMOOTH_FACTOR = 0.7  # Smoothing for drawing lines (0-1)

# Color palette (BGR format for OpenCV)
COLORS = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255),
    'purple': (255, 0, 255),
    'cyan': (255, 255, 0),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
}

DEFAULT_COLOR = 'blue'

# Hand tracking settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5

# Gesture thresholds
FINGER_UP_THRESHOLD = 0.02  # Distance threshold to detect if finger is up
DRAWING_MODE_THRESHOLD = 0.05  # Hand height for drawing mode activation

# UI settings
UI_FONT = 'opencv'  # Font for text
UI_FONT_SCALE = 0.6
UI_THICKNESS = 2
UI_COLOR = (200, 200, 200)  # Light gray
UI_BG_COLOR = (50, 50, 50)  # Dark gray

# Output settings
OUTPUT_DIR = './drawings'
OUTPUT_FORMAT = 'png'  # Format: 'png', 'jpg', etc.
