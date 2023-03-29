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
        while not sta_if.isconnected():
            pass
    print("Connected to network with IP address", sta_if.ifconfig()[0])
    
def server_connect():
    # Define the host and port
    host = "192.168.29.15" 
    port = 1333

    # Create a socket object
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the host and port
    client.connect((host, port))
    print('connected to the server')
    
def send_data(path):
    # Send the JSON data when the button is pressed
#     client.sendall(direction)
#     print('sent to server')
    
    CLIENT_NAME= 'client'
    BROKER_ADDR='192.168.29.15'
    mqttc= MQTTClient(CLIENT_NAME,BROKER_ADDR,keepalive=60)
    mqttc.connect()
    BTN_TOPIC= CLIENT_NAME.encode()+b'/btn/0'
    a=path
    mqttc.publish(BTN_TOPIC, str(a))
    

    
def receive_data():
    # Receive the JSON data
    json_data = client.recv(1024)

    # Decode the byte string to a string
    json_data = json_data.decode()

    # Convert the JSON string to a list
    data = ujson.loads(json_data)
    print(data)
    return data

