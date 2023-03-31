import paho.mqtt.client as mqtt
from time import sleep
from main_ML import *

#--- variables and flags
localhost = "127.0.0.1"
myip = "192.168.0.50"
RCT_flag = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic = "RCT_request")
    client.subscribe(topic = "stop")


def on_message(client, userdata, msg):
    # define global variables
    global part_id
    global RCT_flag
    print(msg.topic)
    #--- initiate the RCT prediction
    if msg.topic == "RCT_request":
        part_id = str(msg.payload.decode("utf-8"))
        print(f"Requested: RCT for {part_id}")
        RCT_flag = True
    if msg.topic == "stop":
        RCT_flag = False
        print("\33[31mPrediction canceled remotely\33[0m")


client = mqtt.Client()
client.connect(localhost,1883,60) # verify the IP address before connect
client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

try:
    while True:
        sleep(1)
        if RCT_flag == True:
            print(f"\33[32m----------------- Predicting RCT for {part_id} -----------------\33[0m")
            int_part_id = int(part_id)
            main(part_id)
            x = 0
            wait = 20
            print("Waiting for next request ...")
            RCT_flag = False
except KeyboardInterrupt:
    print("\33[31mML function stopped from keyboard.\33[0m")
    client.publish(topic= 'status', payload = 'ML function stopped from keyboard')
except:
    client.publish(topic= 'status', payload = 'ML function failure')
    print("\33[31mProgram exited inappropriately.\33[0m")
