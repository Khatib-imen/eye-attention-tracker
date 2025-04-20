# 🧠 AI Vision Projects: YouTube Gesture Controller & Eye Attention Tracker

Welcome to my repository featuring two real-time AI projects built with **Python** and **MediaPipe** for intelligent webcam-based interaction.

---

## 🎥 YouTube Gesture Controller

Control YouTube playback using just your hand gestures — no need for a keyboard or mouse!

### 📌 Overview

This project utilizes computer vision and hand tracking to detect finger gestures and map them to YouTube commands (e.g., play, pause, volume, navigation).

### 🛠️ Technology Stack

- OpenCV – Webcam input & image processing  
- MediaPipe Hands – Real-time hand landmark detection  
- PyAutoGUI – Simulates key presses for YouTube control  
- `cv2.putText()` – Real-time gesture overlay  
- Python `time` module – Manages cooldowns

### ✨ Features

| Gesture                         | Action          |
|----------------------------------|------------------|
| Open Palm                        | ▶️ Play          |
| Fist                             | ⏸️ Pause         |
| Two fingers (index + middle)     | 🔊 Volume Up     |
| Ring + pinky fingers             | 🔉 Volume Down   |
| Pinky only                       | ⏭️ Next Video    |
| All except pinky                 | ⏮️ Previous Video|

✅ Cooldown system prevents accidental repetition.

---

## 👁️ Eye Attention Tracker

A facial landmark-based attention tracker to detect if a person is looking at the screen and trigger an alert when focus is lost.

### 📌 Overview

This tool uses **MediaPipe Face Mesh** to monitor eye and nose positions in real-time and determine if the user is focused. If the person looks away, an alarm plays.

### 🛠️ Technology Stack

- OpenCV – Video frame capture & annotation  
- MediaPipe Face Mesh – Detects key facial landmarks  
- Python `winsound` or `playsound` – To trigger sound alerts  
- Threading – Non-blocking alarm triggering

### ✨ Features

- Tracks eye and nose alignment to determine focus  
- Visual feedback: eye landmark points on screen  
- Alarm sound plays when user is distracted  
- Alarm stops once user re-focuses or performs a specific gesture (e.g., hand wave)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Khatib-imen/eye-attention-tracker.git
cd eye-attention-tracker

### 2. Create a virtual environment (optional)
python -m venv venv
venv\Scripts\activate  # Windows

3. Install dependencies
pip install -r requirements.txt

4. Run a project
python gesture_controller.py   
python eye_attention.py     


🧑‍💻 Author
Imen Khatib
📍 Tunisia





