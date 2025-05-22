from picamera2 import Picamera2
import cv2
import numpy as np
from imutils.video import VideoStream
import time

# Raspberry Pi 카메라 초기화
pi_cam = Picamera2()
pi_cam.configure(pi_cam.create_preview_configuration(main={"size": (320, 240)}))
pi_cam.start()

# USB 웹캠 초기화
usb_cam = VideoStream(src='/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_77FC6BDF-video-index0').start()  # USB 웹캠 
time.sleep(2)  # 초기화 대기

while True:
    # Raspberry Pi 카메라에서 프레임 읽기
    pi_frame = pi_cam.capture_array()
    pi_frame = cv2.cvtColor(pi_frame, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR 포맷 사용

    # USB 웹캠에서 프레임 읽기
    usb_frame = usb_cam.read()

    if usb_frame is not None:
        # 두 카메라 화면을 동시에 출력
        cv2.imshow("Raspberry Pi Camera", pi_frame)
        cv2.imshow("USB Camera", usb_frame)

    # 'q'를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 종료
pi_cam.stop()
usb_cam.stop()
cv2.destroyAllWindows()
