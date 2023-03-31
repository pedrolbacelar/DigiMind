#--- import python libraries
from flask import Flask, request
import json
from time import sleep
from flask_ngrok import run_with_ngrok
import paho.mqtt.client as mqtt

#-- defining variables
localhost = "127.0.0.1"

#--- defining the App
DigiMind = Flask(__name__)
run_with_ngrok(DigiMind)

#--- defining MQTT 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic = "status")

def on_message(client, userdata, msg):
    # print(msg.payload)
    if msg.topic == 'status':
        print(str(msg.payload.decode()))     #-- to print the message string
    
#--- defining application endpoints
@DigiMind.route('/')
def hello_world():
    return 'Hello, World!\nUse an appropriate endpoint such as "/RCT_part" to do more with DigiMind !!'

@DigiMind.route('/RCT_part', methods=['PUT'])
def handle_put_request():
    data = json.loads(str(request.data.decode())) # Get the JSON payload from the request
    print(f"================= {data[0]} ===========================")
    if data[0] == 'True':
        client.publish(topic= 'RCT_request', payload = data[1])
        print("starting prediction")
        response = f"Tracking {data[1]} ..."
    elif data[0] == 'False':
        client.publish(topic= 'stop', payload = 'stop')
        print("stopping prediction")
        response = f"Tracking CANCELED"
    else:
        response = "wrong data"
        print(data)
    
    return response, 200

client = mqtt.Client()
client.connect(localhost, 1883,60) # verify the IP address before connect
client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

if __name__ == '__main__':
    DigiMind.run()