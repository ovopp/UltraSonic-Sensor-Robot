import RPi.GPIO as GPIO         # calling for header file which helps us use GPIO’s of PI
import time                             # calling for time to provide delays in program
GPIO.setwarnings(False)           # do not show any warnings
GPIO.setmode (GPIO.BCM)        # programming the GPIO by BCM pin numbers. (like PIN29 as‘GPIO5’)
GPIO.setup(16,GPIO.OUT)            # initialize GPIO Pins as an output.
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

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
