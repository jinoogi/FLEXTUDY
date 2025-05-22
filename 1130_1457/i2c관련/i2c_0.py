import busio
import digitalio
from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C

# I2C-0 핀 수동 설정
i2c = busio.I2C(scl=digitalio.DigitalInOut(28), sda=digitalio.DigitalInOut(27))  # GPIO28(SCL0), GPIO27(SDA0)

# LCD 설정
lcd_columns = 16
lcd_rows = 2
lcd_address = 0x27  # I2C 주소 확인 필요 (sudo i2cdetect -y 0)
lcd = Character_LCD_I2C(i2c, lcd_columns, lcd_rows, address=lcd_address)

# 메시지 출력
lcd.message = "Hello, I2C-0!"
