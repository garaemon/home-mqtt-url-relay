#!/bin/bash

FILE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd ${FILE_DIR}/..
source setup.sh
source .venv/bin/activate
home-mqtt-url-relay serve
