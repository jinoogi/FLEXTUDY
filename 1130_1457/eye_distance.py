import dlib
import cv2
from imutils import face_utils  # 이 줄을 추가하세요
import time
import RPi.GPIO as GPIO     # 라즈베리파이 GPIO 관련 모듈을 불러옴

GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정

### 이부분은 아두이노 코딩의 setup()에 해당합니다
LED_pin = 2                     # LED 핀은 라즈베리파이 GPIO 2번핀으로 
GPIO.setup(LED_pin, GPIO.OUT)   # LED 핀을 출력으로 설정
GPIO.setup(17, GPIO.OUT)
GPIO.output(LED_pin, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
time.sleep(1)

p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

cap = cv2.VideoCapture(0)

start_time = time.time()
sleep_stack = 0
try:
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
                
        if time.time() - start_time >= 1:
            left_eye = shape[36:42]
            left_eye_length = cv2.norm(left_eye[0] - left_eye[3])
            left_eye_height1 = cv2.norm(left_eye[1] - left_eye[5])
            left_eye_height2 = cv2.norm(left_eye[2] - left_eye[4])
            print(f"left_eye_length: {left_eye_length}, height1: {left_eye_height1}, height2: {left_eye_height2}")

            if( left_eye_height1/left_eye_length < 0.18 and left_eye_height1/left_eye_length < 0.18 ):
                sleep_stack+=1
                print("eye closed!")
                if(sleep_stack >= 3):
                    GPIO.output(17, GPIO.HIGH) # LED 핀에 HIGH 신호 인가(LED 켜짐)
                    time.sleep(2)                   
                    GPIO.output(17, GPIO.LOW)  
            
            else:
                sleep_stack = 0

            print("sleep stack:",sleep_stack)
            cv2.imshow("Output", image)
            start_time = time.time()

        # 5밀리초 기다리고 비트연산으로 하위 8비트값만 추출. 0이면 무한대기
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

### 이부분은 반드시 추가해주셔야 합니다.
finally:                                # try 구문이 종료되면
    GPIO.output(2, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    time.sleep(1)
    GPIO.cleanup()                      # GPIO 핀들을 초기화