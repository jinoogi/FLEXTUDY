import lgpio as lg

# GPIO 핀 번호
SIGNAL_OUT = 22
SWITCH_1 = 23

# 전역 변수
switch_1_state = False

# GPIO 칩 열기
chip = None

# GPIO 설정 함수
def setup_gpio():
    global chip, switch_1_state

    # GPIO 칩 열기
    chip = lg.gpiochip_open(0)  # GPIO 칩 0번 열기

    # 신호용 전원핀 설정, HIGH 출력
    lg.gpio_claim_output(chip, SIGNAL_OUT, 1)  # OUTPUT, 초기 HIGH

    # 스위치 풀다운 저항 설정 및 입력 핀 초기화
    lg.gpio_claim_input(chip, SWITCH_1)  # INPUT 설정

    # 스위치 초기 상태 확인
    switch_1_state = lg.gpio_read(chip, SWITCH_1)
    print(f"Initial Switch State: {switch_1_state}")

    # 이벤트 감지 설정
    lg.callback(chip, SWITCH_1, lg.BOTH_EDGES, switch_1_callback)

# 콜백 함수
def switch_1_callback(chip, gpio, level, tick):
    global switch_1_state
    switch_1_state = lg.gpio_read(chip, SWITCH_1)
    print(f"Switch 1 State Updated to: {switch_1_state} (at tick: {tick})")

# GPIO 정리 함수
def cleanup_gpio():
    global chip
    if chip is not None:
        lg.gpiochip_close(chip)  # GPIO 칩 닫기
