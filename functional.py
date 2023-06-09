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


COLORS = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN]
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
        arm_raise_motor.run_target(speed=60, target_angle=-220, then=Stop.HOLD, wait=True)
        while color == None:
            color = getColorOfObject()
        ev3.light.on(color)
    arm_raise_motor.run_target(speed=-120, target_angle=-380, then=Stop.HOLD, wait=True)

    if waitfor_sensor : return color

def open_claw():
    print("Claw open")
    claw_motor.run_target(speed=80, target_angle=-90, then=Stop.HOLD, wait=True)

def close_claw():
    claw_motor.run_until_stalled(speed=50, then=Stop.HOLD, duty_limit=100)
    return claw_motor.angle()

def rotateToColor(color : Color):
    global total_angle
    print(find_key(dropzones, color), color)
    angle = find_key(dropzones, color)
    if angle == None : return
    arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=angle, wait=True)

def reset_to_pickupzone(_type = ""):
    if _type == "host":
        global total_angle
        arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=total_angle, then=Stop.HOLD, wait=True)
    else:
        arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=0, then=Stop.HOLD, wait=True)

def mesure(type):
    """Returns degress for total arm rotation"""
    global total_angle
    arm_rot_motor.run(speed=ROT_SPEED)
    colors = []
    if type == "host" : colors = COLORS[:2]
    else : colors = COLORS[2:]
    while not touch_sensor.pressed():
        tmp = color_sensor.color()
        if tmp in colors and tmp not in dropzones.values():
            dropzones[arm_rot_motor.angle()] = tmp
            ev3.speaker.beep(frequency=500, duration=50)
    total_angle = arm_rot_motor.angle()
    print(total_angle)
    print("Dropzones: ")
    print(dropzones)
    arm_rot_motor.stop()

def find_key(input_dict, value):
    """Find the key for a value in a dict"""
    return next((k for k, v in input_dict.items() if v == value), None)

def initiation():
    global COLORS
    mailbox = connection.connect(ev3)
    arm_down()
    time.sleep(2)
    arm_raise_motor.reset_angle(angle=0)
    arm_up(waitfor_sensor=False)
    close_claw()
    claw_motor.reset_angle(angle=0)
    if mailbox["type"] == "client":
        arm_rot_motor.reset_angle(angle=0)
        arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=300, then=Stop.HOLD, wait=True)
        mailbox["mbox"].wait_new()
        mailbox["mbox"].send("pickingup")
        reset_to_pickupzone()     
    mesure(mailbox["type"])
    reset_to_waitpos()
    if mailbox["type"] == "host":
        mailbox["mbox"].send("Done")
        mailbox["mbox"].wait_new()
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

def reset_to_waitpos():
    global total_angle
    arm_rot_motor.run_target(speed=ROT_SPEED, target_angle=total_angle/2, then=Stop.HOLD, wait=True)


def ordertime():
    ev3.screen.clear()
    seconds = 0
    ev3.light.on(Color.YELLOW)
    ev3.screen.draw_text(50, 50, str(seconds) + " seconds" , text_color=Color.BLACK, background_color=None)
    while Button.CENTER not in ev3.buttons.pressed():
        if Button.UP in ev3.buttons.pressed():
            seconds += 1
            ev3.screen.clear()
            ev3.screen.draw_text(50, 50, str(seconds) + " seconds" , text_color=Color.BLACK, background_color=None)
            print(seconds)
            time.sleep(1)
        if Button.DOWN in ev3.buttons.pressed():
            if seconds > 0:
                seconds -= 1
                ev3.screen.clear()
                ev3.screen.draw_text(50, 50, str(seconds) + " seconds" , text_color=Color.BLACK, background_color=None)
                print(seconds)
            time.sleep(1)
    ev3.screen.clear()
    ev3.screen.draw_text(50, 50, "Waiting " + str(seconds) + " seconds..." , text_color=Color.BLACK, background_color=None)
    return seconds

def pickup(mailbox):
    while not mail_pickupavalible(mailbox=mailbox): # Lägg till alans funktion här, värdet måste uppdateras, "Total angle" är bevarat från förra gången
        reset_to_waitpos()
        time.sleep(0.5)

    mailbox["mbox"].send("pickingup")

    reset_to_pickupzone(mailbox["type"])
    open_claw()
    arm_down()
    angle = close_claw()
    i = 0
    while abs(angle) < 10:
        i = i+1
        open_claw()
        arm_up(waitfor_sensor=False)
        if i == 3:
            time.sleep(ordertime()) # ordern har kommit
            i = 0
        else:
            count = 0
            while count <= 3:
                count = count + 1
                checkobject_ispresent(check_buttons())
                time.sleep(1)
        arm_down()
        angle = close_claw()
    color = arm_up(waitfor_sensor=True)
    if color not in dropzones.values():
        arm_down()
        open_claw()
        arm_up(waitfor_sensor=False)
        mailbox['mbox'].send("pickupAvaiable")
        time.sleep(1)
        return None
    else:
        mailbox['mbox'].send("pickupAvaiable")
    return color

def drop(color : Color):
    if color not in dropzones.values():
        return
    rotateToColor(color=color)
    arm_down()
    open_claw()
    arm_up(waitfor_sensor=False)

def check_buttons():
    if Button.LEFT in ev3.buttons.pressed() and len(dropzones) <= 1:
        a_color = list(dropzones.values())
        return a_color[0]
    elif Button.UP in ev3.buttons.pressed() and len(dropzones) <= 2:
        a_color = list(dropzones.values())
        return a_color[1]
    elif Button.RIGHT in ev3.buttons.pressed()  and len(dropzones) <= 3:
        a_color = list(dropzones.values())
        return a_color[2]
    return Color.BLACK
