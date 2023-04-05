#!/usr/bin/env pybricks-micropython
import functional as f
from pybricks.parameters import Port, Stop, Direction, Button, Color

#f.arm_down()
#f.arm_up(waitfor_sensor=False)
f.arm_up(waitfor_sensor=False)
f.close_claw()
f.open_claw()
f.arm_down()
f.close_claw()
f.arm_up(waitfor_sensor=True)
# f.mesure()
# f.open_claw()
# f.arm_down()

# alive = True
# while alive:
#     f.drop(color=Color.RED)