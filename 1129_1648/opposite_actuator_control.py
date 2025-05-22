import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# GPIO 핀 번호
CW_PIN = 2
CCW_PIN = 3
STOP_PIN = 4

# 출력설정
GPIO.setup(CW_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(CCW_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(STOP_PIN, GPIO.OUT, initial=GPIO.HIGH)

def lift_table():
    GPIO.output(STOP_PIN,GPIO.HIGH)
    GPIO.output(CCW_PIN,GPIO.HIGH)
    GPIO.output(CW_PIN,GPIO.HIGH)
    GPIO.output(CW_PIN,GPIO.LOW)
    time.sleep(20)
    GPIO.output(STOP_PIN,GPIO.HIGH)
    GPIO.output(CCW_PIN,GPIO.HIGH)
    GPIO.output(CW_PIN,GPIO.HIGH)
    GPIO.output(STOP_PIN,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(STOP_PIN,GPIO.HIGH)

def lower_table():
    GPIO.output(STOP_PIN,GPIO.HIGH)
    GPIO.output(CW_PIN,GPIO.HIGH)
    GPIO.output(CCW_PIN,GPIO.HIGH)
    GPIO.output(CCW_PIN,GPIO.LOW)
    time.sleep(5)
    GPIO.output(STOP_PIN,GPIO.HIGH)
    GPIO.output(CW_PIN,GPIO.HIGH)
    GPIO.output(CCW_PIN,GPIO.HIGH)
    GPIO.output(STOP_PIN,GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(STOP_PIN,GPIO.HIGH)

def stop_table():
    GPIO.output(CCW_PIN,GPIO.HIGH)
    GPIO.output(CW_PIN,GPIO.HIGH)
    GPIO.output(STOP_PIN,GPIO.HIGH)
    GPIO.output(STOP_PIN,GPIO.LOW)

