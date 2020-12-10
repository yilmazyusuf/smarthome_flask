#!/bin/bash
#nohup ./connect_speaker.sh </dev/null &>/dev/null &
bluetoothctl
    pulseaudio -k
pulseaudio -D
bluetoothctl
agent on
default-agent
power on
pair 1B:83:2A:8B:02:37
trust 1B:83:2A:8B:02:37
connect 1B:83:2A:8B:02:37
