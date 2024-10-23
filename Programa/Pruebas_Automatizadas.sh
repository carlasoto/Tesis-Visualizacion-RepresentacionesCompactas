#!/bin/bash

# Obtener la ruta del directorio donde se encuentra el script
SCRIPT_DIR=$(dirname "$0")

# Usar directamente el comando 'python3' en lugar de solicitar la ruta del Python
PYTHON_PATH="python3"

# Solicitar la cantidad de pruebas a realizar
read -p "Cantidad de pruebas a realizar: " times

# Verificar que el número de pruebas sea válido
while ! [[ "$times" =~ ^[0-9]+$ && "$times" -gt 0 ]]
do
    echo "Inválido."
    read -p "Cantidad de pruebas a realizar: " times
done


for ((i=1; i<=times; i++))
do
   echo "Ejecución número $i"
   
   echo "Hora antes de la ejecución: $(date '+%Y-%m-%d %H:%M:%S')"

   # Ejecutar el archivo Auto_main.py ubicado en la misma carpeta que este script
   $PYTHON_PATH "$SCRIPT_DIR/Auto_main.py"

   echo "Hora después de la ejecución: $(date '+%Y-%m-%d %H:%M:%S')"
done
