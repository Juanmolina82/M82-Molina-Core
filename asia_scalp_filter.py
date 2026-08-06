import requests, time, os, sys
from m82_config import CONFIG
from m82_quantum_agi_core import run_quantum_pipeline

TOKEN = os.environ.get("BOT_TOKEN")
CHAT = os.environ.get("CHAT_ID")
TOKEN_V2 = os.environ.get("BOT_TOKEN_V2")
VIP_CHAT = os.environ.get("VIP_BROADCAST_CHAT_ID")

if not TOKEN or not CHAT:
    print("❌ ERROR: Variables BOT_TOKEN o CHAT_ID no detectadas.", flush=True)
    sys.exit(1)

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

NQ_TICKER = "NQ=F"
GC_TICKER = "GC=F"

def send_telegram_msg(token, chat_id, text):
    if not token or not chat_id:
        return
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=4)
    except Exception as e:
        print(f"Error sending message: {e}", flush=True)

def send_voice_alert(text_summary, state, confidence):
    target_token = TOKEN_V2 if TOKEN_V2 else TOKEN
    target_chat = VIP_CHAT if VIP_CHAT else CHAT
    
    voice_msg = (
        f"🎙️ *[M82 REAL-TIME VOICE TRANSMISSION]*\n\n"
        f"⚛️ *Estado Cuántico:* `{state}`\n"
        f"🧠 *Confianza AGI:* `{confidence:.1f}%`\n"
        f"📊 *Detalle:* {text_summary}"
    )
    send_telegram_msg(target_token, target_chat, voice_msg)

def get_telemetry():
    try:
        url_nq = f"https://query1.finance.yahoo.com/v8/finance/chart/{NQ_TICKER}?interval=1m&range=1d&includePrePost=true"
        j_nq = s.get(url_nq, timeout=4).json()
        closes_nq = [float(x) for x in j_nq['chart']['result'][0]['indicators']['quote'][0]['close'] if isinstance(x, (int, float)) and x > 0]
        vols_nq = [float(x) for x in j_nq['chart']['result'][0]['indicators']['quote'][0]['volume'] if isinstance(x, (int, float))]
        
        url_gc = f"https://query1.finance.yahoo.com/v8/finance/chart/{GC_TICKER}?interval=1m&range=1d&includePrePost=true"
        j_gc = s.get(url_gc, timeout=3).json()
        closes_gc = [float(x) for x in j_gc['chart']['result'][0]['indicators']['quote'][0]['close'] if isinstance(x, (int, float)) and x > 0]

        if len(vols_nq) < 20 or len(closes_nq) < 3 or len(closes_gc) < 4:
            return None

        current_nq = closes_nq[-1]
        avg_vol = sum(vols_nq[-20:-3]) / 17.0 if vols_nq[-20:-3] else 1.0
        ratio_nq = sum(vols_nq[-3:]) / (avg_vol * 3.0) if avg_vol > 0 else 0.0
        gc_mom = ((closes_gc[-1] - closes_gc[-4]) / closes_gc[-4]) * 100.0

        return current_nq, ratio_nq, gc_mom
    except Exception as e:
        print(f"Error fetching telemetry: {e}", flush=True)
        return None

print("⚛️ M82 QUANTUM-AGI REALTIME DAEMON ONLINE — Monitoreo continuo activo...", flush=True)

last_state = "SUPERPOSITION_HOLD"

while True:
    data = get_telemetry()
    if data:
        nq_price, ratio, gc_mom = data
        q_res = run_quantum_pipeline(nq_price, CONFIG["NQ_DYNAMIC_SUPPORT"], ratio, gc_mom)
        current_state = q_res['state']
        confidence = q_res['confidence']
        
        # Log local en pantalla
        print(
            f"[{time.strftime('%H:%M:%S')}] NQ: {nq_price:.2f} | Vol: {ratio:.2f}x | GC: {gc_mom:+.2f}% | "
            f"State: {current_state} (|BULL>: {q_res['prob_bull']:.1f}%) | AGI: {confidence:.1f}",
            flush=True
        )

        # Transmisión en tiempo real ante cambio de estado o señal fuerte
        if current_state != last_state and current_state != "SUPERPOSITION_HOLD":
            summary = f"NQ a {nq_price:.2f} (Vol {ratio:.2f}x, GC Mom {gc_mom:+.2f}%)."
            send_voice_alert(summary, current_state, confidence)
            last_state = current_state

    time.sleep(15)
