from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time
from threading import Thread

ev3 = EV3Brick()

arm_rot_motor = Motor(Port.C)
arm_raise_motor = Motor(Port.B)
claw_motor = Motor(Port.A)
color_sensor = ColorSensor(Port.S2)
touch_sensor = TouchSensor(Port.S1)

COLORS = [Color.RED, Color.BLUE]
total_time = None
dropzones = {}

ROT_SPEED = 50

def getColorOfObject():
    tmp = color_sensor.color()
    if tmp in COLORS:
        print(tmp)
        return tmp
    return None

def arm_down():
    arm_raise_motor.run_until_stalled(speed=50, duty_limit=7)
    print("Arm Down")

def arm_up(waitfor_sensor):
    print("Arm Up")
    color = None
    if waitfor_sensor:
        arm_raise_motor.run(speed=-50)
        time.sleep(3.6)
        while color == None:
            color = getColorOfObject()
            if arm_raise_motor.stalled():
                arm_raise_motor.stop()
    arm_raise_motor.run_until_stalled(speed=-50, then=Stop.HOLD, duty_limit=20)

    if waitfor_sensor : return color

def open_claw(withPackage):
    if withPackage:
        claw_motor.run_time(speed=-60, time=0.7*1000, then=Stop.HOLD)
    else:
        claw_motor.run_time(speed=-60, time=1.2*1000, then=Stop.HOLD)
    print("Claw open")

def close_claw():
    claw_motor.run_until_stalled(speed=30, then=Stop.HOLD, duty_limit=80)
    print("Claw Closed")

def rotateToColor(color : Color):
    print(find_key(dropzones, color), color)
    arm_rot_motor.run_time(speed=ROT_SPEED, time=(find_key(dropzones, color)+1) *1000, wait=True)

def reset_rotation(color):
    _time = (total_time-find_key(dropzones, color)+1)*1000
    arm_rot_motor.run_time(speed=-ROT_SPEED, time=_time, wait=True)

def mesure():
    """Returns degress for total arm rotation"""
    global total_time
    start = time.time()
    arm_rot_motor.run(speed=ROT_SPEED)
    print(dropzones)
    while not touch_sensor.pressed():
        tmp = color_sensor.color()
        if tmp in COLORS and tmp not in dropzones.values():
            dropzones[time.time() - start] = tmp   
    total_time = time.time() - start
    print("Dropzones: ")
    print(dropzones)
    arm_rot_motor.stop()
    #Returns to start position
    arm_rot_motor.run_time(speed=-ROT_SPEED, time=total_time*1000, wait=True)
    #return speed * (time.time() - start)

def find_key(input_dict, value):
    """Find the key for a value in a dict"""
    return next((k for k, v in input_dict.items() if v == value), None)

def initiation():
    arm_up(waitfor_sensor=False)
    close_claw()
    mesure()

def pickup():
    open_claw(withPackage=False)
    arm_down()
    close_claw()
    return arm_up(waitfor_sensor=True)

def drop(color : Color):
    rotateToColor(color=color)
    arm_down()
    open_claw(withPackage=True)
    arm_up(waitfor_sensor=False)
    close_claw()
    reset_rotation(find_key(dropzones, color))
