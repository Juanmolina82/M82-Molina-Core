import requests,time
from datetime import datetime
URL="https://ntfy.sh/M82-Molina-Alerts"
s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0"})
def get_oil(t):
 try:
  j=s.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?interval=1m&range=1d",timeout=6).json()
  return float(j['chart']['result'][0]['meta']['regularMarketPrice'])
 except: return 0.0
print("--- CRUDE GUARD V4 NO-EMOJI-HEADER ---")
last_alert=0
while True:
 wti=get_oil("CL=F"); brent=get_oil("BZ=F")
 print(f"[{datetime.now().strftime('%H:%M:%S')}] WTI ${wti:.2f} | Brent ${brent:.2f}")
 if wti and wti<76.90 and (time.time()-last_alert)>900:
  try:
   body=f"QATAR/US-IRAN DEAL IMMINENT\nWTI ${wti:.2f} (<76.90)\nBrent ${brent:.2f}\nBessent today/tomorrow - BP/XOM/CVX risk"
   s.post(URL,data=body.encode('utf-8'),headers={"Title":f"SYNC WTI {wti:.2f} Bessent deal hoy/manana","Priority":"max","Tags":"oil,warning"},timeout=8)
   last_alert=time.time()
  except Exception as e:
   print(f"NTFY ERR {e}")
 time.sleep(60)
