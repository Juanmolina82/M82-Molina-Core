import requests,time,json,os
from datetime import datetime
URL="https://ntfy.sh/M82-Molina-Alerts"
TICKERS=["CAT","MCD","PFE","MRK","AMD","SNDK","BP","XOM","CVX","ET","JPM","GS","MSFT","NVDA","AAPL","META","PLTR","TSLA","CL=F","BZ=F","SPY","QQQ","DIA","BTC-USD","GOLD","W","AMZN"]
STATE="/data/data/com.termux/files/home/M82-Molina-Core/m82_seen.json"
seen=json.load(open(STATE)) if os.path.exists(STATE) else {}
s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0","Content-Type":"text/plain"})
def get_price(t):
 try:
  j=s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?interval=5m&range=1d",timeout=8).json()
  return float(j['chart']['result'][0]['meta'].get('regularMarketPrice') or 0)
 except: return 0.0
def get_eps(t):
 if "=" in t or "-" in t or t in ["SPY","QQQ","DIA"]: return None,None,None
 try:
  r=s.get(f"https://api.nasdaq.com/api/company/{t}/earnings?limit=2",headers={"Accept":"application/json","User-Agent":"Mozilla/5.0"},timeout=8).json()
  if r.get('data',{}).get('earnings'):
   row=r['data']['earnings'][0]
   if row.get('actualEPS'):
    a=float(str(row['actualEPS']).replace('$','').replace(',','').strip())
    e=float(str(row.get('estimatedEPS','0')).replace('$','').replace(',','').strip() or 0)
    return a,e,"NASDAQ"
 except: pass
 try:
  r=s.get(f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{t}?modules=earningsHistory",timeout=8).json()
  hist=r['quoteSummary']['result'][0]['earningsHistory']['history']
  if hist and hist[0].get('epsActual') is not None:
   return float(hist[0]['epsActual']),float(hist[0].get('epsEstimate') or 0),"YAHOO"
 except: pass
 return None,None,None
print(f"--- M82 V12.4 ESTABLE {len(TICKERS)} ---")
cycle=0
while True:
 try:
  for t in TICKERS:
   p=get_price(t); ea,ee,src=get_eps(t)
   now=datetime.now().strftime('%H:%M:%S')
   print(f"[{now}] {t} ${p:.2f} eps={ea} {src}")
   if ea is not None and str(seen.get(t))!=str(ea):
    seen[t]=str(ea); open(STATE,'w').write(json.dumps(seen))
    surp=((ea-ee)/abs(ee)*100) if ee else 0
    s.post(URL,data=f"🔥 {t} HORNO [{src}] EPS {ea} vs {ee} {surp:+.1f}% ${p:.2f} {now}".encode(),headers={"Title":f"HORNO {t} EPS {ea} ${p:.2f}","Priority":"max","Tags":"fire"},timeout=10)
   time.sleep(1.5)
  cycle+=1
  if cycle%10==0:
   prices=[f"{x} ${get_price(x):.2f}" for x in ["CAT","AMD","SNDK","BP","CL=F"]]
   s.post(URL,data=f"{' | '.join(prices)} {datetime.now().strftime('%H:%M VET')}".encode(),headers={"Title":f"VIVO {' | '.join(prices[:2])}","Priority":"low"},timeout=10)
  time.sleep(10)
 except Exception as e:
  print(f"ERR {e}"); time.sleep(5)
