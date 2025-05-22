import smbus
import time
from RPLCD.i2c import CharLCD
# import sleep_detect_facemesh


# I2C 주소 및 LCD 설정
lcd = CharLCD('PCF8574', 0x27, rows=2, cols=16)  # 0x27은 LCD의 I2C 주소입니다. 필요하면 변경하세요.
# lcd.backlight_enabled = False  # 백라이트 끄기
# LCD 초기화 및 메시지 출력

# def display_eye_threshold():
#     try:
#         lcd.clear()
#         lcd.write_string("threshold update")
#         lcd.cursor_pos = (1, 0)
#         lcd.write_string(f"to:{sleep_detect_facemesh.eye_threshold:.2f}")
#         time.sleep(0.5)
#     except TimeoutError as e:
#         print(f"I2C Timeout: {e}")

def i2c_test():
    try:
        lcd.clear()
        lcd.write_string("i2c test")
        lcd.cursor_pos = (1, 0)
        lcd.write_string(f"pass")
        time.sleep(0.5)
    except TimeoutError as e:
        print(f"I2C Timeout: {e}")


# display_eye_threshold()
