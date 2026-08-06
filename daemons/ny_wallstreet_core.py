import requests, time, os, sys
from m82_config import CONFIG
from m82_quantum_agi_core import run_quantum_pipeline

TOKEN = os.environ.get("BOT_TOKEN")
CHAT = os.environ.get("CHAT_ID")
TOKEN_V2 = os.environ.get("BOT_TOKEN_V2")
VIP_CHAT = os.environ.get("VIP_BROADCAST_CHAT_ID")

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

NQ_TICKER = "NQ=F"
VIX_TICKER = "^VIX"
GC_TICKER = "GC=F"

def send_ny_realtime_broadcast(state, confidence, nq_p, vix_v, gc_m):
    target_token = TOKEN_V2 if TOKEN_V2 else TOKEN
    target_chat = VIP_CHAT if VIP_CHAT else CHAT
    
    msg = (
        f"🗽 *[M82 WALL STREET RTH VOICE TRANSMISSION]*\n"
        f"────────────────────────────────\n"
        f"⚛️ *Quantum State:* `{state}`\n"
        f"🧠 *AGI NY Confidence:* `{confidence:.1f}%`\n"
        f"📈 *NQ Price:* `{nq_p:.2f}`\n"
        f"📉 *VIX Level:* `{vix_v:.2f}` (Limit <= 18.50)\n"
        f"🥇 *Gold Mom:* `{gc_m:+.2f}%` (Limit <= 0.50%)\n"
        f"────────────────────────────────\n"
        f"💡 *NY Bias:* Institutional Expansion Active."
    )
    
    try:
        url = f"https://api.telegram.org/bot{target_token}/sendMessage"
        requests.post(url, json={"chat_id": target_chat, "text": msg, "parse_mode": "Markdown"}, timeout=3)
        print("🎙️ REAL-TIME NY VOICE BROADCAST SENT TO TELEGRAM", flush=True)
    except Exception as e:
        print(f"Error NY TG send: {e}", flush=True)

def fetch_ny_telemetry():
    try:
        # Fetch NQ
        u_nq = f"https://query1.finance.yahoo.com/v8/finance/chart/{NQ_TICKER}?interval=1m&range=1d&includePrePost=true"
        j_nq = s.get(u_nq, timeout=3).json()['chart']['result'][0]['indicators']['quote'][0]
        closes_nq = [float(x) for x in j_nq['close'] if isinstance(x, (int, float)) and x > 0]
        vols_nq = [float(x) for x in j_nq['volume'] if isinstance(x, (int, float))]
        
        # Fetch VIX
        u_vix = f"https://query1.finance.yahoo.com/v8/finance/chart/{VIX_TICKER}?interval=1m&range=1d"
        j_vix = s.get(u_vix, timeout=3).json()['chart']['result'][0]['indicators']['quote'][0]
        closes_vix = [float(x) for x in j_vix['close'] if isinstance(x, (int, float)) and x > 0]
        
        # Fetch GC
        u_gc = f"https://query1.finance.yahoo.com/v8/finance/chart/{GC_TICKER}?interval=1m&range=1d&includePrePost=true"
        j_gc = s.get(u_gc, timeout=3).json()['chart']['result'][0]['indicators']['quote'][0]
        closes_gc = [float(x) for x in j_gc['close'] if isinstance(x, (int, float)) and x > 0]

        if len(closes_nq) < 3 or len(closes_vix) < 1 or len(closes_gc) < 4:
            return None

        current_nq = closes_nq[-1]
        vix_val = closes_vix[-1]
        avg_vol = sum(vols_nq[-20:-3]) / 17.0 if vols_nq[-20:-3] else 1.0
        ratio_nq = sum(vols_nq[-3:]) / (avg_vol * 3.0) if avg_vol > 0 else 0.0
        gc_mom = ((closes_gc[-1] - closes_gc[-4]) / closes_gc[-4]) * 100.0

        return current_nq, ratio_nq, vix_val, gc_mom
    except Exception as e:
        print(f"Error fetching NY data: {e}", flush=True)
        return None

print("🗽 M82 WALL STREET (NY RTH) CORE DAEMON ONLINE", flush=True)

last_state = "SUPERPOSITION_HOLD"

while True:
    data = fetch_ny_telemetry()
    if data:
        nq_p, ratio, vix_v, gc_m = data
        
        # Ajuste de ratio para NY RTH (Requiere mayor densidad de volumen: >= 4.5x)
        ny_ratio_adj = ratio * 0.8
        
        q_res = run_quantum_pipeline(nq_p, CONFIG["NQ_DYNAMIC_SUPPORT"], ny_ratio_adj, gc_m)
        current_state = q_res['state']
        confidence = q_res['confidence']
        
        # Interlock extra para EE.UU.: VIX elevado cancela longs automáticos
        if vix_v > 18.50 and current_state == "BULL_ACCUMULATION":
            current_state = "SUPERPOSITION_HOLD"
            confidence *= 0.5

        print(
            f"[{time.strftime('%H:%M:%S')}] NY NQ: {nq_p:.2f} | Vol: {ratio:.2f}x | VIX: {vix_v:.2f} | "
            f"GC: {gc_m:+.2f}% | State: {current_state} | AGI: {confidence:.1f}",
            flush=True
        )

        if current_state != last_state and current_state != "SUPERPOSITION_HOLD":
            send_ny_realtime_broadcast(current_state, confidence, nq_p, vix_v, gc_m)
            last_state = current_state

    time.sleep(10) # Frecuencia de refresco más alta para EE.UU. (10 segundos)
