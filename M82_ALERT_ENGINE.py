import os, sys, requests, time
from datetime import datetime

# Instalar gTTS si no existe para sintetizar voz localmente
try:
    from gtts import gTTS
except ImportError:
    os.system("pip install gTTS requests")
    from gtts import gTTS

TOKEN = os.environ.get("BOT_TOKEN")
CHAT = os.environ.get("CHAT_ID")

def trigger_defensive_audio(bear_avg, bear_count, wti_change):
    now = datetime.now().strftime('%H:%M')
    
    # Texto que dirá la voz institucional
    script_text = (
        f"Atención Chairman. Alerta de riesgo activada a las {now}. "
        f"Modo defensivo encendido. Promedio bajista en {bear_avg:.2f} por ciento con {bear_count} activos en rojo. "
        f"Prohibido abrir nuevas posiciones largas. "
        f"Riesgo en crudo: WTI se desplaza {wti_change:.2f} por ciento. "
        f"Mantener la matriz en observación."
    )
    
    audio_filename = "defensive_alert.mp3"
    
    try:
        # Generar Audio
        tts = gTTS(text=script_text, lang='es', slow=False)
        tts.save(audio_filename)
        
        # Enviar Nota de Voz a Telegram
        if TOKEN and CHAT:
            url = f"https://api.telegram.org/bot{TOKEN}/sendVoice"
            with open(audio_filename, 'rb') as audio:
                files = {'voice': audio}
                data = {'chat_id': CHAT, 'caption': f"🚨 **DEFENSIVE VOICE ALERT** — {now} VET"}
                requests.post(url, data=data, files=files, timeout=10)
                
            print(f"🔊 Alerta de voz enviada con éxito a Telegram.")
    except Exception as e:
        print(f"⚠️ Error generando o enviando audio: {e}")

if __name__ == "__main__":
    # Prueba del motor de audio manual
    trigger_defensive_audio(bear_avg=-1.01, bear_count=45, wti_change=-1.21)
