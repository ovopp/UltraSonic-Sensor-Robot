import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIGGER = 23
ECHO = 24
GPIO.setup(TRIGGER,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

try:
  while True:
    # turn off the trigger pin
    GPIO.output(TRIGGER, False)
    time.sleep(2)
    # turn on the trigger pin
    GPIO.output(TRIGGER, True)
    #send out the 10us pulse
    time.sleep(0.00001)
    # turn off the trigger pin
    GPIO.output(TRIGGER, False)
    # record last lowstamp for ECHO
    while GPIO.input(ECHO)==0:
      start = time.time()
    # record last highstamp for ECHO
    while GPIO.input(ECHO)==1:
      stop = time.time()
    # calculate pulse length
    elapsed = stop-start
    # calculate the distance
    distance = (elapsed * 34000.0) / 2
    print("Distance : %.1f cm" % distance)
except KeyboardInterrupt:   
    print "Ultrasonic Distance Measurement End" 
    GPIO.cleanup()

GPIO.cleanup()