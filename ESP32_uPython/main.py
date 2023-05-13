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
inc=0
statusFlag= 0
last_function_called="wait_msg"
#Function to drive : forward(), left(), right(), sharpleft(), sharpright(), reverse(), stop()
#Functions in network : network_connect(), server_connect(), send_data(path), receive_data()

networking.network_connect()

def sub_cb(topic, msg):
    global inc
    global nodePoint
    global facingDirection
    global last_function_called
    if topic==b"testTopic":
        print("testTopic entered")
        msge_decoded=msg.decode()
        msge=eval(msge_decoded)
        print(msge)
        nodePoint=eval(msge[0])
        #print("The length of node is ",len(nodePoint))
        facingDirection=eval(msge[2])
        #print("The length of direction is ",len(facingDirection))
        #inc=0
        run(msge[0],msge[1])
    if topic==b"interrupt":
        print("interrupt entered")
        inc=0
        global statusFlag
        statusFlag= 1
        
CLIENT_NAME= 'client'
BROKER_ADDR='192.168.29.15'
mqttc= MQTTClient(CLIENT_NAME,BROKER_ADDR,keepalive=1000)
mqttc.connect()
print("connected to broker")
# Subscribe to topic and attach callback function
mqttc.set_callback(sub_cb)
#mqttc.subscribe(b"testTopic")
mqttc.subscribe(b"interrupt")
startingLocation=[2,0]
mqttc.publish("location",str(startingLocation))
def run(path,direction):
    global inc
    global last_function_called
    global statusFlag
    direction=eval(direction)
    path=eval(path)
    #print(len(direction))
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
            ####print("Entered Elif")
            print("stop")
            motordrive.stop() # changed before trial
            time.sleep(0.5)
            topic="location"
            location_info=[]
            if inc<len(nodePoint):
                location_info.append(nodePoint[inc])
                location_info.append(facingDirection[inc])
                
            if location_info != []:
                payload=str(location_info)
                print(payload)
                mqttc.publish(topic,payload)
            inc=inc+1
            ####print("The precheck status is",status)
            #last_function_called="check_msg"
            # Check for incoming messages
            statusFlag=0
            mqttc.check_msg()
#             statusFlag=0
#             inc=0
            ####print("The postcheck status is",status)
            ####print("The Status Flag :",statusFlag)
            ####print("x=",x)
            if statusFlag==1:
                print("Received flag")
            if x>=len(direction) or statusFlag==1:
                status=False

            if x<len(direction) and statusFlag==0:
                if direction[x]== 'straight':
                    motordrive.forward()
                    x=x+1
                    ####print('straight')
                    time.sleep(0.9)
                    
                elif direction[x]=='right':
                    motordrive.sharpright()
                    x=x+2
                    ####print('right')
                    
                elif direction[x]=='left':
                    motordrive.sharpleft()
                    x=x+2
                    ####print('left')
                    
                elif direction[x]=='pause':
                    motordrive.stop()
                    time.sleep(3)
                    x=x+1
                    ####print('pause')
                    
                elif direction[x]=='uTurn':
                    motordrive.uTurn()
                    x=x+2
                    ####print('uTurn')
                    
                
                    
                    
            
              # Adjust the delay time based on the line position to control the robot speed
        if line_position == "center":
            time.sleep(0.01)
        else:
            time.sleep(0.005)
                      
while True:
    ####print("Starting of condition")
    mqttc.subscribe(b"testTopic")
    statusFlag=0
    motordrive.stop()
    inc=0
    ####print("Ending of condition")
    #last_function_called="wait_msg"
    mqttc.wait_msg()
    #print("way to unsubcribe")
    #mqttc.unsubscribe(b"testTopic")
    ####print("before sending completed")
    mqttc.publish("comp","completed")



    
