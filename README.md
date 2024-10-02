# Tesis - Uso de representaciones compactas en la etapa de preparación de datos de Big Time Series para su visualización 

## Requisitos

Es necesario tener la versión adaptada de Python para que `pysdsl` funcione correctamente. 

## Estructura de Carpetas

Este proyecto está adaptado para usar con la siguiente estructura de carpetas del repositorio:
``````
Implementacion/
│
├── Programa/
│ ├── Pruebas_Automatizadas.sh
│ ├── Auto_main.py
│ └── ListadoDatasets.txt
├── Datasets/
└── Resultados/
├── Resultados.csv
└── Graficos/
``````


## Modificación de la Ruta de Python

Hay que modificar la ruta de la versión de Python adaptada en el archivo `Pruebas_Automatizadas.sh` para que apunte a la ubicación correcta del entorno.

Abrir `Pruebas_Automatizadas.sh` y modificar la siguiente línea:
```sh
PYTHON_PATH="/ruta/a/python/adaptado/python3"
```

## Ejecución del Programa

Para ejecutar el programa, utilizar el siguiente comando en la terminal:

```sh
./Pruebas_Automatizadas.sh
```

## Indicación de Datasets
Para especificar los datasets que se desean probar, indicar el nombre del dataset (sin el path, solo el nombre) en el archivo ListadoDatasets.txt. Colocar un nombre de dataset por línea.

Los datasets se encuentran en la carpeta Datasets y hay que escribir el nombre tal como aparecen junto con su extensión.

En el caso de los archivos sobre 25MB, estos no pudieron ser cargados en este repositorio pero se encuentran en los siguientes links:
    https://we.tl/t-iIwEb2Ort2  
        - 1hora_100hz
        - 2horas_100hz
        - 6horas_50hz
        - 6horas_100hz
        - 12horas_100hz
    https://we.tl/t-tjuWuQIbbd 
        - 18horas_100hz
    https://we.tl/t-g7OImal8LS
        - 24horas_100hz

## Resampling de un Dataset
Si se desea resamplear un dataset es necesario seguir los siguientes pasos con los archivos auxiliares:

1. Ejecutar resampling.py
2. Eliminar manualmente las líneas malas del archivo generado en paso 1. usando Ctrl+F para buscar "timestamp;;;;;;" y eliminar las líneas encontradas 
3. Ejecutar arreglarresampling.py

