import RPi.GPIO as GPIO         # calling for header file which helps us use GPIO’s of PI
import time                             # calling for time to provide delays in program
GPIO.setwarnings(False)           # do not show any warnings
x=1
GPIO.setmode (GPIO.BCM)        # programming the GPIO by BCM pin numbers. (like PIN29 as‘GPIO5’)
GPIO.setup(16,GPIO.OUT)            # initialize GPIO Pins as an output.
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

while 1:                               # execute loop forever
    for y in range(4):            # loop for counting up 8 times
        GPIO.output(16, 1)            # pull up the data pin for every bit.
        time.sleep(0.1)            # wait for 100ms
        GPIO.output(20,1)            # pull CLOCK pin high
        time.sleep(0.1)
        GPIO.output(20,0)            # pull CLOCK pin down, to send a rising edge
        GPIO.output(16,0)            # clear the DATA pin
        GPIO.output(21,1)            # pull the SHIFT pin high to put the 8 bit data out parallel
        time.sleep(0.1)
        GPIO.output(21,0)            # pull down the SHIFT pin

    for y in range(4):            # loop for counting up 8 times
        GPIO.output(16,0)            # clear the DATA pin, to send 0
        time.sleep(0.1)            # wait for 100ms
        GPIO.output(20,1)            # pull CLOCK pin high
        time.sleep(0.1)
        GPIO.output(20,0)            # pull CLOCK pin down, to send a rising edge
        GPIO.output(16,0)            # keep the DATA bit low to keep the countdown
        GPIO.output(21,1)            # pull the SHIFT pin high to put the 8 bit data out parallel
        time.sleep(0.1)
        GPIO.output(21,0)