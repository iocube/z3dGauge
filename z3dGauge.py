﻿import ac, acsys

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'DLLs'))
from sim_info import info

import math

#TODO: fix the usage of globals
#TODO: fullscreen
#TODO: render heading, pitch and roll


appName = "z3Dgauge"

#TODO: get screen size
width, height = 2560, 1440


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
    global l_debug
    global acceleration
    global ascii_RPM
    l_kmph = ac.addLabel(appWindow, "KMPH")
    l_rpm = ac.addLabel(appWindow, "RPM")
    l_gear = ac.addLabel(appWindow, "Current gear")
    l_heading = ac.addLabel(appWindow, "Heading")
    l_pitch = ac.addLabel(appWindow, "Pitch")
    l_roll = ac.addLabel(appWindow, "Roll")
    l_debug = ac.addLabel(appWindow, "Debug value: ")

    ascii_RPM = ac.addLabel(appWindow, "")
    acceleration = ac.addLabel(appWindow, "")
    #l_TC = ac.addLabel(appWindow, "TC on/off")      #non-functional
    #l_ABS = ac.addLabel(appWindow, "ABS on/off")    #non-functional

    ac.setPosition(l_kmph, 3, 30)
    ac.setPosition(l_rpm, 3, 60)
    ac.setPosition(l_gear, 3, 80)
    ac.setPosition(l_heading, 3, 100)
    ac.setPosition(l_pitch, 3, 120)
    ac.setPosition(l_roll, 3, 140)
    ac.setPosition(ascii_RPM, 3, 160)
    ac.setPosition(acceleration, 3, 580)

    ac.addRenderCallback(appWindow, appGL) # -> links this app's window to an OpenGL render function

    return appName





def appGL(deltaT):
    
    ## Main
    global gX, gY, gZ, gXleft, gZback 

    center_x = width / 2
    center_y = height / 2
    
    # Square inner
    coord_multiplier = 100
    coord_array = (center_x + 20, center_y + 20, center_x + 20, center_y + 500, center_x + 500, center_y + 500, center_x + 500, center_y + 20)
    modifier_input = 0
    color_rgba = (0, 20, 50, 0.3)
    draw_line(coord_array, 0, 100, modifier_input, color_rgba, coord_multiplier)

    # Square outer
    coord_multiplier = 100
    coord_array = (center_x , center_y , center_x , center_y + 520, center_x + 520, center_y + 520, center_x + 520, center_y )
    modifier_input = 0
    color_rgba = (0, 15, 50, 0.1)
    draw_line(coord_array, 0, 100, modifier_input, color_rgba, coord_multiplier)



    # gas, brake, clutch
    coord_multiplier = 10

    # gas
    coord_array = (700, 700, 700, 700, 710, 700, 710, 700)
    color_rgba = (0, 50, 0, 0.3)
    modifier_input = pedal_gas
    draw_line(coord_array, 0, 100, modifier_input, color_rgba, coord_multiplier)

    # brake
    coord_array = (730, 700, 730, 700, 740, 700, 740, 700)
    color_rgba = (50, 0, 0, 0.3)
    modifier_input = pedal_brake
    draw_line(coord_array, 0, 100, modifier_input, color_rgba, coord_multiplier)

    # clutch
    coord_array = (760, 700, 760, 700, 770, 700, 770, 700)
    color_rgba = (0, 0, 50, 0.3)
    modifier_input = pedal_clutch
    draw_line(coord_array, 0, 100, modifier_input, color_rgba, coord_multiplier)


    coord_multiplier = 10
    # RPM
    # with input current RPM
    num_rpm_blocks = int(iRPM/200)
    static_increase = 20
    distance_increaser = 1
    segment_increaser = 10
    
    rpm_segment_x = center_x
    rpm_segment_y = center_y + 480
    rpm_segment_y_static = center_y + 480
    for segment in range(num_rpm_blocks):
        #coord_array = (rpm_segment_x + distance_increaser, rpm_segment_y_static, 
        #rpm_segment_x + distance_increaser, rpm_segment_y - segment_increaser,
        #rpm_segment_x + segment_increaser + distance_increaser, rpm_segment_y - segment_increaser,
        #rpm_segment_x + segment_increaser + distance_increaser, rpm_segment_y_static)

        coord_array = (rpm_segment_x + distance_increaser, rpm_segment_y - segment_increaser,
        rpm_segment_x + distance_increaser, rpm_segment_y_static, 
        rpm_segment_x + segment_increaser + distance_increaser, rpm_segment_y_static,
        rpm_segment_x + segment_increaser + distance_increaser, rpm_segment_y - segment_increaser
        )
        color_rgba = (25, 25, 25, 0.1)
        color_rgba_maxed = (50, 25, 25, 0.2)
        
        modifier_input = 0
        if iRPM < (maxRPM - 1000):
            draw_line(coord_array, 0, 100, modifier_input, color_rgba, coord_multiplier)
        else:
            draw_line(coord_array, 0, 100, modifier_input, color_rgba_maxed, coord_multiplier)
            
        distance_increaser+=5
        rpm_segment_x += 8
        rpm_segment_y -= 10



    # Gauge segments
    center_x2 = width / 2
    center_y2 = height / 2 + 95

    for head_segment in range(num_rpm_blocks):
        ac.glBegin(acsys.GL.Quads)
        ac.glColor4f(0,50,50,0.3)
        ac.glVertex2f(center_x2 - 20 , center_y2) # top left
        ac.glVertex2f(center_x2 - 20 , center_y2 + 20)   # bottom left
        ac.glVertex2f(center_x2 - 10, center_y2 + 10) # bottom right
        ac.glVertex2f(center_x2 - 10, center_y2)   #top right
        center_x2 = center_x2 + 13
        ac.glEnd()


    # Gauge segments experimental
    c_increase=0.08
    for RPM_segment in range(int(maxRPM/200)):
        ac.glColor4f(c_increase, 0.2, 0.5, 0.3)
        ac.glQuad(center_x - 20 , center_y + 80 ,10 ,10)
        center_x += 13
        c_increase+=0.08

    

def acUpdate(deltaT):

    ac.setTitle(appWindow, "")
    ac.setIconPosition(appWindow, 0, -10000)
    ac.setBackgroundOpacity(appWindow, 0)
    ac.drawBorder(appWindow, 0)
    global l_kmph
    global l_rpm
    global l_gear
    global l_heading
    global l_debug
    global speed
    global RPM, maxRPM, iRPM
    global gear
    global acceleration
    global heading
    global pedal_gas, pedal_brake, pedal_clutch

    # standard info
    speed = str(ac.getCarState(0, acsys.CS.SpeedKMH))
    RPM = str(ac.getCarState(0, acsys.CS.RPM))
    gear = str(ac.getCarState(0, acsys.CS.Gear))

    # car-to-world info
    heading = math.degrees(round(float(str(info.physics.heading)[:5]), 2))
    pitch = str(info.physics.pitch)[:5]
    roll = str(info.physics.roll)

    # pedals info
    # slicing 0.00
    # If live, get val from physics;
    # else if replay, get val from player state
    if info.graphics.status == 2:
        pedal_gas = str(info.physics.gas)[:4]
        pedal_brake = str(info.physics.brake)[:4]
        pedal_clutch = str(info.physics.clutch)[:4]
    elif info.graphics.status == 1:
        pedal_gas = str(ac.getCarState(0, acsys.CS.Gas))[:4]
        pedal_brake = str(ac.getCarState(0, acsys.CS.Brake))[:4]
        pedal_clutch = str(ac.getCarState(0, acsys.CS.Clutch))[:4]

    ac.setText(l_kmph, speed)
    ac.setText(l_rpm, RPM)
    ac.setText(l_gear, gear)
    ac.setText(l_heading, str(heading))
    ac.setText(l_pitch, pitch)
    ac.setText(l_roll, roll)
    
    ac.setText(l_debug, str(pedal_gas))

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


def tacho(anotherRPM):      # thanks to based serb for the function
    return ("l" * int(anotherRPM/200))


#TODO: replace glVertex with ac.glQuad

# coord_array is a list of x0, y0, x1 and so on
# color_rgb is a list for RGBA values
def draw_line(coord_array, min_val, max_val, modifier_input, color_rgba, coord_multiplier):

    # Initial values
    x0 = coord_array[0]
    y0 = coord_array[1]
    x1 = coord_array[2]
    y1 = coord_array[3]
    x2 = coord_array[4]
    y2 = coord_array[5]
    x3 = coord_array[6]
    y3 = coord_array[7]

    y1 = int(y1) - (float(modifier_input) * 700)
    y2 = int(y2) - (float(modifier_input) * 700)

    # 3D Transformation
    x00 = x0 - (abs(gZ) * coord_multiplier)    # forward
    y00 = y0 - (abs(gXleft) * coord_multiplier)    #right
    x11 = x1 - (abs(gZback) * coord_multiplier)    #reverse
    y11 = y1 + (abs(gXleft) * coord_multiplier)    #right
    x22 = x2 + (abs(gZback) * coord_multiplier)    #reverse
    y22 = y2 + (abs(gX) * coord_multiplier)    #left
    x33 = x3 + (abs(gZ) * coord_multiplier)    #forward
    y33 = y3 - (abs(gX) * coord_multiplier)    #left

    # Color unpack
    color_R = color_rgba[0]
    color_G = color_rgba[1]
    color_B = color_rgba[2]
    color_A = color_rgba[3]

    ac.glBegin(acsys.GL.Quads)
    ac.glColor4f(color_R, color_G, color_B, color_A)

    ac.glVertex2f(x00, y00) # top left
    ac.glVertex2f(x11, y11) # bottom left
    ac.glVertex2f(x22, y22) # bottom right
    ac.glVertex2f(x33, y33) # top right
    ac.glEnd()
