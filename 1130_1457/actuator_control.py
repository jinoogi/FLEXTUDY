import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# GPIO 핀 번호
CW_PIN = 2
CCW_PIN = 3
STOP_PIN = 4

# 출력설정
GPIO.setup(CW_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(CCW_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(STOP_PIN, GPIO.OUT, initial=GPIO.LOW)

def lift_table():
    GPIO.output(CW_PIN,GPIO.HIGH)
    time.sleep(5)
    GPIO.output(CW_PIN,GPIO.LOW)