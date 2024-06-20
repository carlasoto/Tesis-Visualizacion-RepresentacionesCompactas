import pandas as pd


# Cargar datos
df = pd.read_csv('/home/carla/Documentos/Tesis/Py/Datasets/Nuevo/6horas.txt', delimiter=';', header=None)

# Convertir la primera columna a datetime
df[0] = pd.to_datetime(df[0], format='%Y%m%d%H%M%S%f')

# Establecer la primera columna como el índice
df.set_index(0, inplace=True)

# Remuestreo a 10 Hz y cálculo del promedio
df_resampled = df.resample('20L').mean() #50hz20L #10hz100L

df_resampled.iloc[:, 1:16] = df_resampled.iloc[:, 1:16].applymap(lambda x: format(x, ".3f")).astype(float)


# Reindexar el DataFrame (esto convierte el índice de datetime a una columna regular)
df_resampled.reset_index(inplace=True)

# Reconversión a timestamp original
df_resampled[0] = df_resampled[0].dt.strftime('%Y%m%d%H%M%S%f').str[:-3]

# Guardar el DataFrame remuestreado en un nuevo archivo CSV
df_resampled.to_csv('/home/carla/Documentos/Tesis/Py/Datasets/Nuevo/6horas_50hz.txt', sep=';', header=False, index=False)
