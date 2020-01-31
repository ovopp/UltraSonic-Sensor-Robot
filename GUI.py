from tkinter import *
from tkinter import ttk
import time
import math
import matplotlib

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
    
    radar.pack()
    
    window.mainloop()
    return

mainWindow()
