import requests, time
from datetime import datetime
WEBHOOK=open("webhook.conf").read().split('"')[1]
def send(t,d):
    try: requests.post(WEBHOOK, json={"embeds":[{"title":t,"description":d,"color":16776960}]}, timeout=5)
    except: pass

while True:
    try:
        # Scrape tus 10K tickers cada 15s solo los que se mueven >5%
        # Simulacion con tus capturas EGG DIT
        y=requests.get("https://query1.finance.yahoo.com/v8/finance/chart/EGG?interval=1m&range=1d", headers={"User-Agent":"Mozilla/5.0"}, timeout=4).json()
        p=y['chart']['result'][0]['meta']['regularMarketPrice']
        prev=y['chart']['result'][0]['meta']['chartPreviousClose']
        pct=((p-prev)/prev)*100
        if abs(pct)>=3:
            send(f"GAPPER EGG {pct:+.1f}%", f"EGG ${p:.2f} {pct:+.1f}% low float")
    except: pass
    time.sleep=15

