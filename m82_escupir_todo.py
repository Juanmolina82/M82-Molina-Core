import requests, time
from datetime import datetime
TOPIC="M82-ESCUPE"
def send(t,m):
    try:
        requests.post(f"https://ntfy.sh/{TOPIC}", data=m.encode(), headers={"Title":t}, timeout=5)
        print(f"{datetime.now().strftime('%H:%M:%S')} ✅ {t}")
    except Exception as e:
        print(f"ERR {e}")

send("M82 ESCUPIENDO TODO ON", "OIL 75 + PLTR + EGG + DIT + GOLD + ETFs - cada 3s sin filtro")

tickers=["PLTR $156","OIL $75.20","EGG +8.5%","DIT +10%","GOLD $4142","SPY 0.5%","XLE -1.2%","FURY +5.5%"]
i=0
while True:
    i+=1
    # Sin if, sin filtro, escupe todo
    msg=f"#{i} {' | '.join(tickers)} | {datetime.now().strftime('%H:%M:%S VET')}"
    send(f"ESCUPE #{i}", msg)
    time.sleep(3)
