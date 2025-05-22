import RPi.GPIO as GPIO

# GPIO 핀 번호
SIGNAL_OUT = 22
SWITCH_1 = 23

# 전역 변수
switch_1_state = False

# GPIO 설정 함수
def setup_gpio():
    global switch_1_state
    GPIO.setmode(GPIO.BCM)

    # 신호용 전원핀 설정, HIGH 출력
    GPIO.setup(SIGNAL_OUT, GPIO.OUT)
    GPIO.output(SIGNAL_OUT, GPIO.HIGH)

    # 스위치 풀다운저항 설정
    GPIO.setup(SWITCH_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # 스위치 초기 상태
    switch_1_state = (GPIO.input(SWITCH_1) == GPIO.HIGH)

    # 기존 이벤트 제거 및 이벤트 감지 추가
    if GPIO.event_detected(SWITCH_1):
        GPIO.remove_event_detect(SWITCH_1)

    GPIO.add_event_detect(SWITCH_1, GPIO.FALLING, callback=switch_1_callback, bouncetime=200)

# 콜백 함수
def switch_1_callback(channel):
    global switch_1_state
    switch_1_state = (GPIO.input(SWITCH_1) == GPIO.HIGH)
    print(f"Switch 1 State Updated to: {switch_1_state}")

# GPIO 정리 함수
def cleanup_gpio():
    GPIO.cleanup()
