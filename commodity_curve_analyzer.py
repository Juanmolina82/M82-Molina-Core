# -*- coding: utf-8 -*-
"""
================================================================================
            M82 GLOBAL INTELLIGENCE - COMMODITY CURVE ANALYZER V1.0
          Sovereign-Grade Analytics: Contango vs Backwardation Engine
================================================================================
"""
import sys
import json
import requests

class M82CurveAnalyzer(object):
    def __init__(self, spot_wti=95.42, future_6m_wti=89.20):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "gemma2:2b"
        
        # ASIGNACIÓN DE CONTRATOS (Simulación de Ingesta en Tiempo Real)
        self.front_month_wti = spot_wti       # Precio actual / Mes más cercano
        self.next_6m_wti = future_6m_wti      # Precio pactado a 6 meses vista
        
    def calcular_estructura_mercado(self):
        print("\n" + "🛢️  " + "="*75)
        print(" [M82 QUANT] ANALIZADOR TÁCTICO DE LA CURVA DE FUTUROS (WTI)")
        print("="*77)
        print(f"• Contrato Front-Month (M1) : ${self.front_month_wti} USD/Bbl")
        print(f"• Contrato Forward (M6)     : ${self.next_6m_wti} USD/Bbl")
        
        # Cálculo del Spread Matemático
        spread = self.next_6m_wti - self.front_month_wti
        print(f"• Spread Neto (M6 - M1)     : ${spread:.2f} USD")
        print("-" * 77)

        # Lógica de Clasificación Estructural
        if spread > 0:
            estructura = "CONTANGO"
            detalle = "El mercado futuro es más caro. Incentivo para almacenar crudo físico y comprar coberturas cortas."
        elif spread < 0:
            estructura = "BACKWARDATION"
            detalle = "El mercado actual exige entrega inmediata. Alta prima geopolítica. Escasez crítica en los terminales."
        else:
            estructura = "MERCADO PLANO"
            detalle = "Equilibrio transicional de oferta y demanda."

        print(f"🚨 CAPA ENERGÉTICA ESTRUCTURAL: {estructura}")
        print(f"ℹ️  Diagnóstico Factual       : {detalle}")
        print("-" * 77)

        # Consultar Directiva Estratégica al Cerebro Local
        contexto = (
            f"La curva del crudo WTI se encuentra en un estado de {estructura} con un spread de {spread:.2f} USD. "
            f"El precio spot está anclado en ${self.front_month_wti} USD. Determina la acción inmediata "
            f"para la asignación de flujos de caja en Molina Holdings LLC."
        )

        payload = {
            "model": self.model_name,
            "prompt": f"[M82 CURVE LOGIC]\n{contexto}\nDictamen de Asignación Física:",
            "stream": False
        }

        try:
            res = requests.post(self.ollama_url, json=payload, timeout=20)
            print(f"\n🧠 DICTAMEN DE INFERENCIA SOBERANA (Gemma 2):\n   {res.json().get('response', '').strip()}")
        except Exception:
            print("\n🛡️ [CONTINGENCIA ACTIVA] Nodo Ollama offline. Aplicando regla mnemónica por defecto:")
            if estructura == "BACKWARDATION":
                print("   >> ACCIÓN: Acelerar despachos hacia refinerías aliadas en Texas. Maximizar caja spot instantánea.")
            else:
                print("   >> ACCIÓN: Almacenar existencias en depósitos estratégicos. Proteger inventario base.")
        print("="*77)

if __name__ == "__main__":
    # Permite inyectar los precios por consola: python script.py [Spot] [Futuro6M]
    spot_in = float(sys.argv[1]) if len(sys.argv) > 1 else 95.42
    future_in = float(sys.argv[2]) if len(sys.argv) > 2 else 89.20
    
    analyzer = M82CurveAnalyzer(spot_wti=spot_in, future_6m_wti=future_in)
    analyzer.calcular_estructura_mercado()
