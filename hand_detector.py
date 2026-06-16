"""Hand detection and tracking using MediaPipe."""

import mediapipe as mp
import numpy as np
from config import MIN_DETECTION_CONFIDENCE, MIN_TRACKING_CONFIDENCE


class HandDetector:
    """Detects and tracks hand landmarks using MediaPipe Hands."""

    def __init__(self):
        """Initialize hand detector with MediaPipe."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_hands(self, frame):
        """Detect hands in the frame.
        
        Args:
            frame: Input video frame (BGR format)
            
        Returns:
            Processed frame with hand landmarks and results object
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results, frame

    def get_hand_landmarks(self, results, frame_width, frame_height):
        """Extract hand landmarks from detection results.
        
        Args:
            results: Hand detection results from MediaPipe
            frame_width: Width of the frame
            frame_height: Height of the frame
            
        Returns:
            List of (x, y) coordinates for 21 hand landmarks, or None
        """
        if not results.multi_hand_landmarks:
            return None

        landmarks = []
        for landmark in results.multi_hand_landmarks[0].landmark:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            landmarks.append((x, y))
        
        return landmarks

    def get_finger_tip(self, landmarks):
        """Get the index finger tip coordinate.
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            (x, y) coordinate of index finger tip (landmark 8)
        """
        if landmarks is None:
            return None
        return landmarks[8]  # Index finger tip

    def is_hand_closed(self, landmarks):
        """Detect if hand is in closed fist position.
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            Boolean indicating if hand is closed
        """
        if landmarks is None:
            return False
        
        # Check distance between fingertips and palm
        palm = landmarks[0]  # Wrist
        finger_tips = [landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]]
        
        distances = [np.sqrt((tip[0] - palm[0])**2 + (tip[1] - palm[1])**2) for tip in finger_tips]
        avg_distance = np.mean(distances)
        
        # If average distance is small, hand is closed
        return avg_distance < 50

    def is_drawing_mode(self, landmarks):
        """Detect if hand is in drawing position (index finger extended).
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            Boolean indicating if hand is in drawing mode
        """
        if landmarks is None:
            return False
        
        # Check if index finger is extended (tip far from base)
        index_tip = landmarks[8]
        index_base = landmarks[5]
        distance = np.sqrt((index_tip[0] - index_base[0])**2 + (index_tip[1] - index_base[1])**2)
        
        # If distance is large, index finger is extended
        return distance > 30

    def release_detector(self):
        """Release resources."""
        self.hands.close()


import cv2
