from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time

ev3 = EV3Brick()

arm_rot_motor = Motor(Port.B)
arm_raise_motor = Motor(Port.B)
claw_motor = Motor(Port.C)
color_sensor = ColorSensor(Port.S2)
touch_sensor = TouchSensor(Port.S4)

COLORS = [Color.RED, Color.BLUE, Color.GREEN]
total_angle = None
dropzones = {}

def getColorOfObject():
    while color_sensor.color() not in COLORS:
        time.sleep(0.05)
    return color_sensor.color()

def arm_down():
    arm_raise_motor.run_until_stalled(speed=15, duty_limit=15, wait=True)
    print("Arm Down")

def arm_up(waitfor_sensor):
    arm_raise_motor.run_until_stalled(speed=-15, duty_limit=25, wait=False)
    if waitfor_sensor:
        color = getColorOfObject()
        print(color)
    print("Arm Up")

def open_claw():
    claw_motor.run_until_stalled(speed=10, duty_limit=60, wait=True)
    print("Claw open")

def close_claw():
    claw_motor.run_until_stalled(speed=-10, duty_limit=80, wait=True)
    print("Claw Closed")

def rotateToColor(color : Color):
    arm_rot_motor.run_target(speed=10, target_angle=find_key(dropzones, color), wait=True)

def reset_rotation(currentDeg):
    arm_rot_motor.run_target(speed=10, target_angle = total_angle - currentDeg, wait=True)

def mesure():
    """Returns degress for total arm rotation"""
    global total_angle
    speed = 10
    start = time.time()
    arm_rot_motor.run(speed=speed)
    while not touch_sensor.pressed():
        if color_sensor.color() in COLORS and color_sensor.color() not in dropzones.values():
            dropzones[speed * (time.time() - start)] = color_sensor.color()    
    total_angle = speed * (time.time() - start)
    print("Dropzones: " + dropzones)
    arm_rot_motor.stop()
    arm_rot_motor.run_target(speed=10, target_angle=-total_angle, wait=True)
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
    arm_down()
    open_claw()
    arm_up(waitfor_sensor=False)
    reset_rotation(find_key(dropzones, color))
