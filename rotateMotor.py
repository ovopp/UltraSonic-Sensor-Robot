import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)           # do not show any warnings

SERVO = 18
TRIGGER = 23
ECHO = 24

GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(TRIGGER,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(16,GPIO.OUT)            # initialize GPIO Pins as an output.
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

p = GPIO.PWM(SERVO, 50) # GPIO 18 for PWM with 50Hz
p.start(2.5)

def ledController(x):
    GPIO.output(16,0) #DATA PIN set to 0
    time.sleep(0.001)
    # Resets the memory in the LEDs
    for i in range(4):    
        GPIO.output(20,1)            # pull CLOCK pin high
        time.sleep(0.001)
        GPIO.output(20,0) 
    
    GPIO.output(16, 1)  #DATA PIN set to 1
    time.sleep(0.001)
    # Sets the number of LEDs to be turned on
    for j in range(x):            # loop for counting up x times    
        GPIO.output(20,1)            # pull CLOCK pin high
        time.sleep(0.001)
        GPIO.output(20,0)            # pull CLOCK pin down, to send a rising edge
    
    GPIO.output(21,1)            # pull up the SHIFT pin
    time.sleep(0.001)
    GPIO.output(21,0)            # pull down the SHIFT pin


def distance(i):
  p.ChangeDutyCycle(2.5 + 1/6 * i)
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
  if (distance < 15):
    ledController(2)
  elif (distance <30):
    ledController(3)
  elif (distance < 45):
    ledController(4)
  else:
    ledController(5)
  print("Angle: ", i * 3)
  print("Distance : %.1f cm" % distance)

def distanceBack(i):
  p.ChangeDutyCycle(12.5 - 1/6 * i)
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
  if (distance < 15):
    ledController(2)
  elif (distance <30):
    ledController(3)
  elif (distance < 45):
    ledController(4)
  else:
    ledController(5)
  print("Angle: ", i * 3)
  print("Distance : %.1f cm" % distance)

try:
  while True:
    for i in range(60):
      p.ChangeDutyCycle(2.5)
      distance(i)
    for i in range(60):
      p.ChangeDutyCycle(12.5)
      distanceBack(i)

except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()



