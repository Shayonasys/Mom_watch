import multiprocessing as mp
import cv2
import time
from pathlib import Path

from config import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    MODEL_PATH,
    VIDEO_PATH,
    LOOKING_DOWN_THRESHOLD,
    TIMER,
)

from vision.face_detector import FaceDetector
from vision.iris_tracker import IrisTracker
from intervention.video_player import VideoPlayer
from whatsapp import send_whatsapp_message


def draw_text(
    frame,
    text,
    position,
    scale=0.65,
    thickness=2,
):

    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        (255, 255, 255),
        thickness,
        cv2.LINE_AA,
    )


def main():

    if not Path(MODEL_PATH).exists():
        print(
            "ERROR: Face Landmarker model not found:"
            "Place face_landmarker.task inside the models folder."
        )
        print(MODEL_PATH)

        return

    if not Path(VIDEO_PATH).exists():
        print(
            "ERROR: Intervention video not found:"
        )
        print(VIDEO_PATH)

        return

    face_detector = FaceDetector()
    iris_tracker = IrisTracker()
    video_player = VideoPlayer(VIDEO_PATH)
    camera = cv2.VideoCapture(CAMERA_INDEX)

    if not camera.isOpened():
        print(
            "ERROR: Could not open webcam."
        )
        face_detector.close()
        
        return

    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        CAMERA_WIDTH,
    )
    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        CAMERA_HEIGHT,
    )

    scroll_start = None
    doomscroll_count=0

    print("Monitoring started")

    try:

        while True:

            success, frame = camera.read()

            if not success:
                continue

            # Mirror webcam
            frame = cv2.flip(
                frame,
                1,
            )

            current = time.time()

            video_player.update()

            result = face_detector.detect(frame)

            face_landmark_points = (result.face_landmarks)

            # Face found
            if face_landmark_points:

                landmarks = (
                    face_landmark_points[0]
                )

                # return landmarks directly as a list.
                if hasattr(
                    landmarks,
                    "landmark"
                ):
                    landmarks = (
                        landmarks.landmark
                    )

                avg_ratio = (
                    iris_tracker.process(
                        landmarks
                    )
                )

                if avg_ratio is not None:
                    
                    is_looking_down = (
                        avg_ratio
                        < LOOKING_DOWN_THRESHOLD
                    )
                    # draw_text(frame, f"Iris ratio: {avg_ratio:.2f}", (20, 40))

                    if is_looking_down:

                        draw_text(frame, "LOOKING DOWN", (20, 75),)

                        if scroll_start is None:
                            scroll_start = (current)
                        elapsed = (current - scroll_start)
                        # draw_text(frame, f"Down time: {elapsed:.1f}s", (20, 110),)


                        # TRIGGER VIDEO
                        if elapsed >= TIMER:

                            if not video_player.is_playing():
                                doomscroll_count+=1
                                video_player.play()

                    else:
                        scroll_start = None
                        # draw_text( frame, "FOCUSED", (20, 75),)
                        

            # No face found
            else:
                scroll_start = None
                # draw_text( frame, "FACE NOT DETECTED", (20, 40),)

            cv2.imshow(
                "DECTECTOR",
                frame,
            )
            # Esc 
            key = cv2.waitKey(1)
            if key == 27:
                break

    finally:

        camera.release()

        face_detector.close()

        video_player.close()

        if doomscroll_count>0:
            print("Doomscrolling detected!")
            print(f"Doomscroll count: {doomscroll_count}")

        cv2.destroyAllWindows()

        send_whatsapp_message(
            "Mom",
            "⚠️Message from MOMwatch\n"
            "\nDoomscrolling detected\ncount:"
            f"{doomscroll_count}\n"
        )


if __name__ == "__main__":

    mp.freeze_support()

    main()