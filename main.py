#!/usr/bin/env pybricks-micropython
import functional as f
from pybricks.parameters import Port, Stop, Direction, Button, Color

mailbox = f.initiation()

alive = True
while alive:
    # if f.checkobject_ispresent(f.check_buttons()) != Color.BLACK:
    #     continue
    color = f.pickup(mailbox)
    f.drop(mailbox, color)