import RPi.GPIO as GPIO
import time


class Servo:
    def __init__(self):
      
        GPIO.setwarnings(False)
        servoPin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPin, GPIO.OUT)
        position = GPIO.PWM(servoPin, 50)
        position.start(2.5)
        time.sleep(0.6)
        #GPIO.cleanup()
        
    def QrScan():
        GPIO.setwarnings(False)
        servoPin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPin, GPIO.OUT)
        position = GPIO.PWM(servoPin, 50)
        position.start(2.5)
        time.sleep(0.6)
        #GPIO.cleanup()

    def FaceScan():
        GPIO.setwarnings(False)
        servoPin = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPin, GPIO.OUT)
        position = GPIO.PWM(servoPin, 50)
        position.start(6.5)
        time.sleep(0.6)
        #position.start(6.5) # QR-scan, 6.5-> face_recognition
        #position,ChangeDutyCycle(6.5)
        #time.sleep(0.6)
        #GPIO.cleanup()

