import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# 핀 번호 설정
OUT_pin = 22
IN_pin = 23

# 핀 설정: IN 핀은 내부 풀다운 저항 활성화
GPIO.setup(OUT_pin, GPIO.OUT)
GPIO.setup(IN_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    GPIO.output(OUT_pin, GPIO.HIGH)
    print("OUT 핀을 HIGH로 설정했습니다.")

    start_time = time.time()
    while time.time() - start_time < 10:  # 10초 동안 루프
        if GPIO.input(IN_pin) == GPIO.HIGH:
            print("스위치 ON (HIGH)")
        else:
            print("스위치 OFF (LOW)")
        time.sleep(0.5)

finally:
    GPIO.output(OUT_pin, GPIO.LOW)
    GPIO.cleanup()
    print("GPIO 정리 후 종료")
