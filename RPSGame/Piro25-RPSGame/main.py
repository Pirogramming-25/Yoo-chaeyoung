import math
import time
import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from webcam import cv2_stream
from visualization import draw_manual, print_RSP_result


def get_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def classify_rsp(landmarks):
    wrist = landmarks[0]
    
    finger_indices = [(8, 6), (12, 10), (16, 14), (20, 18)]
    extended = []

    for tip_idx, pip_idx in finger_indices:
        tip_dist = get_distance(landmarks[tip_idx], wrist)
        pip_dist = get_distance(landmarks[pip_idx], wrist)
        extended.append(tip_dist > pip_dist)

    count = sum(extended)

    if count == 0:
        return 0
    elif count == 2 and extended[0] and extended[1]:
        return 2
    elif count == 4:
        return 1
    else:
        return None


if __name__ == "__main__":
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        running_mode=vision.RunningMode.IMAGE
    )
    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv2_stream()
    if cap is not None:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv.flip(frame, 1)
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            detection_result = detector.detect(mp_image)

            if detection_result and detection_result.hand_landmarks:
                for hand_landmarks in detection_result.hand_landmarks:
                    draw_manual(frame, detection_result)
                    rps_result = classify_rsp(hand_landmarks)
                    print_RSP_result(frame, rps_result)

            cv.imshow('RPS Game', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()