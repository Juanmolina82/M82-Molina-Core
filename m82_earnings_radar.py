import requests, time, datetime
TICKERS = ["SNDK","AMD","SMCI","IONQ","SOUN","NET","UBER"]
for t in TICKERS:
    msg = f"{t} EARNINGS WATCH — Aug 5-6 AMC/BMO — Gamma setup cargado"
    requests.post("https://ntfy.sh/M82-Molina-Alerts", data=msg.encode(), headers={"Title":f"M82 {t} RADAR","Priority":"high","Tags":"fire"})
    print(f"✅ {t} alert sent")
    time.sleep(1)
