import requests, time
from datetime import datetime
WEBHOOK=open("webhook.conf").read().split('"')[1]
def send(t,d,c=15158332):
    try: requests.post(WEBHOOK, json={"embeds":[{"title":t,"description":d,"color":c}]}, timeout=5)
    except: pass
    print(f"{datetime.now().strftime('%H:%M:%S')} OIL {t}")

last_oil=0; last_gold=0
while True:
    try:
        for sym,name in [("CL=F","OIL"),("GC=F","GOLD")]:
            y=requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d", headers={"User-Agent":"Mozilla/5.0"}, timeout=4).json()
            p=y['chart']['result'][0]['meta']['regularMarketPrice']
            if sym=="CL=F":
                if abs(p-last_oil)>=0.10 or p<=75.5: # 10 centavos ya avisa, no 30
                    send(f"🚨 OIL ${p:.2f} {'CRASH <75.5' if p<=75.5 else ''}", f"WTI ${p:.2f} | Goldman $80-90 | Soporte 75", 15158332)
                    last_oil=p
            else:
                if abs(p-last_gold)>=2: # GOLD cada $2
                    send(f"GOLD ${p:.2f}", f"GOLD ${p:.2f} - DDC +9.7% FURY +5.5%", 3447003)
                    last_gold=p
    except Exception as e: print(e)
    time.sleep(6)
