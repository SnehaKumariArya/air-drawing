"""Main Air Drawing Application - Draw in mid-air using hand gestures."""

import cv2
import numpy as np
import os
from datetime import datetime
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, DEFAULT_COLOR, OUTPUT_DIR
from hand_detector import HandDetector
from drawing_canvas import DrawingCanvas
from ui_overlay import UIOverlay


class AirDrawing:
    """Main application class for air drawing."""

    def __init__(self):
        """Initialize the air drawing application."""
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, SCREEN_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, SCREEN_HEIGHT)
        
        self.hand_detector = HandDetector()
        self.canvas = DrawingCanvas(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.ui = UIOverlay()
        
        self.current_color = DEFAULT_COLOR
        self.current_color_bgr = COLORS[self.current_color]
        self.brush_size = 3
        self.mode = 'idle'  # idle, drawing, eraser
        self.show_landmarks = True
        
        # FPS calculation
        self.fps_time = datetime.now()
        self.fps = 0
        
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        print("Air Drawing Application Started!")
        print("Press 'Q' to quit, 'C' to clear, 'S' to save, 'L' to toggle landmarks")

    def handle_keyboard_input(self, key):
        """Handle keyboard input.
        
        Args:
            key: Keyboard input (ord value)
            
        Returns:
            Boolean indicating if the application should continue
        """
        if key == ord('q'):
            return False
        elif key == ord('c'):
            self.canvas.clear()
            self.mode = 'idle'
            print("Canvas cleared!")
        elif key == ord('s'):
            self.save_drawing()
        elif key == ord('l'):
            self.show_landmarks = not self.show_landmarks
            print(f"Landmarks: {'ON' if self.show_landmarks else 'OFF'}")
        # Color selection (1-8 for different colors)
        elif key in range(ord('1'), ord('9')):
            colors_list = list(COLORS.keys())
            color_idx = key - ord('1')
            if color_idx < len(colors_list):
                self.current_color = colors_list[color_idx]
                self.current_color_bgr = COLORS[self.current_color]
                print(f"Color changed to: {self.current_color}")
        # Brush size adjustment
        elif key == ord('+') or key == ord('='):
            self.brush_size = min(self.brush_size + 1, 10)
            print(f"Brush size: {self.brush_size}")
        elif key == ord('-'):
            self.brush_size = max(self.brush_size - 1, 1)
            print(f"Brush size: {self.brush_size}")
        
        return True

    def count_raised_fingers(self, landmarks):
        """Count raised fingers in the hand.
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            Number of raised fingers
        """
        if landmarks is None:
            return 0
        
        # Finger tip and PIP joint indices
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        finger_pips = [6, 10, 14, 18]  # PIP joints
        
        raised_fingers = 0
        
        # Check each finger (except thumb)
        for tip_idx, pip_idx in zip(finger_tips, finger_pips):
            if landmarks[tip_idx][1] < landmarks[pip_idx][1]:  # Tip above PIP
                raised_fingers += 1
        
        # Check thumb separately
        if landmarks[4][0] < landmarks[3][0]:  # Thumb tip to the left of thumb IP
            raised_fingers += 1
        
        return raised_fingers

    def update_mode(self, raised_fingers, hand_detected):
        """Update drawing mode based on hand gesture.
        
        Args:
            raised_fingers: Number of raised fingers
            hand_detected: Boolean indicating if hand is detected
        """
        if not hand_detected:
            self.mode = 'idle'
            self.canvas.reset_stroke()
        elif raised_fingers == 1:  # Index finger only
            self.mode = 'drawing'
        elif raised_fingers >= 2:  # Two or more fingers
            self.mode = 'eraser'
        else:
            self.mode = 'idle'
            self.canvas.reset_stroke()

    def process_frame(self, frame):
        """Process a single frame.
        
        Args:
            frame: Input video frame
            
        Returns:
            Processed frame with overlay
        """
        # Flip frame for selfie view
        frame = cv2.flip(frame, 1)
        
        # Get hand landmarks
        results, _ = self.hand_detector.detect_hands(frame)
        landmarks = self.hand_detector.get_hand_landmarks(results, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        hand_detected = landmarks is not None
        
        # Get finger tip for drawing
        if hand_detected:
            finger_tip = self.hand_detector.get_finger_tip(landmarks)
            raised_fingers = self.count_raised_fingers(landmarks)
            self.update_mode(raised_fingers, hand_detected)
            
            # Draw or erase
            if self.mode == 'drawing':
                self.canvas.draw_line(finger_tip, self.current_color_bgr, self.brush_size)
            elif self.mode == 'eraser':
                self.canvas.erase(finger_tip)
            else:
                self.canvas.reset_stroke()
        else:
            self.mode = 'idle'
            self.canvas.reset_stroke()
        
        # Get canvas
        display_frame = self.canvas.get_canvas()
        
        # Draw hand landmarks if enabled
        if self.show_landmarks and hand_detected:
            display_frame = self.ui.draw_hand_landmarks(display_frame, landmarks, (0, 255, 0))
        
        # Draw UI overlays
        display_frame = self.ui.draw_instructions(display_frame)
        display_frame = self.ui.draw_color_palette(display_frame, self.current_color)
        display_frame = self.ui.draw_status(display_frame, self.mode, self.current_color, self.brush_size)
        display_frame = self.ui.draw_fps(display_frame, self.fps)
        
        return display_frame

    def calculate_fps(self):
        """Calculate frames per second."""
        current_time = datetime.now()
        delta = (current_time - self.fps_time).total_seconds()
        if delta > 0:
            self.fps = 1.0 / delta
        self.fps_time = current_time

    def save_drawing(self):
        """Save the current drawing to a file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"drawing_{timestamp}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        if self.canvas.save_drawing(filepath):
            print(f"Drawing saved: {filepath}")
        else:
            print(f"Failed to save drawing")

    def run(self):
        """Main application loop."""
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to read frame from camera")
                    break
                
                # Process frame
                display_frame = self.process_frame(frame)
                
                # Calculate FPS
                self.calculate_fps()
                
                # Display frame
                cv2.imshow('Air Drawing - Press Q to quit', display_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key != 255:  # If a key was pressed
                    if not self.handle_keyboard_input(key):
                        break
        
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        self.cap.release()
        self.hand_detector.release_detector()
        cv2.destroyAllWindows()
        print("Air Drawing Application Closed!")


if __name__ == "__main__":
    app = AirDrawing()
    app.run()
