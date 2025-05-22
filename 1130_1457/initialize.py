import RPi.GPIO as GPIO   
import time

GPIO.setmode(GPIO.BCM) 

CW_pin = 2                     # LED 핀은 라즈베리파이 GPIO 2번핀으로 
CCW_pin = 17
GPIO.setup(CW_pin, GPIO.OUT,initial=GPIO.LOW)   # LED 핀을 출력으로 설정
GPIO.setup(CCW_pin, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(CCW_pin, GPIO.HIGH)
time.sleep(4) 

GPIO.output(CW_pin, GPIO.LOW)
GPIO.output(CCW_pin, GPIO.LOW)
time.sleep(1)
GPIO.cleanup() 