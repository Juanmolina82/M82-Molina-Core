import requests, time, os
from datetime import datetime
TOKEN = os.environ.get("BOT_TOKEN", "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4")
CHAT = os.environ.get("CHAT_ID", "1020305418")
NTFY_URL = "https://ntfy.sh/M82-ESCUPE"
s = requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0"})

TICKERS = ["AMD","NVDA","PLTR","SMH","SOXX","AVGO","TSM","MU","ARM","META","AAPL","SPY","QQQ","^GSPC","ES=F","NQ=F","^VIX","CL=F","GC=F","EGG","DIT","FURY"]

def get_extended_data(tk):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?interval=1m&range=1d&includePrePost=true"
        j = s.get(url, timeout=4).json()
        meta = j['chart']['result'][0]['meta']
        reg = float(meta.get('regularMarketPrice') or 0)
        prev = float(meta.get('chartPreviousClose') or meta.get('previousClose') or reg)
        reg_pct = ((reg-prev)/prev*100) if prev else 0
        post = meta.get('postMarketPrice')
        pre = meta.get('preMarketPrice')
        ext_price = 0; ext_pct = 0; type_ext="REG"
        if post and float(post)!=reg and post!=0:
            ext_price = float(post)
            ext_pct = ((ext_price - reg)/reg*100) if reg else 0
            type_ext="AH"
        elif pre and float(pre)!=reg and pre!=0:
            ext_price = float(pre)
            ext_pct = ((ext_price - prev)/prev*100) if prev else 0
            type_ext="PRE"
        return reg, reg_pct, ext_price, ext_pct, type_ext
    except:
        return 0,0,0,0,"ERR"

def build():
    lines=[]
    lines.append(f"📺 CONSOLIDADO EXTENDED {datetime.now().strftime('%H:%M:%S VET')} 3s")
    lines.append(f"AMD Q2 $11.5B +50% BEAT CAPEX $808M +108% = -7% AH")
    lines.append("─"*52)
    lines.append(f"{'TICKER':<6} {'REGULAR':<14} {'EXTENDED (PRE/AH)'}")
    lines.append("─"*52)
    for tk in TICKERS:
        rp,r_pct,ep,e_pct,state = get_extended_data(tk)
        if rp==0: continue
        reg_str = f"${rp:.2f} {r_pct:+.1f}%"
        if state!="REG" and ep>0:
            sym="🟢" if e_pct>=0 else "🔴"
            ext_str=f"{sym} ${ep:.2f} {e_pct:+.1f}% {state}"
        else:
            ext_str="─ REGULAR ─"
        lines.append(f"{tk:<6} {reg_str:<14} {ext_str}")
    return "\n".join(lines)

def send(txt):
    try: s.post(NTFY_URL, data=txt.encode('utf-8'), headers={"Title": f"CONSOLIDADO {datetime.now().strftime('%H:%M:%S')}","Priority":"max"}, timeout=3)
    except: pass
    try: s.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":CHAT,"text": txt}, timeout=3)
    except: pass

print("CONSOLIDADO 3s INICIADO - TABLA UNICA")
while True:
    try:
        rpt=build(); print(rpt); print(); send(rpt)
        time.sleep(3)
    except Exception as e:
        print(f"ERR {e}"); time.sleep(1)
