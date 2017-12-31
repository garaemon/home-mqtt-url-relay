#!/usr/bin/env python

import logging
from urllib.parse import urlparse
import os

import paho.mqtt.client as mqtt

logger = logging.getLogger()


class MQTTBase(object):
    MQTT_URL_ENV = 'CLOUDMQTT_URL'

    def __init__(self):
        self.is_connected = False
        self.verify_mqtt_env()
        self.connect_mqtt()

    def connect_mqtt(self):
        self.mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)
        url = urlparse(os.environ[self.MQTT_URL_ENV])
        self.mqtt_client.username_pw_set(username=url.username,
                                         password=url.password)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_publish = self.on_publish
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.connect(url.hostname, port=url.port)

    def on_connect(self, client, userdata, flags, rc):
        self.is_connected = True
        logging.info('Connected to MQTT Broker')
        print('Connected to MQTT Broker')

    def on_message(self, client, userdata, flags, rc):
        pass

    def on_disconnect(self, client, userdata, rc):
        logging.info('Connection lost')

    def on_publish(self, client, userdata, rc):
        logging.info('published')

    def verify_mqtt_env(self):
        if self.MQTT_URL_ENV not in os.environ:
            raise Exception('No %s is defined' % self.MQTT_URL_ENV)

    def block_until_connect(self):
        while self.is_connected is False:
            self.mqtt_client.loop(timeout=1.0)

    def run_forever(self):
        self.mqtt_client.loop_forever()

    def proc(self, timeout=1.0):
        self.mqtt_client.loop(timeout=timeout)

    def disconnect(self):
        self.mqtt_client.disconnect()

    def subscribe(self, topic):
        self.mqtt_client.subscribe(topic)

if __name__ == '__main__':
    b = MQTTBase()
    b.block_until_connect()
