# -*- coding: utf-8 -*-
"""
================================================================================
       M82 MACRO INTELLIGENCE - ATLANTIC FFO FLOWS & ARBITRAJE V16.0
     Sovereign-Grade Governance: Cash Flow Generation & Atlantic Infrastructure
================================================================================
"""
import sys
import json
import requests

class M82AtlanticCashFlows(object):
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "gemma2:2b"
        
        # PARAMETRIZACIÓN DEL EJE ATLÁNTICO (MONITOREO DE ACTIVOS TANGIBLES)
        self.brent_base = 93.11
        self.guyana_fcf_yield = 18.5       # Porcentaje de Free Cash Flow Yield promedio
        self.argentina_shale_growth = 12.0 # Tasa de crecimiento operativa en infraestructura base
        
        # MÉTRICAS DE VALORACIÓN VS CRECIMIENTO
        self.ev_ebitda_target = 4.2        # Múltiplo objetivo de entrada para activos Midstream

    def evaluar_flujos_atlantico(self):
        print("\n" + "🏛️  " + "="*75)
        print(" [M82 INFRASTRUCTURE V16.0] — ATLANTIC AXIS CASH FLOW RUNTIME")
        print("="*79)
        print(f"🛢️  Brent Reference    : ${self.brent_base} USD/Bbl")
        print(f"🇬🇾  Guyana Asset Yield : {self.guyana_fcf_yield}% Free Cash Flow Yield (Premium)")
        print(f"🇦🇷  Argentina Growth   : +{self.argentina_shale_growth}% en Infraestructura Logística")
        print(f"📊 EV/EBITDA Target    : {self.ev_ebitda_target}x (Foco exclusivo en Control Layer)")
        print("-" * 79)

        contexto_flows = (
            f"Con el Brent a ${self.brent_base}, las operaciones del Eje Atlantico (Guyana/Argentina) "
            f"estan generando un FCF Yield del {self.guyana_fcf_yield}%. La disciplina de capital de las Majors "
            f"dirige el flujo monetario a estos hubs eficientes con un EV/EBITDA de {self.ev_ebitda_target}x. "
            f"Determina la estrategia de captura de rendimiento para el libro de Molina Holdings."
        )

        payload = {
            "model": self.model_name,
            "prompt": f"[M82 ATLANTIC CORE]\nContexto: {contexto_flows}\nDictamen de Asignación FFO:",
            "stream": False
        }

        try:
            res = requests.post(self.ollama_url, json=payload, timeout=25)
            print(f"🧠 DICTAMEN DE INTELIGENCIA SOBERANA (Gemma 2):\n{res.json().get('response', '').strip()}")
        except Exception:
            print("🛡️ [STANDALONE MODE] Procesador cognitivo resguardado.")
            print("   >> DIRECTIVA: El FFO del Eje Atlántico es inmune al riesgo de transporte de Oriente Medio.")
            print("   >> ACCIÓN: Priorizar contratos de transporte de volumen (Take-or-Pay) indexados a inflación.")
        print("="*79)

if __name__ == "__main__":
    engine = M82AtlanticCashFlows()
    engine.evaluar_flujos_atlantico()
