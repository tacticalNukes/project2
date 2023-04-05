from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time
import threading

ev3 = EV3Brick()

arm_rot_motor = Motor(Port.C)
arm_raise_motor = Motor(Port.B)
claw_motor = Motor(Port.A)
color_sensor = ColorSensor(Port.S2)
touch_sensor = TouchSensor(Port.S1)

COLORS = [Color.RED, Color.BLUE]
total_time = None
dropzones = {}

def getColorOfObject():
    print("Start Looking")
    while color_sensor.color() not in COLORS:
        print(color_sensor.color())
    return color_sensor.color()

def arm_down():
    arm_raise_motor.run_until_stalled(speed=40, duty_limit=10)
    print("Arm Down")

def arm_up(waitfor_sensor):
    t1 = threading.Thread(target = lambda : arm_raise_motor.run_until_stalled(speed=-50, then=Stop.HOLD, duty_limit=20))
    t1.start()
    if waitfor_sensor:
        t2 = threading.Thread(target=getColorOfObject)
        t2.start()
        color = getColorOfObject()
        print(color)
        t2.join()

    t1.join()
    print("Arm Up")

def open_claw():
    claw_motor.run_time(speed=-60, time=1.5*1000, then=Stop.HOLD)
    print("Claw open")

def close_claw():
    claw_motor.run_until_stalled(speed=30, then=Stop.HOLD, duty_limit=80)
    print("Claw Closed")

def rotateToColor(color : Color):
    arm_rot_motor.run_time(speed=50, time=find_key(dropzones, color), wait=True)

def reset_rotation(currentDeg):
    arm_rot_motor.run_time(speed=50, time=total_time - currentDeg, wait=True)

def mesure():
    """Returns degress for total arm rotation"""
    global total_time
    _speed = 50
    start = time.time()
    arm_rot_motor.run(speed=_speed)
    print(dropzones)
    while not touch_sensor.pressed():
        if color_sensor.color() in COLORS and color_sensor.color() not in dropzones.values():
            dropzones[time.time() - start] = color_sensor.color()    
    total_time = time.time() - start
    print("Dropzones: ")
    print(dropzones)
    arm_rot_motor.stop()
    #Returns to start position
    arm_rot_motor.run_time(speed=-_speed, time=total_time*1000, wait=True)
    #return speed * (time.time() - start)

def find_key(input_dict, value):
    """Find the key for a value in a dict"""
    return next((k for k, v in input_dict.items() if v == value), None)

def pickup():
    open_claw()
    arm_down()
    close_claw()
    arm_up(waitfor_sensor=True)

def drop(color : Color):
    rotateToColor(color=color)
    arm_down()
    open_claw()
    arm_up(waitfor_sensor=False)
    reset_rotation(find_key(dropzones, color))
