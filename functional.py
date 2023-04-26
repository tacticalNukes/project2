from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, LogicMailbox
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, TextMailbox

import time
import connection

ev3 = EV3Brick()

arm_rot_motor = Motor(Port.C)
arm_raise_motor = Motor(Port.B)
claw_motor = Motor(Port.A)
color_sensor = ColorSensor(Port.S2)
touch_sensor = TouchSensor(Port.S1)

COLORS = [Color.YELLOW, Color.GREEN, Color.RED, Color.BLUE]
dropzones = {}

ROT_SPEED = 150

def getColorOfObject():
    tmp = color_sensor.color()
    if tmp in COLORS:
        return tmp
    return None

def arm_down():
    print("Arm Down")
    arm_raise_motor.run_until_stalled(speed=230, then=Stop.COAST, duty_limit=20)

def arm_up(waitfor_sensor):
    print("Arm Up")
    color = None
    if waitfor_sensor:
        arm_raise_motor.run_target(speed=60, target_angle=340, then=Stop.HOLD, wait=True)
        while color == None:
            color = getColorOfObject()
        ev3.light.on(color)
    arm_raise_motor.run_until_stalled(speed=-120, then=Stop.HOLD, duty_limit=30)

    if waitfor_sensor : return color

def open_claw():
    print("Claw open")
    claw_motor.run_target(speed=80, target_angle=-90, then=Stop.HOLD, wait=True)

def close_claw():
    claw_motor.run_until_stalled(speed=50, then=Stop.HOLD, duty_limit=80)
    return claw_motor.angle()

def rotateToColor(color : Color):
    global total_angle
    print(find_key(dropzones, color), color)
    if color not in dropzones.values():
        arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=total_angle, wait=True)
        return "Total angle"
    else:
        arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=find_key(dropzones, color), wait=True)
        return "Other"

def reset_to_pickupzone():
    arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=0, then=Stop.HOLD, wait=True)

def mesure():
    """Returns degress for total arm rotation"""
    global total_angle
    arm_rot_motor.reset_angle(angle=0)
    arm_rot_motor.run(speed=ROT_SPEED)
    while not touch_sensor.pressed():
        tmp = color_sensor.color()
        if tmp in COLORS and tmp not in dropzones.values():
            dropzones[arm_rot_motor.angle()] = tmp
    total_angle = arm_rot_motor.angle()
    print("Dropzones: ")
    print(dropzones)
    arm_rot_motor.stop()

def find_key(input_dict, value):
    """Find the key for a value in a dict"""
    return next((k for k, v in input_dict.items() if v == value), None)

def initiation():
    mailbox = connection.connect(ev3)
    arm_up(waitfor_sensor=False)
    arm_raise_motor.reset_angle(angle=0)
    close_claw()
    claw_motor.reset_angle(angle=0)
    if mailbox["type"] == "client":
        mailbox["mbox"].wait_new()
    mesure()
    if mailbox["type"] == "client":
        reset_to_pickupzone()
    else:
        reset_to_pickupzone()
        mailbox["mbox"].send("Other")
    return mailbox

def mail_pickupavalible(mailbox):
    if mailbox["mbox"].read() != "pickingup":
        return True
    return False

def checkobject_ispresent(color : Color):
    if color == Color.BLACK: return color
    ev3.light.off()
    rotateToColor(color=color)
    open_claw()
    arm_down()
    angle = close_claw()
    if abs(angle) < 5:
        ev3.light.on(Color.RED)
    else:
        ev3.light.on(Color.GREEN)
    open_claw()
    arm_up(waitfor_sensor=False)
    return color

def pickup(mailbox):
    while mailbox["mbox"].read() != "Other" and mailbox["type"] == "client":
        time.sleep(1)
    print(mailbox["mbox"].read())
    reset_to_pickupzone()
    open_claw()
    arm_down()
    angle = close_claw()
    if mailbox["type"] == "client":
        color = arm_up(waitfor_sensor=True)
        return color
    i = 0
    while abs(angle) < 5:
        i = i+1
        open_claw()
        arm_up(waitfor_sensor=False)
        if i == 3:
            #mailbox["mbox"].send("Wait for new order")
            time.sleep(15) # ordern har kommit
            i = 0
        else:
            time.sleep(3)
        arm_down()
        angle = close_claw()
    color = arm_up(waitfor_sensor=True)
    return color

def drop(mailbox, color : Color):
    dropspot = rotateToColor(color=color)
    arm_down()
    open_claw()
    arm_up(waitfor_sensor=False)
    if mailbox["type"] == "host":
        if dropspot == "Other":
            mailbox["mbox"].send("Other")
        else:
            mailbox["mbox"].send("Total Angle")

def check_buttons():
    if Button.LEFT in ev3.buttons.pressed() and len(dropzones) <= 1:
        a_color = dropzones.values()[0]
        return a_color
    elif Button.UP in ev3.buttons.pressed() and len(dropzones) <= 2:
        a_color = dropzones.values()[1]
        return a_color
    elif Button.RIGHT in ev3.buttons.pressed()  and len(dropzones) <= 3:
        a_color = dropzones.values()[2]
        return a_color
    return Color.BLACK