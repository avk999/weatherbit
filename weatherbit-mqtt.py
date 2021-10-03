from config import *
import paho.mqtt.client as mqtt
import random
import requests
import json
import logging
import sys


client =mqtt.Client(MQTT_CLIENT+'_'+str(random.randint(0,100000)))
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_HOST, MQTT_PORT)

wb_data={
    'country':WEATHERBIT_COUNTRY,
    'key':WEATHERBIT_KEY,
    'postal_code':WEATHERBIT_POSTAL_CODE
}

headers={
    'Accept': 'application/json'
}

try:
    r=requests.get(WEATHERBIT_ENDPOINT, headers=headers, params=wb_data)
    pass
except Exception as e:
    client.publish(MQTT_TOPIC_PREFIX+'/status', e.__str__())
    logging.log(logging.ERROR, e.__str__())
    client.disconnect()
    sys.exit()

if r.status_code != 200:
    err="ERROR, Status={}, text={}".format(r.status_code, r.text)
    client.publish(MQTT_TOPIC_PREFIX+'/status')
    logging.log(logging.ERROR, err)
    client.disconnect()
    sys.exit()
res=json.dumps(r.json()['data'][0])



client.publish(MQTT_TOPIC_PREFIX+'/data', payload=res)
client.publish(MQTT_TOPIC_PREFIX+'/status', payload='OK')
client.disconnect()