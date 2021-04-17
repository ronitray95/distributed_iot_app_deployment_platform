#!/bin/bash

cp -r Scripts/* hackathon/AlgoRepo

python application_manager.py
python sensor_manager.py
python sensor.py
