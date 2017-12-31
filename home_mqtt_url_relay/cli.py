#!/usr/bin/env python

import os
import json
from urllib.error import URLError
from urllib.request import urlopen

import fire
import paho.mqtt.client as mqtt

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '..')

from .mqtt_base import MQTTBase

class CliApp(object):
    'Application class for cli usage'

    def serve(self, port=8880, database_directory=os.path.join(PROJECT_DIR, 'db')):
        'Run server'
        self.mqtt_client = MQTTBase()
        self.mqtt_client.connect_mqtt()
        self.mqtt_client.mqtt_client.on_message = self.any_callback
        self.mqtt_client.subscribe('any')
        self.mqtt_client.block_until_connect()
        self.mqtt_client.run_forever()

    def any_callback(self, client, userdata, message):
        print(message.payload) # byte array of url
        url = message.payload.decode('utf-8')
        print('Opening {}'.format(url))
        try:
            urlopen(url)
        except URLError as e:
            print('Exception: {}'.format(str(e)))



def main():
    'Entry point of web-eremote-mini'
    fire.Fire(CliApp)

if __name__ == '__main__':
    main()