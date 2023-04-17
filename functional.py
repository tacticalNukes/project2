from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, LogicMailbox
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time

ev3 = EV3Brick()

arm_rot_motor = Motor(Port.C)
arm_raise_motor = Motor(Port.B)
claw_motor = Motor(Port.A)
color_sensor = ColorSensor(Port.S2)
touch_sensor = TouchSensor(Port.S1)

COLORS = [Color.YELLOW, Color.GREEN, Color.RED, Color.BLUE]
dropzones = {}
SERVER = BluetoothMailboxServer()
MBOX = TextMailbox('box', SERVER)

ROT_SPEED = 50

def getColorOfObject():
    tmp = color_sensor.color()
    if tmp in COLORS:
        print(tmp)
        return tmp
    return None

def arm_down():
    arm_raise_motor.run_until_stalled(speed=50, duty_limit=7)
    print(arm_raise_motor.angle())
    print("Arm Down")

def arm_up(waitfor_sensor):
    print("Arm Up")
    color = None
    if waitfor_sensor:
        arm_raise_motor.run_target(speed=60, target_angle=315, then=Stop.HOLD, wait=True)
        print("Checking Color")
        while color == None:
            color = getColorOfObject()
    arm_raise_motor.run_until_stalled(speed=-80, then=Stop.HOLD, duty_limit=20)

    if waitfor_sensor : return color

def open_claw():
    claw_motor.run_target(speed=60, target_angle=-90, then=Stop.HOLD, wait=True)
    print("Claw open")

def close_claw():
    claw_motor.run_until_stalled(speed=30, then=Stop.HOLD, duty_limit=80)
    return claw_motor.angle()
    # Om vinkeln är mindre än 5 finns ett objekt
    print("Claw Closed")

def rotateToColor(color : Color):
    print(find_key(dropzones, color), color)
    arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=find_key(dropzones, color), wait=True)

def reset_rotation():
    arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=0, then=Stop.HOLD, wait=True)

def mesure():
    """Returns degress for total arm rotation"""
    global total_angle
    arm_rot_motor.reset_angle(angle=0)
    arm_rot_motor.run(speed=ROT_SPEED)
    print(dropzones)
    while not touch_sensor.pressed():
        tmp = color_sensor.color()
        if tmp in COLORS and tmp not in dropzones.values():
            dropzones[arm_rot_motor.angle()] = tmp
    total_angle = arm_rot_motor.angle()
    print("Dropzones: ")
    print(dropzones)
    arm_rot_motor.stop()
    #Returns to start position
    arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=0, then=Stop.HOLD, wait=True)
    #return speed * (time.time() - start)

def find_key(input_dict, value):
    """Find the key for a value in a dict"""
    return next((k for k, v in input_dict.items() if v == value), None)

def initiation():
    connect()
    arm_up(waitfor_sensor=False)
    arm_raise_motor.reset_angle(angle=0)
    close_claw()
    claw_motor.reset_angle(angle=0)
    mesure()

def checkobject_ispresent(color : Color):
    rotateToColor(color=color)
    open_claw()
    arm_down()
    close_claw()
    
def pickup():
    open_claw()
    arm_down()
    close_claw()
    color = arm_up(waitfor_sensor=True)
    ev3.light = color
    return color

def drop(color : Color):
    rotateToColor(color=color)
    arm_down()
    open_claw()
    arm_up(waitfor_sensor=False)
    reset_rotation()

def connect():
  ev3.screen.clear()
  ev3.screen.draw_text(5, 50, "Connecting...")
  SERVER.wait_for_connection()
  ev3.screen.clear()
  ev3.screen.draw_text(5, 50, "Connected!")
  ev3.speaker.beep()

def sendcommands():
  MBOX.send(MSG_DONE)
  MBOX.wait()
  MBOX.send(MSG_FINDPARK)
  MBOX.wait()
  MBOX.send(MSG_LEAVEPARK)
  MBOX.wait()
  MBOX.send(MSG_PARKED)
  MBOX.wait()
  MBOX.send(MSG_TURN)
  MBOX.wait()
  MBOX.send(MSG_RETURN)
  
  MBOX.send(MSG_DONE)

MSG_DONE = "Done"
MSG_FINDPARK = "Find Parking"
MSG_LEAVEPARK = "Leave Parking"
MSG_PARKED = "In Parking"
MSG_TURN = "Turn 180"
MSG_RETURN = "Return 180"

sendcommands()