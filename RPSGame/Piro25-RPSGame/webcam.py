# cv를 통한 라이브스트림 비디오 캡쳐 관련 레거시 코드
# https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html


## Capture Video from Camera ##

import cv2 as cv

def cv2_stream():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return None
    return cap

if __name__ == "__main__":
    cap = cv2_stream()
    if cap is not None:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow('frame', gray)
            if cv.waitKey(1) == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()