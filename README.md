# PoseForm AI — Real-Time Workout Form Corrector

*"An AI-Powered Coach for Perfecting Exercise Form"*

---

## 📖 Overview

This repository contains **PoseForm AI**, a real-time workout assistant that uses a standard webcam to function as a virtual personal trainer. It leverages computer vision to analyze a user's exercise form, count repetitions, and provide immediate, actionable feedback.

The project is built entirely in Python and demonstrates an end-to-end application of pose estimation for a practical, interactive purpose. It's designed to be modular, allowing for easy expansion with new exercises and correction logic.

---

## 🧩 How PoseForm AI Works

1.  **Webcam Capture & Processing**
    -   The application uses **OpenCV** to capture the live video feed from the user's webcam.
    -   Each frame is resized and flipped to create a natural, mirror-like experience.

2.  **Pose Estimation**
    -   Google's **MediaPipe** library performs real-time pose estimation on each frame.
    -   The model identifies 33 key body landmarks (joints like shoulders, elbows, hips, knees) and returns their coordinates, creating a "virtual skeleton."

3.  **Kinematic Analysis**
    -   Using the virtual skeleton's coordinates, the application calculates the angles of relevant body joints in real-time.
    -   For a bicep curl, it's the elbow angle. For a squat, it's the knee and back angles.

4.  **Rule-Based Exercise Logic**
    -   Each exercise has a dedicated "Corrector" class containing a state machine and a set of rules.
    -   It tracks joint angles to determine the exercise stage (e.g., "up" or "down"), counts valid repetitions, and provides corrective feedback (e.g., "SQUAT LOWER!").

---

## ✨ Key Features

* **Real-Time Analysis**: Provides instant feedback on every frame for immediate form correction.
* **Multi-Exercise Support**: Includes modules for Bicep Curls, Squats, Push-Ups, and Tricep Extensions.
* **Accurate Rep Counting**: Automatically counts valid repetitions based on a full range of motion.
* **Live Form Correction**: Displays visual and audio cues to help the user correct common mistakes.
* **Interactive Dashboard**: A user-friendly interface built with **Streamlit** allows for easy exercise selection.
* **Modular Design**: The object-oriented structure makes it simple to add new exercises.

---

## 🛠️ Tech Stack

* **Core Logic**: Python
* **Pose Estimation**: MediaPipe
* **Video & Image Processing**: OpenCV, NumPy
* **Web Dashboard**: Streamlit
* **Audio Feedback**: Pygame

---

## 🏗️ Repository Structure
```bash
PoseForm-AI/
│── dashboard.py                # The main Streamlit web application
│── pose_detector.py              # Class for MediaPipe pose detection
│── exercise_correctors.py        # Contains the logic for each exercise
│── sounds/                       # Folder for audio feedback files
│   ├── rep_complete.wav
│   └── ...
│── requirements.txt              # Project dependencies
└── README.md                     # Project documentation (this file)
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hasankablawe/PoseForm-AI
cd PoseForm-AI
```
