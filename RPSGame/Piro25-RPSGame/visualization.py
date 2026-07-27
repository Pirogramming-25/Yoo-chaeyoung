import cv2 as cv

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (0, 9), (9, 10), (10, 11), (11, 12),
    (0, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17)
]


def draw_manual(image, detection_result):
    if detection_result is None or not detection_result.hand_landmarks:
        return image

    h, w, _ = image.shape

    for hand_landmarks in detection_result.hand_landmarks:
        points = []
        for lm in hand_landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            points.append((cx, cy))

        for start_idx, end_idx in HAND_CONNECTIONS:
            cv.line(image, points[start_idx], points[end_idx], (0, 255, 0), 2)

        for pt in points:
            cv.circle(image, pt, 5, (0, 0, 255), cv.FILLED)
            
    return image


def print_RSP_result(image, rps_result):
    if rps_result is None or rps_result not in [0, 1, 2]:
        text = ""
    else:
        text_list = ["Rock", "Paper", "Scissors"]
        text = text_list[rps_result]
    
    font = cv.FONT_HERSHEY_SIMPLEX
    org = (50, 100)
    font_scale = 2
    color = (255, 255, 255)
    thickness = 3

    cv.putText(image, text, org, font, font_scale, color, thickness, cv.LINE_AA)

    return image