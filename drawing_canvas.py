"""Drawing canvas management."""

import cv2
import numpy as np
from config import SCREEN_WIDTH, SCREEN_HEIGHT, DRAWING_THICKNESS, ERASER_THICKNESS


class DrawingCanvas:
    """Manages the drawing canvas and strokes."""

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        """Initialize drawing canvas.
        
        Args:
            width: Canvas width
            height: Canvas height
        """
        self.width = width
        self.height = height
        self.canvas = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
        self.previous_point = None
        self.is_drawing = False

    def draw_line(self, current_point, color, thickness=DRAWING_THICKNESS):
        """Draw a line on the canvas.
        
        Args:
            current_point: (x, y) tuple for current point
            color: BGR color tuple
            thickness: Line thickness
        """
        if current_point is None:
            return
        
        if self.previous_point is not None:
            cv2.line(self.canvas, self.previous_point, current_point, color, thickness, cv2.LINE_AA)
        
        self.previous_point = current_point

    def erase(self, current_point, thickness=ERASER_THICKNESS):
        """Erase on the canvas.
        
        Args:
            current_point: (x, y) tuple for current point
            thickness: Eraser thickness
        """
        if current_point is None:
            return
        
        # Draw white circle to erase
        cv2.circle(self.canvas, current_point, thickness // 2, (255, 255, 255), -1)

    def clear(self):
        """Clear the entire canvas."""
        self.canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        self.previous_point = None
        self.is_drawing = False

    def reset_stroke(self):
        """Reset for a new stroke."""
        self.previous_point = None

    def get_canvas(self):
        """Get the current canvas image.
        
        Returns:
            Canvas image (BGR format)
        """
        return self.canvas.copy()

    def save_drawing(self, filepath):
        """Save the drawing to a file.
        
        Args:
            filepath: Output file path
            
        Returns:
            Boolean indicating success
        """
        try:
            cv2.imwrite(filepath, self.canvas)
            return True
        except Exception as e:
            print(f"Error saving drawing: {e}")
            return False
