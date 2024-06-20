import pandas as pd
from pathlib import Path

current_dir = Path(__file__).resolve().parent

# Indicar el nombre del archivo a resamplear
input_file = current_dir / 'Datasets' / '6horas.txt'
# Indicar nombre según la versión del resampleo (50 o 10 Hz)
output_file = current_dir / 'Datasets' / '6horas_50hz.txt'

df = pd.read_csv(input_file, delimiter=';', header=None)

# Convertir la primera columna a datetime
df[0] = pd.to_datetime(df[0], format='%Y%m%d%H%M%S%f')

df.set_index(0, inplace=True)

# Selección de frecuencia para remuestreo
# Para 50Hz: 20L
# Para 10Hz: 100L
df_resampled = df.resample('20L').mean()  

df_resampled.iloc[:, 1:16] = df_resampled.iloc[:, 1:16].applymap(lambda x: format(x, ".3f")).astype(float)

df_resampled.reset_index(inplace=True)

# Reconversión a timestamp original
df_resampled[0] = df_resampled[0].dt.strftime('%Y%m%d%H%M%S%f').str[:-3]

df_resampled.to_csv(output_file, sep=';', header=False, index=False)
