from picamera2 import Picamera2
import cv2

# Raspberry Pi 카메라 초기화
pi_cam = Picamera2()
pi_cam.configure(pi_cam.create_preview_configuration(main={"size": (320, 240)}))
pi_cam.start()

while True:
    # Raspberry Pi 카메라에서 프레임 읽기
    pi_frame = pi_cam.capture_array()
    pi_frame = cv2.cvtColor(pi_frame, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR 포맷 사용

    # 프레임 출력
    cv2.imshow("Raspberry Pi Camera", pi_frame)

    # 'q'를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 종료
pi_cam.stop()
cv2.destroyAllWindows()
