# 🛡️ MOMwatch

**MOMwatch** is a computer-vision productivity tool inspired by a mother's care from a distance. Tool detects prolonged downward gaze, interrupts doomscrolling with a custom intervention video and sending alert message to mom. Turning technology into a gentle reminder of care and connection for children whose mothers cannot always be physically present.

A **laptop-based productivity tool** that detects sustained downward gaze using a webcam, MediaPipe Face Landmarker, and iris landmarks when you are repeatedly looking downward, such as checking or using a phone while working on your laptop.

If the downward gaze continues for longer than the configured threshold, triggers an intervention video.

At the end of the session, it counts the number of doomscrolling incidents and send a report through WhatsApp Web automation.

## System Requirements

Currently intended for: Windows 10, Windows 11.

A laptop/desktop with a working webcam is required.

Python 3.10 or later recommended.

VLC Media Player: Install VLC from the official website.

MicrosoftEdge for whatsapp web automation.

## 1. Model

Download the Face Landmarker model from the official MediaPipe documentation/model resources:

https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker

Put it here:

models/face_landmarker.task

## 2. Intervention video

Put ANY compatible video here:

assets/video.mp4

The video is played from the beginning to the end. Looking back up does NOT close the video.

---

## How It Works

1. Tracks eye movement: The webcam uses MediaPipe to track facial and iris landmarks and detect prolonged downward gaze.
2. Detects doomscrolling: If the user looks downward continuously for a configured time, FocusGuard considers it a doomscrolling event and triggers the intervention video.
3. Reports the session: Each event is counted, and when the user exits, the total count can be sent through WhatsApp Web.

## Installation

1. Clone the repository

git clone https://github.com/Shayonasys/.git

2. Install dependencies

pip install -r requirements.txt

4. Run app.py

python app.py

## Configuration

change the configuration values in config.py for customization.

LOOKING_DOWN_THRESHOLD = 0.62
Controls how much downward iris movement is required.

TIMER = 8.0
How long the user must continuously look down before triggering.
