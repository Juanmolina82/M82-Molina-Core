#!/bin/bash
echo -e "\033[1;33m[M82 GATEWAY]: Verificando puertos activos en el Core...\033[0m"

# 1. Rastrear el socket 8080 usando netstat de forma compatible con Termux
PID_ACTIVO=$(netstat -tulnp 2>/dev/null | grep :8080 | awk '{print $7}' | cut -d'/' -f1)

if [ ! -z "$PID_ACTIVO" ]; then
    echo -e "\033[1;31m[AVISO]: Detectada instancia previa ejecutándose en el PID: $PID_ACTIVO. Liberando puerto de forma segura...\033[0m"
    kill -9 $PID_ACTIVO
    sleep 1
else
    echo -e "\033[1;32m[OK]: El puerto 8080 está limpio y listo para transmisión.\033[0m"
fi

# 2. Asegurar el Wake-Lock para evitar suspensiones del dispositivo móvil
termux-wake-lock

# 3. Lanzar el motor con los parámetros por defecto de Refinitiv
echo -e "\033[1;34m[M82 ENGINE]: Inicializando www.molina82.com de manera limpia...\033[0m"
python3 m82_robust_platform.py 95.10 91.00
