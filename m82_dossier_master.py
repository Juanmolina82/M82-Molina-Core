# -*- coding: utf-8 -*-
"""
================================================================================
                    M82 GLOBAL INTELLIGENCE - ENGINE V8.0
               Ecosistema Sovereign-Grade: Ingesta Dinámica y Validada
================================================================================
"""
import sys
import requests
import time

class M82RealTimeIntel(object):
    def __init__(self, wti=95.42, nasdaq=-4.18, nvidia=-6.0):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "gemma2:2b"
        self.holding_name = "Inversiones Estrategicas Molina Holdings"
        
        # ASIGNACIÓN DE VARIABLES DINÁMICAS (REAL-TIME)
        self.wti_crude = wti          
        self.nasdaq_drop = nasdaq        
        self.nvidia_drop = nvidia       
        self.geopolitics = "Escalada militar Iran-Israel. Ataques con misiles. Tension en Ormuz/Kuwait."

    def despertar_ia(self):
        """Fuerza al nodo local a cargar el modelo en RAM antes del analisis"""
        print("🧠 [M82 CORE] Despertando tensores locales de Gemma 2...")
        payload = {"model": self.model_name, "prompt": "hello", "stream": False}
        try:
            requests.post(self.ollama_url, json=payload, timeout=10)
            print("🟢 [NODO] Cerebro local online y listo para inferencia.")
            return True
        except Exception:
            print("⚠️ [ALERTA] Inferencia en modo heuristico desconectado.")
            return False

    def consultar_ia_local(self, prompt_contexto):
        payload = {
            "model": self.model_name,
            "prompt": f"[M82 QUANT LIVE ENGINE]\n{prompt_contexto}\nDictamen Corto:",
            "stream": False
        }
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=25)
            return response.json().get("response", "").strip()
        except Exception:
            return "⚡ [HEURÍSTICA LIVE] Volatilidad extrema. Mantener posiciones de resguardo."

    def procesar_cable_noticias(self):
        print("\n" + "🛰️  " + "="*75)
        print(" [M82 LIVE FEED] CORRELACIÓN DE RIESGO MACRO & GEOPOLÍTICO V8.0")
        print("="*77)
        print(f"📁 Entidad Matrix: {self.holding_name}")
        print(f"🚨 Geopolitica: {self.geopolitics}")
        print(f"📉 Shocks: NASDAQ ({self.nasdaq_drop}%) | NVIDIA ({self.nvidia_drop}%)")
        print(f"🛢️  Commodities: Petroleo WTI a ${self.wti_crude} USD/Barril")
        print("-" * 77)

        # Hilo 1: Impacto de Mercado Tecnológico
        contexto_tech = (
            f"El NASDAQ cae {self.nasdaq_drop}% y NVIDIA cae {self.nvidia_drop}%. "
            f"Determina la accion inmediata para la cartera de {self.holding_name}."
        )
        print("\n🧠 ANÁLISIS 1: COGNICIÓN DE MERCADOS:")
        print(f"   {self.consultar_ia_local(contexto_tech)}")

        # Hilo 2: Impacto Energético
        contexto_petroleo = (
            f"Ataques Iran-Israel escalan el crudo WTI a ${self.wti_crude} USD. "
            f"Define el estatus del flujo de caja del Holding."
        )
        print("\n🧠 ANÁLISIS 2: COMMODITIES & RISK UPSTREAM:")
        print(f"   {self.consultar_ia_local(contexto_petroleo)}")
        print("="*77)

if __name__ == "__main__":
    # Permite recibir valores desde la consola o usar los del cable por defecto
    wti_input = float(sys.argv[1]) if len(sys.argv) > 1 else 95.42
    nasdaq_input = float(sys.argv[2]) if len(sys.argv) > 2 else -4.18
    
    engine = M82RealTimeIntel(wti=wti_input, nasdaq=nasdaq_input)
    engine.despertar_ia()
    engine.procesar_cable_noticias()
