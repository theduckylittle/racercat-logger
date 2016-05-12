# RacerCat Telemetry Capture System
![RacerCat Logo](/logo-sm.png?raw=true) 

## Description
Modular python based telemetry capture system.  The goal is to provide an extensible telemetry capture system than can work with multiple types of input. Currently tested:

1. Garmin GLO for GPS capture.
2. Raspberry Pi Sense HAT for accelerometer data.

## Setting up the Dev Environment

```bash
virtualenv --python=python2 --prompt="(rc-logger) " ./env
pip install -r requirements.txt
```
