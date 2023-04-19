from pybricks.parameters import Color, Button
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxClient, BluetoothMailboxServer, TextMailbox

hostRobot = 'robot1'

def connect(ev3):
    while True:
        if Button.RIGHT in ev3.buttons.pressed():
            bluetoothInfo = get_mailbox(True)
            ev3.light.on(Color.RED)
            ev3.screen.print("Awaiting Connection...")
            bluetoothInfo[0].wait_for_connection(1)
            ev3.light.off()
            wait(1000)
            ev3.light.on(Color.GREEN)
            return { 'type': 'Server', 'mbox':bluetoothInfo[1] }
        if Button.LEFT in ev3.buttons.pressed():
            bluetoothInfo = get_mailbox(False)
            ev3.screen.print("Connecting")
            ev3.light.on(Color.RED)
            bluetoothInfo[0].connect(hostRobot)
            ev3.light.off()
            wait(1000)
            ev3.light.on(Color.GREEN)
            ev3.screen.print("Connected")
            return { 'type': 'Client', 'mbox':bluetoothInfo[1] }
        wait(20)

def get_mailbox(isServer):
    if isServer:
        connection = BluetoothMailboxServer()
        mailbox = TextMailbox('host',connection)
    else:
        connection = BluetoothMailboxClient()
        mailbox = TextMailbox('host',connection)
    return connection,mailbox

def wait_mail(string, mbox, ev3):
    received = False
    ev3.light.on(Color.RED)
    color_val = 0
    while not received:
        if mbox.read() == string:
            received = True
        if color_val % 300 == 0:
            ev3.light.on(Color.ORANGE)
        elif color_val % 300 == 150:
            ev3.light.on(Color.RED)
        wait(10)
        color_val += 1
    ev3.light.on(Color.GREEN)
    return True


def mail_pickupaviable(mailbox):
    if mailbox.read() != "pickingUp":
        return True
    return False