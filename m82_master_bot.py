# -*- coding: utf-8 -*-
import requests
import json

TOKEN = "8600412468:AAE9rQQC2Z0ReE4qJ1R9amDfm5m4sO2-wM4"
CHAT_ID = "1020305418"

def test_conexion():
    print("🛰️ [M82 INFRASTRUCTURE] Verificando estado del Bot...")
    # Verificar el token con la API oficial de Telegram
    url_me = f"https://api.telegram.org/bot{TOKEN}/getMe"
    try:
        r = requests.get(url_me, timeout=10)
        if r.status_code == 200:
            print(f"🟢 BOT ONLINE: @{r.json()['result']['username']} está autenticado correctamente.")
        else:
            print(f"❌ ERROR DE TOKEN: {r.text}")
            return
    except Exception as e:
        print(f"❌ FALLO DE RED EN LA TERMINAL: {e}")
        return

    # Forzar envío de mensaje de presencia institucional
    url_msg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "🏛️ *M82 SOVEREIGN BOT ONLINE*\n\nSincronización de Capas Completada.\n• Capa Energética: Activa (WTI $91.48)\n• Capa de Cómputo: Resiliente (Intel/Cerebras Alpha)\n\n_El nodo de control está transmitiendo en vivo._",
        "parse_mode": "Markdown"
    }
    try:
        res = requests.post(url_msg, json=payload, timeout=10)
        if res.status_code == 200:
            print("🚀 PING EXITOSO: Mensaje enviado al canal. Revisa tu Telegram ahora.")
        else:
            print(f"⚠️ TELEGRAM RECHAZÓ EL ENVÍO: {res.text}")
    except Exception as e:
        print(f"❌ FALLO AL ENVIAR MENSAJE: {e}")

if __name__ == "__main__":
    test_conexion()
