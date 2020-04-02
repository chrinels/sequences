#!/usr/bin/env bash


VENV=$HOME/VirtualEnvironments/gold-sequence

python3 -m venv $VENV
source $VENV/bin/activate

pip3 install -U pip
pip3 install -U -r requirements.txt
