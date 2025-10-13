import numpy as np

# --- MediaPipe Landmark Constants (Optimization for Readability) ---
# This makes the code self-documenting.
LEFT_SHOULDER = 11
LEFT_ELBOW = 13
LEFT_WRIST = 15
RIGHT_SHOULDER = 12
RIGHT_ELBOW = 14
RIGHT_WRIST = 16
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28

# --- Base Class for Shared Logic ---
class ExerciseCorrectorBase:
    """Base class to share the angle calculation method."""
    def _calculate_angle(self, p1, p2, p3):
        p1, p2, p3 = np.array(p1), np.array(p2), np.array(p3)
        radians = np.arctan2(p3[1] - p2[1], p3[0] - p2[0]) - np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

# --- Bicep Curl Corrector ---
class BicepCurlCorrector(ExerciseCorrectorBase):
    def __init__(self):
        self.rep_counter_left, self.stage_left, self.feedback_left, self.percentage_left = 0, "down", "Start", 0
        self.rep_counter_right, self.stage_right, self.feedback_right, self.percentage_right = 0, "down", "Start", 0

    def _process_arm(self, angle, stage, rep_counter):
        """Helper function to process logic for a single arm curl."""
        feedback = "Correct"
        sound_to_play = None
        percentage = np.interp(angle, (30, 160), (100, 0))

        if stage == 'down' and angle < 30:
            stage, rep_counter = "up", rep_counter + 1
            sound_to_play = 'rep'
        elif stage == 'up' and angle > 160:
            stage = "down"
        
        # Form correction logic
        if stage == 'up' and angle > 50:
            feedback = 'CURL HIGHER!'
        elif stage == 'down' and angle < 150:
            feedback = 'EXTEND FULLY!'
            
        return stage, rep_counter, feedback, percentage, sound_to_play

    def process_landmarks(self, lm_list):
        # --- LEFT ARM ---
        angle_left = self._calculate_angle(lm_list[LEFT_SHOULDER][1:], lm_list[LEFT_ELBOW][1:], lm_list[LEFT_WRIST][1:])
        self.stage_left, self.rep_counter_left, self.feedback_left, self.percentage_left, sound_l = self._process_arm(
            angle_left, self.stage_left, self.rep_counter_left
        )
        # --- RIGHT ARM ---
        angle_right = self._calculate_angle(lm_list[RIGHT_SHOULDER][1:], lm_list[RIGHT_ELBOW][1:], lm_list[RIGHT_WRIST][1:])
        self.stage_right, self.rep_counter_right, self.feedback_right, self.percentage_right, sound_r = self._process_arm(
            angle_right, self.stage_right, self.rep_counter_right
        )
        return 'rep' if sound_l == 'rep' or sound_r == 'rep' else None

# --- Squat Corrector ---
class SquatCorrector(ExerciseCorrectorBase):
    def __init__(self):
        self.rep_counter, self.stage, self.feedback, self.percentage = 0, "up", "Start", 0

    def process_landmarks(self, lm_list):
        sound_to_play = None
        knee_angle = self._calculate_angle(lm_list[RIGHT_HIP][1:], lm_list[RIGHT_KNEE][1:], lm_list[RIGHT_ANKLE][1:])
        back_angle = self._calculate_angle(lm_list[RIGHT_SHOULDER][1:], lm_list[RIGHT_HIP][1:], lm_list[RIGHT_KNEE][1:])
        self.percentage = np.interp(knee_angle, (90, 160), (100, 0))
        
        self.feedback = "Correct Form"

        if back_angle < 150:
            self.feedback = "KEEP BACK STRAIGHT"
        elif self.stage == 'up' and knee_angle < 90:
            self.stage, self.rep_counter = "down", self.rep_counter + 1
            sound_to_play = 'rep'
        elif self.stage == 'down' and knee_angle > 160:
            self.stage = "up"
        elif self.stage == 'down' and knee_angle > 100:
            self.feedback = "SQUAT LOWER!"
            
        return sound_to_play

# --- Triceps Extension Corrector ---
class TricepExtensionCorrector(ExerciseCorrectorBase):
    def __init__(self):
        self.rep_counter_left, self.stage_left, self.feedback_left, self.percentage_left = 0, "down", "Start", 0
        self.rep_counter_right, self.stage_right, self.feedback_right, self.percentage_right = 0, "down", "Start", 0

    def _process_arm(self, angle, stage, rep_counter):
        """Helper function to process logic for a single arm extension."""
        feedback = "Correct"
        sound_to_play = None
        percentage = np.interp(angle, (90, 160), (0, 100))
        
        if stage == 'down' and angle > 160:
            stage, rep_counter = "up", rep_counter + 1
            sound_to_play = 'rep'
        elif stage == 'up' and angle < 90:
            stage = "down"
            
        if stage == 'up' and angle < 150:
            feedback = 'EXTEND FULLY!'
        elif stage == 'down' and angle > 100:
            feedback = 'LOWER MORE!'
        
        return stage, rep_counter, feedback, percentage, sound_to_play

    def process_landmarks(self, lm_list):
        # --- LEFT ARM ---
        angle_left = self._calculate_angle(lm_list[LEFT_SHOULDER][1:], lm_list[LEFT_ELBOW][1:], lm_list[LEFT_WRIST][1:])
        self.stage_left, self.rep_counter_left, self.feedback_left, self.percentage_left, sound_l = self._process_arm(
            angle_left, self.stage_left, self.rep_counter_left
        )
        # --- RIGHT ARM ---
        angle_right = self._calculate_angle(lm_list[RIGHT_SHOULDER][1:], lm_list[RIGHT_ELBOW][1:], lm_list[RIGHT_WRIST][1:])
        self.stage_right, self.rep_counter_right, self.feedback_right, self.percentage_right, sound_r = self._process_arm(
            angle_right, self.stage_right, self.rep_counter_right
        )
        return 'rep' if sound_l == 'rep' or sound_r == 'rep' else None

# --- Push Up Corrector ---
class PushUpCorrector(ExerciseCorrectorBase):
    def __init__(self):
        self.rep_counter, self.stage, self.feedback, self.percentage = 0, "up", "Start", 0

    def process_landmarks(self, lm_list):
        sound_to_play = None
        # Use right arm for push-up calculation
        elbow_angle = self._calculate_angle(lm_list[RIGHT_SHOULDER][1:], lm_list[RIGHT_ELBOW][1:], lm_list[RIGHT_WRIST][1:])
        hip_angle = self._calculate_angle(lm_list[RIGHT_SHOULDER][1:], lm_list[RIGHT_HIP][1:], lm_list[RIGHT_ANKLE][1:])
        self.percentage = np.interp(elbow_angle, (90, 160), (100, 0))
        
        self.feedback = "Correct Form"

        if hip_angle < 160:
            self.feedback = "STRAIGHTEN YOUR BACK"
        elif self.stage == 'up' and elbow_angle < 90:
            self.stage, self.rep_counter = "down", self.rep_counter + 1
            sound_to_play = 'rep'
        elif self.stage == 'down' and elbow_angle > 160:
            self.stage = "up"
        elif self.stage == 'down' and elbow_angle > 100:
            self.feedback = "GO LOWER!"
        
        return sound_to_play

