import requests, time; from datetime import datetime
URL="https://ntfy.sh/M82-Molina-Alerts"; S=requests.Session()
TICKERS=["PFE","CAT","MCD","MRK","AMD"] # SNDK FUERA hasta mañana
def getp(t):
 try:
  r=S.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?interval=1m&range=1d",timeout=8).json()
  m=r['chart']['result'][0]['meta']; return m['regularMarketPrice']
 except: return 0
while True:
 for t in TICKERS:
  p=getp(t); S.post(URL,data=f"{t} ${p:.2f} {datetime.now().strftime('%H:%M VET')} HOY".encode(),headers={"Title":f"{t} ${p:.2f}"},timeout=10); time.sleep(1)
 time.sleep(600)
