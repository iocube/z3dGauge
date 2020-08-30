#importing the thingies

import ac, acsys


import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'DLLs'))

from sim_info import info

print(info.graphics.tyreCompound, info.physics.rpms, info.static.playerNick)



appName = "z3Dgauge"
width, height = 640, 640

appWindow = 0






def acMain(ac_version): #app window init; global variables for later updating go here
    global appWindow
    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.setSize(appWindow, width, height)

    ac.log("z3D Gauge loaded")
    ac.console("z3D Gauge console test")

    ####################################################declaring gauge elements
    # gonna need new textures like
    # rpm_bar = ac.newTexture(app_path + theme_path + "rpm_bar.png")

    global l_kmph, l_rpm, l_gear, acceleration
    global ascii_RPM
    l_kmph = ac.addLabel(appWindow, "KMPH")
    l_rpm = ac.addLabel(appWindow, "RPM")
    l_gear = ac.addLabel(appWindow, "Current gear")
    ascii_RPM = ac.addLabel(appWindow, "")
    acceleration = ac.addLabel(appWindow, "")
    #l_TC = ac.addLabel(appWindow, "TC on/off")      #non-functional
    #l_ABS = ac.addLabel(appWindow, "ABS on/off")    #non-functional

    ac.setPosition(l_kmph, 3, 30)
    ac.setPosition(l_rpm, 3, 60)
    ac.setPosition(l_gear, 3, 80)
    ac.setPosition(ascii_RPM, 3, 160)
    ac.setPosition(acceleration, 3, 180)

    ac.addRenderCallback(appWindow, appGL) # -> links this app's window to an OpenGL render function

    return appName

def appGL(deltaT):
    

    x0 = 50
    y0 = 50
    x1 = 50
    y1 = 300
    x2 = 200
    y2 = 350
    x3 = 250
    y3 = 50  # so I'm gonna have to find a way to make these variables be affected by gforces
    ac.glBegin(acsys.GL.Quads)
    ac.glVertex2f(5, 5) # top left in brainlet terms aka for dummies like me
    ac.glVertex2f(5, 20)   # bottom left
    ac.glVertex2f(20, 30) # bottom right
    ac.glVertex2f(20, 5)   #top right
    ac.glEnd()

    

def acUpdate(deltaT):

    ac.setBackgroundOpacity(appWindow, 0)
    ac.drawBorder(appWindow, 0)
    global l_kmph, l_rpm, l_gear, speed, RPM, gear, acceleration

    speed = str(ac.getCarState(0, acsys.CS.SpeedKMH))
    RPM = str(ac.getCarState(0, acsys.CS.RPM))
    gear = str(ac.getCarState(0, acsys.CS.Gear))

    ac.setText(l_kmph, speed)
    ac.setText(l_rpm, RPM)
    ac.setText(l_gear, gear)
    

    global ascii_RPM, ARPM

    iRPM = float(RPM)
    maxRPM = float(info.static.maxRpm)

    ARPM = tacho(iRPM)

    if iRPM >= (maxRPM - 200):
        ARPM = ARPM + "[!]"
    
    ac.setText(ascii_RPM, ARPM)
    accelerationS = str(ac.getCarState(0, acsys.CS.AccG)) # returns a tuple with x y z; so X is sideways, Y and Z idk - to find out!
    ac.setText(acceleration, accelerationS)
    print(acceleration)


def tacho(anotherRPM):      #idk wtf is going on anymore; thanks to based serb for the function though
    # l = [image] * int(anotherRPM/200))

    return ("l" * int(anotherRPM/200))
