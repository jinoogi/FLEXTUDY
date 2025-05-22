import RPi.GPIO as GPIO
import sleep_detect_facemesh
from display import i2c_test

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
    sleep_detect_facemesh.eye_threshold += 0.01
    print(f"eye threshold updated to: {sleep_detect_facemesh.eye_threshold:.2f}")
    i2c_test()

def switch_down_callback(channel):
    sleep_detect_facemesh.eye_threshold -= 0.01
    print(f"eye threshold updated to: {sleep_detect_facemesh.eye_threshold:.2f}")
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

GPIO.add_event_detect(SWITCH_UP, GPIO.RISING, callback=switch_up_callback, bouncetime=1000)
GPIO.add_event_detect(SWITCH_DOWN, GPIO.RISING, callback=switch_down_callback, bouncetime=1000)

import bluetooth
import time
import atexit

# 블루투스 소켓 생성
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

BLUETOOTH_CONNECT_BUTTON = 22
GPIO.setup(BLUETOOTH_CONNECT_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
# 처음엔 연결안됐다고 초기화
is_bluetooth_connected = False

def TRY_BLUETOOTH_CONNECT(channel):
    global sock, is_bluetooth_connected

    # 기존 소켓 닫기
    if 'sock' in globals() and sock is not None:
        try:
            sock.close()
            print("Previous socket closed.")
        except Exception as e:
            print(f"Error while closing socket: {e}")

    # 새 소켓 생성
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    
    try:
        # sock.close()
        sock.connect(("98:DA:60:04:F9:81", 1))
        is_bluetooth_connected = True
        print("Connected to HC-06")
    except Exception as e:
        is_bluetooth_connected = False
        print(e)
        print(f"Socket status: {sock}")
        print("Connection failed:")    

GPIO.remove_event_detect(BLUETOOTH_CONNECT_BUTTON)
GPIO.add_event_detect(BLUETOOTH_CONNECT_BUTTON, GPIO.RISING, callback=TRY_BLUETOOTH_CONNECT, bouncetime=200)

def close_bluetooth_socket():
    global sock, is_bluetooth_connected
    if sock:
        print("Closing Bluetooth socket...")
        sock.close()
        is_bluetooth_connected = False

# 코드종료시 소켓닫고 연결여부 False로 설정
atexit.register(close_bluetooth_socket)