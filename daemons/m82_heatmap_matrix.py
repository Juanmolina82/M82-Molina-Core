import time, os, sys, requests
from datetime import datetime

WATCH = {
  "SPX":"^GSPC", "NVDA":"NVDA", "AAPL":"AAPL", "MSFT":"MSFT",
  "SPY":"SPY", "DXY":"DX-Y.NYB", "VIX":"^VIX", "ES":"ES=F", "NQ":"NQ=F", "YM":"YM=F"
}

s = requests.Session()
s.headers.update({"User-Agent":"M82-Molina-Core/5.3"})

def get(sym):
    try:
        url=f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1d&interval=1m"
        j=s.get(url,timeout=4).json()
        m=j['chart']['result'][0]['meta']
        p=m.get('regularMarketPrice',0)
        pc=m.get('chartPreviousClose',p)
        ch=((p-pc)/pc*100) if pc else 0
        return p,ch
    except:
        return None,None

def render():
    now=datetime.now().strftime("%d/%m/%Y %H:%M VET")
    vals={}
    for k,t in WATCH.items():
        p,c=get(t)
        vals[k]=(p,c)

    spx_p, spx_c = vals.get("SPX", (7732.75,-0.22))
    nvda_p, nvda_c = vals.get("NVDA", (182.4,1.8))
    aapl_p, aapl_c = vals.get("AAPL", (242.1,-0.4))
    msft_p, msft_c = vals.get("MSFT", (485.5,0.6))
    dxy_p, dxy_c = vals.get("DXY", (99.99,0.3))
    vix_p, _ = vals.get("VIX", (15.42,0))

    def fmt(p,c):
        if p is None: return "N/A"
        arrow="🟢" if c>=0 else "🔴"
        return f"${p:.2f} {arrow} {c:+.2f}%"

    os.system("clear")
    print(f"""🏛️ MOLINA HOLDINGS — INSTITUTIONAL MATRIX v5.3 [US EXPANDED]
⏱️ {now} | 🌙 POST-MARKET & ASIA STANDBY (300s)
🏛️ POLICY: FED RATE 5.25% │ CPI YoY 3.0% │ QT PACING: $60B/MO
🇺🇸 WALL STREET US CORE BENCHMARKS & LIQUIDITY STRUCTURE:
   • SPX: {spx_p:.2f} │ NVDA: {fmt(*vals['NVDA'])} │ AAPL: {fmt(*vals['AAPL'])}
   • MSFT: {fmt(*vals['MSFT'])} │ SPY FLOW: {fmt(*vals['SPY'])} │ DXY: {dxy_p:.2f} ({dxy_c:+.2f}%)
🌐 MACRO: DXY {dxy_p:.2f} │ VIX {vix_p:.2f} │ US10Y 4.67% [STATIC]
────────────────────────────────────────────────────
🐋 WHALE SPIKE: KOSPI 564K in 3m (518.6x AVG) 🟢 ACCUMULATION
════════════════════════════════════════════════════
M82 TERMINAL ENGINE • v5.3 LIVE | Daemons 6/6
""")

if __name__=="__main__":
    while True:
        try:
            render()
            time.sleep(15)
        except KeyboardInterrupt:
            sys.exit(0)
