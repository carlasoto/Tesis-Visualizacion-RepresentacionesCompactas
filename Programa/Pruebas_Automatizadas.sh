#!/bin/bash

# Obtener la ruta del directorio donde se encuentra el script
SCRIPT_DIR=$(dirname "$0")

# Solicitar al usuario la ruta del Python que desea utilizar
read -p "Ingresar ruta del ambiente Python: " PYTHON_PATH

while [ ! -x "$PYTHON_PATH" ]; do
    echo "Ruta inválida."
    read -p "Ingresar ruta del ambiente Python: " PYTHON_PATH
done

read -p "Cantidad de pruebas a realizar: " times

while ! [[ "$times" =~ ^[0-9]+$ && "$times" -gt 0 ]]
do
    echo "Inválido."
    read -p "Cantidad de puebas a realizas: " times
done

for ((i=1; i<=times; i++))
do
   echo "Ejecución número $i"
   
   echo "Hora antes de la ejecución: $(date '+%Y-%m-%d %H:%M:%S')"

   # Ejecutar el archivo Auto_main.py ubicado en la misma carpeta que este script
   $PYTHON_PATH "$SCRIPT_DIR/Auto_main.py"

   echo "Hora después de la ejecución: $(date '+%Y-%m-%d %H:%M:%S')"
done
