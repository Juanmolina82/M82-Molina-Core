import requests, time, os, sys

# Credenciales de Telegram
TOKEN = os.environ.get("BOT_TOKEN")
CHAT = os.environ.get("CHAT_ID")

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

# Umbrales Institucionales
NQ_HARD_FLOOR = 29500.0
DXY_INTERLOCK_LIMIT = 100.20
KOSPI_BREAKOUT = 6350.0

def fetch_ticker(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m&range=1d"
    try:
        r = s.get(url, timeout=5).json()
        meta = r['chart']['result'][0]['meta']
        return meta.get('regularMarketPrice', 0.0)
    except Exception:
        return 0.0

def send_alert(msg):
    if not TOKEN or not CHAT:
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        s.post(url, json={"chat_id": CHAT, "text": msg, "parse_mode": "Markdown"}, timeout=4)
    except Exception as e:
        print(f"Error TG: {e}", flush=True)

print("🌙 [ASIA STANDBY DAEMON v2.5.1] ACTIVATED...", flush=True)

while True:
    nq_price = fetch_ticker("NQ=F")
    dxy_price = fetch_ticker("DX-Y.NYB")
    vix_price = fetch_ticker("^VIX")

    timestamp = time.strftime('%H:%M:%S VET')
    
    # Evaluar Interlocks y Condiciones de Intervención
    dxy_freeze = dxy_price >= DXY_INTERLOCK_LIMIT
    floor_breach = nq_price < NQ_HARD_FLOOR
    
    state = "SUPERPOSITION_HOLD"
    confidence = 58
    action = "STANDBY (NO ENTRY)"

    if dxy_freeze:
        state = "HARD_FREEZE_LONG"
        action = "🚨 DXY INTERLOCK TRIGGERED (DXY >= 100.20) - LONGS FROZEN"
        confidence = 0
    elif dxy_price < 99.90 and nq_price > NQ_HARD_FLOOR:
        state = "BULL_ACCUMULATION"
        action = "EXECUTE SCALP LONG"
        confidence = 72

    output = (
        f"[{timestamp}] 🌙 ASIA MONITOR | NQ: ${nq_price:.2f} | DXY: {dxy_price:.2f} | VIX: {vix_price:.2f}\n"
        f"├─ State: {state} (Confidence: {confidence}/100)\n"
        f"├─ Action: {action}\n"
        f"└─ Hard Floor Support: ${NQ_HARD_FLOOR:.2f} | DXY Max: {DXY_INTERLOCK_LIMIT}"
    )

    print(output, flush=True)

    # Si hay un Freeze o una condición crítica, notifica a Telegram
    if dxy_freeze:
        send_alert(f"🚨 *[M82 RISK WARDEN]* DXY rompió el umbral `{dxy_price:.2f}` (Limit: `{DXY_INTERLOCK_LIMIT}`). *Longs congelados en sesión Asia.*")

    # Refresh interval de 300 segundos (5 min) para Asia Standby
    time.sleep(300)
