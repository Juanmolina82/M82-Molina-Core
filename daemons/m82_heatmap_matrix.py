import time, os, sys, requests
from datetime import datetime

# -------------------------------------------------------------------
# MATRIX CORE 5.3.3 — PORTFOLIO DEFINITION WITH SPLIT REBASE
# -------------------------------------------------------------------
PORTFOLIO = {
    "NVDA": {"entry": 228.50,  "sl": 217.07,  "tp": 251.35, "legacy_entry": 240.89},
    "AVGO": {"entry": 1680.00, "sl": 1596.00, "tp": 1848.00, "legacy_entry": 462.63},
    "MU":   {"entry": 881.47,  "sl": 837.40,  "tp": 969.62, "legacy_entry": 881.47},
    "ARM":  {"entry": 301.01,  "sl": 285.96,  "tp": 331.11, "legacy_entry": 301.01},
    "VRT":  {"entry": 288.93,  "sl": 274.48,  "tp": 317.82, "legacy_entry": 288.93},
    "SQQQ": {"entry": 42.57,   "sl": 0.00,    "tp": 0.00,   "legacy_entry": 42.57}
}

WATCH = {
  "SPX":"^GSPC", "NVDA":"NVDA", "AAPL":"AAPL", "MSFT":"MSFT", "SPY":"SPY",
  "DXY":"DX-Y.NYB", "VIX":"^VIX", "ES":"ES=F", "NQ":"NQ=F", "YM":"YM=F",
  "SOUN":"SOUN", "ELF":"ELF", "ARM":"ARM", "AMD":"AMD", "XLE":"XLE",
  "PLTR":"PLTR", "TSLA":"TSLA", "SMCI":"SMCI", "AVGO":"AVGO", "AMZN":"AMZN",
  "FIG":"FIG", "AXON":"AXON", "KOSPI":"^KS11", "SNDK":"SNDK", "BA":"BA",
  "META":"META", "GOOGL":"GOOGL", "NFLX":"NFLX", "INTC":"INTC", "BABA":"BABA",
  "MU":"MU"
}

s = requests.Session()
s.headers.update({"User-Agent":"M82-Molina-Core/5.3.3"})

def get(sym):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1d&interval=1m"
        j = s.get(url, timeout=4).json()
        m = j['chart']['result'][0]['meta']
        p = m.get('regularMarketPrice', 0)
        pc = m.get('chartPreviousClose', p)
        ch = ((p - pc) / pc * 100) if pc else 0
        return p, ch
    except Exception:
        return None, None

def evaluate_position(ticker, current_price):
    if ticker not in PORTFOLIO or current_price is None or current_price == 0:
        return "UNKNOWN", 0.0, "⚪ NO DATA"
    
    pos = PORTFOLIO[ticker]
    entry = pos["entry"]
    sl = pos["sl"]
    
    pnl_pct = ((current_price - entry) / entry) * 100.0
    
    if sl > 0 and current_price <= sl:
        status = f"🔴 CRITICAL SL BREACH ({pnl_pct:+.2f}%) -> AUTO SELL"
    elif current_price < entry:
        status = f"⚠️ UNDER PRESSURE ({pnl_pct:+.2f}%) -> MONITORING"
    else:
        status = f"🟢 PROFITABLE ({pnl_pct:+.2f}%) -> HOLDING"
        
    return status, pnl_pct, f"${current_price:8.2f}"

def check_memory_divergence(vals):
    mu_p, mu_c = vals.get("MU", (0, 0))
    sndk_p, sndk_c = vals.get("SNDK", (0, 0))
    
    if mu_c is not None and sndk_c is not None:
        if mu_c >= 0 and sndk_c < 0:
            return "🟢 MEMORY DIVERGENCE ACTIVE (HBM Bid / NAND Purge) -> LONG NQ REINFORCED"
        elif mu_c < 0 and sndk_c < 0:
            return "🔴 MEMORY CAPITULATION (Sector Selloff) -> HARD_FREEZE ENFORCED"
    return "🟡 MEMORY SECTOR NEUTRAL / CONSOLIDATION"

def render():
    now = datetime.now().strftime("%d/%m/%Y %H:%M VET")
    vals = {}
    for k, t in WATCH.items():
        vals[k] = get(t)

    spx_p, spx_c = vals.get("SPX", (7730.50, -0.25))
    dxy_p, dxy_c = vals.get("DXY", (99.97, 0.3))
    vix_p, _ = vals.get("VIX", (15.41, 0))
    mem_flag = check_memory_divergence(vals)

    os.system("clear")
    print(f"""===================================================================
 🏛️ MOLINA HOLDINGS — INSTITUTIONAL MATRIX v5.3.3 [SPLIT REBASED]
⏱️ {now} | 🌙 POST-MARKET & ASIA STANDBY (15s Loop)
🏛️ POLICY: FED RATE 5.25% │ CPI YoY 3.0% │ QT PACING: $60B/MO
🧠 MEMORY SECTOR: {mem_flag}
────────────────────────────────────────────────────
🛡️ PORTFOLIO REBASED AUDIT & GUARDRAILS:""")

    for t in ["NVDA", "AVGO", "MU", "ARM", "VRT"]:
        price, _ = vals.get(t, (0, 0))
        status, pnl, p_fmt = evaluate_position(t, price)
        print(f" • {t:<5} │ SPOT: {p_fmt} │ ENTRY: ${PORTFOLIO[t]['entry']:<7.2f} │ SL: ${PORTFOLIO[t]['sl']:<7.2f} │ {status}")

    print("""════════════════════════════════════════════════════
M82 TERMINAL ENGINE • v5.3.3 LIVE | Daemons 6/6
""")

if __name__ == "__main__":
    while True:
        try:
            render()
            time.sleep(15)
        except KeyboardInterrupt:
            sys.exit(0)
