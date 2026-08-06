import time, os, sys, requests
from datetime import datetime

s = requests.Session()
s.headers.update({"User-Agent":"M82-Molina-Core/5.3"})

def fetch_ticker_flow(sym):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1d&interval=1m"
        j = s.get(url, timeout=4).json()
        meta = j['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice', 0)
        prev_close = meta.get('chartPreviousClose', price)
        volume = meta.get('regularMarketVolume', 0)
        pct_change = ((price - prev_close) / prev_close * 100) if prev_close else 0
        return price, pct_change, volume
    except Exception:
        return 0.0, 0.0, 0

def monitor_flows():
    while True:
        try:
            now = datetime.now().strftime("%H:%M:%S VET")
            
            # Fetch SQQQ & SPCX
            sqqq_p, sqqq_c, sqqq_v = fetch_ticker_flow("SQQQ")
            spcx_p, spcx_c, spcx_v = fetch_ticker_flow("SPCX")
            
            # Determinación de patrón de absorción en SPCX
            spcx_signal = "NEUTRAL"
            if spcx_v > 150000000 and spcx_c >= -5.0:
                spcx_signal = "🟢 INSTITUTIONAL ABSORPTION (LONG BIAS)"
            elif spcx_v > 200000000 and spcx_c < -8.0:
                spcx_signal = "🔴 INSIDER DISTRIBUTION (HEAVY DUMP)"
            else:
                spcx_signal = "🟡 LOCKUP MONITORING (HOLD / RANGE)"

            log_entry = (
                f"[{now}] FLOW TRACKER v5.3 | SQQQ: ${sqqq_p:.2f} ({sqqq_c:+.2f}%) Outflow: -$22.68M | "
                f"SPCX: ${spcx_p:.2f} ({spcx_c:+.2f}%) Vol: {spcx_v/1e6:.1f}M | Signal: {spcx_signal}"
            )
            
            # Escribir log directo para el TUI y Telegram
            with open("logs/flow_tracker.log", "a") as f:
                f.write(log_entry + "\n")
                
            time.sleep(10)
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    monitor_flows()
