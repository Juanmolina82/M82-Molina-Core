import requests, time, json, os
from datetime import datetime
TOPIC = "M82-ESCUPE"
URL = f"https://ntfy.sh/{TOPIC}"
STATE_FILE = "m82_v3_state.json"
s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
TOP_ETFS = {
    "SPY": "MERCADO", "QQQ": "MERCADO", "IWM": "SMALL CAP", "DIA": "MERCADO",
    "XLK": "TECH", "XLF": "BANCO", "XLE": "ENERGY", "XLV": "SALUD", "XLI": "INDUSTRIAL",
    "SMH": "CHIPS", "IBB": "BIOTECH", "KRE": "BANCO REG", "XOP": "OIL GAS",
    "GLD": "ORO", "SLV": "PLATA", "USO": "OIL ETF", "TLT": "BONO 20Y", "IEF": "BONO 10Y",
    "EEM": "EMERGENTE", "VXX": "MIEDO", "HYG": "HIGH YIELD"
}
seen = json.load(open(STATE_FILE)) if os.path.exists(STATE_FILE) else {}
def send(title, msg, pri="high", tag="fire"):
    try:
        requests.post(URL, data=msg.encode('utf-8'), headers={"Title": title, "Priority": pri, "Tags": tag}, timeout=5)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {title}")
    except Exception as e: print(e)
def get_price(tk):
    try:
        j = s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?interval=1m&range=1d", timeout=5).json()
        meta = j['chart']['result'][0]['meta']
        p = float(meta.get('regularMarketPrice') or 0)
        prev = float(meta.get('chartPreviousClose') or p)
        pct = ((p-prev)/prev*100) if prev else 0
        return p, pct
    except: return 0,0
print(f"--- M82 V3 ETFs + MACRO -> {TOPIC} ---")
send("M82 V3 ONLINE 🚀", f"ETFs Top 20 + World Economy\nXLE/XOP= OIL 75 | GLD=$4142 | TLT= Fed | VXX= Miedo\nMacro: CPI/Fed/NFP/PMI\nSolo alertas >1%", "high", "rocket")
cycle=0
while True:
    try:
        cycle+=1
        summary=[]
        for tk, sector in TOP_ETFS.items():
            p, pct = get_price(tk)
            if p==0: continue
            key = f"{tk}_{datetime.now().strftime('%H')}_{int(pct*10)}"
            if abs(pct)>=1.0 and not seen.get(key):
                seen[key]=True
                tag = "droplet" if tk in ["XLE","XOP","USO"] else "coin" if tk=="GLD" else "chart_with_upwards_trend" if pct>0 else "chart_with_downwards_trend"
                if tk in ["XLE","XOP","USO"] and pct<-1:
                    send(f"🛢️ ENERGY CRASH {tk} {pct:+.2f}%", f"{tk} {sector} ${p:.2f} {pct:+.2f}%\nOIL WTI 75 en riesgo", "max", "droplet")
                elif tk=="GLD" and abs(pct)>=0.8:
                    send(f"🥇 GOLD {pct:+.2f}%", f"GLD ${p:.2f} {pct:+.2f}%\nGold 4142 | DDC FURY", "high", "coin")
                elif tk in ["SPY","QQQ"] and abs(pct)>=1:
                    send(f"⚠️ MERCADO {tk} {pct:+.2f}%", f"{tk} ${p:.2f} {pct:+.2f}%\nSi SPY cae, EGG DIT caen", "max", "warning")
                elif tk=="TLT" and pct>1:
                    send(f"📈 BONOS TLT {pct:+.2f}%", f"TLT ${p:.2f} {pct:+.2f}%\nFed recorta = TECH vuela", "high", "bank")
                elif tk=="VXX" and pct>2:
                    send(f"😱 MIEDO VXX {pct:+.2f}%", f"VXX ${p:.2f} {pct:+.2f}%\nMiedo sube = vende", "max", "rotating_light")
                elif abs(pct)>=1.2:
                    send(f"{sector} {tk} {pct:+.2f}%", f"{tk} ${p:.2f} {pct:+.2f}%", "high", tag)
            summary.append(f"{tk} {pct:+.1f}%")
            time.sleep(0.8)
        if cycle % 15 == 0:
            send("💓 PULSO ETFs", " | ".join(summary[:8]), "low", "bar_chart")
        with open(STATE_FILE,'w') as f: json.dump(seen,f)
        if datetime.now().hour==0: seen={}
        time.sleep(20)
    except Exception as e:
        print(f"ERR {e}")
        time.sleep(10)
