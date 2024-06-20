#!/bin/bash

# Ruta relativa al Python personalizado
CURRENT_DIR=$(pwd)
# Solo necesitas subir un nivel para llegar a /home/casoto/tesis desde /home/casoto/tesis/Implementacion-PA/Programa
PYTHON_PATH="/home/casoto/tesis/pysdsl/./envPython/python/install/bin/python3"

# Número de veces que deseas ejecutar el script
times=5

for ((i=1; i<=times; i++))
do
   echo "Ejecución número $i"
   
   # Imprimir la hora actual antes de la ejecución
   echo "Hora antes de la ejecución: $(date '+%Y-%m-%d %H:%M:%S')"

   $PYTHON_PATH "/home/casoto/tesis/Implementacion-PA/Programa/Auto_main.py"

   # Imprimir la hora actual después de la ejecución
   echo "Hora después de la ejecución: $(date '+%Y-%m-%d %H:%M:%S')"
done
