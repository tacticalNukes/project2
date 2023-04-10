#!/usr/bin/env pybricks-micropython
import functional as f
from pybricks.parameters import Port, Stop, Direction, Button, Color

f.initiation()

alive = True
while alive:
    f.drop(f.pickup())