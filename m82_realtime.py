import requests,time
from datetime import datetime
URL="https://ntfy.sh/M82-Molina-Alerts"
s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0","Accept":"application/json"})
last_pltr=0
last_wti=0
last_alert=0
print("--- M82 REALTIME V5 15s PLTR + WTI ---")
while True:
 try:
  # WTI
  try:
   j=s.get("https://query1.finance.yahoo.com/v8/finance/chart/CL=F?interval=1m&range=1d",timeout=5).json()
   wti=float(j['chart']['result'][0]['meta']['regularMarketPrice'])
  except: wti=last_wti
  # PLTR
  try:
   j2=s.get("https://query1.finance.yahoo.com/v8/finance/chart/PLTR?interval=1m&range=1d",timeout=5).json()
   pltr=float(j2['chart']['result'][0]['meta']['regularMarketPrice'])
  except: pltr=last_pltr

  now=datetime.now().strftime('%H:%M:%S')
  if pltr!=last_pltr or wti!=last_wti:
   print(f"[{now}] PLTR ${pltr:.2f} | WTI ${wti:.2f}")
   last_pltr,last_wti=pltr,wti

  # Alertas PLTR pilas
  if pltr>=151.00 and (time.time()-last_alert)>180:
   body=f"PLTR BREAKOUT ${pltr:.2f} > 151 Otherworldly intacto\nWTI ${wti:.2f}"
   s.post(URL,data=body.encode('utf-8'),headers={"Title":f"PLTR BREAK {pltr:.2f}","Priority":"max","Tags":"pltr,breakout"},timeout=6)
   last_alert=time.time()
  if pltr>0 and pltr<148.90 and (time.time()-last_alert)>300:
   body=f"PLTR STOP RIESGO ${pltr:.2f} < 148.90\nSal de scalp si estas en 150.82\nWTI ${wti:.2f}"
   s.post(URL,data=body.encode('utf-8'),headers={"Title":f"PLTR RISK {pltr:.2f}","Priority":"max"},timeout=6)
   last_alert=time.time()
 except Exception as e:
  print(f"ERR {e}")
 time.sleep(15)
