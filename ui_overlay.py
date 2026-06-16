"""UI overlay for air drawing application."""

import cv2
from config import UI_FONT_SCALE, UI_THICKNESS, UI_COLOR, UI_BG_COLOR, COLORS


class UIOverlay:
    """Manages UI elements on the display."""

    def __init__(self):
        """Initialize UI overlay."""
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def draw_instructions(self, frame):
        """Draw instruction text on frame.
        
        Args:
            frame: Input frame
            
        Returns:
            Frame with instructions
        """
        instructions = [
            "INSTRUCTIONS:",
            "Index finger up -> Draw",
            "Two fingers up -> Eraser",
            "C -> Clear canvas",
            "S -> Save drawing",
            "Q -> Quit",
            "1-8 -> Change color"
        ]
        
        y_offset = 30
        for i, instruction in enumerate(instructions):
            cv2.putText(frame, instruction, (10, y_offset + i * 25),
                       self.font, UI_FONT_SCALE, UI_COLOR, UI_THICKNESS)
        
        return frame

    def draw_color_palette(self, frame, current_color):
        """Draw color palette on frame.
        
        Args:
            frame: Input frame
            current_color: Name of current color
            
        Returns:
            Frame with color palette
        """
        colors_list = list(COLORS.items())
        palette_x = 10
        palette_y = frame.shape[0] - 50
        box_size = 40
        spacing = 5
        
        for idx, (color_name, color_bgr) in enumerate(colors_list):
            x = palette_x + idx * (box_size + spacing)
            y = palette_y
            
            # Draw color box
            cv2.rectangle(frame, (x, y), (x + box_size, y + box_size), color_bgr, -1)
            
            # Highlight current color
            if color_name == current_color:
                cv2.rectangle(frame, (x - 2, y - 2), (x + box_size + 2, y + box_size + 2),
                            (255, 255, 255), 3)
        
        return frame

    def draw_status(self, frame, mode, color, brush_size):
        """Draw status information on frame.
        
        Args:
            frame: Input frame
            mode: Drawing mode ('drawing', 'eraser', 'idle')
            color: Current color name
            brush_size: Current brush size
            
        Returns:
            Frame with status information
        """
        status_text = f"Mode: {mode.upper()} | Color: {color} | Size: {brush_size}"
        cv2.putText(frame, status_text, (frame.shape[1] - 400, 30),
                   self.font, UI_FONT_SCALE, UI_COLOR, UI_THICKNESS)
        
        return frame

    def draw_hand_landmarks(self, frame, landmarks, color=(0, 255, 0)):
        """Draw hand landmarks on frame.
        
        Args:
            frame: Input frame
            landmarks: List of hand landmarks (x, y) tuples
            color: Color for landmarks
            
        Returns:
            Frame with hand landmarks drawn
        """
        if landmarks is None:
            return frame
        
        # Draw circles at each landmark
        for landmark in landmarks:
            cv2.circle(frame, landmark, 3, color, -1)
        
        # Draw lines connecting landmarks (palm structure)
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),  # Index
            (0, 9), (9, 10), (10, 11), (11, 12),  # Middle
            (0, 13), (13, 14), (14, 15), (15, 16),  # Ring
            (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
        ]
        
        for start, end in connections:
            if start < len(landmarks) and end < len(landmarks):
                cv2.line(frame, landmarks[start], landmarks[end], color, 1)
        
        return frame

    def draw_fps(self, frame, fps):
        """Draw FPS counter on frame.
        
        Args:
            frame: Input frame
            fps: Frames per second
            
        Returns:
            Frame with FPS counter
        """
        cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 150, frame.shape[0] - 10),
                   self.font, UI_FONT_SCALE, (0, 255, 0), UI_THICKNESS)
        
        return frame
