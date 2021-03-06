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

#Seting up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # do not show any warnings

#Assigning the GPIO pin numbers
SERVO = 18
TRIGGER = 23
ECHO = 24

#Initializing the GPIO components
GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(16, GPIO.OUT)  # initialize GPIO Pins as an output.
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

TweetDistance = 70  # Distance to which it will tweet.

p = GPIO.PWM(SERVO, 50)  # GPIO 18 for PWM with 50Hz
p.start(2.5)

#Setting up Twython for tweeting
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

# Setup DHT11 Temperature Reading
dht = Adafruit_DHT.DHT11
temp = 23  # default temp

# Thread variables
on = False
speed = 7


def tweet(message):
    twitter.update_status(status=message)
    print("tweeted!")

#Starts servo motor (sweeps back and forth)
def startServo():
    global on
    while True:
        if on:
            distanceStart()
            distanceBack()
            humidity, temperature = Adafruit_DHT.read_retry(dht, 4)
            print(temperature)
            if temperature != None:
                temp = temperature
                


# Function for starting the servo button thread
def startServoThread():
    global on
    if on:
        on = False
    else:
        on = True

def ledController(x):
    GPIO.output(16, 0)  # DATA PIN set to 0
    time.sleep(0.001)
    # Resets the memory in the LEDs
    for l in range(4):
        GPIO.output(20, 1)  # pull CLOCK pin high
        time.sleep(0.001)
        GPIO.output(20, 0)

    GPIO.output(16, 1)  # DATA PIN set to 1
    time.sleep(0.001)
    # Sets the number of LEDs to be turned on
    for j in range(x):  # loop for counting up x times
        GPIO.output(20, 1)  # pull CLOCK pin high
        time.sleep(0.001)
        GPIO.output(20, 0)  # pull CLOCK pin down, to send a rising edge

    GPIO.output(21, 1)  # pull up the SHIFT pin
    time.sleep(0.001)
    GPIO.output(21, 0)  # pull down the SHIFT pin


# Function to rotate and measure from 0 -> 180
def distanceStart():
    #Initializing global variables TwetDistance (distance used to determine wether to tweet or not), temp (temperature) and speed (speed of the motor)
    global TweetDistance, temp, speed
    print("In distance start")
    for j in range(60):
        #Rotates the servo 3 degrees
        p.ChangeDutyCycle(2.5 + 1 / 6 * j)
        #Sends a pulse of sound
        GPIO.output(TRIGGER, False)
        time.sleep(1-0.094*speed)
        GPIO.output(TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(TRIGGER, False)
        #Measures the start and stop of the echo wave
        while GPIO.input(ECHO) == 0:
            start = time.time()
        while GPIO.input(ECHO) == 1:
            stop = time.time()
        #Calculates the distance based of echo length ad temperature
        elapsed = stop - start
        length = (elapsed * (33150.0 + 0.6 * temp)) / 2
        #Depending on the distance, the LEDs will turn on
        if length < 15:
            ledController(2)
        elif length < 30:
            ledController(3)
        elif length < 45:
            ledController(4)
        else:
            ledController(5)
        #Displays the angle and distance to the terminal
        print("Angle: ", j * 3)
        print("Distance : %.1f cm" % length)
        #Changes the length used to tweet
        TweetDistance = length
        #Draws a line on radar for the corresponding length and angle
        drawDist(j * 3, length)


# Function to rotate and measure from 180 -> 0
def distanceBack():
    global TweetDistance, temp, speed
    print("in distance back")
    #Measures every 3 degrees of servo rotation
    for k in range(60):
        #Rotate servo
        p.ChangeDutyCycle(12.5 - 1 / 6 * k)
        #Sends pulse
        GPIO.output(TRIGGER, False)
        time.sleep(1-0.094*speed)
        GPIO.output(TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(TRIGGER, False)
        #Measures start and stop of the echo
        while GPIO.input(ECHO) == 0:
            start = time.time()
        while GPIO.input(ECHO) == 1:
            stop = time.time()
        #Calculates the distance based of echo length ad temperature
        elapsed = stop - start
        length = (elapsed * (33150.0 + 0.6 * temp / 2)) / 2
        #Lights up the LEDs according to distance
        if length < 15:
            ledController(2)
        elif length < 30:
            ledController(3)
        elif length < 45:
            ledController(4)
        else:
            ledController(5)
        #Prints the angle and distance to the terminal
        print("Angle: ", 180 - k * 3)
        print("Distance : %.1f cm" % length)
        #Changes the length tweet uses
        TweetDistance = length
        #Draws a line on the radar at the current angle and distance
        drawDist(180 - k * 3, length)

linelist = []
# Draws a distance line on the canvas
def drawDist(angle, length):
    index = int(angle/ 3)
    angle = angle*math.pi/180
            
    if length > 70:
        length = 70 #max size length can be without making it like huge
    length *= 2.7
    if len(linelist) == 61:
        radar.delete(linelist[index])
        line = radar.create_line(290 + length * math.sin(angle - math.pi / 2), 290 - length * math.cos(angle - math.pi / 2),
                      290, 290, fill="green")
        linelist[index] = line
    
    else:
        #Draws a line at the specified angle and distance on the radar
        line = radar.create_line(290 + length * math.sin(angle - math.pi / 2), 290 - length * math.cos(angle - math.pi / 2),
                      290, 290, fill="green")
        linelist.append(line)


# If the distance is less than 10cm then it tweets the current distance
def tweetEvent():
    print("tweet event")
    if TweetDistance < 10:
        tweet("Current Distance: " + str(TweetDistance) + " cm. You're too close!")
    return

#Changes the speed of the servo motor
def submitspeed():
    global speed
    k = speedEntry.get()
    #Checks if the value is a valid speed 11+ and an integer
    try:
        if float(k) is not float:
            k = float(k)
            if k < 11 and k > 0:
                speed = k
                print("Value OK, speed changed to: " + str(speed))
            else:
                print("Value not within 1-10")
    except ValueError:
        print("Entry not a valid number")
            
        

# Thread to control servo functionality
thread = threading.Thread(target=startServo, args=())
thread.daemon = True
thread.start()

try:
    '''
    The main window of the GUI
    Creates the main window of the GUI has 4 columns and 8 rows
    Contains the graph, option based features, radio button to 
    determine feature and submission box to change rate of measurement
    '''

    # Creates window
    window = Tk()
    window.geometry("1300x500")
    window.title("Sonar Interface")  # sets title
    # Allows for resizing
    for i in range(10):
        window.columnconfigure(i, weight=1)
        window.rowconfigure(i, weight=1)

    # Creates radar canvas
    radar = Canvas(window, height="400", width="700")

    # Adds radar arc
    mainArc = 100, 100, 480, 480
    arcOuter = radar.create_arc(mainArc, start=0, extent=180, fill="black", outline="white")

    '''Reference curves: The curves are used to easily measure the distance that the sensor detects'''
    shift1 = 2*551 / 7
    innerArc1 = 100 + shift1, 100 + shift1, 480 - shift1, 480 - shift1
    arcInner1 = radar.create_arc(innerArc1, start=0, extent=180, outline="white", fill="")

    shift2 = 2*460 / 7
    innerArc2 = 100 + shift2, 100 + shift2, 480 - shift2, 480 - shift2
    arcInner2 = radar.create_arc(innerArc2, start=0, extent=180, outline="white", fill="")

    shift3 = 2*370 / 7
    innerArc3 = 100 + shift3, 100 + shift3, 480 - shift3, 480 - shift3
    arcInner3 = radar.create_arc(innerArc3, start=0, extent=180, outline="white", fill="")

    shift4 = 2*280 / 7
    innerArc4 = 100 + shift4, 100 + shift4, 480 - shift4, 480 - shift4
    arcInner4 = radar.create_arc(innerArc4, start=0, extent=180, outline="white", fill="")

    shift5 = 2*190 / 7
    innerArc5 = 100 + shift5, 100 + shift5, 480 - shift5, 480 - shift5
    arcInner5 = radar.create_arc(innerArc5, start=0, extent=180, outline="white", fill="")

    shift6 = 2*100 / 7
    innerArc6 = 100 + shift6, 100 + shift6, 480 - shift6, 480 - shift6
    arcInner6 = radar.create_arc(innerArc6, start=0, extent=180, outline="white", fill="")

    '''Reference lines: Lines used to measure the angle of the measurements'''
    distance = 70 * 2.7  # The distance of the lines used for reference (maximum)

    angle1 = math.pi / 4
    AngleRef1 = radar.create_line(290 + distance * math.sin(angle1 - math.pi / 2),
                                  290 - distance * math.cos(angle1 - math.pi / 2), 290, 290, fill="white")

    angle2 = math.pi / 2
    AngleRef2 = radar.create_line(290 + distance * math.sin(angle2 - math.pi / 2),
                                  290 - distance * math.cos(angle2 - math.pi / 2), 290, 290, fill="white")

    angle3 = 3 * math.pi / 4
    AngleRef3 = radar.create_line(290 + distance * math.sin(angle3 - math.pi / 2),
                                  290 - distance * math.cos(angle3 - math.pi / 2), 290, 290, fill="white")

    '''Reference labels: The values of each of the reference curves and arcs'''
    # Angle labels
    angleLabel1 = Label(radar, text="0*")
    angleLabel1.pack()
    radar.create_window(60, 280, window=angleLabel1)

    angleLabel2 = Label(radar, text="45*")
    angleLabel2.pack()
    radar.create_window(140, 120, window=angleLabel2)

    angleLabel3 = Label(radar, text="90*")
    angleLabel3.pack()
    radar.create_window(300, 80, window=angleLabel3)

    angleLabel4 = Label(radar, text="135*")
    angleLabel4.pack()
    radar.create_window(440, 120, window=angleLabel4)

    angleLabel5 = Label(radar, text="180*")
    angleLabel5.pack()
    radar.create_window(540, 280, window=angleLabel5)

    # Distance labels
    distanceLabel1 = Label(radar, text="0")
    distanceLabel1.pack()
    radar.create_window(290, 310, window=distanceLabel1)

    distanceLabel2 = Label(radar, text="20")
    distanceLabel2.pack()
    radar.create_window(350, 310, window=distanceLabel2)

    distanceLabel3 = Label(radar, text="40")
    distanceLabel3.pack()
    radar.create_window(400, 310, window=distanceLabel3)

    distanceLabel4 = Label(radar, text="60")
    distanceLabel4.pack()
    radar.create_window(450, 310, window=distanceLabel4)

    radar.grid(row=1, rowspan=2, column=1)

    '''Twitter API interactions'''
    # Label describing tweet conditions
    tweetLabel = Label(window,
                       text="This button will tweet if the distance sensor \n is reportin a distance less than 10cm")
    tweetLabel.grid(column=2, row=1, sticky="S")

    # Button that sends tweet if the conditions are met
    tweetButton = Button(window, text="TWEET", command=tweetEvent, width="20")
    tweetButton.grid(column=2, row=2, sticky="N")

    # Button that starts the servo and reads
    servoButton = Button(window, text="SERVO on/off", command=startServoThread, width="20")
    servoButton.grid(column=2, row=3, sticky="N")
    
    # Entry that takes in servo speed
    speedEntry = Entry(window)
    speedEntry.grid(column=2, row=4)
    Button(window, text="Submit speed (1-10)", command = submitspeed, width='20').grid(column=3,row=4, sticky='N')
    
           
    # The main window loop
    window.mainloop()

except KeyboardInterrupt:
    window.destroy()
    p.stop()
    GPIO.output(16, 0)  # DATA PIN set to 0
    time.sleep(0.001)
    # Resets the memory in the LEDs
    for l in range(4):
        GPIO.output(20, 1)  # pull CLOCK pin high
        time.sleep(0.001)
        GPIO.output(20, 0)
    GPIO.output(21, 1)  # pull up the SHIFT pin
    time.sleep(0.001)
    GPIO.output(21, 0)
    GPIO.cleanup()
    
    print("program done")


