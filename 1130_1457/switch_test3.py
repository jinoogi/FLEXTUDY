import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
BLUETOOTH_CONNECT_BUTTON = 22  # 버튼이 연결된 핀 번호

# GPIO 초기화
GPIO.setmode(GPIO.BCM)  # 핀 넘버링 방식 설정 (BCM 모드)
GPIO.setup(BLUETOOTH_CONNECT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 풀다운 저항 설정

print("Press the button to see the status...")

try:
    # 버튼 상태를 반복적으로 읽음
    while True:
        button_state = GPIO.input(BLUETOOTH_CONNECT_BUTTON)  # 버튼 상태 읽기
        print(f"Button State: {'PRESSED' if button_state else 'RELEASED'}")
        time.sleep(0.1)  # 0.1초 간격으로 상태 확인
except KeyboardInterrupt:
    print("Exiting program...")

finally:
    GPIO.cleanup()  # GPIO 설정 해제
