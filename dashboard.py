import streamlit as st
import cv2
import numpy as np
import pygame
import time # NEW: Import the time module
from pose_detector import pose_detector
from exercise_correctors import BicepCurlCorrector, SquatCorrector, TricepExtensionCorrector, PushUpCorrector

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Workout Assistant", layout="wide")

# --- ASSETS & INITIALIZATION ---
try:
    pygame.mixer.init()
    rep_sound = pygame.mixer.Sound('sounds/rep_complete.wav')
except (pygame.error, FileNotFoundError):
    st.warning("Sound file 'rep_complete.wav' not found. Audio feedback will be disabled. Please create a 'sounds' folder with the required audio file.")
    rep_sound = None

EXERCISE_MAP = {
    "Bicep Curl": BicepCurlCorrector,
    "Squat": SquatCorrector,
    "Tricep Extension": TricepExtensionCorrector,
    "Push-Up": PushUpCorrector
}

# --- SIDEBAR CONTROLS ---
st.sidebar.title("Workout Controls")
selected_exercise = st.sidebar.selectbox("Choose an exercise", list(EXERCISE_MAP.keys()))
run = st.sidebar.button('Start Webcam')

# --- MAIN PANEL ---
st.title("PoseForm AI: Workout Corrector")
frame_placeholder = st.empty()

# --- CREATE PLACEHOLDERS FOR STATS UNDER THE VIDEO ---
col1, col2 = st.columns(2)
with col1:
    left_stats_placeholder = st.empty()
with col2:
    right_stats_placeholder = st.empty()


if run:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Error: Could not open webcam.")
    else:
        # --- NEW: COUNTDOWN LOGIC ---
        st.info("Get in position! Starting in 5 seconds...")
        for i in range(5, 0, -1):
            is_frame, frame = cap.read()
            if not is_frame:
                break
            frame = cv2.flip(frame, 1)
            
            # Display countdown on the frame
            h, w, _ = frame.shape
            text = str(i)
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 5, 10)
            text_x = (w - text_size[0]) // 2
            text_y = (h + text_size[1]) // 2
            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 10, cv2.LINE_AA)
            
            frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
            time.sleep(1)
        # --- END NEW ---
        
        # --- INITIALIZE CORRECTOR ---
        exercise_corrector = EXERCISE_MAP[selected_exercise]()
        detector = pose_detector()

        while cap.isOpened():
            is_frame, frame = cap.read()
            if not is_frame:
                st.write("The video capture has ended.")
                break

            # Process frame for pose
            frame = cv2.flip(frame, 1)
            small_frame = cv2.resize(frame, (640, 480))
            annotated_frame, results = detector.find_pose(small_frame, draw=True)
            lm_list = detector.get_positions(annotated_frame, results)

            sound_to_play = None
            if len(lm_list) != 0:
                sound_to_play = exercise_corrector.process_landmarks(lm_list)
            
            if sound_to_play == 'rep' and rep_sound:
                rep_sound.play()

            # --- DISPLAY STATS UNDER THE VIDEO ---
            if isinstance(exercise_corrector, (BicepCurlCorrector, TricepExtensionCorrector)):
                with left_stats_placeholder.container():
                    st.markdown("### Left Arm")
                    st.markdown(f'**Reps:** <h1 style="color: white;">{exercise_corrector.rep_counter_left}</h1>', unsafe_allow_html=True)
                    st.info(f'Feedback: {exercise_corrector.feedback_left}')

                with right_stats_placeholder.container():
                    st.markdown("### Right Arm")
                    st.markdown(f'**Reps:** <h1 style="color: white;">{exercise_corrector.rep_counter_right}</h1>', unsafe_allow_html=True)
                    st.info(f'Feedback: {exercise_corrector.feedback_right}')

            else: # For single metric exercises
                with left_stats_placeholder.container():
                    st.markdown(f'**Reps:** <h1 style="color: white;">{exercise_corrector.rep_counter}</h1>', unsafe_allow_html=True)
                    st.info(f'Feedback: {exercise_corrector.feedback}')
                right_stats_placeholder.empty()
            
            # Display the video frame
            frame_placeholder.image(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB), channels="RGB")
        
        cap.release()
        cv2.destroyAllWindows()
else:
    st.info('Click "Start Webcam" in the sidebar to begin your workout.')

