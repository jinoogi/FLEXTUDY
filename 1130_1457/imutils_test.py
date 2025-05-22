from imutils.video import VideoStream
import cv2
import time

# 스트림 시작
vs = VideoStream(src=2).start()
time.sleep(2.0)  # 카메라 초기화 대기

while True:
    # 가장 최근 프레임 읽기
    frame = vs.read()
    if frame is None:
        print("빈 프레임")
        continue

    # 프레임 처리
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 스트림 정리
vs.stop()
cv2.destroyAllWindows()
