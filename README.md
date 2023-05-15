# project2 - PA1473 - Software Development: Agile Project

## Introduction

This is a agile based project with our supervisers as customers.
The product we agreed on to deliver is a software that controlls a LEGO EV3 robot arm.
The robot can sort LEGO bricks based on color. The robot can also collaborate with one identical robot,
the two robots work together to sort the colored LEGO bricks that are getting delivered.

## Getting started

### Installing LEGO® MINDSTORMS® EV3 MicroPython
Begin with starting up Visual Studio Code, go to extentions and search for EV3.
Select the extension with the name "LEGO® MINDSTORMS® EV3 MicroPython".
Install that extenstion.

### Connecting your robot to your computer
Start of by connecting your EV3 robot and your computer with the microusb cable.
After that open Visual Studio Code and the project.
On the bottom left there is a small tab "EV3DEV DEVICE BROWSER".
Right click and press "connect to a diffrent device".
Is everying is correct done your EV3 robot should come up, then just press ENTER.

### Connecting two robots
This program require two robots at the moment. Connecting two EV3 robots via bluetooth are done by
going in to each robots bluetooth settings. On one of the robots (Does not matter which one) check in the
checkbox "visible". After that go to your other robot and go down to devices. Select your other EV3 and press
connect. Press "Pair" on both robots (Might only be on one of them).

### Clone git repository
Begin with starting up Visual Studio Code, press the "Clone git repository" on the home page.
Go this projects homepage on github and click the green "<> Code" button. Make sure that the link mode is set to "HTTPS".
Copy the HTTPS link and paste it in your Visual Studio Code (The bar on the top of your window).

### Good to know
For the project to work you need a EV3 robot that is identical to ours.
That also means that the ports that we have calibrated in our code might not work for you.
Easyest way to transfer the code over to the robot is by using an microusb cable.

## Building and running

After connecting your robot to your computer you can run transfer the code
from Visual Studio Code to the robot by pressing the small "download" button in
the "EV3DEV DEVICE BROWSER" tab.

You can now run the code you just transferred by either navigating on the EV3 robot or run the program from your computer. If you would like to debug we recommend running it through your computer becouse
you can see potential error messages.

### What needs to be done before every start?
So the robots calibrations in the begining of the program works correctly please confirm this checklist.
- Rotate the robot rotation motor so the arm of the robot is poining perpendicular to the robots body when looking from the side of the robot that has the EV3 (the arm should be poining left if seen from the EV3).
- The arm of the robot should be at its lowest point, the claw should be as close to the ground as possible.

### Program walk through
Note: This program requires 2 robots at the moment. <br>
The software is built up with 3 diffrent classes. main.py ; functional.py ; connection.py.

#### main.py
This class starts the initilization of the robot and has the main while loop. This class was made so functional mostly contain functions. We wanted the code to be as clean and easy to read as possible.

#### functional.py
Note: The variable COLORS MUST contain all the colors that the robot should see. Also the three first colors in the list COLORS will only be recognized by the "host" and all the colors after that can only be recognized by the client. Example: COLORS = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN] means that the robot that is host can see Red, Blue, Yellow. The client can only see green. More about "host" and "client" under connection.py <br>
This class was made to mostly contain functions, it would be very flexible. We wanted each function to just do one specific thing. Then have one or two bigger functions that connected all the small ones. Therefore we did not write the same code over and over again and it was easy to read. When we implemented the collaboration between two robots the code got a litte messy.

#### connection.py
This class contains 2 functions. Connect and get_mailbox. This class function is to return what type
each of the two connected robots are. One robot is "host" and one is "client". By having this class we dont have to
write two diffrent programs for the host and the client. 

#### Program
To start the program start main.py. <br>
First connection.py runs on both robots. Now, dependning on which robot you
would like to be host you either press the right or left button on each EV3. The host robot is the one
that will be placed on the left side seen from the EV3s-side, when collaborating with the other robot. <br>
Note: Dont press for example right respective left on both robots, this will probobly result in a crash. <br>

##### Calibration
The robots now know which one is the host and which one is the client. Now the calibration begins. The host robot initialize its calibration first. The robot arm will rotate until it hits the button on the other side. It will save the amount of degrees it takes to rotate from the start posision to the max-angle. At the same time it will scan for colors with the color sensor. <br>
Note: It can only see the colors that have been put in the COLORS variable (The three first colors in the list). <br>
So if you would like to create a dropzone for example red, you hold up the red LEGO brick at the position you would like the dropzone to be at. Make sure that the color sensor can see the red brick. When the color sensor sees the color it will save the degrees it has to rotate from the start position  to get to that now saved dropzone for the red bricks. Make sure to calibrate all the colors that you would like the host robot to sort. <br>

After the calibration of the host robot the client does the same calibration. So be ready with the colored bricks. <br>

##### Pickup and Drop
First the client robot goes to the pick up zone and checks if there is a brick there. It can check this by reading the angle the claw motor runs. If the claw is fully closed there is no brick there. It then goes up and waits for three seconds. It then goes down again and checks. This will be repeated three times. After the third time the robot will go up and wait for input on the robot buttons. This is were you can set how many seconds will pass before the next order arive. Doing so by pressing the up and down buttons on that robot, then pressing center. The robot will then wait that amount of seconds before going down and checking if an new item has arrived. <br>

If the robot picks up and item the arm of the robot will raise so the colorsensor can see what color the pickedup brick has. If the color if the brick isnt in the calibrated dropzones it will lower it again and make the other robot pick it up instead. <br>
If the color if the brick is in the calibrated dropzones it will rotate to that dropzone and drop of the brick.
At the same time it sends to the other robot that the pick up zone is clear. This will make the robots more efficient, becouse they dont stop if it isnt necessary. <br>

##### Check if and dropzones has any bricks in it
If you would like to check if a specific dropzone has a brick in it you can hold the buttons on the EV3 as follows :
- Left button --> First calibrated dropzone
- Up button --> Second calibrated dropzone
- Right button --> Third calibrated dropzone <br>
The robot will then rotate to the selected dropzone and check if there is a brick there. If there is a brick at that dropzone the light on the EV3 will turn green. If not the light will turn red.

## Features

Lastly, you should write which of the user stories you did and didn't develop in this project, in the form of a checklist. Like this:
### Released
- [x] US01: I want the robot to pick up items
- [x] US01B I want the robot to pick up items from a designated position
- [x] US02: I want the robot to drop off items
- [x] US02B I want the robot to drop items off at a designated position
- [x] US04 I want the robot to tell me the color of an item.
- [x] US04B I want the robot to tell me the color of an item at a designated position
- [x] US05: I want the robot to drop items off at different locations based on the color of the item.
- [x] US06: I want the robot to be able to pick up items from elevated positions.
- [x] US08: I want to be able to calibrate maximum of three different colors and assign them to specific drop-off zones.
- [x] US08B I want to be able to callibrate items with three diffrent colors and drop the items off at specific dropp off zones based on color
- [x] US09 I want the robot to check the pickup location peridoically to see if a new item has arrived
- [x] US12 I want to able to manually set the locations and heights of on pickup zone and two dropoff zones
- [x] US13 Faster
§
### What we think will be released on workshop 3
- [x] US11 I want two robots to communicate and work together on items sorting without colliding with each other
- [x] US10 I want the robots to sort items at a specific time

### What we are unsure about
- [ ] US03 I want the robot to be able to determine if an item is present at a given location.
