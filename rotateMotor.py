import RPi.GPIO as GPIO
import time

SERVO = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT)

p = GPIO.PWM(SERVO, 50) # GPIO 18 for PWM with 50Hz
p.start(2.5)
try:
  while True:
    p.ChangeDutyCycle(2.5)
    time.sleep(1)
    p.ChangeDutyCycle(5)
    time.sleep(1)
    p.ChangeDutyCycle(7.5)
    time.sleep(1)
    p.ChangeDutyCycle(10)
    time.sleep(1)
    p.ChangeDutyCycle(12.5)
    time.sleep(1)
    p.ChangeDutyCycle(10)
    time.sleep(1)
    p.ChangeDutyCycle(7.5)
    time.sleep(1)
    p.ChangeDutyCycle(5)
    time.sleep(1)
    p.ChangeDutyCycle(2.5)
    time.sleep(1)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()