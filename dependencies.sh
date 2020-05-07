#!/bin/bash

sudo apt update
sudo apt-get install --yes curl
sudo apt install --yes python3-pip python-pip ruby-foreman awscli python3-boto3 redis python3-hiredis python3-lxml python-lxml gunicorn gunicorn3
pip3 install --user Flask requests tavern feedgen rfeed
pip install --user feedgen rfeed requests