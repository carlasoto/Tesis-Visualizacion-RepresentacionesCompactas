import pysdsl
from datetime import datetime, timedelta
import pandas as pd
import tempfile
import time
import numpy as np
import os
import sys


def deshacer_transformacion(numero_transformado):
        if numero_transformado % 2 == 0:
            return numero_transformado // 2
        else:
            return -(numero_transformado + 1) // 2
def transformar_numero(numero):
        if numero >= 0:
            return 2 * numero
        else:
            return -2 * numero - 1

def preparacion_data(codificacion,file_path):
    
    nombre_dataset = file_path
    print(nombre_dataset)

    tiempo_preparacion_inicio = time.time()

    if codificacion == 1:
        vec_type = pysdsl.IntVector
        int_type = pysdsl.VariableLengthCodesVectorEliasGamma
        dec_type = pysdsl.DirectAccessibleCodesVector4
        timestamp_type = pysdsl.EncVectorEliasGamma
    elif codificacion == 2:
        vec_type = pysdsl.IntVector
        int_type = pysdsl.DirectAccessibleCodesVector4
        dec_type = pysdsl.DirectAccessibleCodesVector4
        timestamp_type = pysdsl.EncVectorEliasGamma
    elif codificacion == 3:
        vec_type = np.array
        timestamp_type = pysdsl.EncVectorEliasGamma
    elif codificacion == 4:
        vec_type = np.array
        timestamp_type = np.array
    elif codificacion == 5:
        vec_type = []
        timestamp_type = pysdsl.EncVectorEliasGamma

    n_vector = 1
    cant_lineas = 0
    timestamps = []
    vector_sensores_nl = []
    vector_partes_enteras = []
    vector_partes_decimales = []

    for i in range(1, 17):
        globals()[f'int_part_{i}'] = []
        globals()[f'dec_part_{i}'] = []

    with open(nombre_dataset, "r") as archivo:
        lineas = archivo.readlines()

    def procesar_lineas_numpy_con_timestamps(lineas, numpy_arrays=None):
        if numpy_arrays is None:
            numpy_arrays = [np.array([]) for _ in range(16)]
        
        timestamps = np.array([])
        cant_lineas = 0

        for line in lineas:
            values = line.strip().split(";")
            timestamp = int(values[0])
            timestamps = np.append(timestamps, float(timestamp))
            
            for i, value in enumerate(values[1:]):
                if len(value) <= 8:
                    numpy_arrays[i] = np.append(numpy_arrays[i], float(value))
            
            cant_lineas += 1 

        return timestamps, cant_lineas, numpy_arrays

    def procesar_lineas_listas_con_timestamps(lineas, listas=None):
        if listas is None:
            listas = [[] for _ in range(16)]
        
        timestamps = []
        cant_lineas = 0

        for line in lineas:
            values = line.strip().split(";")
            timestamp = int(values[0])
            timestamps.append(float(timestamp))
            
            for i, value in enumerate(values[1:]):
                if len(value) <= 8:
                    listas[i].append(float(value))            
            cant_lineas += 1 
        return timestamps, cant_lineas, listas
    
    def procesar_lineas_numpy_timestamps_edc(lineas, numpy_arrays=None):
        if numpy_arrays is None:
            numpy_arrays = [np.array([]) for _ in range(16)]
        
        timestamps = []
        cant_lineas = 0

        for line in lineas:
            values = line.strip().split(";")
            timestamp = int(values[0])
            timestamps.append(timestamp)            
            
            for i, value in enumerate(values[1:]):
                if len(value) <= 8:
                    numpy_arrays[i] = np.append(numpy_arrays[i], float(value))
            
            cant_lineas += 1 

        return timestamps, cant_lineas, numpy_arrays

    def procesar_lineas(lineas, transformar_numero):
        global int_part_1, dec_part_1, int_part_2, dec_part_2, int_part_3, dec_part_3, int_part_4, dec_part_4, int_part_5, dec_part_5, int_part_6, dec_part_6, int_part_7, dec_part_7, int_part_8, dec_part_8, int_part_9, dec_part_9, int_part_10, dec_part_10, int_part_11, dec_part_11, int_part_12, dec_part_12, int_part_13, dec_part_13, int_part_14, dec_part_14, int_part_15, dec_part_15, int_part_16, dec_part_16
        int_s = 0
        dec_s = 0
        timestamps = []
        n_vector = 1
        cant_lineas = 0

        for line in lineas:
            values = line.strip().split(";")
            timestamp = int(values[0])
            timestamps.append(timestamp)
            for value in values[1:]:
                if len(value) <= 2:
                    int_s = int(value)
                    if int_s < 0: 
                        int_s = transformar_numero(int_s) #caso -3
                else:
                    pos = value.find(".")
                    parte_ent = value[:pos]
                    parte_dec = value[pos+1:]
                    if len(parte_dec)==1:
                        parte_dec = parte_dec + "00"
                    elif len(parte_dec)==2:
                        parte_dec = parte_dec + "0"

                    parte1 = int(parte_ent) 
                    parte2 = int(parte_dec)

                    if parte1 < 0:
                        parte1 = -parte1
                        parte2 = -parte2
                    elif parte1 == 0 and parte_ent.startswith('-'):
                        parte1 = 0
                        parte2 = -parte2

                    int_s = parte1
                    dec_s = transformar_numero(parte2)

                if len(value) > 8: 
                    del value
                else:
                    if n_vector == 1:
                        if len(value) <= 2:
                            int_part_1.append(int_s)
                            dec_part_1.append(0)
                        else:
                            int_part_1.append(int_s)
                            dec_part_1.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 2:
                        if len(value) <= 2:
                            int_part_2.append(int_s)
                            dec_part_2.append(0)
                        else:
                            int_part_2.append(int_s)
                            dec_part_2.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 3:
                        if len(value) <= 2:
                            int_part_3.append(int_s)
                            dec_part_3.append(0)
                        else:
                            int_part_3.append(int_s)
                            dec_part_3.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 4:
                        if len(value) <= 2:
                            int_part_4.append(int_s)
                            dec_part_4.append(0)
                        else:
                            int_part_4.append(int_s)
                            dec_part_4.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 5:
                        if len(value) <= 2:
                            int_part_5.append(int_s)
                            dec_part_5.append(0)
                        else:
                            int_part_5.append(int_s)
                            dec_part_5.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 6:
                        if len(value) <= 2:
                            int_part_6.append(int_s)
                            dec_part_6.append(0)
                            del value
                        else:
                            int_part_6.append(int_s)
                            dec_part_6.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 7:
                        if len(value) <= 2:
                            int_part_7.append(int_s)
                            dec_part_7.append(0)
                        else:
                            int_part_7.append(int_s)
                            dec_part_7.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 8:
                        if len(value) <= 2:
                            int_part_8.append(int_s)
                            dec_part_8.append(0)
                        else:
                            int_part_8.append(int_s)
                            dec_part_8.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 9:
                        if len(value) <= 2:
                            int_part_9.append(int_s)
                            dec_part_9.append(0)
                        else:
                            int_part_9.append(int_s)
                            dec_part_9.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 10:
                        if len(value) <= 2:
                            int_part_10.append(int_s)
                            dec_part_10.append(0)
                        else:
                            int_part_10.append(int_s)
                            dec_part_10.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 11:
                        if len(value) <= 2:
                            int_part_11.append(int_s)
                            dec_part_11.append(0)
                        else:
                            int_part_11.append(int_s)
                            dec_part_11.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 12:
                        if len(value) <= 2:
                            int_part_12.append(int_s)
                            dec_part_12.append(0)
                        else:
                            int_part_12.append(int_s)
                            dec_part_12.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 13:
                        if len(value) <= 2:
                            int_part_13.append(int_s)
                            dec_part_13.append(0)
                        else:
                            int_part_13.append(int_s)
                            dec_part_13.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 14:
                        if len(value) <= 2:
                            int_part_14.append(int_s)
                            dec_part_14.append(0)
                        else:
                            int_part_14.append(int_s)
                            dec_part_14.append(int(dec_s))
                        n_vector += 1
                    elif n_vector == 15:
                        if len(value) <= 2:
                            int_part_15.append(int_s)
                            dec_part_15.append(0)
                        else:
                            int_part_15.append(int_s)
                            dec_part_15.append(int(dec_s))
                        n_vector += 1
                    else:
                        if len(value) <= 2:
                            int_part_16.append(int_s)
                            dec_part_16.append(0)
                        else:
                            int_part_16.append(int_s)
                            dec_part_16.append(int(dec_s))
            n_vector = 1
            cant_lineas += 1
        
        return timestamps, cant_lineas

    if codificacion == 3:
        timestamps, cant_lineas, numpy_arrays = procesar_lineas_numpy_timestamps_edc(lineas)
        numpy_1, numpy_2, numpy_3, numpy_4, numpy_5, numpy_6, numpy_7, numpy_8, numpy_9, numpy_10, numpy_11, numpy_12, numpy_13, numpy_14, numpy_15, numpy_16 = numpy_arrays
        sdsl_timestamps= pysdsl.IntVector(timestamps)
        tam_original_timestamps = sdsl_timestamps.size_in_mega_bytes
        timestamps.clear()
        timestamps = timestamp_type(sdsl_timestamps)
        compact_tam_ts = timestamps.size_in_mega_bytes
    elif codificacion == 4:
        timestamps, cant_lineas, numpy_arrays = procesar_lineas_numpy_con_timestamps(lineas)
        numpy_1, numpy_2, numpy_3, numpy_4, numpy_5, numpy_6, numpy_7, numpy_8, numpy_9, numpy_10, numpy_11, numpy_12, numpy_13, numpy_14, numpy_15, numpy_16 = numpy_arrays
        tam_original_timestamps = timestamps.nbytes / (1024 * 1024)
    elif codificacion == 5:
        timestamps, cant_lineas, listas = procesar_lineas_listas_con_timestamps(lineas)
        lista_1, lista_2, lista_3, lista_4, lista_5, lista_6, lista_7, lista_8, lista_9, lista_10, lista_11, lista_12, lista_13, lista_14, lista_15, lista_16 = listas
        sdsl_timestamps= pysdsl.IntVector(timestamps)
        tam_original_timestamps = sdsl_timestamps.size_in_mega_bytes
        timestamps.clear()
        timestamps = timestamp_type(sdsl_timestamps)
        compact_tam_ts = timestamps.size_in_mega_bytes
    else:
        timestamps, cant_lineas = procesar_lineas(lineas, transformar_numero)
        sdsl_timestamps= pysdsl.IntVector(timestamps)
        tam_original_timestamps = sdsl_timestamps.size_in_mega_bytes
        timestamps = timestamp_type(sdsl_timestamps) 
        compact_tam_ts = timestamps.size_in_mega_bytes

    cant_datos = cant_lineas*16
    print()
    #print("Cantidad de lineas: ", cant_lineas)

    ##### MANEJO DE TIMESTAMPS
    '''
    sdsl_timestamps= pysdsl.IntVector(timestamps)
    tam_original_timestamps = sdsl_timestamps.size_in_mega_bytes
    #print("OG TS = ",tam_original_timestamps)
    compact_ts = timestamp_type(sdsl_timestamps)
    compact_tam_ts = compact_ts.size_in_mega_bytes
    #print("COMPACT TS = ",compact_tam_ts)
    '''

    sdsl_int_1 = vec_type(int_part_1)  
    sdsl_dec_1 = vec_type(dec_part_1)
    sdsl_int_2 = vec_type(int_part_2)
    sdsl_dec_2 = vec_type(dec_part_2)
    sdsl_int_3 = vec_type(int_part_3)
    sdsl_dec_3 = vec_type(dec_part_3)
    sdsl_int_4 = vec_type(int_part_4)
    sdsl_dec_4 = vec_type(dec_part_4)
    sdsl_int_5 = vec_type(int_part_5)
    sdsl_dec_5 = vec_type(dec_part_5)
    sdsl_int_6 = vec_type(int_part_6)
    sdsl_dec_6 = vec_type(dec_part_6)
    sdsl_int_7 = vec_type(int_part_7)
    sdsl_dec_7 = vec_type(dec_part_7)
    sdsl_int_8 = vec_type(int_part_8)
    sdsl_dec_8 = vec_type(dec_part_8)
    sdsl_int_9 = vec_type(int_part_9)
    sdsl_dec_9 = vec_type(dec_part_9)
    sdsl_int_10 = vec_type(int_part_10)
    sdsl_dec_10 = vec_type(dec_part_10)
    sdsl_int_11 = vec_type(int_part_11)
    sdsl_dec_11 = vec_type(dec_part_11)
    sdsl_int_12 = vec_type(int_part_12)
    sdsl_dec_12 = vec_type(dec_part_12)
    sdsl_int_13 = vec_type(int_part_13)
    sdsl_dec_13 = vec_type(dec_part_13)
    sdsl_int_14 = vec_type(int_part_14)
    sdsl_dec_14 = vec_type(dec_part_14)
    sdsl_int_15 = vec_type(int_part_15)
    sdsl_dec_15 = vec_type(dec_part_15)
    sdsl_int_16 = vec_type(int_part_16)
    sdsl_dec_16 = vec_type(dec_part_16)
    '''
    Imprimir todos los vectores 1 al 16
    for i in range(1, 17):
        sdsl_int = i
        sdsl_dec = i
        exec(f"print(sdsl_int_{i})")
        exec(f"print(sdsl_dec_{i})")
    ''' 
    
    #### CODIFICACION PYSDSL
    if codificacion == 1 or codificacion == 2:
        tam_original_sensores_int = sdsl_int_1.size_in_mega_bytes + sdsl_int_2.size_in_mega_bytes + sdsl_int_3.size_in_mega_bytes + sdsl_int_4.size_in_mega_bytes + sdsl_int_5.size_in_mega_bytes + sdsl_int_6.size_in_mega_bytes + sdsl_int_7.size_in_mega_bytes + sdsl_int_8.size_in_mega_bytes + sdsl_int_9.size_in_mega_bytes + sdsl_int_10.size_in_mega_bytes + sdsl_int_11.size_in_mega_bytes + sdsl_int_12.size_in_mega_bytes + sdsl_int_13.size_in_mega_bytes + sdsl_int_14.size_in_mega_bytes + sdsl_int_15.size_in_mega_bytes + sdsl_int_16.size_in_mega_bytes
        tam_original_sensores_dec = sdsl_dec_1.size_in_mega_bytes + sdsl_dec_2.size_in_mega_bytes + sdsl_dec_3.size_in_mega_bytes + sdsl_dec_4.size_in_mega_bytes + sdsl_dec_5.size_in_mega_bytes + sdsl_dec_6.size_in_mega_bytes + sdsl_dec_7.size_in_mega_bytes + sdsl_dec_8.size_in_mega_bytes + sdsl_dec_9.size_in_mega_bytes + sdsl_dec_10.size_in_mega_bytes + sdsl_dec_11.size_in_mega_bytes + sdsl_dec_12.size_in_mega_bytes + sdsl_dec_13.size_in_mega_bytes + sdsl_dec_14.size_in_mega_bytes + sdsl_dec_15.size_in_mega_bytes + sdsl_dec_16.size_in_mega_bytes
        tam_original_sensores = tam_original_sensores_int + tam_original_sensores_dec
        #print("OG int = ",tam_original_sensores_int)
        #print("OG dec = ",tam_original_sensores_dec)
        #print("OG total = ",tam_original_sensores)
        #print()
        compact_vector_int_1 = int_type(sdsl_int_1)
        compact_vector_dec_1 = dec_type(sdsl_dec_1)
        compact_vector_int_2 = int_type(sdsl_int_2)
        compact_vector_dec_2 = dec_type(sdsl_dec_2)
        compact_vector_int_3 = int_type(sdsl_int_3)
        compact_vector_dec_3 = dec_type(sdsl_dec_3)
        compact_vector_int_4 = int_type(sdsl_int_4)
        compact_vector_dec_4 = dec_type(sdsl_dec_4)
        compact_vector_int_5 = int_type(sdsl_int_5)
        compact_vector_dec_5 = dec_type(sdsl_dec_5)
        compact_vector_int_6 = int_type(sdsl_int_6)
        compact_vector_dec_6 = dec_type(sdsl_dec_6)
        compact_vector_int_7 = int_type(sdsl_int_7)
        compact_vector_dec_7 = dec_type(sdsl_dec_7)
        compact_vector_int_8 = int_type(sdsl_int_8)
        compact_vector_dec_8 = dec_type(sdsl_dec_8)
        compact_vector_int_9 = int_type(sdsl_int_9)
        compact_vector_dec_9 = dec_type(sdsl_dec_9)
        compact_vector_int_10 = int_type(sdsl_int_10)
        compact_vector_dec_10 = dec_type(sdsl_dec_10)
        compact_vector_int_11 = int_type(sdsl_int_11)
        compact_vector_dec_11 = dec_type(sdsl_dec_11)
        compact_vector_int_12 = int_type(sdsl_int_12)
        compact_vector_dec_12 = dec_type(sdsl_dec_12)
        compact_vector_int_13 = int_type(sdsl_int_13)
        compact_vector_dec_13 = dec_type(sdsl_dec_13)
        compact_vector_int_14 = int_type(sdsl_int_14)
        compact_vector_dec_14 = dec_type(sdsl_dec_14)
        compact_vector_int_15 = int_type(sdsl_int_15)
        compact_vector_dec_15 = dec_type(sdsl_dec_15)
        compact_vector_int_16 = int_type(sdsl_int_16)
        compact_vector_dec_16 = dec_type(sdsl_dec_16)
        
        compact_vector_sensores_int = compact_vector_int_1.size_in_mega_bytes + compact_vector_int_2.size_in_mega_bytes + compact_vector_int_3.size_in_mega_bytes + compact_vector_int_4.size_in_mega_bytes + compact_vector_int_5.size_in_mega_bytes + compact_vector_int_6.size_in_mega_bytes + compact_vector_int_7.size_in_mega_bytes + compact_vector_int_8.size_in_mega_bytes + compact_vector_int_9.size_in_mega_bytes + compact_vector_int_10.size_in_mega_bytes + compact_vector_int_11.size_in_mega_bytes + compact_vector_int_12.size_in_mega_bytes + compact_vector_int_13.size_in_mega_bytes + compact_vector_int_14.size_in_mega_bytes + compact_vector_int_15.size_in_mega_bytes + compact_vector_int_16.size_in_mega_bytes
        compact_vector_sensores_dec = compact_vector_dec_1.size_in_mega_bytes + compact_vector_dec_2.size_in_mega_bytes + compact_vector_dec_3.size_in_mega_bytes + compact_vector_dec_4.size_in_mega_bytes + compact_vector_dec_5.size_in_mega_bytes + compact_vector_dec_6.size_in_mega_bytes + compact_vector_dec_7.size_in_mega_bytes + compact_vector_dec_8.size_in_mega_bytes + compact_vector_dec_9.size_in_mega_bytes + compact_vector_dec_10.size_in_mega_bytes + compact_vector_dec_11.size_in_mega_bytes + compact_vector_dec_12.size_in_mega_bytes + compact_vector_dec_13.size_in_mega_bytes + compact_vector_dec_14.size_in_mega_bytes + compact_vector_dec_15.size_in_mega_bytes + compact_vector_dec_16.size_in_mega_bytes
        compact_vector_sensores = compact_vector_sensores_int + compact_vector_sensores_dec
        #print("Tamaño vectores compactos INT = ",compact_vector_sensores_int)
        #print("Tamaño vectores compactos DEC = ",compact_vector_sensores_dec)
        #print("Tamaño vectores compactos TOTAL = ",compact_vector_sensores)
        #print()
        #print("TOTAL SUMA TIMESTAMP Y SENSORES (MB): ",compact_tam_ts+compact_vector_sensores)
        vector_partes_enteras = [compact_vector_int_1,compact_vector_int_2,compact_vector_int_3,compact_vector_int_4,compact_vector_int_5,compact_vector_int_6,compact_vector_int_7,compact_vector_int_8,compact_vector_int_9,compact_vector_int_10,compact_vector_int_11,compact_vector_int_12,compact_vector_int_13,compact_vector_int_14,compact_vector_int_15,compact_vector_int_16]
        vector_partes_decimales = [compact_vector_dec_1,compact_vector_dec_2,compact_vector_dec_3,compact_vector_dec_4,compact_vector_dec_5,compact_vector_dec_6,compact_vector_dec_7,compact_vector_dec_8,compact_vector_dec_9,compact_vector_dec_10,compact_vector_dec_11,compact_vector_dec_12,compact_vector_dec_13,compact_vector_dec_14,compact_vector_dec_15,compact_vector_dec_16]

    elif codificacion == 3 or codificacion == 4:
        def size_in_mega_bytes(numpy_array):
            return numpy_array.nbytes / (1024 * 1024)
        tam_numpy_sensores = sum([size_in_mega_bytes(arr) for arr in [numpy_1, numpy_2, numpy_3, numpy_4, numpy_5, numpy_6, numpy_7, numpy_8, numpy_9, numpy_10, numpy_11, numpy_12, numpy_13, numpy_14, numpy_15, numpy_16]])
        vector_sensores_nl = [numpy_1, numpy_2, numpy_3, numpy_4, numpy_5, numpy_6, numpy_7, numpy_8, numpy_9, numpy_10, numpy_11, numpy_12, numpy_13, numpy_14, numpy_15, numpy_16]
        #print("OG Numpy = ",tam_numpy_sensores)

    elif codificacion == 5:
        def size_in_mega_bytes(obj):
            return sys.getsizeof(obj) / (1024 * 1024)
        tam_listas_sensores = sum([size_in_mega_bytes(arr) for arr in [lista_1, lista_2, lista_3, lista_4, lista_5, lista_6, lista_7, lista_8, lista_9, lista_10, lista_11, lista_12, lista_13, lista_14, lista_15, lista_16]])
        vector_sensores_nl = [lista_1, lista_2, lista_3, lista_4, lista_5, lista_6, lista_7, lista_8, lista_9, lista_10, lista_11, lista_12, lista_13, lista_14, lista_15, lista_16]

    tiempo_preparacion_fin = time.time()
    tiempo_preparacion = tiempo_preparacion_fin - tiempo_preparacion_inicio
    #print("Tiempo Preparación de Datos: ",tiempo_preparacion)

    return tiempo_preparacion, timestamps, cant_lineas, (vector_partes_enteras, vector_partes_decimales) if codificacion in [1, 2] else (vector_sensores_nl if codificacion in [3, 4, 5] else None)
