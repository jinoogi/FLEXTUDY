import smbus
import time
from RPLCD.i2c import CharLCD

# I2C 주소 및 LCD 설정
lcd = CharLCD('PCF8574', 0x27, rows=2, cols=16)  # 0x27은 LCD의 I2C 주소입니다. 필요하면 변경하세요.

# LCD 초기화 및 메시지 출력
def main():
    try:
        lcd.clear()
        lcd.write_string("Hello, World!")  # 첫 줄에 출력
        time.sleep(2)  # 2초 대기

        lcd.cursor_pos = (1, 0)  # 두 번째 줄 첫 번째 칸으로 이동
        lcd.write_string("Raspberry Pi")
        time.sleep(2)  # 2초 대기

    except KeyboardInterrupt:
        print("프로그램 종료")
    finally:
        lcd.clear()  # LCD 초기화

if __name__ == "__main__":
    main()
