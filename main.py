#!/usr/bin/env pybricks-micropython
import functional as f
from pybricks.parameters import Port, Stop, Direction, Button, Color

import time

mailbox = f.initiation()

alive = True
while alive:
    if f.checkobject_ispresent(f.check_buttons()) != None:
        continue
    f.drop(f.pickup(mailbox))