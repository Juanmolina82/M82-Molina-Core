import requests, time, os, sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

TOKEN = os.environ.get("BOT_TOKEN")
CHAT = os.environ.get("CHAT_ID")
NTFY = "https://ntfy.sh/M82-ESCUPE"

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

FED_RATE = "5.25%"
CPI_YoY = "3.0%"

MACRO_TICKERS = ["DX-Y.NYB", "^IRX", "^FVX", "^TNX", "^TYX", "^VIX", "CL=F", "GC=F"]

TICKERS = [
    # Índices Mundiales
    "^GSPC", "^NDX", "^DJI", "^RUT", "^GDAXI", "^FCHI", "^FTSE", "^IBEX", "FEZ", "^N225", "^HSI", "000300.SS", "^NSEI",
    # Futuros de Índices & Commodities
    "ES=F", "NQ=F", "YM=F", "RTY=F", "NG=F", "RB=F", "SI=F", "HG=F", "ZC=F", "ZS=F", "ZW=F",
    # Wall Street ETFs & Mega-Caps
    "SPY", "QQQ", "DIA", "IWM", "VTI", "VOO", "VUG", "SCHD", "GLD", "SLV", "SMH", "SOXX", "XLE", "URA",
    "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA",
    # Wall Street Sectores
    "JPM", "BAC", "GS", "MS", "V", "MA", "BRK-B", "LLY", "JNJ", "PFE", "UNH", "WMT", "COST", "PG", "KO", "PEP", "CAT", "GE", "LMT", "BA", "XOM", "CVX",
    # Tech, Cloud & Ciberseguridad
    "AMD", "ARM", "TSM", "AVGO", "MU", "QCOM", "INTC", "PLTR", "CRWD", "PANW", "SNOW", "NET", "SHOP", "SQ", "COIN", "HOOD", "MSTR", "MARA",
    # España & Bonos
    "SAN.MC", "BBVA.MC", "IBE.MC", "ITX.MC", "TEF.MC", "REP.MC", "TLT", "IEF", "SHY", "LQD", "HYG", "JNK"
]

NAMES = {
    "^GSPC": "SPX", "^NDX": "NASDAQ100", "^DJI": "DOW30", "^RUT": "RUSSELL2000",
    "^GDAXI": "DAX40", "^FCHI": "CAC40", "^FTSE": "FTSE100", "^IBEX": "IBEX35",
    "FEZ": "EUROSTOXX50", "^N225": "NIKKEI225", "^HSI": "HANGSENG", "000300.SS": "CSI300", "^NSEI": "NIFTY50",
    "GC=F": "GOLD", "CL=F": "WTI", "^VIX": "VIX", "ES=F": "ES_FUT", "NQ=F": "NQ_FUT", "YM=F": "DOW_FUT", "RTY=F": "RTY_FUT",
    "JPM": "JPMORGAN", "BAC": "BofA", "GS": "GOLDMAN", "MS": "M_STANLEY", "V": "VISA", "MA": "MASTERCARD", "BRK-B": "BERKSHIRE",
    "LLY": "LILLY", "JNJ": "J&J", "PFE": "PFIZER", "UNH": "UNH", "WMT": "WALMART", "COST": "COSTCO", "PG": "P&G", "KO": "COCACOLA", "PEP": "PEPSI",
    "CAT": "CATERPILLAR", "GE": "GE", "LMT": "LOCKHEED", "BA": "BOEING",
    "SAN.MC": "SANTANDER", "BBVA.MC": "BBVA", "IBE.MC": "IBERDROLA", "ITX.MC": "INDITEX", "TEF.MC": "TELEFONICA", "REP.MC": "REPSOL",
    "DX-Y.NYB": "DXY", "DX=F": "DXY", "^IRX": "US03M", "^FVX": "US05Y", "^TNX": "US10Y", "^TYX": "US30Y",
    "GOOGL": "GOOG", "MSFT": "MSFT", "AMZN": "AMZN", "TSLA": "TSLA",
    "CRWD": "CRWD", "PANW": "PANW", "SNOW": "SNOW", "NET": "NET", "SHOP": "SHOP", "SQ": "SQ", "COIN": "COIN", "HOOD": "HOOD",
    "MSTR": "MSTR", "MARA": "MARA", "XLE": "XLE", "XOM": "XOM", "CVX": "CVX", "URA": "URA", "QCOM": "QCOM", "INTC": "INTC"
}

NEWS_CACHE = {"data": [], "ts": 0}
LAST_AH = {}

def fetch_news():
    if time.time() - NEWS_CACHE["ts"] < 60:
        return NEWS_CACHE["data"]
    try:
        url = "https://query2.finance.yahoo.com/v1/finance/search?q=market&newsCount=3"
        j = s.get(url, timeout=4).json()
        headlines = [f"📰 [{n.get('publisher')}] {n.get('title')}" for n in j.get('news', []) if n.get('title')][:3]
        if headlines:
            NEWS_CACHE["data"] = headlines
            NEWS_CACHE["ts"] = time.time()
        return NEWS_CACHE["data"]
    except Exception:
        return NEWS_CACHE["data"]

def fetch(tk):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?interval=1m&range=1d&includePrePost=true"
        j = s.get(url, timeout=3).json()
        m = j['chart']['result'][0]['meta']
        
        reg = float(m.get('regularMarketPrice') or 0)
        prev = float(m.get('chartPreviousClose') or m.get('previousClose') or reg)
        rp = ((reg - prev) / prev * 100) if prev else 0
        
        clean = NAMES.get(tk, tk)
        ext_p, ext_pct, ext_type = 0.0, 0.0, "REG"
        
        state = m.get('marketState', '')
        post = m.get('postMarketPrice')
        pre = m.get('preMarketPrice')
        
        if post and float(post) > 0:
            p = float(post)
            if abs(p - reg) > 0.001:
                ext_p = p
                ext_pct = ((p - reg) / reg * 100) if reg else 0
                ext_type = "AH"
        elif pre and float(pre) > 0 and state in ('PRE', 'PREPRE'):
            p = float(pre)
            if abs(p - prev) > 0.001:
                ext_p = p
                ext_pct = ((p - prev) / prev * 100) if prev else 0
                ext_type = "PRE"

        if ext_type != "REG":
            LAST_AH[clean] = (ext_p, ext_pct, ext_type)
        elif clean in LAST_AH:
            ext_p, ext_pct, ext_type = LAST_AH[clean]

        return {"ticker": clean, "price": reg, "pct": rp, "ext_price": ext_p, "ext_pct": ext_pct, "ext_type": ext_type}
    except Exception:
        return None

while True:
    try:
        ALL_TO_FETCH = list(set(MACRO_TICKERS + TICKERS))
        
        with ThreadPoolExecutor(max_workers=15) as executor:
            results = list(executor.map(fetch, ALL_TO_FETCH))
            
        valid_results = [r for r in results if r and r["price"] > 0]
        
        macro_data = {r["ticker"]: r for r in valid_results if r["ticker"] in [NAMES.get(m, m) for m in MACRO_TICKERS]}
        dataset = [r for r in valid_results if r["ticker"] not in [NAMES.get(m, m) for m in MACRO_TICKERS]]
        
        bulls = sorted([d for d in dataset if d["pct"] >= 0], key=lambda x: x["pct"], reverse=True)
        bears = sorted([d for d in dataset if d["pct"] < 0], key=lambda x: x["pct"])
        
        now = datetime.now().strftime('%d/%m/%Y • %H:%M:%S VET')
        out = []
        out.append("🏛️ MOLINA HOLDINGS | QUANT & MACRO MATRIX")
        out.append(f"⏱️ {now} | REAL-TIME STREAMING FEED")
        
        dxy = macro_data.get("DXY", {})
        us03m = macro_data.get("US03M", {})
        us05y = macro_data.get("US05Y", {})
        us10y = macro_data.get("US10Y", {})
        us30y = macro_data.get("US30Y", {})
        vix = macro_data.get("VIX", {})
        wti = macro_data.get("WTI", {})
        gold = macro_data.get("GOLD", {})

        vix_val = vix.get('price', 0)
        dxy_pct = dxy.get('pct', 0)
        
        alerts = []
        if vix_val >= 20.0:
            alerts.append(f"🔥 HIGH VOLATILITY ALERT: VIX AT {vix_val:.2f}")
        if abs(dxy_pct) >= 1.0:
            alerts.append(f"💵 DXY SHOCK: {dxy_pct:+.1f}% MOVE")

        if alerts:
            out.append("🚨 " + " | ".join(alerts))
        else:
            out.append("✅ MACRO RISK STATUS: STABLE / NORMAL")

        out.append(f"🏛️ POLICY: FED RATE {FED_RATE} │ CPI YoY {CPI_YoY}")
        out.append(
            f"🌐 YIELDS: US03M {us03m.get('price', 0):.2f}% │ US05Y {us05y.get('price', 0):.2f}% │ "
            f"US10Y {us10y.get('price', 0):.2f}% │ US30Y {us30y.get('price', 0):.2f}%"
        )
        out.append(
            f"🌐 MACRO: DXY {dxy.get('price', 0):.2f} ({dxy_pct:+.1f}%) │ "
            f"VIX {vix_val:.2f} │ WTI ${wti.get('price', 0):.2f} │ GOLD ${gold.get('price', 0):.1f}"
        )
        
        headlines = fetch_news()
        if headlines:
            out.append("────────────────────────────────────────────────────")
            out.extend(headlines)

        out.append("════════════════════════════════════════════════════")
        out.append(f"{'ASSET':<12} │ {'REGULAR SESSION':<16} │ {'EXTENDED (PRE/AH)':<16}")
        out.append("────────────────────────────────────────────────────")
        out.append("🟩 LONG / BULLISH MOMENTUM")
        out.append("────────────────────────────────────────────────────")
        
        for d in bulls:
            reg_fmt = f"${d['price']:>7.2f} 🟢 {d['pct']:>+5.1f}%"
            ext_fmt = f"{'🟢' if d['ext_pct'] >= 0 else '🔴'} ${d['ext_price']:>6.2f} ({d['ext_pct']:>+4.1f}% {d['ext_type']})" if d['ext_type'] != "REG" else ""
            out.append(f"{d['ticker']:<12} │ {reg_fmt:<16} │ {ext_fmt}")
            
        out.append("────────────────────────────────────────────────────")
        out.append("🟥 SHORT / BEARISH & RISK FLUX")
        out.append("────────────────────────────────────────────────────")
        
        for d in bears:
            reg_fmt = f"${d['price']:>7.2f} 🔴 {d['pct']:>+5.1f}%"
            ext_fmt = f"{'🟢' if d['ext_pct'] >= 0 else '🔴'} ${d['ext_price']:>6.2f} ({d['ext_pct']:>+4.1f}% {d['ext_type']})" if d['ext_type'] != "REG" else ""
            out.append(f"{d['ticker']:<12} │ {reg_fmt:<16} │ {ext_fmt}")
            
        out.append("════════════════════════════════════════════════════\n")
        
        full_report = "\n".join(out)
        print(full_report, flush=True)
        
        # Envíos HTTP con manejo de errores
        priority = "urgent" if alerts else "max"
        if NTFY:
            try:
                s.post(NTFY, data=full_report.encode('utf-8'), headers={"Title": "M82 INSTITUTIONAL MATRIX", "Priority": priority}, timeout=5)
            except Exception as e:
                print(f"ERR NTFY: {e}", flush=True)
            
        if TOKEN and CHAT:
            try:
                s.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": CHAT, "text": f"```\n{full_report}\n```", "parse_mode": "Markdown"}, timeout=5)
            except Exception as e:
                print(f"ERR TELEGRAM: {e}", flush=True)
            
        time.sleep(5) # Pausa estratégica de 5s para evitar baneos de API en background
    except Exception as e:
        print(f"ERR GLOBAL: {e}", flush=True)
        time.sleep(2)
