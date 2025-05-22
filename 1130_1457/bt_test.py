import dlib
import cv2
from imutils import face_utils
import time
import RPi.GPIO as GPIO
import bluetooth

# GPIO setup
GPIO.setmode(GPIO.BCM)
LED_pin = 2
GPIO.setup(LED_pin, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.output(LED_pin, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
time.sleep(1)

# Create Bluetooth socket and set up connection
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
arduino_mac = "98:DA:60:04:F9:81"  # Replace with your Arduino's MAC address
port = 1

# Bluetooth connection function
def connect_bluetooth():
    connected = False
    while not connected:
        try:
            print("Attempting to connect to Arduino...")
            sock.connect((arduino_mac, port))
            print("Connected to Arduino")
            connected = True
        except bluetooth.btcommon.BluetoothError as e:
            print(f"Connection failed: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

connect_bluetooth()  # Connect to Arduino via Bluetooth

# Load face landmark model
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

# Start camera capture
cap = cv2.VideoCapture(0)
start_time = time.time()
sleep_stack = 0

try:
    while True:
        _, image = cap.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        
        # Process each detected face in the frame
        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            for (x, y) in shape:
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
                
        # Check for drowsiness every second
        if time.time() - start_time >= 1:
            left_eye = shape[36:42]
            left_eye_length = cv2.norm(left_eye[0] - left_eye[3])
            left_eye_height1 = cv2.norm(left_eye[1] - left_eye[5])
            left_eye_height2 = cv2.norm(left_eye[2] - left_eye[4])
            print(f"left_eye_length: {left_eye_length}, height1: {left_eye_height1}, height2: {left_eye_height2}")

            # Drowsiness detection condition
            if (left_eye_height1 / left_eye_length < 0.18 and left_eye_height2 / left_eye_length < 0.18):
                sleep_stack += 1
                print("eye closed!")
                
                if sleep_stack >= 3:  # If drowsiness threshold is met
                    GPIO.output(17, GPIO.HIGH)  # Set GPIO17 to HIGH
                    print("Drowsiness detected: GPIO17 set to HIGH")
                    
                    # Send signal to Arduino
                    try:
                        sock.send("Activate")
                        print("Sent: Activate to Arduino")
                    except bluetooth.btcommon.BluetoothError as e:
                        print(f"Bluetooth send error: {e}")
                        connect_bluetooth()  # Reconnect if an error occurs
                    
                    time.sleep(2)  # Wait to allow motor operation
                    GPIO.output(17, GPIO.LOW)  # Reset GPIO17
                    print("GPIO17 set to LOW")
            
            else:
                sleep_stack = 0

            print("sleep stack:", sleep_stack)
            cv2.imshow("Output", image) # for hotspot?
            start_time = time.time()

        # Exit on pressing ESC
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()

finally:
    # Clean up GPIO and close Bluetooth socket
    GPIO.output(2, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    sock.close()
    GPIO.cleanup()
    print("GPIO cleaned up and Bluetooth connection closed")
