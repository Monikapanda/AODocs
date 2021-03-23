#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CD $DIR
echo "Current Path:" $DIR

echo "Installing PIP..."
python3 get-pip.py

echo "Installing Python dependency libraries"
pip install jsonlib
pip install google-api-python-client
pip install oauth2client
pip install httplib2
