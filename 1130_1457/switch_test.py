import RPi.GPIO as GPIO     # 라즈베리파이 GPIO 관련 모듈을 불러옴
import time

GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정

### 이부분은 아두이노 코딩의 setup()에 해당합니다
OUT_pin = 8                     # LED 핀은 라즈베리파이 GPIO 2번핀으로 
IN_pin = 7
GPIO.setup(OUT_pin, GPIO.OUT)
GPIO.setup(IN_pin, GPIO.IN)

GPIO.output(OUT_pin,GPIO.HIGH)
time.sleep(10)
GPIO.output(OUT_pin,GPIO.LOW)
GPIO.cleanup()