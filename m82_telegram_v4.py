import requests, time, json, os
from datetime import datetime
TOKEN=os.getenv("BOT_TOKEN","8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4")
CHAT="1020305418"
STATE="m82_tg_state.json"
s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0"})
WATCH={"PLTR":{"type":"BREAKOUT","break":155},"CL=F":{"type":"OIL","risk":74.0,"top":76.9},"GC=F":{"type":"GOLD","level":4100},"EGG":{"type":"MOLINA","pct":2.5},"DIT":{"type":"MOLINA","pct":2.5},"FURY":{"type":"MOLINA","pct":2.5},"SPY":{},"QQQ":{},"DIA":{},"IWM":{},"SMH":{},"XLK":{},"XLE":{},"XOP":{},"GLD":{},"SLV":{},"VXX":{},"EEM":{}}
seen=json.load(open(STATE)) if os.path.exists(STATE) else {}
def send(t,m):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":CHAT,"text":f"{t}\n{m}"}, timeout=5)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {t}")
    except Exception as e: print(e)
def get(tk):
    try:
        j=s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?interval=1m&range=1d", timeout=5).json()
        meta=j['chart']['result'][0]['meta']
        p=float(meta.get('regularMarketPrice') or 0)
        prev=float(meta.get('chartPreviousClose') or p)
        pct=((p-prev)/prev*100) if prev else 0
        return p,pct
    except: return 0,0
send("M82 TELEGRAM V4 ONLINE 🚀","PLTR 156 | OIL 75.20 | GOLD 4142 | EGG DIT FURY\n+ 20 ETFs\nSMH +5.23% XLK +4.74% DIA +1.81% IWM +1.74% SLV +3.18%\nAndroid 100% - ntfy muerto bypass")
c=0
while True:
    try:
        for tk,cfg in WATCH.items():
            p,pct=get(tk)
            if p==0: continue
            if cfg.get('type')=="OIL" and p<=cfg['risk'] and not seen.get(f"OIL_{int(p)}"):
                seen[f"OIL_{int(p)}"]=True; send(f"🛢️ OIL RIESGO ${p:.2f}", f"WTI ${p:.2f} rompio riesgo")
            if cfg.get('type')=="BREAKOUT" and p>=cfg['break'] and not seen.get(f"{tk}_{int(p)}"):
                seen[f"{tk}_{int(p)}"]=True; send(f"🚀 PLTR BREAK ${p:.2f}", f"PLTR ${p:.2f}")
            if cfg.get('type')=="MOLINA" and abs(pct)>=2.5 and not seen.get(f"{tk}_{pct:.1f}_{datetime.now().hour}"):
                seen[f"{tk}_{pct:.1f}_{datetime.now().hour}"]=True; send(f"💎 {tk} {pct:+.2f}% ${p:.2f}", f"{tk} volando")
            if abs(pct)>=1.2 and not seen.get(f"{tk}_{int(pct*10)}_{datetime.now().hour}"):
                if tk in ["SMH","XLK","DIA","IWM","XLE","SLV","VXX","SPY","QQQ"]:
                    seen[f"{tk}_{int(pct*10)}_{datetime.now().hour}"]=True; send(f"📊 {tk} {pct:+.2f}% ${p:.2f}", f"Risk-On masivo")
            time.sleep(0.7)
        c+=1;
        if c%30==0:
            with open(STATE,'w') as f: json.dump(seen,f)
        time.sleep(15)
    except Exception as e:
        print(e); time.sleep(5)
