import sys
import os
import subprocess

def ejecutar_en_musculo(comando_sistema):
    """Ejecuta comandos nativos del sistema (el músculo) desde el cerebro."""
    try:
        resultado = subprocess.run(
            comando_sistema, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if resultado.returncode == 0:
            return resultado.stdout.strip()
        else:
            return f"Error en músculo: {resultado.stderr.strip()}"
    except Exception as e:
        return f"Fallo crítico de hardware: {str(e)}"

def procesar_comando(comando):
    cmd = comando.strip().lower()
    
    if cmd == "salir":
        print("\n[+] Apagando de forma segura el ecosistema M82-Molina...")
        sys.exit(0)
        
    elif cmd == "status":
        print("\n--- ESTADO DEL SÚPER-SISTEMA ---")
        print("[Cerebro - Python]: Operativo y estable.")
        # Usamos el músculo para validar quién es el usuario en el móvil
        usuario = ejecutar_en_musculo("whoami")
        print(f"[Músculo - Sistema]: Conexión NATIVA activa (Usuario: {usuario}).")
        print("-" * 32)
        
    elif cmd == "ayuda":
        print("\nComandos de la Plataforma:")
        print("  status  : Muestra el estado real de los módulos unificados.")
        print("  sistema : Ejecuta un comando directo en el móvil (Ej: sistema ls).")
        print("  ayuda   : Muestra este menú.")
        print("  salir   : Cierra la plataforma.")
        
    elif cmd.startswith("sistema "):
        # Extrae el comando nativo después de la palabra 'sistema '
        cmd_nativo = comando[8:]
        print(f"\n[Cerebro] Enviando orden al Músculo: '{cmd_nativo}'...")
        salida = ejecutar_en_musculo(cmd_nativo)
        print(f"\n--- RESPUESTA DEL MÚSCULO ---\n{salida}\n----------------------------")
        
    else:
        print(f"\n[Cerebro]: Analizando '{comando}'... Comando no reconocido por los módulos.")

def iniciar_sistema():
    print("=" * 50)
    print("      SISTEMA UNIFICADO M82 - MOLINA IA v1.1      ")
    print("=" * 50)
    print("[+] Inicializando el Cerebro (MOLINA IA)...")
    print("[+] Conectando e indexando el Músculo (M82)...")
    print("[Sistema]: Ecosistema enlazado. Escribe 'ayuda' o 'salir'.\n")
    
    while True:
        try:
            orden = input("M82-Molina > ")
            if orden.strip():
                procesar_comando(orden)
        except (KeyboardInterrupt, EOFError):
            print("\n\n[+] Apagado forzado. Desconectando módulos.")
            break

if __name__ == "__main__":
    iniciar_sistema()
