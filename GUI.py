import time
import math
import matplotlib
import RPi.GPIO as GPIO
import time
import threading
import Adafruit_DHT

from tkinter import *
from tkinter import ttk
from twython import Twython
from twython import TwythonStreamer
from auth import (
    consumer_key, consumer_secret, access_token, access_token_secret
)

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

TweetDistance = 70                 # Distance to which it will tweet.

p = GPIO.PWM(SERVO, 50) # GPIO 18 for PWM with 50Hz
p.start(2.5)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

# Setup DHT11 Temperature Reading
dht = Adafruit_DHT.DHT11


def tweet (message):
    twitter.update_status(status=message)
    print("tweeted!")

def startServo():
    while(True):
        distanceStart()
        distanceBack()
        
def startTemp():
    global temp
    while(True):
        humidity, temperature = Adafruit_DHT.read_retry(dht, 12)
        if(temperature != NULL):
            temp = temperature
            
            
            
def startServoThread():
    thread = threading.Thread(target=startServo, args=())
    thread.daemon = True
    thread.start()
    
    
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

def distanceStart():
    global TweetDistance
    print("In distance start")
    for j in range(60):
        p.ChangeDutyCycle(2.5 + 1/6*j)
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
        distance = (elapsed * (33150.0 + 0.6*temp)) / 2
        if (distance < 15):
            ledController(2)
        elif (distance <30):
            ledController(3)
        elif (distance < 45):
            ledController(4)
        else:
            ledController(5)
        print("Angle: ", j * 3)
        print("Distance : %.1f cm" % distance)
        TweetDistance = distance
        drawDist(j*3, distance)

def distanceBack():
    global TweetDistance
    print("in distance back")
    for k in range(60):
        p.ChangeDutyCycle(12.5 - 1/6 * k)
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
        distance = (elapsed * (33150.0 + 0.6*Adafruit_DHT.read_retry(dht, 12))) / 2
        if (distance < 15):
            ledController(2)
        elif (distance <30):
            ledController(3)
        elif (distance < 45):
            ledController(4)
        else:
            ledController(5)
        print("Angle: ", 180-k*3)
        print("Distance : %.1f cm" % distance)
        TweetDistance = distance
        drawDist(180-k*3, distance)
  
#Draws a distance line on the canvas
def drawDist(angle, distance):
    radar.create_line(145 + distance*math.sin(angle - math.pi/2), 145 - distance*math.cos(angle - math.pi/2), 145, 145, fill="green")

#If the distance is less than 10cm then it tweets the current distance
def tweetEvent ():
    print("tweet event")
    if (TweetDistance < 10):
        tweet("Current Distance: " + str(TweetDistance))
    return

# Thread to take care of temperature readings
thread1 = threading.Thread(target=startTemp)
thread1.daemon = True
thread1.start()


try:
    '''
    The main window of the GUI
    Creates the main window of the GUI has 4 columns and 8 rows
    Contains the grph, option based features, radio button to determine feature and submission box to change rate of measurement
    '''

    #Creates window
    window = Tk();
    window.geometry("1000x500")
    window.title("Sonar Interface")  # sets title
    #Allows for resizing
    for i in range(10):
        window.columnconfigure(i, weight=1)
        window.rowconfigure(i, weight=1)
          
    #Creates radar canvas
    radar = Canvas (window, height="300", width="300")

    #Adds radar arc
    mainArc = 50, 50, 240, 240
    arcOuter = radar.create_arc(mainArc, start=0, extent=180, fill="black", outline="white")

    '''Reference curves: The curves are used to easily measure the distance that the sensor detects'''
    shift1 = 550/7
    innerArc1 = 50+shift1, 50+shift1, 240-shift1, 240-shift1
    arcInner1 = radar.create_arc(innerArc1, start=0, extent=180, outline="white", fill="")

    
    shift2 = 460/7
    innerArc2 = 50+shift2, 50+shift2, 240-shift2, 240-shift2
    arcInner2 = radar.create_arc(innerArc2, start=0, extent=180, outline="white", fill="")

    shift3 = 370/7
    innerArc3 = 50+shift3, 50+shift3, 240-shift3, 240-shift3
    arcInner3 = radar.create_arc(innerArc3, start=0, extent=180, outline="white", fill="")

    shift4 = 280/7
    innerArc4 = 50+shift4, 50+shift4, 240-shift4, 240-shift4
    arcInner4 = radar.create_arc(innerArc4, start=0, extent=180, outline="white", fill="")

    shift5 = 190/7
    innerArc5 = 50+shift5, 50+shift5, 240-shift5, 240-shift5
    arcInner5 = radar.create_arc(innerArc5, start=0, extent=180, outline="white", fill="")

    shift6 = 100/7
    innerArc6 = 50+shift6, 50+shift6, 240-shift6, 240-shift6
    arcInner6 = radar.create_arc(innerArc6, start=0, extent=180, outline="white", fill="")

    
    '''Reference lines'''
    distance = 70*1.35 #The distance of the lines used for reference (maximum)

    angle1 = math.pi/4
    AngleRef1 = radar.create_line(145 + distance*math.sin(angle1 - math.pi/2), 145 - distance*math.cos(angle1 - math.pi/2), 145, 145, fill="white")

    angle2 = math.pi/2
    AngleRef2 = radar.create_line(145 + distance*math.sin(angle2 - math.pi/2), 145 - distance*math.cos(angle2 - math.pi/2), 145, 145, fill="white")

    angle3 = 3*math.pi/4
    AngleRef3 = radar.create_line(145 + distance*math.sin(angle3 - math.pi/2), 145 - distance*math.cos(angle3 - math.pi/2), 145, 145, fill="white")


    '''Reference labels'''
    #Angle labels
    angleLabel1 = Label(radar, text="0*")
    angleLabel1.pack()
    radar.create_window(30, 140, window=angleLabel1)

    angleLabel2 = Label(radar, text="45*")
    angleLabel2.pack()
    radar.create_window(70, 60, window=angleLabel2)

    angleLabel3 = Label(radar, text="90*")
    angleLabel3.pack()
    radar.create_window(150, 40, window=angleLabel3)

    angleLabel4 = Label(radar, text="135*")
    angleLabel4.pack()
    radar.create_window(220, 60, window=angleLabel4)

    angleLabel5 = Label(radar, text="180*")
    angleLabel5.pack()
    radar.create_window(270, 140, window=angleLabel5)

    
    #Distance labels
    distanceLabel1 = Label(radar, text="0")
    distanceLabel1.pack()
    radar.create_window(145, 155, window=distanceLabel1)

    distanceLabel2 = Label(radar, text="20")
    distanceLabel2.pack()
    radar.create_window(175, 155, window=distanceLabel2)

    distanceLabel3 = Label(radar, text="40")
    distanceLabel3.pack()
    radar.create_window(200, 155, window=distanceLabel3)

    distanceLabel4 = Label(radar, text="60")
    distanceLabel4.pack()
    radar.create_window(225, 155, window=distanceLabel4)
        
    radar.grid(row=1, rowspan=2, column=1)
    
    '''Twitter API interactions'''
    #Label describing tweet conditions
    tweetLabel = Label(window, text="This button will tweet if the distance sensor is reportin a distance less than 10cm")
    tweetLabel.grid(column=2, row=1, sticky="S")
    
    #Button that sends tweet if the conditions are met
    tweetButton = Button(window, text="TWEET", command=tweetEvent, width="20")
    tweetButton.grid(column=2, row=2, sticky="N")
    
    #Button that starts the servo and reads
    servoButton = Button(window, text="START SERVO", command=startServoThread, width="20")
    servoButton.grid(column=2, row=3, sticky="N")
    
    #The main window loop
    window.mainloop()
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()

