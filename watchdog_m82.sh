#!/data/data/com.termux/files/usr/bin/sh
export BOT_TOKEN="8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
export CHAT_ID="1020305418"
cd ~/M82-Molina-Core
if ! pgrep -f m82_final.py > /dev/null; then
  echo "[$(date)] M82 CAIDO - REINICIANDO" >> watchdog.log
  BOT_TOKEN=$BOT_TOKEN CHAT_ID=$CHAT_ID nohup python3 -u m82_final.py > final.log 2>&1 &
fi
