from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder='../www')

# Ruta para servir la interfaz web (www/index.html)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Ruta para servir archivos estáticos adicionales (CSS, JS, imágenes) si los hay
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# API de procesamiento lógico e inteligente de M82-Molina
@app.route('/api/calcular', methods=['POST'])
def calcular():
    datos = request.json
    comando = datos.get('comando', '').strip()
    
    if not comando:
        return jsonify({'status': 'error', 'message': 'Comando vacío'})
    
    partes = comando.split(' ')
    accion = partes[0].toLowerCase() if hasattr(partes[0], 'toLowerCase') else partes[0].lower()
    
    try:
        # Lógica de logística interplanetaria (Luna -> Marte)
        if accion == 'disparar':
            toneladas = float(partes[1])
            vel_escape_luna = 2380  # m/s
            masa_kg = toneladas * 1000
            energia_mj = 0.5 * masa_kg * (vel_escape_luna ** 2) / 1000000
            
            # Comparativa con gravedad terrestre
            energia_tierra_mj = 0.5 * masa_kg * (11200 ** 2) / 1000000
            ahorro = energia_tierra_mj / energia_mj
            
            respuesta = (
                f"[Cerebro Python v2.0]: Procesando dinámica orbital...\n"
                f" -> Masa crítica: {toneladas} Tons eyectadas desde base Lunar.\n"
                f" -> Energía cinética neta: {energia_mj:,.2f} MJ.\n"
                f" -> Factor de eficiencia: ¡Requiere {ahorro:.1f} veces MENOS energía que desde la Tierra!"
            )
            return jsonify({'status': 'success', 'resultado': respuesta, 'tipo': 'interplanetario', 'valor': energia_mj})

        # Lógica de recolección energética de estrellas
        elif accion == 'estelar':
            cobertura = float(partes[1])
            sol_total_yw = 384.6  # YottaWatts
            potencia_capturada = sol_total_yw * cobertura
            
            respuesta = (
                f"[Cerebro Python v2.0]: Análisis de Enjambre Estelar.\n"
                f" -> Cobertura orbital simulada: {cobertura * 100:.6f}%\n"
                f" -> Energía capturada en tiempo real: {potencia_capturada:.6f} YottaWatts.\n"
                f" -> Clasificación: Infraestructura de Escala Kardashev Tipo II."
            )
            return jsonify({'status': 'success', 'resultado': respuesta, 'tipo': 'estelar', 'valor': potencia_capturada})

        else:
            return jsonify({'status': 'error', 'message': f"Comando '{accion}' no reconocido por el sistema central."})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': f"Error en los parámetros numéricos: {str(e)}"})

if __name__ == '__main__':
    # Arranca el servidor integrado en el puerto 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
