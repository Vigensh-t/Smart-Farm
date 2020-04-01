import config
import network
import time
from machine import ADC, Pin
from umqtt.simple import MQTTClient



PUMP_PIN = ---
SWIM_LEVEL_PIN = ----

MQTT_TOPIC_MOISTURE = "home/moisture"
MQTT_TOPIC_TANK = "home/tank"
MQTT_TOPIC_IRRIGATE = "home/irrigate"


def run_pump():
  print("pumping water")
  pump = Pin(-----)
  pump(1)
  time.sleep(3)
  pump(0)
  print("turning off")


def read_moisture():
  adc = ADC(0)
  return adc.read()


def read_tank_full():
  tank = Pin(-----------)
  return not tank()


def connect_wifi():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(config.ssid, config.password)
    time.sleep(5)
  
  

def connect_mqtt():
  client = MQTTClient(config.mqtt_client_id, config.mqtt_broker, 1883, config.mqtt_user, config.mqtt_password)
  client.set_callback(on_mqtt)
  client.connect()
  print("Connected to MQTT on {}".format(config.mqtt_broker))
  client.subscribe(MQTT_TOPIC_IRRIGATE)
  print("Subscribed to topic {}".format(MQTT_TOPIC_IRRIGATE))
  return client


def on_mqtt(topic, msg):
  print(topic, msg)
  if topic == MQTT_TOPIC_IRRIGATE:
    if (msg == b"water_avocado"):
      run_pump()
  else:
    print("Unknown topic {}".format(topic))


def main():
  connect_wifi()
  mqtt = connect_mqtt()

  while 1:
    val = read_moisture()
    is_full = read_tank_full()
    mqtt.check_msg()
    print(val, is_full)
    print("Sending moisture to {}".format(MQTT_TOPIC_MOISTURE))
    normalized_moisture = 100 - (val * 100 / 1024.0)
    mqtt.publish(MQTT_TOPIC_MOISTURE, bytes(str(int(normalized_moisture)), 'utf-8'))
    mqtt.publish(MQTT_TOPIC_TANK, bytes(str(is_full), 'utf-8'))
    time.sleep(5)

  while 1:
    mqtt.check_msg()


if __name__== "__main__":
  main()
