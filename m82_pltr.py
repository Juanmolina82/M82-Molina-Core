import requests, time
from datetime import datetime
WH="https://discord.com/api/webhooks/TU_WEBHOOK_PLTR" # o https://ntfy.sh/M82-PLTR
WEBHOOK=open("webhook.conf").read().split('"')[1] if True else WH
def send(t,d):
    try: requests.post(WEBHOOK, json={"embeds":[{"title":t,"description":d,"color":3066993}]}, timeout=5)
    except: pass
    print(f"{datetime.now().strftime('%H:%M:%S')} PLTR {t}")

last=0
while True:
    try:
        y=requests.get("https://query1.finance.yahoo.com/v8/finance/chart/PLTR?interval=1m&range=1d", headers={"User-Agent":"Mozilla/5.0"}, timeout=4).json()
        p=y['chart']['result'][0]['meta']['regularMarketPrice']
        prev=y['chart']['result'][0]['meta']['chartPreviousClose']
        pct=((p-prev)/prev)*100
        if abs(p-last)>=0.25: # cada 25 centavos
            send(f"PLTR ${p:.2f} {pct:+.2f}%", f"PLTR ${p:.2f} {pct:+.2f}% {datetime.now().strftime('%H:%M:%S VET')}")
            last=p
    except: pass
    time.sleep(8)
