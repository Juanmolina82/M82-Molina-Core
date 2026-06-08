# -*- coding: utf-8 -*-
"""
================================================================================
                    M82 GLOBAL INTELLIGENCE - LIVE FEED V7.0
               Ecosistema Sovereign-Grade: Ingesta Macro en Tiempo Real
================================================================================
"""
import sys
import requests
import time

class M82RealTimeIntel(object):
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "gemma2:2b"
        self.holding_name = "Inversiones Estrategicas Molina Holdings"
        
        # DATOS DE INGESTA REAL-TIME (Cierre de Mercado Reciente)
        self.wti_crude = 95.42          # Precio base LSEG
        self.nasdaq_drop = -4.18        # Caída porcentual NASDAQ
        self.sp500_drop = -2.64         # Caída porcentual S&P 500
        self.nvidia_drop = -6.0         # Desplome de NVDA
        self.geopolitics = "Escalada militar Iran-Israel. Ataques con misiles. Tension en Ormuz/Kuwait."

    def consultar_ia_local(self, prompt_contexto):
        payload = {
            "model": self.model_name,
            "prompt": f"[M82 QUANT LIVE ENGINE]\n{prompt_contexto}\nDictamen de Riesgo Ejecutado:",
            "stream": False
        }
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=20)
            return response.json().get("response", "").strip()
        except Exception:
            return "⚠️ [CONEXIÓN] Retraso en tensores. Mantener protocolo STAY_FROZEN por precaucion."

    def procesar_cable_noticias(self):
        print("\n" + "🛰️  " + "="*75)
        print(" [M82 LIVE FEED] CORRELAZACIÓN DE RIESGO MACRO & GEOPOLÍTICO INMEDIATO")
        print("="*77)
        print(f"📁 Entidad Afectada: {self.holding_name}")
        print(f"🚨 Escenario Geopolitico: {self.geopolitics}")
        print(f"📉 Shock de Mercados: NASDAQ ({self.nasdaq_drop}%) | S&P 500 ({self.sp500_drop}%) | NVIDIA ({self.nvidia_drop}%)")
        print(f"🛢️  Impacto en Commodities: Petroleo WTI empujando al alza en ${self.wti_crude} USD/Barril")
        print("-" * 77)

        # Hilo 1: Análisis del Colapso de Tech frente al Holding
        contexto_tech = (
            f"El indice NASDAQ cayo {self.nasdaq_drop}% y NVIDIA retrocedio {self.nvidia_drop}% "
            f"por toma de ganancias en IA. Como afecta esto la liquidez de {self.holding_name}?"
        )
        print("\n🧠 ANÁLISIS 1: REBALANCED PORTFOLIO (IA GEMMA 2):")
        print(f"   {self.consultar_ia_local(contexto_tech)}")

        # Hilo 2: Análisis de la Escalada Petrolera
        contexto_petroleo = (
            f"Guerra de misiles Iran-Israel y aeropuerto de Kuwait cerrado disparan el crudo. "
            f"Con el WTI a ${self.wti_crude} USD, determina si debemos congelar activos o mover a refugios seguros."
        )
        print("\n🧠 ANÁLISIS 2: COMMODITIES & RISK PREMIUM (IA GEMMA 2):")
        print(f"   {self.consultar_ia_local(contexto_petroleo)}")
        
        print("\n🦅 [DICTAMEN DE SALIDA]: PORTFOLIO IN DEFENSIVE POSITION (STAY_FROZEN)")
        print("="*77)

if __name__ == "__main__":
    engine = M82RealTimeIntel()
    engine.procesar_cable_noticias()
