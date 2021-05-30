import paho.mqtt.client as mqtt
from django.conf import settings
from .smsc_api import *

smsc = SMSC()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if (msg.topic == 'device/alarm'):
        from .views import set_log
        set_log(msg)
        r = smsc.send_sms(settings.SEND_PHONE, "Warning!", sender='SMSC.RU')
        print(r)
    elif (msg.topic == 'device/config'):
        from .views import set_config
        set_config(msg)



def on_publish(mosq, obj, mid):
    print("Publish mid: " + str(mid))
    

def on_subscribed(mosq, obj, mid, granted_qos):
    #print("Subscribed mid: " + str(mid) + ", qos: " + str(granted_qos))
    pass

def on_log(mosq, obj, mid, string):
    print("Log: " + str(string))
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.username_pw_set('host', 'host')
client.on_log = on_log
client.on_publish = on_publish
client.on_subscribed = on_subscribed

client.connect(settings.MQTT_HOST, settings.MQTT_PORT, 60)
client.subscribe("device/alarm", 0)
client.subscribe("device/config", 0)
#client.subscribe("v1/devices/me/attributes", 0)
#client.subscribe("v1/devices/me/rpc/request/+", 0)

#client.publish("v1/devices/me/telemetry", '{"temp": 123}')

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

#client.loop_start()

#client.publish("v1/devices/me/telemetry", json.dumps(config))

