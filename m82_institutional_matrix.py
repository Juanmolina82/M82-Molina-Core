import requests, time, os, sys
import xml.etree.ElementTree as ET
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

TOKEN = os.environ.get("BOT_TOKEN")
CHAT = os.environ.get("CHAT_ID")
NTFY = "https://ntfy.sh/M82-ESCUPE"
TIMESTAMP_FILE = ".last_tg_send"

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

FED_RATE = "5.25%"
CPI_YoY = "3.0%"

MACRO_TICKERS = ["DX-Y.NYB", "^IRX", "^FVX", "^TNX", "^TYX", "^VIX", "USDJPY=X", "USDCNH=X"]
FUTURES_TICKERS = ["ES=F", "NQ=F", "YM=F", "RTY=F", "CL=F", "GC=F", "SI=F", "HG=F", "NG=F", "RB=F", "ZC=F", "ZS=F", "ZW=F"]

TICKERS = [
    "^N225", "^HSI", "000300.SS", "^SSEC", "^KS11", "^AXJO", "^NSEI", "^TWII",
    "^GSPC", "^NDX", "^DJI", "^RUT", "^GDAXI", "^FCHI", "^FTSE", "^IBEX", "FEZ",
    "SPY", "QQQ", "DIA", "IWM", "VTI", "VOO", "VUG", "SCHD", "GLD", "SLV", "SMH", "SOXX", "XLE", "URA",
    "SIL", "SILJ", "GDX", "COPX", "XOP", "OIH", "TAN", "ITA", "PAVE",
    "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA",
    "JPM", "BAC", "GS", "MS", "V", "MA", "BRK-B", "LLY", "JNJ", "PFE", "UNH", "WMT", "COST", "PG", "KO", "PEP", "CAT", "GE", "LMT", "BA", "XOM", "CVX",
    "AMD", "ARM", "TSM", "AVGO", "MU", "QCOM", "INTC", "PLTR", "CRWD", "PANW", "SNOW", "NET", "SHOP", "SQ", "COIN", "HOOD", "MSTR", "MARA",
    "SAN.MC", "BBVA.MC", "IBE.MC", "ITX.MC", "TEF.MC", "REP.MC", "TLT", "IEF", "SHY", "LQD", "HYG", "JNK",
    "TALO", "CRGY", "IAUX", "SOUN", "AXON", "SNDK", "VECO", "ELF", "FIG"
]

NAMES = {
    "^N225": "NIKKEI225", "^HSI": "HANGSENG", "000300.SS": "CSI300", "^SSEC": "SHANGHAI",
    "^KS11": "KOSPI", "^AXJO": "ASX200", "^NSEI": "NIFTY50", "^TWII": "TAIWAN_TWSE",
    "USDJPY=X": "USD/JPY", "USDCNH=X": "USD/CNH",
    "^GSPC": "SPX", "^NDX": "NASDAQ100", "^DJI": "DOW30", "^RUT": "RUSSELL2000",
    "^GDAXI": "DAX40", "^FCHI": "CAC40", "^FTSE": "FTSE100", "^IBEX": "IBEX35",
    "FEZ": "EUROSTOXX50", "GC=F": "GOLD_FUT", "CL=F": "WTI_FUT", "SI=F": "SILVER_FUT", "HG=F": "COPPER_FUT",
    "NG=F": "NATGAS_FUT", "RB=F": "GASO_FUT", "ZC=F": "CORN_FUT", "ZS=F": "SOY_FUT", "ZW=F": "WHEAT_FUT",
    "^VIX": "VIX", "ES=F": "ES_FUT", "NQ=F": "NQ_FUT", "YM=F": "DOW_FUT", "RTY=F": "RTY_FUT",
    "JPM": "JPMORGAN", "BAC": "BofA", "GS": "GOLDMAN", "MS": "M_STANLEY", "V": "VISA", "MA": "MASTERCARD", "BRK-B": "BERKSHIRE",
    "LLY": "LILLY", "JNJ": "J&J", "PFE": "PFIZER", "UNH": "UNH", "WMT": "WALMART", "COST": "COSTCO", "PG": "P&G", "KO": "COCACOLA", "PEP": "PEPSI",
    "CAT": "CATERPILLAR", "GE": "GE", "LMT": "LOCKHEED", "BA": "BOEING",
    "SAN.MC": "SANTANDER", "BBVA.MC": "BBVA", "IBE.MC": "IBERDROLA", "ITX.MC": "INDITEX", "TEF.MC": "TELEFONICA", "REP.MC": "REPSOL",
    "DX-Y.NYB": "DXY", "DX=F": "DXY", "^IRX": "US03M", "^FVX": "US05Y", "^TNX": "US10Y", "^TYX": "US30Y",
    "GOOGL": "GOOG", "MSFT": "MSFT", "AMZN": "AMZN", "TSLA": "TSLA",
    "CRWD": "CRWD", "PANW": "PANW", "SNOW": "SNOW", "NET": "NET", "SHOP": "SHOP", "SQ": "SQ", "COIN": "COIN", "HOOD": "HOOD",
    "MSTR": "MSTR", "MARA": "MARA", "XLE": "XLE", "XOM": "XOM", "CVX": "CVX", "URA": "URA", "QCOM": "QCOM", "INTC": "INTC",
    "TALO": "TALO", "CRGY": "CRGY", "IAUX": "IAUX",
    "SIL": "SILVER_ETF", "SILJ": "SILVER_JR", "GDX": "GOLD_MINERS", "COPX": "COPPER_MINERS",
    "XOP": "OIL_GAS_EP", "OIH": "OIL_SERVICES", "TAN": "SOLAR_ETF", "ITA": "DEFENSE_ETF", "PAVE": "INFRA_ETF",
    "SOUN": "SOUN", "AXON": "AXON", "SNDK": "SNDK", "VECO": "VECO", "ELF": "ELF", "FIG": "FIG"
}

INDICES_AND_FUTURES = ["SPX", "NASDAQ100", "DOW30", "RUSSELL2000", "DAX40", "CAC40", "FTSE100", "IBEX35", "EUROSTOXX50", "NIKKEI225", "HANGSENG", "CSI300", "SHANGHAI", "KOSPI", "ASX200", "NIFTY50", "TAIWAN_TWSE", "ES_FUT", "NQ_FUT", "DOW_FUT", "RTY_FUT", "GOLD_FUT", "WTI_FUT", "SILVER_FUT", "COPPER_FUT", "NATGAS_FUT", "GASO_FUT", "CORN_FUT", "SOY_FUT", "WHEAT_FUT"]

NEWS_CACHE = {"data": [], "ts": 0}

def get_last_tg_time():
    if os.path.exists(TIMESTAMP_FILE):
        try:
            with open(TIMESTAMP_FILE, "r") as f:
                return float(f.read().strip())
        except Exception:
            return 0
    return 0

def set_last_tg_time(ts):
    try:
        with open(TIMESTAMP_FILE, "w") as f:
            f.write(str(ts))
    except Exception:
        pass

def fetch_top_wire_news():
    if time.time() - NEWS_CACHE["ts"] < 300:
        return NEWS_CACHE["data"]
    headlines = []
    feeds = [
        ("BusinessWire", "https://www.businesswire.com/portal/site/home/news/rss/"),
        ("GlobeNewswire", "https://www.globenewswire.com/RssFeed/org/Notified.xml")
    ]
    for name, url in feeds:
        try:
            r = s.get(url, timeout=4, headers={"User-Agent": "Mozilla/5.0"})
            content = r.content.replace(b'& ', b'&amp; ')
            root = ET.fromstring(content)
            for item in root.findall('./channel/item')[:2]:
                t = item.find('title')
                if t is not None and t.text:
                    headlines.append(f"📰 [{name}] {t.text[:110]}")
            if len(headlines) >= 4:
                break
        except Exception:
            continue

    if headlines:
        NEWS_CACHE["data"] = headlines[:4]
        NEWS_CACHE["ts"] = time.time()
    return NEWS_CACHE["data"]

def detect_whale_spike(tk, closes, volumes):
    if len(volumes) < 20 or len(closes) < 3:
        return None
    valid_vols = [v for v in volumes[-20:-3] if isinstance(v, (int, float))]
    if not valid_vols:
        return None
    avg_vol = sum(valid_vols) / len(valid_vols)
    
    last_3m_vols = [v for v in volumes[-3:] if isinstance(v, (int, float))]
    last_3m_vol = sum(last_3m_vols)
    
    if avg_vol == 0 or last_3m_vol < 100000:
        return None
        
    ratio = last_3m_vol / (avg_vol * 3) if avg_vol > 0 else 1.0
    if ratio >= 2.8:
        c_last = closes[-1] if closes[-1] is not None else 0
        c_prev = closes[-3] if closes[-3] is not None else c_last
        side = "🟢 ACCUMULATION" if c_last >= c_prev else "🔴 SELLING PRESSURE"
        return f"⚡ WHALE SPIKE: {tk} {last_3m_vol/1e3:.0f}K in 3m ({ratio:.1f}x AVG) {side}"
    return None

def fetch(tk):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tk}?interval=1m&range=1d&includePrePost=true"
        j = s.get(url, timeout=3).json()
        res = j['chart']['result'][0]
        m = res['meta']
        q = res.get('indicators', {}).get('quote', [{}])[0]
        closes = q.get('close', []) or []
        volumes = q.get('volume', []) or []

        valid_ticks = [float(x) for x in closes if isinstance(x, (int, float)) and x > 0]
        price = valid_ticks[-1] if valid_ticks else float(m.get('regularMarketPrice') or 0)

        prev = float(m.get('chartPreviousClose') or m.get('previousClose') or price)
        pct = ((price - prev) / prev * 100) if prev else 0.0

        state = m.get('marketState', '')
        ext_p, ext_pct, ext_type = 0.0, 0.0, "REG"
        post = m.get('postMarketPrice')
        pre = m.get('preMarketPrice')

        if state == 'POST' and post:
            ext_p = float(post)
            ext_pct = ((ext_p - price) / price * 100) if price else 0
            ext_type = "AH"
        elif state in ('PRE', 'PREPRE') and pre:
            ext_p = float(pre)
            ext_pct = ((ext_p - prev) / prev * 100) if prev else 0
            ext_type = "PRE"

        clean_tk = NAMES.get(tk, tk)
        whale_alert = detect_whale_spike(clean_tk, closes, volumes)

        if price > 0:
            return {
                "ticker": clean_tk,
                "price": price,
                "pct": pct,
                "ext_price": ext_p,
                "ext_pct": ext_pct,
                "ext_type": ext_type,
                "whale": whale_alert
            }
    except Exception:
        pass
    return None

while True:
    t_start = time.time()
    try:
        now_dt = datetime.now()
        h, m_min = now_dt.hour, now_dt.minute
        
        if (h == 9 and m_min >= 30) or (h == 10):
            TG_INTERVAL = 45
            mode_label = "⚡ POWER OPEN ENGINE (45s)"
        else:
            TG_INTERVAL = 300
            mode_label = "🌙 POST-MARKET & ASIA STANDBY (300s)"

        ALL_TO_FETCH = list(set(MACRO_TICKERS + FUTURES_TICKERS + TICKERS))
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(fetch, ALL_TO_FETCH))
            
        valid_results = [r for r in results if r and r["price"] > 0]
        
        macro_names = [NAMES.get(m, m) for m in MACRO_TICKERS]
        futures_names = [NAMES.get(m, m) for m in FUTURES_TICKERS]
        
        macro_data = {r["ticker"]: r for r in valid_results if r["ticker"] in macro_names}
        futures_data = [r for r in valid_results if r["ticker"] in futures_names]
        dataset = [r for r in valid_results if r["ticker"] not in macro_names and r["ticker"] not in futures_names]
        
        whale_spikes = [r["whale"] for r in valid_results if r and r.get("whale")]

        # MÓDULO POST-MARKET EARNINGS ALPHA
        EARNINGS_MAP = {
            "SOUN": {"beat": 84.85}, "AXON": {"beat": 1.96}, "SNDK": {"beat": 12.26},
            "VECO": {"beat": 0.00}, "ELF": {"beat": 0.00}, "FIG": {"beat": 0.00}
        }
        earnings_alpha = []
        for r in valid_results:
            if r["ticker"] in EARNINGS_MAP and r.get("ext_type") in ("AH", "PRE"):
                info = EARNINGS_MAP[r["ticker"]]
                side_icon = '🟢' if r.get('ext_pct', 0) >= 0 else '🔴'
                earnings_alpha.append(f"{side_icon} {r['ticker']} {r['ext_pct']:+.2f}% EXT (Ref Beat {info['beat']:.2f}%)")

        bulls_all = sorted([d for d in dataset if d["pct"] >= 0], key=lambda x: x["pct"], reverse=True)
        bears_all = sorted([d for d in dataset if d["pct"] < 0], key=lambda x: x["pct"])
        
        bulls = bulls_all[:5]
        bears = bears_all[:5]
        
        bull_count = len(bulls_all)
        bear_count = len(bears_all)
        bear_avg = (sum(d['pct'] for d in bears_all) / bear_count) if bear_count else 0.0
        
        now = now_dt.strftime('%d/%m/%Y %H:%M VET')
        latency = round(time.time() - t_start, 1)
        
        header_out = []
        header_out.append("🏛️ MOLINA HOLDINGS — INSTITUTIONAL MATRIX v4.4.2")
        header_out.append(f"⏱️ {now} | {mode_label}")
        
        dxy = macro_data.get("DXY", {})
        us10y = macro_data.get("US10Y", {})
        vix = macro_data.get("VIX", {})
        usdjpy = macro_data.get("USD/JPY", {})
        usdcnh = macro_data.get("USD/CNH", {})

        header_out.append(f"🏛️ POLICY: FED RATE {FED_RATE} │ CPI YoY {CPI_YoY}")
        header_out.append(
            f"🌐 MACRO: DXY {dxy.get('price', 0):.2f} ({dxy.get('pct', 0):+.1f}%) │ US10Y {us10y.get('price', 0):.2f}% │ VIX {vix.get('price', 0):.2f}"
        )
        header_out.append(
            f"🌏 ASIA FX: USD/JPY {usdjpy.get('price', 0):.2f} ({usdjpy.get('pct', 0):+.2f}%) │ "
            f"USD/CNH {usdcnh.get('price', 0):.4f} ({usdcnh.get('pct', 0):+.2f}%)"
        )
        
        # FUTUROS — MONOSPACE UNIFICADO (2 ASSETS/LINE)
        header_out.append("────────────────────────────────────────────────────")
        header_out.append("⚡ CONTINUOUS DERIVATIVES & FUTURES (GLOBEX / CME):")

        def fmt_fixed(f, nick):
            icon = "🟢" if f["pct"] >= 0 else "🔴"
            return f"{nick:<4} {f['price']:>8.2f} {icon}{f['pct']:>+6.2f}%"

        NICK = {
            "ES_FUT": "ES", "NQ_FUT": "NQ", "DOW_FUT": "YM", "RTY_FUT": "RTY",
            "WTI_FUT": "WTI", "NATGAS_FUT": "NG", "GASO_FUT": "RB",
            "GOLD_FUT": "GOLD", "SILVER_FUT": "SILV", "COPPER_FUT": "HG",
            "CORN_FUT": "CORN", "SOY_FUT": "SOYB", "WHEAT_FUT": "WEAT"
        }
        f_map = {f["ticker"]: f for f in futures_data}

        def get_line(keys, label):
            items = [f_map[k] for k in keys if k in f_map]
            if not items: return None
            parts = [fmt_fixed(f, NICK.get(f["ticker"], f["ticker"][:4])) for f in items]
            if len(parts) > 2:
                return [f"{label} │ {' │ '.join(parts[:2])}", f"     │ {' │ '.join(parts[2:])}"]
            else:
                return [f"{label} │ {' │ '.join(parts)}"]

        lines = []
        for keys, label in [
            (["ES_FUT", "NQ_FUT", "DOW_FUT", "RTY_FUT"], "EQTY"),
            (["WTI_FUT", "NATGAS_FUT", "GASO_FUT"], "ENRG"),
            (["GOLD_FUT", "SILVER_FUT", "COPPER_FUT"], "METL"),
            (["CORN_FUT", "SOY_FUT", "WHEAT_FUT"], "AGRI"),
        ]:
            res = get_line(keys, label)
            if res:
                lines.extend(res)

        for l in lines:
            header_out.append(l)

        if earnings_alpha:
            header_out.append("────────────────────────────────────────────────────")
            header_out.append("📊 POST-MARKET EARNINGS ALPHA (M82 Audit):")
            for ea in earnings_alpha[:4]:
                header_out.append(f"• {ea}")

        if whale_spikes:
            header_out.append("────────────────────────────────────────────────────")
            header_out.append("🐋 INSTITUTIONAL WHALE VOLUME SPIKES (3m Window):")
            for ws in whale_spikes[:4]:
                header_out.append(f"• {ws}")

        wire_news = fetch_top_wire_news()
        if wire_news:
            header_out.append("────────────────────────────────────────────────────")
            header_out.append("📰 WIRE BREAKING NEWS:")
            header_out.extend(wire_news)

        bulls_out = []
        bulls_out.append("════════════════════════════════════════════════════")
        bulls_out.append(f"🟩 TOP 5 BULLISH LEADERS ({bull_count} GREEN)")
        bulls_out.append("────────────────────────────────────────────────────")
        
        for d in bulls:
            price_str = f"{d['price']:>9.2f}" if d['ticker'] in INDICES_AND_FUTURES else f"${d['price']:>7.2f}"
            reg_fmt = f"{price_str} 🟢 {d['pct']:>+5.1f}%"
            ext_price_str = f"${d['ext_price']:>6.2f}" if d['ticker'] not in INDICES_AND_FUTURES else f"{d['ext_price']:>7.1f}"
            ext_fmt = f"{'🟢' if d['ext_pct'] >= 0 else '🔴'} {ext_price_str} ({d['ext_pct']:>+4.1f}% {d['ext_type']})" if d['ext_type'] != "REG" else ""
            bulls_out.append(f"{d['ticker']:<13} │ {reg_fmt:<16} │ {ext_fmt}")

        bears_out = []
        bears_out.append("────────────────────────────────────────────────────")
        bears_out.append(f"🟥 TOP 5 BEARISH LEADERS ({bear_count} RED)")
        bears_out.append("────────────────────────────────────────────────────")
        
        for d in bears:
            price_str = f"{d['price']:>9.2f}" if d['ticker'] in INDICES_AND_FUTURES else f"${d['price']:>7.2f}"
            reg_fmt = f"{price_str} 🔴 {d['pct']:>+5.1f}%"
            ext_price_str = f"${d['ext_price']:>6.2f}" if d['ticker'] not in INDICES_AND_FUTURES else f"{d['ext_price']:>7.1f}"
            ext_fmt = f"{'🟢' if d['ext_pct'] >= 0 else '🔴'} {ext_price_str} ({d['ext_pct']:>+4.1f}% {d['ext_type']})" if d['ext_type'] != "REG" else ""
            bears_out.append(f"{d['ticker']:<13} │ {reg_fmt:<16} │ {ext_fmt}")
            
        bears_out.append("════════════════════════════════════════════════════")
        bears_out.append(f"M82 TERMINAL ENGINE • v4.4.2 MONOSPACE MASTER | Latency: ~{latency}s | {now}\n")
        
        full_report = "\n".join(header_out + bulls_out + bears_out)
        print(full_report, flush=True)
        
        current_time = time.time()
        last_sent = get_last_tg_time()
        
        if current_time - last_sent >= TG_INTERVAL:
            if TOKEN and CHAT:
                try:
                    r = s.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                               data={"chat_id": CHAT, "text": f"```\n{full_report}\n```", "parse_mode": "Markdown"}, timeout=5)
                    if r.status_code == 200:
                        set_last_tg_time(current_time)
                except Exception as e:
                    print(f"TG Error: {e}", flush=True)
            
        time.sleep(60)
    except Exception as e:
        time.sleep(30)
