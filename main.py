#!/usr/bin/env pybricks-micropython
import functional as f
from pybricks.parameters import Port, Stop, Direction, Button, Color

f.mesure()

alive = True
while alive:
    f.drop(color=Color.RED)