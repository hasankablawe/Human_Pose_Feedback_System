import streamlit as st
import cv2
import numpy as np
import pygame
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

# Create a single placeholder for the stats area
stats_placeholder = st.empty()


if run:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Error: Could not open webcam.")
    else:
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

            # --- DISPLAY STATS UNDER THE VIDEO (HORIZONTAL LAYOUT) ---
            # Use a container within the placeholder to redraw stats each frame
            with stats_placeholder.container():
                if isinstance(exercise_corrector, (BicepCurlCorrector, TricepExtensionCorrector)):
                    # Create two columns for left and right arm stats
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### Left Arm")
                        st.markdown(f'**Reps:** <h1 style="color: white;">{exercise_corrector.rep_counter_left}</h1>', unsafe_allow_html=True)
                        st.markdown(f'**Stage:** <h3 style="color: cyan;">{exercise_corrector.stage_left.upper()}</h3>', unsafe_allow_html=True)
                        st.info(f'Feedback: {exercise_corrector.feedback_left}')

                    with col2:
                        st.markdown("### Right Arm")
                        st.markdown(f'**Reps:** <h1 style="color: white;">{exercise_corrector.rep_counter_right}</h1>', unsafe_allow_html=True)
                        st.markdown(f'**Stage:** <h3 style="color: cyan;">{exercise_corrector.stage_right.upper()}</h3>', unsafe_allow_html=True)
                        st.info(f'Feedback: {exercise_corrector.feedback_right}')

                else: # For single metric exercises like Squat and Push-Up
                    # Create three columns for reps, stage, and feedback
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown('**Reps**')
                        st.markdown(f'<h1 style="color: white;">{exercise_corrector.rep_counter}</h1>', unsafe_allow_html=True)
                    with col2:
                        st.markdown('**Stage**')
                        st.markdown(f'<h3 style="color: cyan;">{exercise_corrector.stage.upper()}</h3>', unsafe_allow_html=True)
                    with col3:
                        st.markdown('**Feedback**')
                        st.info(f'{exercise_corrector.feedback}')
            
            # Display the video frame
            frame_placeholder.image(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB), channels="RGB")
        
        cap.release()
        cv2.destroyAllWindows()
else:
    st.info('Click "Start Webcam" in the sidebar to begin your workout.')

