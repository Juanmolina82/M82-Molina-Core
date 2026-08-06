import yfinance as yf, requests, time
from datetime import datetime
URL="https://ntfy.sh/M82-Molina-Alerts"
TICKERS=["PFE","CAT","MCD","MRK","ET","DUK","BP","AMD"]  # SNDK FUERA
for t in TICKERS:
    try:
        tk=yf.Ticker(t)
        price=tk.fast_info.get('last_price',0)
        msg=f"{t} HOY MARTES 4 - ${price:.2f} - {datetime.now().strftime('%H:%M VET')}"
        print(msg)
        requests.post(URL, data=msg.encode(), headers={"Title":f"📊 {t} ${price:.2f}"}, timeout=10)
        time.sleep(1.5)
    except Exception as e:
        print(e)
