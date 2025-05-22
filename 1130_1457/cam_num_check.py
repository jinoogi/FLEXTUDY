import cv2

cap = cv2.VideoCapture(1)  # /dev/video2
if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 가져올 수 없습니다.")
        break

    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'를 눌러 종료
        break

cap.release()
cv2.destroyAllWindows()
