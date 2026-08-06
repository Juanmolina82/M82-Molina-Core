import requests, time
from datetime import datetime

TICKERS = ["PFE","CAT","MCD","MRK","ET","DUK","BP","AMD","SNDK","SMCI"]
URL = "https://ntfy.sh/M82-Molina-Alerts"
session = requests.Session()

def get_price_light(t):
    # Yahoo quote API ligero, sin lxml, sin cffi, sin segfault
    try:
        r = session.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?interval=1d&range=1d", timeout=10).json()
        meta = r['chart']['result'][0]['meta']
        return meta['regularMarketPrice'], meta.get('previousClose', meta['regularMarketPrice'])
    except:
        return 0,0

def send(title, msg):
    for _ in range(3):
        try:
            r = session.post(URL, data=msg.encode(), headers={"Title":title[:60],"Priority":"high","Tags":"chart_with_upwards_trend"}, timeout=10)
            if r.status_code==200:
                print(f"✅ {title}")
                return True
        except: time.sleep(2)
    return False

print(f"--- M82 V9.1 ULTRA-LIGHT {datetime.now()} ---")
for t in TICKERS:
    price, prev = get_price_light(t)
    chg = ((price-prev)/prev*100) if prev else 0
    # Calendario fijo Aug 3-7 de tus capturas
    cal = {
        "PFE":"Tue BMO","CAT":"Tue BMO","MCD":"Tue BMO","MRK":"Tue BMO","ET":"Tue BMO","DUK":"Tue BMO","BP":"Tue BMO",
        "AMD":"Tue AMC 4:15pm ET","SNDK":"Wed Aug 5 AMC","SMCI":"Wed AMC"
    }.get(t,"Aug 3-7")

    msg = f"{t} — EARNINGS V9.1\n💰 ${price:.2f} ({chg:+.2f}%)\n📅 {cal}\n📊 EPS Est: Ver TipRanks\n💵 Live Price Only (no lxml)\n🕒 {datetime.now().strftime('%H:%M VET')}"

    send(f"📊 {t} ${price:.2f} {cal}", msg)
    time.sleep(1.5)

send("✅ V9.1 SCAN COMPLETO", "10 tickers sin segfault - listo para hoy BMO + AMD AMC + SNDK mañana")
