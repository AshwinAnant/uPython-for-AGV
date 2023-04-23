from umqtt.simple import MQTTClient
import time
import socket
import network
import ujson


def network_connect():
    # Connecting to the internert
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to network...")
        sta_if.active(True)
        sta_if.connect("Ragupathy_Home", "Ragupathy@2")
        #sta_if.connect("RK", "halamathihabibo")
        while not sta_if.isconnected():
            pass
    print("Connected to network with IP address", sta_if.ifconfig()[0])
    
def send_data(path):
    # Send the JSON data when the button is pressed
#     client.sendall(direction)
#     print('sent to server')
    

    CLIENT_NAME= 'client'
    BROKER_ADDR='192.168.43.248'
    mqttc= MQTTClient(CLIENT_NAME,BROKER_ADDR,keepalive=120)
    mqttc.connect()
    BTN_TOPIC= CLIENT_NAME.encode()+b'/btn/0'
    a=path
    mqttc.publish(BTN_TOPIC, str(a))
    #mqttc.disconnect()
    

