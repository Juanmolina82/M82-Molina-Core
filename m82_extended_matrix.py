import requests, time, os
from datetime import datetime
TOKEN=os.environ.get("BOT_TOKEN","8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4")
CHAT=os.environ.get("CHAT_ID","1020305418")
NTFY="https://ntfy.sh/M82-ESCUPE"
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0"})

TICKERS=["AMD","NVDA","PLTR","SMH","SOXX","AVGO","TSM","MU","ARM","META","AAPL","SPY","QQQ","SLV","CL=F","GC=F","EGG","DIT","FURY","ES=F","NQ=F","^GSPC","^VIX"]
NAMES={"^GSPC":"SPX","ES=F":"ES","NQ=F":"NQ","^VIX":"VIX","GC=F":"GOLD","CL=F":"WTI"}

def fetch(tk):
 try:
  j=s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?interval=1m&range=1d&includePrePost=true",timeout=4).json()
  m=j['chart']['result'][0]['meta']
  reg=float(m.get('regularMarketPrice') or 0); prev=float(m.get('chartPreviousClose') or m.get('previousClose') or reg)
  rp=((reg-prev)/prev*100) if prev else 0
  post=m.get('postMarketPrice'); pre=m.get('preMarketPrice')
  ep=0; e_pct=0; typ="REG"
  st=m.get('marketState','')
  if post and float(post)!=0 and abs(float(post)-reg)>0.01: ep=float(post); e_pct=((ep-reg)/reg*100) if reg else 0; typ="AH"
  elif st=='PRE' and pre and float(pre)!=0: ep=float(pre); e_pct=((ep-prev)/prev*100) if prev else 0; typ="PRE"
  return {"ticker":NAMES.get(tk,tk),"price":reg,"pct":rp,"ext_price":ep,"ext_pct":e_pct,"ext_type":typ}
 except: return None

def build():
 data=[]
 for tk in TICKERS:
  r=fetch(tk)
  if r and r["price"]>0: data.append(r)
 positives=[d for d in data if d["pct"]>=0]; negatives=[d for d in data if d["pct"]<0]
 positives.sort(key=lambda x: x["pct"], reverse=True); negatives.sort(key=lambda x: x["pct"])
 now=datetime.now().strftime('%H:%M:%S VET')
 out=[]
 out.append(f"📺 MATRIX M82 EXTENDED | {now} | 3s CONSOLIDADO")
 out.append(f"AMD Q2 $11.5B +50% BEAT CAPEX $808M +108% → -7% AH | PLTR +29%")
 out.append("═"*54)
 out.append("🟢 GANADORES / BULLISH (REGULAR & EXTENDED)")
 out.append("─"*54)
 out.append(f"{'TICK':<5} {'REGULAR':<14} {'EXTENDED (PRE/AH)':<20}")
 out.append("─"*54)
 for d in positives:
  reg_str=f"${d['price']:.2f} +{d['pct']:.1f}%"
  if d['ext_type']!="REG" and d['ext_price']!=0:
   tag="🟢" if d['ext_pct']>=0 else "🔴"
   ext_str=f"{tag} ${d['ext_price']:.2f} {d['ext_pct']:+.1f}% {d['ext_type']}"
  else: ext_str="── CLOSED ──"
  out.append(f"{d['ticker']:<5} {reg_str:<14} {ext_str}")
 out.append("")
 out.append("🔴 PERDEDORES / BEARISH (REGULAR & EXTENDED)")
 out.append("─"*54)
 out.append(f"{'TICK':<5} {'REGULAR':<14} {'EXTENDED (PRE/AH)':<20}")
 out.append("─"*54)
 for d in negatives:
  reg_str=f"${d['price']:.2f} {d['pct']:.1f}%"
  if d['ext_type']!="REG" and d['ext_price']!=0:
   tag="🟢" if d['ext_pct']>=0 else "🔴"
   ext_str=f"{tag} ${d['ext_price']:.2f} {d['ext_pct']:+.1f}% {d['ext_type']}"
  else: ext_str="── CLOSED ──"
  out.append(f"{d['ticker']:<5} {reg_str:<14} {ext_str}")
 out.append("═"*54)
 out.append("M82-MOLINA-CORE • 1 SOLO MENSAJE • 3s")
 return "\n".join(out)

def send(txt):
 try: s.post(NTFY, data=txt.encode('utf-8'), headers={"Title": f"MATRIX 3s {datetime.now().strftime('%H:%M:%S')}","Priority":"max"},timeout=3)
 except: pass
 try: s.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id":CHAT,"text": txt},timeout=3)
 except: pass

print("MATRIX CONSOLIDADO 3s ON - BULL/BEAR SEPARADOS")
while True:
 try:
  rpt=build(); print(rpt); print(); send(rpt); time.sleep(3)
 except Exception as e: print(e); time.sleep(1)
