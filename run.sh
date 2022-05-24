#!/usr/bin/env bash

python3.9 -m venv ./py39
source ./py39/bin/activate
pip install -r requirements.txt
python main.py
