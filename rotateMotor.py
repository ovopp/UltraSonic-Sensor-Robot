import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

SERVO = 18
TRIGGER = 23
ECHO = 24

GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(TRIGGER,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

p = GPIO.PWM(SERVO, 50) # GPIO 18 for PWM with 50Hz
p.start(2.5)


def distance(i):
  p.ChangeDutyCycle(2.5 + 0.5 * i)
  GPIO.output(TRIGGER, False)
  time.sleep(0.06)
  GPIO.output(TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(TRIGGER, False)
  while GPIO.input(ECHO)==0:
    start = time.time()
  while GPIO.input(ECHO)==1:
    stop = time.time()
  elapsed = stop-start
  distance = (elapsed * 34000.0) / 2
  return distance

try:
  for i in range(20):
    distance(i)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()



