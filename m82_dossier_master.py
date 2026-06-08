# -*- coding: utf-8 -*-
"""
================================================================================
                    M82 GLOBAL INTELLIGENCE - ENGINE V9.0
             Ecosistema Sovereign-Grade: Misión, Visión e Inteligencia
================================================================================
"""
import sys
import requests
import time

class M82SovereignCore(object):
    def __init__(self, wti=95.42, nasdaq=-4.18, nvidia=-6.0):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "gemma2:2b"
        self.holding_name = "Inversiones Estrategicas Molina Holdings"
        
        # FILOSOFÍA CORPORATIVA SOBERANA
        self.mision = "Garantizar la autonomía analítica, la resiliencia operativa y la absoluta privacidad de los flujos financieros y estratégicos del Holding, procesando inteligencia global localmente y sin dependencia de infraestructuras centralizadas externas."
        self.vision = "Consolidar el ecosistema M82 Molina-Core como un búnker tecnológico auto-sustentable de Grado Soberano para el año 2027, capaz de predecir fluctuaciones macroeconómicas y gestionar activos mediante agentes cognitivos 100% desconectados."

        # ASIGNACIÓN DE VARIABLES
        self.wti_crude = wti          
        self.nasdaq_drop = nasdaq        
        self.nvidia_drop = nvidia       
        self.geopolitics = "Escalada militar Iran-Israel (Ataques de misiles). Shock tecnologico en Wall Street."

    def desplegar_manifiesto(self):
        """Imprime la identidad institucional del holding en la consola corporativa"""
        print("\n" + "🏛️  " + "="*75)
        print("                 M82 MOLINA-CORE - MANIFIESTO INSTITUCIONAL")
        print("="*79)
        print(f"🎯 MISIÓN SOBERANA:\n   '{self.mision}'")
        print(f"\n🔮 VISIÓN ESTRATÉGICA (Hacia 2027):\n   '{self.vision}'")
        print("="*79)
        time.sleep(1)

    def despertar_ia(self):
        print("🧠 [M82 CORE] Inicializando modelo local Gemma 2 según directivas del Manifiesto...")
        payload = {"model": self.model_name, "prompt": "init", "stream": False}
        try:
            requests.post(self.ollama_url, json=payload, timeout=10)
            print("🟢 [NODO COGNITIVO] Alineado con la Misión del Holding. Online.")
            return True
        except Exception:
            print("⚠️ [CONTINGENCIA] Ejecutando bajo protocolos heurísticos defensivos.")
            return False

    def consultar_ia_local(self, prompt_contexto):
        payload = {
            "model": self.model_name,
            "prompt": f"[M82 MANIFESTO ALIGNED ENGINE]\nDirectiva: {self.mision}\nContexto actual: {prompt_contexto}\nDictamen Soberano:",
            "stream": False
        }
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=25)
            return response.json().get("response", "").strip()
        except Exception:
            return "⚡ [HEURÍSTICA CORE] Volatilidad extrema. Custodia de capitales activa."

    def procesar_operaciones(self):
        print("\n" + "🛰️  " + "="*75)
        print(" [M82 LIVE FEED] CORRELACIÓN BAJO PRINCIPIOS DE GOBERNANZA V9.0")
        print("="*77)
        print(f"📁 Entidad Operadora: {self.holding_name}")
        print(f"📉 Variables: NASDAQ ({self.nasdaq_drop}%) | NVIDIA ({self.nvidia_drop}%) | WTI (${self.wti_crude} USD)")
        print("-" * 77)

        # Análisis Guiado por la Misión
        contexto = (
            f"Bajo nuestra Mision de autonomia, evalua la toma de ganancias de NVIDIA ({self.nvidia_drop}%) "
            f"y los misiles en Medio Oriente. ¿Como debe actuar el fondo defensivo de Molina Holdings?"
        )
        print("\n🧠 DICTAMEN INTEGRADO DE INTELIGENCIA DE MERCADOS:")
        print(f"   {self.consultar_ia_local(contexto)}")
        print("="*77)

if __name__ == "__main__":
    wti_param = float(sys.argv[1]) if len(sys.argv) > 1 else 95.42
    nasdaq_param = float(sys.argv[2]) if len(sys.argv) > 2 else -4.18
    
    core = M82SovereignCore(wti=wti_param, nasdaq=nasdaq_param)
    core.desplegar_manifiesto()
    core.despertar_ia()
    core.procesar_operaciones()
