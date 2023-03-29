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

#networking.mqtt_connect()
networking.network_connect()
#networking.server_connect()
def sub_cb(topic, msg):
    msge=msg.decode()
    msge=eval(msge)
    print(msge[0])
    print(msge[1])
    run(msge[0],msge[1])
CLIENT_NAME= 'client'
BROKER_ADDR='192.168.29.15'
mqttc= MQTTClient(CLIENT_NAME,BROKER_ADDR,keepalive=120)
mqttc.connect()
print("connected to broker")
# Subscribe to topic and attach callback function
mqttc.set_callback(sub_cb)
mqttc.subscribe("testTopic")

def run(path,direction):
    direction=eval(direction)
    path=eval(path)
    print(len(direction))
    # Main program loop
    x=0
    k=0
    status=True
    while status==True:
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
            print("stop")

            if k<len(path):
                #networking.send_data(path[k])
                k=k+1
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
            motordrive.stop() # changed before trial
            time.sleep(0.5)
#             print("stop")
            
            
            if x<len(direction):
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
                    
                elif direction[x]=='pause':
                    motordrive.stop()
                    time.sleep(3)
                    x=x+1
                    print('pause')
                    
                elif direction[x]=='uTurn':
                    motordrive.right()
                    motordrive.right()
                    x=x+2
                    print('uTurn')
                    
                if x>=len(direction):
                    status=False
                    
            
              # Adjust the delay time based on the line position to control the robot speed
        if line_position == "center":
            time.sleep(0.01)
        else:
            time.sleep(0.005)
                      
while True:
    mqttc.wait_msg()

