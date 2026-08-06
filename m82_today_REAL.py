import yfinance as yf, requests, time
from datetime import datetime
URL="https://ntfy.sh/M82-Molina-Alerts"
TICKERS=["PFE","CAT","MCD","MRK","ET","DUK","BP"]

for t in TICKERS:
    try:
        tk=yf.Ticker(t)
        price=tk.fast_info['last_price']
        ed=tk.earnings_dates
        if ed is not None and not ed.empty and 'Reported EPS' in ed.columns:
            row=ed.iloc[0]
            eps_a=row.get('Reported EPS','N/A')
            eps_e=row.get('EPS Estimate','N/A')
            rev_e="ver earnings_dates"
            surp=row.get('Surprise(%)','N/A')
            msg=f"{t} REAL REPORT HOY MARTES 4\n💰 ${price:.2f}\nEPS Actual: {eps_a} vs Est: {eps_e}\nSurprise: {surp}\nFecha index: {ed.index[0]}"
        else:
            # No actual aún, manda estimate
            msg=f"{t} BMO HOY — AUN SIN ACTUAL (pre-market)\n💰 Precio live: ${price:.2f}\nEPS Est: Pendiente en API\nScaneado: {datetime.now().strftime('%H:%M VET')}\nTip: actual cae en 10-20 min post earnings"
        print(msg)
        requests.post(URL, data=msg.encode(), headers={"Title":f"📊 {t} HOY REAL {datetime.now().strftime('%H:%M')}"}, timeout=10)
        time.sleep(2)
    except Exception as e:
        print(f"{t} err {e}")

requests.post(URL, data=b"BMO Martes 4 escaneo real terminado - sin actuals aun, esperando release", headers={"Title":"✅ SCAN REAL TERMINADO"})
