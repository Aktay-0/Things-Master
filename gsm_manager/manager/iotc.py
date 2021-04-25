import paho.mqtt.client as mqtt
import json
import time
import re

class Config():
    config_data = {}

config = Config()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if re.match(r"^v1/devices/me/rpc/request/.+", msg.topic):
        data = json.loads(msg.payload)
        if data['method'] == 'update':
            config.config_data = data['params']
            bft = msg.topic.split('/')
            client.publish("v1/devices/me/rpc/response/" + bft[len(bft) - 1], '{"status": 0}')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(mosq, obj, mid):
    print("Publish mid: " + str(mid))