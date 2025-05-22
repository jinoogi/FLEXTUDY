import cv2
from imutils.video import VideoStream
from picamera2 import Picamera2
from combine_image import combine_image
import mediapipe as mp

# BlazePose 모델 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 상체 웹캠 초기화
upper_cam = VideoStream(src='/dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._HD20W_SN0001-video-index0').start()
# 하체 카메라 모듈 초기화
pi_cam = Picamera2()
pi_cam.configure(pi_cam.create_preview_configuration(main={"size": (320, 240)}))
pi_cam.start()

while True:
    # 상체 이미지 읽기
    upper_image = upper_cam.read()
    # 하체 이미지 읽기
    lower_image = pi_cam.capture_array()
    lower_image = cv2.cvtColor(lower_image, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR 포맷 사용

    # 두 이미지를 합치기
    combined_image = combine_image(upper_image, lower_image)

    # BGR 이미지를 RGB로 변환
    combined_image_rgb = cv2.cvtColor(combined_image, cv2.COLOR_BGR2RGB)
    results = pose.process(combined_image_rgb)

    # 랜드마크가 감지되면 이미지에 그리기
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            combined_image, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS
        )

    # 합쳐진 이미지 표시
    cv2.imshow('Combined Video', combined_image)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 해제
upper_cam.stop()
pi_cam.stop()
cv2.destroyAllWindows()