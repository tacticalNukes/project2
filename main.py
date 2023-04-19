#!/usr/bin/env pybricks-micropython
import functional as f
from pybricks.parameters import Port, Stop, Direction, Button, Color
import connection

host = connection.connect()

f.initiation()

alive = True
while alive:
    f.drop(f.pickup())