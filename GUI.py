from tkinter import *
from tkinter import ttk
import time
import math
import matplotlib
#import Twitter_API
window = Tk();

'''
The main window of the GUI
Creates the main window of the GUI has 4 columns and 8 rows
Contains the grph, option based features, radio button to determine feature and submission box to change rate of measurement
'''
def mainWindow ():
    #Draws a distance line on the canvas
    def drawDist(angle, distance):
        distance*=1.35
        radar.create_line(145 + distance*math.sin(angle - math.pi/2), 145 - distance*math.cos(angle - math.pi/2), 145, 145, fill="green")

    #Creates window
    window.geometry("1000x500")
    window.title("Sonar Interface")  # sets title
    for i in range(10):
        window.columnconfigure(i, weight=1)
        window.rowconfigure(i, weight=1)

    #Creates radar canvas
    radar = Canvas (window, height="300", width="300")

    #Adds radar arc
    mainArc = 50, 50, 240, 240
    arcOuter = radar.create_arc(mainArc, start=0, extent=180, fill="black", outline="white")

    for i in range(60):
        drawDist(i*math.pi/60, 20);
        drawDist(i*math.pi/60+math.pi/180, 20);
        drawDist(i*math.pi/60+2*math.pi/180, 20);

    '''Reference curves'''
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
    distance = 70*1.35
    
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
    tweetLabel = Label(window, text="This button will tweet if the distance sensor is reportin a distance less than 10cm")
    tweetLabel.grid(column=2, row=1, sticky="S")
    
    tweetButton = Button(window, text="TWEET")
    tweetButton.grid(column=2, row=2, sticky="N")
    window.mainloop()
    return

mainWindow()
