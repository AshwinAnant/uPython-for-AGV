from machine import Pin, DAC
import time
import pinout

# Function to drive the robot forward
# Function to drive the robot forward
def forward():
    pinout.motor_left_forward(1)
    pinout.motor_left_reverse(0)
    pinout.motor_right_forward(1)
    pinout.motor_right_reverse(0)

# Function to turn the robot left
def left():
    pinout.motor_left_forward(0)
    pinout.motor_left_reverse(1)
    pinout.motor_right_forward(1)
    pinout.motor_right_reverse(0)

# Function to turn the robot right
def right():
    pinout.motor_left_forward(1)
    pinout.motor_left_reverse(0)
    pinout.motor_right_forward(0)
    pinout.motor_right_reverse(1)
    
# Function to turn the robot sharp left
def sharpleft():
    pinout.motor_left_forward(0)
    pinout.motor_left_reverse(0)
    pinout.motor_right_forward(1)
    pinout.motor_right_reverse(0)
    time.sleep(2.5)

# Function to turn the robot sharp right
def sharpright():
    pinout.motor_left_forward(1)
    pinout.motor_left_reverse(0)
    pinout.motor_right_forward(0)
    pinout.motor_right_reverse(0)
    time.sleep(2.5)


# Function to turn the robot reverse
def reverse():
    pinout.motor_left_forward(0)
    pinout.motor_left_reverse(1)
    pinout.motor_right_forward(0)
    pinout.motor_right_reverse(1)
    
# Function to stop the robot
def stop():
    pinout.motor_left_forward(0)
    pinout.motor_left_reverse(0)
    pinout.motor_right_forward(0)
    pinout.motor_right_reverse(0)

def uTurn():
    pinout.motor_left_forward(1)
    pinout.motor_left_reverse(0)
    pinout.motor_right_forward(0)
    pinout.motor_right_reverse(1)
    time.sleep(2.8)
