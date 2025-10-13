import mediapipe as mp
import cv2
import numpy as np

class pose_detector:
    """
    A class to detect and draw human pose landmarks using MediaPipe.
    """
    def __init__(self, model_complexity=1, smooth_landmarks=True, enable_segmentation=False, 
                 smooth_segmentation=True, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        
        self.mp_pose = mp.solutions.pose
        self.landmarks = self.mp_pose.PoseLandmark 
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.pose = self.mp_pose.Pose(
            model_complexity=model_complexity,
            smooth_landmarks=smooth_landmarks,
            enable_segmentation=enable_segmentation,
            smooth_segmentation=smooth_segmentation,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def find_pose(self, image, draw=True):
        """
        Processes an image to find pose landmarks.
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        
        results = self.pose.process(image_rgb)
        
        if draw and results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )
            
        return image, results

    def get_positions(self, image, results):
        """
        Extracts the x, y coordinates of all landmarks.
        """
        lm_list = []
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

    def find_angle(self, lm_list, p1, p2, p3):
        """
        Calculates the angle between three points from a landmark list.
        """
        x1, y1 = lm_list[p1][1:]
        x2, y2 = lm_list[p2][1:]
        x3, y3 = lm_list[p3][1:]

        angle = np.degrees(np.arctan2(y3 - y2, x3 - x2) - np.arctan2(y1 - y2, x1 - x2))
        
        if angle < 0:
            angle += 360
        if angle > 180:
            angle = 360 - angle
            
        return angle
