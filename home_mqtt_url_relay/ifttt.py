#!/usr/bin/env python

from urllib.request import urlopen, Request
import json
import os

IFTTT_WEBHOOK_URL_FMT = 'https://maker.ifttt.com/trigger/{}/with/key/{}'


def run_ifttt_webhook(value1=None, value2=None, value3=None):
    'Call ifttt webhook'
    event = 'home_mqtt_url_relay'
    key = os.environ['IFTTT_KEY']
    url = IFTTT_WEBHOOK_URL_FMT.format(event, key)
    data = json.dumps({'value1': value1, 'value2': value2, 'value3': value3}).encode('utf-8')
    request = Request(url, data=data, method='POST', headers={"Content-Type": "application/json"})
    return urlopen(request)


def main():
    run_ifttt_webhook('value1')


if __name__ == '__main__':
    main()