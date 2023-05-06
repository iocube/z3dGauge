import ac, acsys


import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'DLLs'))

from sim_info import info


#TODO: fix the usage of globals
#TODO: fullscreen
#TODO: render heading, pitch and roll


appName = "z3Dgauge"
width, height = 640, 640

appWindow = 0

gX = 1.1
gY = 1.1
gZ = 1.1
gZback = 0.0
gXleft = 0.0




def acMain(ac_version): #app window init; global variables for later updating go here
    global appWindow

    
    global width, height
    appWindow = ac.newApp(appName)
    ac.setTitle(appWindow, appName)
    ac.setSize(appWindow, width, height)

    ac.log("z3D Gauge loaded")
    ac.console("z3D Gauge console test")

    ####################################################declaring gauge elements
    # will need new textures like
    # rpm_bar = ac.newTexture(app_path + theme_path + "rpm_bar.png")

    global l_kmph
    global l_rpm
    global l_gear
    global l_heading
    global l_pitch
    global l_roll
    global acceleration
    global ascii_RPM
    l_kmph = ac.addLabel(appWindow, "KMPH")
    l_rpm = ac.addLabel(appWindow, "RPM")
    l_gear = ac.addLabel(appWindow, "Current gear")
    l_heading = ac.addLabel(appWindow, "Heading")
    l_pitch = ac.addLabel(appWindow, "Pitch")
    l_roll = ac.addLabel(appWindow, "Roll")

    ascii_RPM = ac.addLabel(appWindow, "")
    acceleration = ac.addLabel(appWindow, "")
    #l_TC = ac.addLabel(appWindow, "TC on/off")      #non-functional
    #l_ABS = ac.addLabel(appWindow, "ABS on/off")    #non-functional

    ac.setPosition(l_kmph, 3, 30)
    ac.setPosition(l_rpm, 3, 60)
    ac.setPosition(l_gear, 3, 80)
    ac.setPosition(ascii_RPM, 3, 160)
    ac.setPosition(acceleration, 3, 580)

    ac.addRenderCallback(appWindow, appGL) # -> links this app's window to an OpenGL render function

    return appName

def appGL(deltaT):
    
    global gX, gY, gZ, gXleft, gZback
    
    # drawing the gauge's background primitive aka a square
    # initial values
    x0 = 20.0   # point 1
    y0 = 20.0
    x1 = 20.0   # point 2
    y1 = 500.0 #500
    x2 = 500.0   # point 3
    y2 = 500.0
    x3 = 500.0 #500  point 4
    y3 = 20.0  # so I'm gonna have to find a way to make these variables be affected by gforces

    # calculated values with gforces into account
    #x00 = x0 + (abs(gZ)*100)    # forward
    #y00 = y0 + (abs(gXleft)*100)    #right
    #x11 = x1 + (abs(gZback)*100)    #reverse
    #y11 = y1 - (abs(gXleft)*100)    #right
    #x22 = x2 - (abs(gZback)*100)    #reverse
    #y22 = y2 - (abs(gX)*100)    #left
    #x33 = x3 - (abs(gZ)*100)    #forward
    #y33 = y3 + (abs(gX)*100)    #left


    # calculated values with gforces into account
    x00 = x0 - (abs(gZ)*100)    # forward
    y00 = y0 - (abs(gXleft)*100)    #right
    x11 = x1 - (abs(gZback)*100)    #reverse
    y11 = y1 + (abs(gXleft)*100)    #right
    x22 = x2 + (abs(gZback)*100)    #reverse
    y22 = y2 + (abs(gX)*100)    #left
    x33 = x3 + (abs(gZ)*100)    #forward
    y33 = y3 - (abs(gX)*100)    #left


    ac.glBegin(acsys.GL.Quads)
    ac.glColor4f(50,0,0,0.5)

    ac.glVertex2f(x00, y00) # top left in brainlet terms aka for dummies like me
    ac.glVertex2f(x11, y11)   # bottom left
    ac.glVertex2f(x22, y22) # bottom right
    ac.glVertex2f(x33, y33)   #top right
    ac.glEnd()

    

def acUpdate(deltaT):

    ac.setBackgroundOpacity(appWindow, 0)
    ac.drawBorder(appWindow, 0)
    global l_kmph
    global l_rpm
    global l_gear
    global l_heading
    global speed
    global RPM
    global gear
    global acceleration

    # standard info
    speed = str(ac.getCarState(0, acsys.CS.SpeedKMH))
    RPM = str(ac.getCarState(0, acsys.CS.RPM))
    gear = str(ac.getCarState(0, acsys.CS.Gear))

    # car-to-world info
    heading = str(info.physics.heading)
    pitch = str(info.physics.pitch)
    roll = str(info.physics.roll)

    ac.setText(l_kmph, speed)
    ac.setText(l_rpm, RPM)
    ac.setText(l_gear, gear)
    ac.setText(l_heading, heading)
    ac.setText(l_pitch, pitch)
    ac.setText(l_roll, roll)
    

    global ascii_RPM, ARPM

    iRPM = float(RPM)
    maxRPM = float(info.static.maxRpm)

    ARPM = tacho(iRPM)

    if iRPM >= (maxRPM - 200):
        ARPM = ARPM + "[!]"
    
    ac.setText(ascii_RPM, ARPM)
    
    accelerationS = str(ac.getCarState(0, acsys.CS.AccG)) # returns a tuple with x y z; so X is sideways, Y is up and down and Z forward reverse
    accelerationTest = ac.getCarState(0, acsys.CS.AccG) # this is the non-printing one I'm gonna work with

    global gX, gY, gZ, gZback, gXleft

    gX = round(accelerationTest[0], 3)  # then the car's turning left basically, gforces pulling the car to the right
    if gX > 0:  
        gXleft = 0
    else:
        gXleft = gX
        gX = 0.0
    gY = round(accelerationTest[1], 3)
    gZ = round(accelerationTest[2], 3)
    gZback = gZ # forking gZ into two, this one will be used for reverse gforces
    if gZ < 0:
        gZback = gZ
        gZ = 0.0
    else:
        gZback = 0.0
        
    #ac.setText(acceleration, accelerationS)
    #print(acceleration)


def tacho(anotherRPM):      #idk wtf is going on anymore; thanks to based serb for the function though
    # l = [image] * int(anotherRPM/200))

    return ("l" * int(anotherRPM/200))
