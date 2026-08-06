#!/bin/bash
source ~/.env_m82
export BOT_TOKEN
export CHAT_ID

while true; do
    python3 m82_institutional_matrix.py
    sleep 2
done
