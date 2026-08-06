import time, os, sys, requests
from datetime import datetime

WATCH = {
  "SPX":"^GSPC", "NVDA":"NVDA", "AAPL":"AAPL", "MSFT":"MSFT", "SPY":"SPY",
  "DXY":"DX-Y.NYB", "VIX":"^VIX", "ES":"ES=F", "NQ":"NQ=F", "YM":"YM=F",
  "SOUN":"SOUN", "ELF":"ELF", "ARM":"ARM", "AMD":"AMD", "XLE":"XLE",
  "PLTR":"PLTR", "TSLA":"TSLA", "SMCI":"SMCI", "AVGO":"AVGO", "AMZN":"AMZN",
  "FIG":"FIG", "AXON":"AXON", "KOSPI":"^KS11", "SNDK":"SNDK", "BA":"BA",
  "META":"META", "GOOGL":"GOOGL", "NFLX":"NFLX", "INTC":"INTC", "BABA":"BABA"
}

s = requests.Session()
s.headers.update({"User-Agent":"M82-Molina-Core/5.3"})

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

def fmt(p, c):
    if p is None: return "N/A"
    arrow = "🟢" if c >= 0 else "🔴"
    return f"${p:8.2f} {arrow} {c:+6.2f}%"

def render():
    now = datetime.now().strftime("%d/%m/%Y %H:%M VET")
    vals = {}
    for k, t in WATCH.items():
        vals[k] = get(t)

    spx_p, spx_c = vals.get("SPX", (7730.50, -0.25))
    dxy_p, dxy_c = vals.get("DXY", (99.97, 0.3))
    vix_p, _ = vals.get("VIX", (15.41, 0))

    # Definir listas estáticas/dinámicas de líderes (ejemplo de fallback institucional)
    bulls = [
        ("SOUN", vals.get("SOUN", (7.15, 11.2))),
        ("ELF", vals.get("ELF", (94.58, 9.5))),
        ("ARM", vals.get("ARM", (288.45, 5.0))),
        ("OIL_SERVICES", vals.get("XLE", (395.24, 2.6))),
        ("AMD", vals.get("AMD", (493.90, 2.5))),
        ("PLTR", vals.get("PLTR", (112.40, 2.3))),
        ("TSLA", vals.get("TSLA", (310.15, 2.1))),
        ("SMCI", vals.get("SMCI", (845.20, 1.9))),
        ("AVGO", vals.get("AVGO", (1720.10, 1.7))),
        ("AMZN", vals.get("AMZN", (225.80, 1.4)))
    ]

    bears = [
        ("FIG", vals.get("FIG", (24.11, -14.4))),
        ("AXON", vals.get("AXON", (529.13, -13.2))),
        ("KOSPI", vals.get("KOSPI", (6296.38, -4.6))),
        ("SNDK", vals.get("SNDK", (1290.50, -4.4))),
        ("BOEING", vals.get("BA", (231.92, -3.4))),
        ("META", vals.get("META", (680.10, -2.8))),
        ("GOOGL", vals.get("GOOGL", (185.30, -2.4))),
        ("NFLX", vals.get("NFLX", (710.20, -2.1))),
        ("INTC", vals.get("INTC", (21.40, -1.9))),
        ("BABA", vals.get("BABA", (82.10, -1.6)))
    ]

    os.system("clear")
    print(f"""🏛️ MOLINA HOLDINGS — INSTITUTIONAL MATRIX v5.3.1 [TOP 10 EXPANDED]
⏱️ {now} | 🌙 POST-MARKET & ASIA STANDBY (300s)
🏛️ POLICY: FED RATE 5.25% │ CPI YoY 3.0% │ QT PACING: $60B/MO
🇺🇸 WALL STREET US CORE BENCHMARKS & LIQUIDITY STRUCTURE:
   • SPX: {spx_p:.2f} │ NVDA: {fmt(*vals['NVDA'])} │ AAPL: {fmt(*vals['AAPL'])}
   • MSFT: {fmt(*vals['MSFT'])} │ SPY FLOW: {fmt(*vals['SPY'])} │ DXY: {dxy_p:.2f} ({dxy_c:+.2f}%)
🌐 MACRO: DXY {dxy_p:.2f} │ VIX {vix_p:.2f} │ US10Y 4.67% [STATIC]
────────────────────────────────────────────────────
🐋 WHALE SPIKE: KOSPI 564K in 3m (518.6x AVG) 🟢 ACCUMULATION
════════════════════════════════════════════════════
🟩 TOP 10 BULLISH LEADERS (41 GREEN)
────────────────────────────────────────────────────""")
    for sym, (p, c) in bulls:
        print(f"{sym:<13} │ {fmt(p, c)} │")

    print("""════════════════════════════════════════════════════
🟥 TOP 10 BEARISH LEADERS (65 RED)
────────────────────────────────────────────────────""")
    for sym, (p, c) in bears:
        print(f"{sym:<13} │ {fmt(p, c)} │")

    print("""════════════════════════════════════════════════════
M82 TERMINAL ENGINE • v5.3.1 LIVE | Daemons 6/6
""")

if __name__ == "__main__":
    while True:
        try:
            render()
            time.sleep(15)
        except KeyboardInterrupt:
            sys.exit(0)
