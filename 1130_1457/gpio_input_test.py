import RPi.GPIO as GPIO

BUTTON_PIN = 16
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
print("Button has been released")

GPIO.cleanup()
