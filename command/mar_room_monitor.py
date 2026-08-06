import os
import sys
import requests
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
KPLER_API_KEY = os.getenv("KPLER_API_KEY")

class WarRoomMonitorM82:
    def __init__(self):
        self.last_traffic = 6
        self.last_status = "INIT"
        self.debug_pin = os.getenv("M82_DEBUG_PIN", "238-571-527")

    def get_hormuz_traffic(self):
        try:
            url = "https://api.kpler.com/v2/straits/hormuz/transits"
            headers = {
                "Authorization": f"Bearer {KPLER_API_KEY}",
                "Accept": "application/json"
            }
            params = {"vessel_types": "VLCC,Suezmax", "last_days": 1}
            r = requests.get(url, headers=headers, params=params, timeout=8)
            if r.status_code == 200:
                data = r.json()
                transits = data.get("transits", [])
                self.last_traffic = len(transits)
                return self.last_traffic
            else:
                print(f"[Kpler API] Status {r.status_code}. Usando fallback local.")
                return self.last_traffic
        except Exception as e:
            print(f"[Conexión] No se pudo conectar a la API: {e}. Usando fallback local.")
            return self.last_traffic

    def sync_m82_vault(self, traffic, status):
        url = os.getenv("M82_VAULT_URL", "http://127.0.0.1:8080/api/v1/update_metrics")
        payload = {
            "traffic_24h": traffic,
            "strait": "Hormuz",
            "engine_status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "debug_pin": self.debug_pin
        }
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"[Vault] Servidor local offline: {e}")

    def alert(self, level, msg):
        token = os.getenv("TG_BOT_TOKEN")
        chat_id = os.getenv("TG_CHAT_ID_MHG")
        ts = datetime.now(timezone.utc).strftime('%H:%M UTC')
        full_msg = f"*M82 WAR ROOM* | {ts} | *{level}*\n{msg}"
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage", 
                json={"chat_id": chat_id, "text": full_msg, "parse_mode": "Markdown"},
                timeout=5
            )
        except Exception as e:
            print(f"[Telegram] Error al enviar alerta: {e}")

    def check_triggers(self):
        traffic = self.get_hormuz_traffic()
        
        # Umbrales Actualizados v3.14.2
        if traffic <= 4:
            new_status = "CRITICAL"
            msg = f"Hormuz Traffic: {traffic} VLCC/d\nCRITICAL LEVEL: <= 4 VLCC/d. IPC dovish, pero <4 sigue siendo hard stop. Faja $118-122 Hardened."
        elif traffic < 6:
            new_status = "v3.13"
            msg = f"Hormuz Traffic: {traffic} VLCC/d\nCHINA_PANIC_BUY: 5 VLCC/d. v3.13 Active. Con IPC -0.4%. Faja $115-118. VEZE: 90."
        elif traffic >= 11:
            new_status = "GCC_SURGE"
            msg = f"Hormuz Traffic: {traffic} VLCC/d\nGCC_SURGE: >= 11 VLCC/d. v3.13.3 Hold. Yields bajando, Faja §92-94. VEZE: 60."
        else:
            new_status = "STATUS_QUO"
            msg = f"Hormuz Traffic: {traffic} VLCC/d\nSTATUS QUO: 6-10 VLCC/d. v3.13.3 Base. IPC frío. Faja: $96-100. VEZE: 65-75."

        if new_status != self.last_status:
            self.last_status = new_status
            self.alert(new_status, msg)
            self.sync_m82_vault(traffic, new_status)

    def run(self):
        print("M82 Monitor Iniciado de forma Segura...")
        self.check_triggers()
        while True:
            time.sleep(900)
            self.check_triggers()

if __name__ == "__main__":
    monitor = WarRoomMonitorM82()
    monitor.run()
