import RPi.GPIO as GPIO
from display import i2c_test

from picamera2 import Picamera2
import cv2
import numpy as np
from imutils.video import VideoStream
import time

# Raspberry Pi 카메라 초기화
pi_cam = Picamera2()
pi_cam.configure(pi_cam.create_preview_configuration(main={"size": (320, 240)}))
pi_cam.start()


# GPIO 설정 초기화
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
# GPIO 핀 번호
SWITCH_1 = 23
SWITCH_2 = 24
SWITCH_3 = 25

SWITCH_UP = 9
SWITCH_DOWN = 10

# 스위치 풀다운저항 설정
GPIO.setup(SWITCH_1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SWITCH_2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SWITCH_3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.setup(SWITCH_UP, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SWITCH_DOWN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# 전역 변수
switch_1_state = ( GPIO.input(SWITCH_1) == GPIO.HIGH )
switch_2_state = ( GPIO.input(SWITCH_2) == GPIO.HIGH )
switch_3_state = ( GPIO.input(SWITCH_3) == GPIO.HIGH )

# 콜백 함수
def switch_1_callback(channel):
    global switch_1_state
    switch_1_state = ( GPIO.input(SWITCH_1) == GPIO.HIGH )
    print(f"Switch 1 State Updated to: {switch_1_state}")

def switch_2_callback(channel):
    global switch_2_state
    switch_2_state = ( GPIO.input(SWITCH_2) == GPIO.HIGH )
    print(f"Switch 2 State Updated to: {switch_2_state}")

def switch_3_callback(channel):
    global switch_3_state
    switch_3_state = ( GPIO.input(SWITCH_3) == GPIO.HIGH )
    print(f"Switch 3 State Updated to: {switch_3_state}")

def switch_up_callback(channel):
    # sleep_detect_facemesh.eye_threshold += 0.01
    # print(f"eye threshold updated to: {sleep_detect_facemesh.eye_threshold:.2f}")
    i2c_test()

def switch_down_callback(channel):
    # sleep_detect_facemesh.eye_threshold -= 0.01
    # print(f"eye threshold updated to: {sleep_detect_facemesh.eye_threshold:.2f}")
    i2c_test()

# 기존이벤트 제거
GPIO.remove_event_detect(SWITCH_1)
GPIO.remove_event_detect(SWITCH_2)
GPIO.remove_event_detect(SWITCH_3)

GPIO.remove_event_detect(SWITCH_UP)
GPIO.remove_event_detect(SWITCH_DOWN)

# 이벤트 감지 추가
GPIO.add_event_detect(SWITCH_1, GPIO.BOTH, callback=switch_1_callback, bouncetime=200)
GPIO.add_event_detect(SWITCH_2, GPIO.BOTH, callback=switch_2_callback, bouncetime=200)
GPIO.add_event_detect(SWITCH_3, GPIO.BOTH, callback=switch_3_callback, bouncetime=200)

GPIO.add_event_detect(SWITCH_UP, GPIO.RISING, callback=switch_up_callback, bouncetime=100)
GPIO.add_event_detect(SWITCH_DOWN, GPIO.RISING, callback=switch_down_callback, bouncetime=100)

while True:
    # Raspberry Pi 카메라에서 프레임 읽기
    pi_frame = pi_cam.capture_array()
    pi_frame = cv2.cvtColor(pi_frame, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR 포맷 사용

    cv2.imshow("Raspberry Pi Camera", pi_frame)

    # 'q'를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 종료
pi_cam.stop()
cv2.destroyAllWindows()
