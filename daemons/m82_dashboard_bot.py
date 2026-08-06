import requests, time, os, sys, glob

TOKEN = os.environ.get("BOT_TOKEN")
CHAT = os.environ.get("CHAT_ID")
TOKEN_V2 = os.environ.get("BOT_TOKEN_V2")
VIP_CHAT = os.environ.get("VIP_BROADCAST_CHAT_ID")

s = requests.Session()

def get_updates(offset=None):
    if not TOKEN:
        return []
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?timeout=5"
    if offset:
        url += f"&offset={offset}"
    try:
        r = s.get(url, timeout=7).json()
        return r.get("result", [])
    except Exception:
        return []

def send_telegram_msg(text):
    if not TOKEN or not CHAT:
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        s.post(url, json={"chat_id": CHAT, "text": text, "parse_mode": "Markdown"}, timeout=4)
    except Exception as e:
        print(f"Error TG send: {e}", flush=True)

def analyze_quantum_hitrate():
    log_files = glob.glob("logs/*.log")
    bull_count = 0
    bear_count = 0
    hold_count = 0
    
    for log_path in log_files:
        try:
            with open(log_path, "r") as f:
                lines = f.readlines()
                for line in lines[-500:]: # Analiza las últimas 500 líneas
                    if "BULL_ACCUMULATION" in line:
                        bull_count += 1
                    elif "BEAR_FLUSH" in line:
                        bear_count += 1
                    elif "SUPERPOSITION_HOLD" in line:
                        hold_count += 1
        except Exception:
            pass
            
    total = bull_count + bear_count + hold_count
    if total == 0:
        return "⚠️ Sin suficientes datos estocásticos registrados aún."
        
    bull_pct = (bull_count / total) * 100.0
    bear_pct = (bear_count / total) * 100.0
    hold_pct = (hold_count / total) * 100.0
    
    report = (
        f"📊 *[M82 QUANTUM METRICS & HIT RATE DASHBOARD]*\n"
        f"────────────────────────────────\n"
        f"🎯 *Total Muestras Analizadas:* `{total}`\n"
        f"📈 *|BULL⟩ Accumulation:* `{bull_count}` (`{bull_pct:.1f}%`)\n"
        f"📉 *|BEAR⟩ Flush:* `{bear_count}` (`{bear_pct:.1f}%`)\n"
        f"⚛️ *Superposition Hold:* `{hold_count}` (`{hold_pct:.1f}%`)\n"
        f"────────────────────────────────\n"
        f"🛡️ *Dynamic Hard Floor:* `$29,500.00` [FIXED]\n"
        f"💡 *Recomendación AGI:* "
        f"{'🔥 Subir peso Whale a 0.50' if bull_pct >= 65 else '⚖️ Mantener pesos [0.45, 0.35, 0.20]'}"
    )
    return report

def check_process_health():
    daemons = ["asia_scalp_filter.py", "ny_wallstreet_core.py", "m82_market_scanner.py"]
    dead_services = []
    
    for d in daemons:
        # Verifica procesos en ps aux
        res = os.popen(f"ps aux | grep '{d}' | grep -v grep").read().strip()
        if not res:
            dead_services.append(d)
            
    if dead_services:
        alert = f"🚨 *[M82 HEALTH CHECK ALERT]*\nServicios caídos detectados: `{dead_services}`\n🔄 Resucitando daemons automáticamente..."
        send_telegram_msg(alert)
        os.system("~/start_m82.sh")

print("🤖 M82 DASHBOARD & HEALTH-CHECK BOT ACTIVE...", flush=True)

offset = None
last_health_check = time.time()

while True:
    updates = get_updates(offset)
    for u in updates:
        offset = u["update_id"] + 1
        msg = u.get("message", {})
        text = msg.get("text", "").strip().lower()
        
        if text in ["/status", "/metrics", "/dashboard", "status", "metrics"]:
            dashboard_text = analyze_quantum_hitrate()
            send_telegram_msg(dashboard_text)
            
    # Ejecuta el Health Check de PIDs cada 30 segundos
    if time.time() - last_health_check > 30:
        check_process_health()
        last_health_check = time.time()
        
    time.sleep(2)
