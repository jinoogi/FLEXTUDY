#include <SoftwareSerial.h>

// Bluetooth module pins
SoftwareSerial bluetooth(10, 11); // RX, TX pins for HC-06

// Motor driver pins
const int MOTOR_PIN1 = 9; // Motor control pin 1
const int MOTOR_PIN2 = 8; // Motor control pin 2

// Pressure sensor pins
const int FSR_PIN1 = A0; // Left pressure sensor
const int FSR_PIN2 = A1; // Right pressure sensor

// Constants for pressure sensors
const float VCC = 4.98;
const float R_DIV = 1786.0;
const int FORCE_THRESHOLD = 10;

// Posture detection variables
const unsigned long LYING_TIME_THRESHOLD = 3000; // 3 seconds
unsigned long lyingStartTime = 0;
int lyingStack = 0; // Stack counter for lying posture

void setup() {
  // Initialize Serial and Bluetooth
  Serial.begin(9600);
  bluetooth.begin(9600);

  // Initialize pins
  pinMode(MOTOR_PIN1, OUTPUT);
  pinMode(MOTOR_PIN2, OUTPUT);
  pinMode(FSR_PIN1, INPUT);
  pinMode(FSR_PIN2, INPUT);
  stopMotor(); // Ensure motor is stopped at start

  // Initial messages
  Serial.println("System ready.");
  bluetooth.println("Bluetooth ready.");
}

void loop() {
  // Process motor activation commands
  processMotorActivation();

  // Process stack requests and posture updates
  processStackAndRequests();

  delay(100); // Small delay for stability
}

// MotorActivate라는 명령이 들어오면 모터작동
void processMotorActivation() {
  if (bluetooth.available()) {
    String command = bluetooth.readString(); // Read command as string
    if (command.indexOf("MotorActivate") >= 0) {
      Serial.println("Received MotorActivate command.");
      bluetooth.println("Motor activated.");
      startMotorClockwise(); // Activate motor
      delay(10000);           // Run motor for 10 second
      stopMotor();           // Stop motor
    }
  }
}

// Request라는 명령이 들어오면 누운여부 전송
void processStackAndRequests() {

  // Check for request commands
  if (bluetooth.available()) {
    String command = bluetooth.readString(); // Read command as string
    if (command.indexOf("is_lying") >= 0) {
      Serial.println("Received ls_lying command.");
      // Check if posture needs to be updated
      String lying = isLying();
      bluetooth.println(lying);
    }
  }
}

// 기댄여부 확인하고 문자열로 여부반환
String isLying() {
  float force1 = readForce(FSR_PIN1);
  float force2 = readForce(FSR_PIN2);

  if (force1 < FORCE_THRESHOLD && force2 < FORCE_THRESHOLD) {
    return "true";
  } else {
    return "false";
  }
}

void startMotorClockwise() {
  digitalWrite(MOTOR_PIN1, HIGH);
  digitalWrite(MOTOR_PIN2, LOW);
  Serial.println("Motor started (CW).");
}

void stopMotor() {
  digitalWrite(MOTOR_PIN1, LOW);
  digitalWrite(MOTOR_PIN2, LOW);
  Serial.println("Motor stopped.");
}
