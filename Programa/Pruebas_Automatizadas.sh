#!/bin/bash

CURRENT_DIR=$(pwd)

#Modificar aqui por la versión local que se tenga del ambiente de python de Irri
PYTHON_PATH="/home/casoto/tesis/pysdsl/./envPython/python/install/bin/python3"

# Número de veces a ejecutar el script
times=5

for ((i=1; i<=times; i++))
do
   echo "Ejecución número $i"
   
   echo "Hora antes de la ejecución: $(date '+%Y-%m-%d %H:%M:%S')"

   $PYTHON_PATH "$CURRENT_DIR/Auto_main.py"

   echo "Hora después de la ejecución: $(date '+%Y-%m-%d %H:%M:%S')"
done
