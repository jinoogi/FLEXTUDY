import dlib
import cv2
from imutils import face_utils
import time
import RPi.GPIO as GPIO
import bluetooth

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Set the GPIO mode to BCM
LED_pin = 2  # Pin for LED
GPIO.setup(LED_pin, GPIO.OUT)  # Set LED pin as output
GPIO.setup(17, GPIO.OUT)  # Pin 17 setup for drowsiness detection
GPIO.output(LED_pin, GPIO.LOW)  # Initialize LED to OFF
GPIO.output(17, GPIO.LOW)  # Initialize pin 17 to LOW
time.sleep(1)  # Delay to ensure setup is stable

# Create Bluetooth socket and set up connection
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)  # Initialize Bluetooth socket for RFCOMM
arduino_mac = "98:DA:60:04:F9:81"  # Replace with your Arduino's MAC address
port = 1  # Bluetooth port

# Bluetooth connection function
def connect_bluetooth():
    """Attempt to connect to the Arduino via Bluetooth with retries if connection fails."""
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
            time.sleep(5)  # Retry after 5 seconds if connection fails

connect_bluetooth()  # Connect to Arduino via Bluetooth

# Load face landmark model
p = "shape_predictor_68_face_landmarks.dat"  # Path to facial landmark model
detector = dlib.get_frontal_face_detector()  # Initialize face detector
predictor = dlib.shape_predictor(p)  # Initialize facial landmark predictor

# Start camera capture
cap = cv2.VideoCapture(0)  # Start video capture from camera
start_time = time.time()  # Timer to track time intervals
sleep_stack = 0  # Counter for drowsiness events

try:
    while True:
        _, image = cap.read()  # Capture frame from camera
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
        rects = detector(gray, 0)  # Detect faces in the grayscale frame
        
        # Process each detected face in the frame
        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)  # Predict facial landmarks for the detected face
            shape = face_utils.shape_to_np(shape)  # Convert landmarks to numpy array
            for (x, y) in shape:
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)  # Draw circles on each landmark
                
        # Check for drowsiness every second
        if time.time() - start_time >= 1:
            left_eye = shape[36:42]  # Extract points for left eye
            left_eye_length = cv2.norm(left_eye[0] - left_eye[3])  # Calculate left eye width
            left_eye_height1 = cv2.norm(left_eye[1] - left_eye[5])  # Height between top and bottom points
            left_eye_height2 = cv2.norm(left_eye[2] - left_eye[4])  # Height between inner top and bottom points
            print(f"left_eye_length: {left_eye_length}, height1: {left_eye_height1}, height2: {left_eye_height2}")

            # Drowsiness detection condition
            if (left_eye_height1 / left_eye_length < 0.18 and left_eye_height2 / left_eye_length < 0.18):
                sleep_stack += 1
                print("eye closed!")
                
                # If drowsiness threshold is met, activate alert
                if sleep_stack >= 3:  # Threshold for triggering drowsiness alert
                    GPIO.output(17, GPIO.HIGH)  # Set GPIO17 to HIGH
                    print("Drowsiness detected: GPIO17 set to HIGH")
                    
                    # Send signal to Arduino via Bluetooth
                    try:
                        sock.send("Sleep detected! Actiavte Chair Motor")  # Send "Activate" signal to Arduino
                        print("Rasbpi Sent: Activate to Motor!!!!!")
                    except bluetooth.btcommon.BluetoothError as e:
                        print(f"Bluetooth send error: {e}")
                        connect_bluetooth()  # Reconnect if Bluetooth error occurs
                    
                    time.sleep(2)  # Delay to allow motor operation
                    GPIO.output(17, GPIO.LOW)  # Reset GPIO17 to LOW
                    print("GPIO17 set to LOW")
            
            else:
                sleep_stack = 0  # Reset counter if eyes are not closed

            print("sleep stack:", sleep_stack)
            cv2.imshow("Output", image)  # Display the frame
            start_time = time.time()  # Reset the timer for next interval

        # Exit on pressing ESC
        k = cv2.waitKey(5) & 0xFF
        if k == 27:  # Exit loop if ESC key is pressed
            break

    cv2.destroyAllWindows()  # Close OpenCV windows
    cap.release()  # Release video capture

finally:
    # Clean up GPIO and close Bluetooth socket
    GPIO.output(2, GPIO.LOW)  # Turn off LED
    GPIO.output(17, GPIO.LOW)  # Reset GPIO17
    sock.close()  # Close Bluetooth socket
    GPIO.cleanup()  # Clean up GPIO setup
    print("GPIO cleaned up and Bluetooth connection closed")
