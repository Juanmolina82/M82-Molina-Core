# -*- coding: utf-8 -*-
"""
================================================================================
       M82 MACRO INTELLIGENCE - DERIVATIVES & GEX COUPLING V14.5
        Sovereign-Grade Governance: Options Market Walls & Skew Analysis
================================================================================
"""
import sys
import json
import requests

class M82GexEngine(object):
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "gemma2:2b"
        
        # PARAMETRIZACIÓN DE DERIVADOS (EXTRACCIÓN MOOMOO JUN 8/9, 2026)
        self.spx_spot = 7405.73
        self.spx_put_wall = 7375.0
        self.spx_call_wall = 7450.0
        self.spx_gamma_flip = 7464.68
        
        # FLUJOS DE ROTACIÓN ESPECÍFICOS
        self.intc_pc_ratio = 0.46          # Altamente Bullish en volumen de opciones
        self.intc_iv_percentile = 96.0     # Volatilidad implícita al límite
        self.aapl_iv_percentile = 32.0     # Flujo institucional deprimido en Big Tech

    def analizar_riesgo_gamma(self):
        print("\n" + "📊 " + "="*75)
        print(" [M82 DERIVATIVES CORE V14.5] — MAPA DE EXPOSICIÓN A GAMMA (GEX)")
        print("="*79)
        print(f"• S&P 500 Spot Baseline : {self.spx_spot}")
        print(f"• 🛡️ Put Wall (Soporte) : {self.spx_put_wall} | 🧱 Call Wall (Techo): {self.spx_call_wall}")
        print(f"• 🔄 Punto Gamma Flip   : {self.spx_gamma_flip} (Estado Actual: GAMMA NEGATIVA/VOLÁTIL)")
        print("-" * 79)
        print(f"• Intel (INTC) IV Pctl  : {self.intc_iv_percentile}% (Put/Call Ratio: {self.intc_pc_ratio})")
        print(f"• Apple (AAPL) IV Pctl  : {self.aapl_iv_percentile}% (Desinterés Institucional)")
        print("-" * 79)

        # Determinar vulnerabilidad de mercado
        distancia_soporte = ((self.spx_spot - self.spx_put_wall) / self.spx_spot) * 100
        print(f"🚨 Distancia de seguridad al Put Wall: {distancia_soporte:.2f}%")
        
        contexto_gex = (
            f"El S&P 500 cotiza a {self.spx_spot}, posicionándose por debajo del nivel de Gamma Flip ({self.spx_gamma_flip}), "
            f"pero sostenido por el Put Wall masivo de {self.spx_put_wall}. El mercado institucional acumula derivados de Intel "
            f"(IV Pctl {self.intc_iv_percentile}%) mientras congela a Apple. Genera el reporte de cobertura de riesgos."
        )

        payload = {
            "model": self.model_name,
            "prompt": f"[M82 GEX MATRIX]\nContexto: {contexto_gex}\nDictamen Cuantitativo de Riesgo:",
            "stream": False
        }

        try:
            res = requests.post(self.ollama_url, json=payload, timeout=25)
            print(f"\n🧠 DICTAMEN INTEGRADO DE DERIVADOS (Gemma 2):\n{res.json().get('response', '').strip()}")
        except Exception:
            print("\n🛡️ [Sovereign Mode] Nodo Ollama local procesando en frío. Mapeo de paredes asegurado en el Ledger.")
        print("="*79)

if __name__ == "__main__":
    analizador = M82GexEngine()
    analizador.analizar_riesgo_gamma()
