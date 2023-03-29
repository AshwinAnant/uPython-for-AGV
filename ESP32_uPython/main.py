# Import necessary libraries
from umqtt.simple import MQTTClient
from machine import Pin, DAC
import pinout
import motordrive
import networking
import time
import socket
import network
import ujson
#Function to drive : forward(), left(), right(), sharpleft(), sharpright(), reverse(), stop()
#Functions in network : network_connect(), server_connect(), send_data(path), receive_data()


networking.network_connect()
networking.server_connect()
data=networking.receive_data()
direction=data[0]
path=data[1]
# Main program loop

x=0
k=0
while True:
    
    # Read the sensor values
    left_value=pinout.left_sensor.value()
    right_value=pinout.right_sensor.value()
    center_value=pinout.center_sensor.value()
    left_most_value=pinout.left_most_sensor.value()
    right_most_value=pinout.right_most_sensor.value()
    
    # Determine the line position
    if left_most_value ==1 and left_value == 1 and center_value == 1 and right_value == 1 and right_most_value ==1:
        line_position = "center"
    elif left_most_value ==0 or right_most_value ==0:
        line_position = "stop"
    elif left_value == 1 and center_value == 1 and right_value == 0:
        line_position = "right"
    elif left_value == 0 and center_value == 1 and right_value == 1:
        line_position = "left"
    elif  left_value == 1 and center_value == 0 and right_value == 1:
        line_position = "center"

    
    # Determine the robot's action based on the line position
    if line_position == "center":
        motordrive.forward()
        #print("center")
        
    elif line_position == "left":
        motordrive.left()
        #print("left")
        
    elif line_position == "right":
        motordrive.right()
        #print("right")
        
    elif line_position == "stop":
        motordrive.stop()
        time.sleep(0.5)
        networking.send_data(path[k])
        if k<len(path):
            k=k+1
            
        if direction[x]== 'straight':
            motordrive.forward()
            x=x+1
            print('straight')
            time.sleep(0.5)
            
        elif direction[x]=='right':
            motordrive.sharpright()
            x=x+2
            print('right')

        elif direction[x]=='left':
            motordrive.sharpleft()
            x=x+2
            print('left')
        #x=x+1

       # print("stop")
        

    # Adjust the delay time based on the line position to control the robot speed
    if line_position == "center":
        time.sleep(0.01)
    else:
        time.sleep(0.005)
