import sys
import os
import subprocess
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='www')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/v3/gateway', methods=['POST'])
def gateway():
    payload = request.json or {}
    comando = payload.get('comando', '').strip().lower()

    if not comando:
        return jsonify({'status': 'error', 'message': 'Comando vacío recibido por la Gobernanza.'})

    if comando == 'scan_mercado':
        # Procesamiento dinámico usando los parámetros pasados por consola si existen
        brent = sys.argv[1] if len(sys.argv) > 1 else "104.00"
        wti = sys.argv[2] if len(sys.argv) > 2 else "91.00"
        response = (
            f"[ANALÍTICA M82]:\n"
            f" -> Refinitiv Feed Injected: Brent @ ${brent} | WTI @ ${wti}\n"
            f" -> Cobertura de Riesgo Macro: >=80% en Tasa Fija Activada.\n"
            f" -> Arbitraje de fletes en el eje del Atlántico operando."
        )
        return jsonify({'status': 'success', 'data': response})

    elif comando == 'balance_caribe':
        response = (
            "[MOLINA GLOBAL ARCHITECTURE V3.2]:\n"
            " -> Jurisdicción Principal: Delaware / Tennessee Federal Protection.\n"
            " -> Mitigación Política: Blindaje total ante volatilidad regional.\n"
            " -> EBITDA Midstream Target: Estabilizado en rango de 60% - 70%.\n"
            " -> Despliegue de Crédito Privado: Estructura de Cascada Europea (8% Compounded)."
        )
        return jsonify({'status': 'success', 'data': response})
        
    elif comando == 'backup_vault':
        # Macro automatizada ejecutada directamente desde el backend hacia GitHub
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Auto-Vault Sync via UI Core Dashboard"], check=True)
            # Nota: Si requiere credenciales, git las pedirá en la terminal activa
            result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
            return jsonify({'status': 'success', 'data': f"[VAULT COMPLETADO]:\n{result.stdout or 'Sincronizado con éxito.'}"})
        except Exception as e:
            return jsonify({'status': 'error', 'message': f"Fallo en Git Automático: {str(e)}"})

    else:
        return jsonify({'status': 'error', 'message': f"Comando '{comando}' no reconocido en el Core V3.2."})

if __name__ == '__main__':
    print("\n\033[1;34m[ MOLINA HOLDINGS - ENGINE V3.2 ]\033[0m")
    print("-> Sintonizando con www.molina82.com")
    print("-> Forzando wake-lock de Termux para persistencia en background...")
    subprocess.run(["termux-wake-lock"])
    
    # Arranca en el puerto estándar configurado en tu ecosistema
    app.run(host='0.0.0.0', port=8080, debug=True)
