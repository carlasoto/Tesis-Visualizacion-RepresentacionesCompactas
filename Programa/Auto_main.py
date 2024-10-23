from Visualizacion_ClaseIterador import graficar
from pathlib import Path
import csv

def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)

if __name__ == "__main__":
    # El directorio actual donde está el codigo
    current_dir = Path(__file__).resolve().parent

    # Rutas a los archivos y directorios
    output_csv = current_dir / '../Resultados' / 'Resultados.csv'
    prefix_path = current_dir / '../Datasets'
    listado_datasets = current_dir / 'ListadoDatasets.txt'
    graficos_dir = current_dir / '../Resultados' / 'Graficos'

    graficos_dir.mkdir(parents=True, exist_ok=True)

    def get_file_path(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]

    file_paths = get_file_path(listado_datasets)
    
    # Procesar cada archivo en la lista
    for file_name in file_paths:
        file_path = prefix_path / file_name  # Construir la ruta completa del archivo
        for codificacion in range(1, 5):
            tiempo_renderizado, tamaño_total, fig = graficar(codificacion, file_path)

            # Obtener el nombre del dataset y construir el nombre del archivo HTML
            dataset = file_path.stem  # Obtener el nombre del archivo sin extensión
            filename = graficos_dir / f"{dataset}_{codificacion}.html"
            fig.write_html(filename)  # Guardar el gráfico como HTML

            # Imprimir información de progreso
            print(f"Procesando {dataset} con codificación {codificacion}")
            print("Tiempo de creación del gráfico: ", tiempo_renderizado)
            print("Tamaño total:", tamaño_total)

            # Guardar los resultados en el archivo CSV
            data = [dataset, codificacion, tiempo_renderizado, tamaño_total]
            write_to_csv(output_csv, data)
