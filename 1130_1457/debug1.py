import RPi.GPIO as GPIO     # 라즈베리파이 GPIO 관련 모듈을 불러옴
import time                 # 시간관련 모듈을 불러옴

GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정

### 이부분은 아두이노 코딩의 setup()에 해당합니다
CW_pin = 2                    
CCW_pin = 3
STOP_pin = 4
GPIO.setup(CW_pin, GPIO.OUT)  
GPIO.setup(CCW_pin, GPIO.OUT)
GPIO.setup(STOP_pin, GPIO.OUT)  

# 테스트용 
GPIO.output(CW_pin, GPIO.HIGH) 
GPIO.output(CCW_pin, GPIO.HIGH) 
GPIO.output(STOP_pin, GPIO.HIGH) 


try:                                    
    while True:          
        GPIO.output(CW_pin, GPIO.LOW) 
        time.sleep(1)   
        GPIO.output(CW_pin, GPIO.HIGH)                
        GPIO.output(CCW_pin, GPIO.LOW)  
        time.sleep(1)                   
        GPIO.output(CCW_pin, GPIO.HIGH)    
        GPIO.output(STOP_pin, GPIO.LOW)  
        time.sleep(1)                   
        GPIO.output(STOP_pin, GPIO.HIGH)    

        GPIO.output(CW_pin, GPIO.HIGH) 
        GPIO.output(CCW_pin, GPIO.HIGH) 
        GPIO.output(STOP_pin, GPIO.HIGH) 
        time.sleep(1)      

### 이부분은 반드시 추가해주셔야 합니다.
finally:                                # try 구문이 종료되면
    GPIO.output(CW_pin, GPIO.HIGH) 
    GPIO.output(CCW_pin, GPIO.HIGH) 
    GPIO.output(STOP_pin, GPIO.HIGH) 
    GPIO.cleanup()                      # GPIO 핀들을 초기화