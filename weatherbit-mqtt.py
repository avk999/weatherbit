from config import *
import paho.mqtt.client as mqtt
import random
import requests
import json
import logging


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
    sys.exit()

if r.status_code != 200:
    err=f"Status={r.status_code}, text={r.text}"
    client.publish(MQTT_TOPIC_PREFIX+'/status')
    logging.log(logging.ERROR, err)
    sys.exit()
res=json.dumps(r.json()['data'][0])

# res= """
# {"rh": 86.33, "pod": "n", "lon": 5.0451, "pres": 100.13, "timezone": "Europe/Amsterdam", "ob_time": "2021-10-03 13:47", "country_code": "NL", "clouds": 100, "ts": 1633268847, "solar_rad": 70.1, "state_code": "07", "city_name": "Weesp", "wind_spd": 3.95476, "wind_cdir_full": "southwest", "wind_cdir": "SW", "slp": 1001.14, "vis": 2, "h_angle": 30, "sunset": "17:12", "dni": 732.78, "dewpt": 11.5, "snow": 0, "uv": 1.42631, "precip": 1, "wind_dir": 232, "sunrise": "05:46", "ghi": 389.41, "dhi": 86.35, "aqi": 38, "lat": 52.3044, "weather": {"icon": "r01d", "code": 500, "description": "Light rain"}, "datetime": "2021-10-03:13", "temp": 13.8, "station": "D3248", "elev_angle": 24.99, "app_temp": 13.8}
# """

client.publish(MQTT_TOPIC_PREFIX+'/data', payload=res)
client.publish(MQTT_TOPIC_PREFIX+'/status', payload='OK')