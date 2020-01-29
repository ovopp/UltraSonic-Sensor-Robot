import RPi.GPIO as GPIO
from tkinter import *

# Setting up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Setting up
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 1/50)



