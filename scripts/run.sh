#! /bin/sh

set -ex

pip3.7 install -r requirements.txt

screen -XS alice-skill quit || true   # Stop current alice session

cd code

sleep 2

screen -dmS alice-skill python3.7 main.py