#! /bin/sh

set -ex

screen -XS alice-skill quit || true   # Stop current alice session

cd code

screen -dmS alice-skill python3.7 main.py