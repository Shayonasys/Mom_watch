from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "face_landmarker.task"

VIDEO_PATH = BASE_DIR / "assets" / "UPLOAD_YOUR_VIDEO.mp4"


CAMERA_INDEX = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920

LOOKING_DOWN_THRESHOLD = 0.25

TIMER = 8.0
