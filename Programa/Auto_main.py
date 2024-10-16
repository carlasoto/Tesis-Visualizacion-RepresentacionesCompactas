from Visualizacion_ClaseIterador import graficar
from pathlib import Path
import csv

def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)

if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    output_csv = current_dir / 'Resultados' / 'Resultados.csv'
    prefix_path = current_dir / '../Datasets'
    listado_datasets = current_dir / 'ListadoDatasets.txt'
    graficos_dir = current_dir / 'Resultados' / 'Graficos'

    def get_file_path(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]

    file_paths = get_file_path(listado_datasets)
    
    for file_path in file_paths:
        file_path = str(prefix_path) + "/" + file_path
        for codificacion in range(1, 5):
            tiempo_renderizado, tamaño_total, fig = graficar(codificacion, file_path)

            dataset = file_path.split('/')[-1].replace('.txt', '')
            filename = graficos_dir / f"{dataset}_{codificacion}.html"
            fig.write_html(filename)

            print(f"Procesando {dataset} con codificación {codificacion}")
            print("Tiempo de creación del gráfico: ", tiempo_renderizado)
            print("Tamaño total:", tamaño_total)

            data = [dataset, codificacion, tiempo_renderizado, tamaño_total]
            write_to_csv(output_csv, data)

