# Tesis - Uso de representaciones compactas en la etapa de preparación de datos de Big Time Series para su visualización 

## Requisitos

Es necesario tener instalado SDSL4py para acceder a la implementación de estructuras de datos compactas desde Python. Para ello, clone el repositorio
   
```sh
git clone git@github.com:carlasoto/Tesis-Visualizacion-RepresentacionesCompactas.git --recursive 
cd Tesis-Visualizacion-RepresentacionesCompactas/sdsl4py
```
Luego, instale SDSL4py. Como sugerencia, se recomienda crear un nuevo ambiente en Python (en este caso, llamado `sdsl4py-env`)
```sh
mkdir sdsl4py-env
python3 -m venv sdsl4py-env
source sdsl4py-env/bin/activate
pip install .
```

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

## Ejecución del Programa

1. Contar con la versión del ambiente python adaptado en alguna carpeta del sistema
2. Clonar este repositorio
3. Acceder a carpeta Implementacion/Programa
4. En caso de que se desee ejecutar el programa con algún dataset en específico, favor abrir ListadoDatasets.txt y dejar indicado en el achivo solo el/los conjunto/s que se desea (por defecto incluye todos los conjuntos de datos usados para pruebas de la tesis)
5. Desde la ruta Implementación/Programa ejecutar el archivo con:
   ```sh
    ./Pruebas_Automatizadas.sh
    ```
7. El programa consultará la ruta donde está instalado el ambiente de python adaptado y la cantidad de veces que se desea correr la ejecución por cada dataset.
8. Los resultados de cada ejecución serán almacenados en la capeta Implementacion/Resultados, la planilla excel Resultados.csv contiene los valores de tiempo y espacio, mientras que en la carpeta Implementacion/Resultados/Graficos se encuentran los gráficos resultantes de cada pueba.


## Indicación de Datasets
Para especificar los datasets que se desean probar, indicar el nombre del dataset (sin el path, solo el nombre) en el archivo ListadoDatasets.txt. Colocar un nombre de dataset por línea. Por defecto, el archivo contiene los nombres de cada uno de los datasets probados en la etapa de expeimentación de la tesis.

Los datasets se encuentran en la carpeta Datasets y hay que escribir el nombre tal como aparecen junto con su extensión.

En el caso de los archivos sobre 25MB, estos no pudieron ser cargados en este repositorio pero se encuentran en los siguientes links:
    https://we.tl/t-iIwEb2Ort2 (1hora_100hz, 2horas_100hz, 6horas_50hz, 6horas_100hz, 12horas_100hz)
    https://we.tl/t-tjuWuQIbbd (18horas_100hz)
    https://we.tl/t-g7OImal8LS (24horas_100hz)

## Resampling de un Dataset
Si se desea resamplear un nuevo dataset es necesario seguir los siguientes pasos con los archivos auxiliares:

1. Ejecutar resampling.py
2. Eliminar manualmente las líneas malas del archivo generado en paso 1. usando Ctrl+F para buscar "timestamp;;;;;;" y eliminar las líneas encontradas 
3. Ejecutar arreglarresampling.py

