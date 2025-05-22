import dlib
import cv2
from imutils import face_utils  # 이 줄을 추가하세요

p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

cap = cv2.VideoCapture(0)
 
while True:
    _, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    
    # 한 프레임에 여러 사람의 얼굴이 있을 수 있으니까 반복문으로 처리
    for (i, rect) in enumerate(rects):
		    # 랜드마크 점들 추출
        shape = predictor(gray, rect)
        # full_object_detection 객체라서 넘파이배열로 형변환
        shape = face_utils.shape_to_np(shape)
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
            
    cv2.imshow("Output", image)
    # 5밀리초 기다리고 비트연산으로 하위 8비트값만 추출. 0이면 무한대기
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()