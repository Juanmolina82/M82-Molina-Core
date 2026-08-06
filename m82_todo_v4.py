import requests, time, json, os
from datetime import datetime
TOPIC="M82-ESCUPE"
URL=f"https://ntfy.sh/{TOPIC}"
STATE="m82_v4_state.json"
s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0"})
# --- CONFIG TOTAL ---
WATCH = {
    # TUS CORE
    "PLTR": {"type":"BREAKOUT","break":155},
    "CL=F": {"type":"OIL","risk":74.0,"top":76.9},
    "GC=F": {"type":"GOLD","level":4100},
    "EGG": {"type":"MOLINA","pct":2.5},
    "DIT": {"type":"MOLINA","pct":2.5},
    "FURY": {"type":"MOLINA","pct":2.5},
    # ETFs TOP
    "SPY": {"type":"MERCADO"}, "QQQ": {"type":"MERCADO"}, "DIA": {"type":"MERCADO"}, "IWM": {"type":"SMALL"},
    "XLK": {"type":"SECTOR"}, "XLF": {"type":"SECTOR"}, "XLE": {"type":"ENERGY"}, "XLV": {"type":"SECTOR"},
    "SMH": {"type":"CHIPS"}, "IBB": {"type":"BIO"}, "KRE": {"type":"BANCO"}, "XOP": {"type":"ENERGY"},
    "GLD": {"type":"ORO"}, "SLV": {"type":"PLATA"}, "USO": {"type":"ENERGY"}, "TLT": {"type":"BONO"},
    "VXX": {"type":"MIEDO"}, "EEM": {"type":"EMERGENTE"}
}
seen=json.load(open(STATE)) if os.path.exists(STATE) else {}
def send(t,m,p="high",tag="fire"):
    try:
        requests.post(URL, data=m.encode('utf-8'), headers={"Title":t,"Priority":p,"Tags":tag}, timeout=5)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {t}")
    except Exception as e: print(e)
def get(tk):
    try:
        j=s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?interval=1m&range=1d", timeout=5).json()
        meta=j['chart']['result'][0]['meta']
        price=float(meta.get('regularMarketPrice') or 0)
        prev=float(meta.get('chartPreviousClose') or price)
        pct=((price-prev)/prev*100) if prev else 0
        return price,pct
    except: return 0,0

send("M82 TODO V4 ONLINE 🚀", "PLTR 156 | OIL 75.20 | GOLD 4142 | EGG DIT FURY\n+ 20 ETFs TOP\nXLE XOP=crudo | SMH XLK=tech | VXX=miedo | GLD/SLV=oro", "high", "rocket")
c=0
while True:
    try:
        c+=1
        for tk,cfg in WATCH.items():
            p,pct=get(tk)
            if p==0: continue
            k=f"{tk}_{int(p)}"
            # OIL
            if cfg['type']=="OIL":
                if p <= cfg['risk'] and not seen.get(f"OIL_RISK_{int(p)}"):
                    seen[f"OIL_RISK_{int(p)}"]=True
                    send(f"🛢️ OIL RIESGO ${p:.2f}", f"WTI ${p:.2f} ROMPIO ${cfg['risk']} - Riesgo Hormuz\nXLE XOP se hunden, SPY en peligro", "max", "droplet")
                if p >= cfg['top'] and not seen.get(f"OIL_TOP_{int(p)}"):
                    seen[f"OIL_TOP_{int(p)}"]=True
                    send(f"🔥 OIL PUMP ${p:.2f}", f"WTI ${p:.2f} arriba de ${cfg['top']} - Energy vuela", "high", "fire")
            # PLTR
            if cfg['type']=="BREAKOUT" and p>=cfg['break'] and not seen.get(f"{tk}_{int(p)}"):
                seen[f"{tk}_{int(p)}"]=True
                send(f"🚀 PLTR BREAK ${p:.2f}", f"PLTR ${p:.2f} sobre {cfg['break']} breakout confirmado", "high", "rocket")
            # MOLINA
            if cfg['type']=="MOLINA" and abs(pct)>=cfg['pct'] and not seen.get(f"{tk}_{pct:.1f}_{datetime.now().hour}"):
                seen[f"{tk}_{pct:.1f}_{datetime.now().hour}"]=True
                send(f"💎 {tk} {pct:+.2f}% ${p:.2f}", f"{tk} {pct:+.2f}% ${p:.2f}\nMolina Core explotando", "high", "gem")
            # ETFs MASIVOS
            if cfg['type'] in ["MERCADO","CHIPS","SECTOR","ENERGY","MIEDO","ORO","PLATA"] and abs(pct)>=1.0:
                key=f"{tk}_{int(pct*10)}_{datetime.now().hour}"
                if not seen.get(key):
                    seen[key]=True
                    send(f"{cfg['type']} {tk} {pct:+.2f}%", f"{tk} ${p:.2f} {pct:+.2f}%\nSMH {pct:+.2f} = PLTR\nXLE {pct:+.2f} = OIL", "high", "chart_with_upwards_trend")
            time.sleep(0.7)
        if c%20==0:
            with open(STATE,'w') as f: json.dump(seen,f)
        if datetime.now().hour==0: seen={}
        time.sleep(15)
    except Exception as e:
        print(f"ERR {e}")
        time.sleep(5)
