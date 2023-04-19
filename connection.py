

def connect():
  while not connected:
        if Button.CENTER in ev3.buttons.pressed():
            ev3.speaker.beep()
            connect()
            break
        wait(20)
    wait(200)

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