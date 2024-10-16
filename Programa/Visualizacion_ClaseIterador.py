from __future__ import print_function
import dash
from dash import dcc
from dash import html
import pandas as pd
# from plotly_resampler import FigureResampler, FigureWidgetResampler, register_plotly_resampler, unregister_plotly_resampler
from plotly.offline import plot
import plotly.offline as pyo
import plotly.graph_objects as go
from flask import request
import time
import cProfile
import numpy as np
import math
from plotly.subplots import make_subplots
from datetime import datetime
import sdsl4py
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output,State
from sys import getsizeof, stderr
from itertools import chain
from collections import deque
try:
    from reprlib import repr
except ImportError:
    pass
import tempfile
import os
import sys
from PreparacionDatos import preparacion_data, deshacer_transformacion

porcentaje_puntos = 100

colores = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'pink', 'brown', 'gray', 'cyan', 'magenta', 'lime', 'teal', 'navy', 'olive', 'maroon']
nombres = ['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8', 'Sensor 9', 'Sensor 10', 'Sensor 11', 'Sensor 12', 'Sensor 13', 'Sensor 14', 'Sensor 15', 'Sensor 16']


def size_in_mega_bytes(numpy_array):
    return numpy_array.nbytes / (1024 * 1024)

def size_in_mega_bytes_listas(lst):
    return sys.getsizeof(lst) / (1024 * 1024)

def graficar(codificacion,file_path):
    class claseIterador:
        ## Constructor
        ## n=cantidad de lineas total  #n_puntos=cantidad de puntos a graficar
        def __init__(self, n, int_vector, dec_vector,codificacion):
            self.int_part = int_vector
            self.dec_part = dec_vector
            #self.timestamps = timestamps
            self.current = 0
            self.n = n
            #self.porcentaje = porcentaje
            self.codificacion = codificacion

            '''if self.porcentaje == 10:
                self.n_puntos = (n*16)/10
            elif self.porcentaje == 25:
                self.n_puntos = (n*16)/4
            elif self.porcentaje == 50:
                self.n_puntos = (n*16)/2
            elif self.porcentaje == 75:
                self.n_puntos = ((n*16)/4)*3
            elif self.porcentaje == 100:
                self.n_puntos = n*16
            else:
                self.porcentaje = None
                print("Porcentaje no soportado")
            '''

        def __iter__(self):
            return self

        def __next__(self):

            if self.current < self.n:
                entera = self.int_part[self.current] 
                decimal = self.dec_part[self.current]
                
                decimal_original = deshacer_transformacion(decimal)
                if decimal_original < 0:
                    parte_decimal = decimal_original / 1000
                    v = entera + abs(parte_decimal)
                    v = -v
                elif decimal == 0:
                    v = deshacer_transformacion(entera)
                else:
                    parte_decimal = decimal_original / 1000
                    v = entera + parte_decimal
                #timestamp = self.timestamps[self.current]
                self.current += 1
                return v#,timestamp
            raise StopIteration

        def get_total_size(self, verbose=False):
            if codificacion == 1 or codificacion == 2:   
                tam_tot = self.int_part.size_in_mega_bytes+self.dec_part.size_in_mega_bytes
            elif codificacion == 3 or codificacion == 4:
                def size_in_mega_bytes(numpy_array):
                    return numpy_array.nbytes / (1024 * 1024)
                tam_tot = size_in_mega_bytes(self.int_part)+size_in_mega_bytes(self.dec_part)
            return tam_tot 

    class claseIteradorSoloTimestamps:
        ## Constructor
        ## n=cantidad de lineas total  #n_puntos=cantidad de puntos a graficar
        def __init__(self, n, vector_sensores,timestamps, codificacion):
            self.vector_sensor = vector_sensores
            self.timestamps = timestamps
            self.current = 0
            self.n = n
            self.codificacion = codificacion
            #print(len(vector_sensores))
            #print(len(timestamps))

            if len(self.vector_sensor) != len(self.timestamps):
                raise ValueError("vector_sensores y timestamps deben tener la misma longitud.")

        def __iter__(self):
            return self

        def __next__(self):
            if self.current < self.n:
                timestamp = self.timestamps[self.current]
                self.current += 1
                return timestamp
            raise StopIteration

        def get_total_size(self, verbose=False):
            def size_in_mega_bytes(numpy_array):
                return numpy_array.nbytes / (1024 * 1024)
            tam_tot = size_in_mega_bytes(self.vector_sensor)
            return tam_tot

    tiempo_preparacion, timestamps, cant_lineas, data = preparacion_data(codificacion,file_path)
    if codificacion in [1, 2]:
        vector_partes_enteras, vector_partes_decimales = data
    elif codificacion in [3, 4, 5]:
        vector_sensores_nl = data
    else:
        pass

    tamaño_bytes = 0
    tiempo_renderizado = 0
    tiempo_instancia = 0
    tam_timestamps = 0

 
    if codificacion == 1 or codificacion == 2:
        fig = go.Figure()
        inicio = time.time()

        instancia1 = claseIterador(cant_lineas, vector_partes_enteras[0], vector_partes_decimales[0], codificacion) 
        instancia2 = claseIterador(cant_lineas, vector_partes_enteras[1], vector_partes_decimales[1], codificacion)
        instancia3 = claseIterador(cant_lineas, vector_partes_enteras[2], vector_partes_decimales[2], codificacion)
        instancia4 = claseIterador(cant_lineas, vector_partes_enteras[3], vector_partes_decimales[3], codificacion)
        instancia5 = claseIterador(cant_lineas, vector_partes_enteras[4], vector_partes_decimales[4], codificacion)
        instancia6 = claseIterador(cant_lineas, vector_partes_enteras[5], vector_partes_decimales[5], codificacion)
        instancia7 = claseIterador(cant_lineas, vector_partes_enteras[6], vector_partes_decimales[6], codificacion)
        instancia8 = claseIterador(cant_lineas, vector_partes_enteras[7], vector_partes_decimales[7], codificacion)
        instancia9 = claseIterador(cant_lineas, vector_partes_enteras[8], vector_partes_decimales[8], codificacion)
        instancia10 = claseIterador(cant_lineas, vector_partes_enteras[9], vector_partes_decimales[9], codificacion)
        instancia11 = claseIterador(cant_lineas, vector_partes_enteras[10], vector_partes_decimales[10], codificacion)
        instancia12 = claseIterador(cant_lineas, vector_partes_enteras[11], vector_partes_decimales[11], codificacion)
        instancia13 = claseIterador(cant_lineas, vector_partes_enteras[12], vector_partes_decimales[12], codificacion)
        instancia14 = claseIterador(cant_lineas, vector_partes_enteras[13], vector_partes_decimales[13], codificacion)
        instancia15 = claseIterador(cant_lineas, vector_partes_enteras[14], vector_partes_decimales[14], codificacion)
        instancia16 = claseIterador(cant_lineas, vector_partes_enteras[15], vector_partes_decimales[15], codificacion)

        instancia_fin = time.time()

        for i in range(1, 17):  # Desde 1 hasta 16
            instancia = locals()[f'instancia{i}']
            tamaño_bytes += instancia.get_total_size(verbose=False)
        
        df = pd.DataFrame({
            'Timestamps': pd.to_datetime(timestamps, format='%Y%m%d%H%M%S%f'),  
            'Sensor 1': instancia1,
            'Sensor 2': instancia2,
            'Sensor 3': instancia3,
            'Sensor 4': instancia4,
            'Sensor 5': instancia5,
            'Sensor 6': instancia6,
            'Sensor 7': instancia7,
            'Sensor 8': instancia8,
            'Sensor 9': instancia9,
            'Sensor 10': instancia10,
            'Sensor 11': instancia11,
            'Sensor 12': instancia12,
            'Sensor 13': instancia13,
            'Sensor 14': instancia14,
            'Sensor 15': instancia15,
            'Sensor 16': instancia16,
        })

        fig = px.line(df, x='Timestamps', y=['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5', 'Sensor 6', 'Sensor 7', 'Sensor 8', 'Sensor 9', 'Sensor 10', 'Sensor 11', 'Sensor 12', 'Sensor 13', 'Sensor 14', 'Sensor 15', 'Sensor 16'])
    
        fin = time.time()
        
        tiempo_instancia = instancia_fin - inicio
        tiempo_renderizado = fin - inicio - tiempo_instancia
        tam_timestamps = timestamps.size_in_mega_bytes
        
    elif codificacion == 3:
        fig = px.line()
        inicio = time.time()

        for i in range(16):
            y_data = vector_sensores_nl[i]
            x_data = pd.to_datetime(timestamps, format='%Y%m%d%H%M%S%f')  
            tamaño_bytes += size_in_mega_bytes(vector_sensores_nl[i])      
            fig.add_trace(go.Scatter(x=x_data, y=y_data, line_color=colores[i], name=nombres[i]))  
        
        fin = time.time()
        tiempo_renderizado = fin - inicio
        tam_timestamps = timestamps.size_in_mega_bytes

    elif codificacion == 4:
        fig = px.line()
        inicio = time.time()

        for i in range(16):
            y_data = vector_sensores_nl[i]
            x_data = pd.to_datetime(timestamps, format='%Y%m%d%H%M%S%f')        
            tamaño_bytes += size_in_mega_bytes(vector_sensores_nl[i]) 
            traza = px.line(pd.DataFrame({'timestamp': x_data, 'value': y_data}), x="timestamp", y="value")
            traza.update_traces(line_color=colores[i], name=nombres[i])
            fig.add_trace(go.Scatter(x=x_data, y=y_data, line_color=colores[i], name=nombres[i]))        
                    
        fin = time.time()
        tiempo_renderizado = fin - inicio
        tam_timestamps = size_in_mega_bytes(timestamps)
        
    elif codificacion == 5:
        fig = px.line()
        inicio = time.time()

        for i in range(16):
            y_data = vector_sensores_nl[i]
            x_data = pd.to_datetime(timestamps, format='%Y%m%d%H%M%S%f')
            tamaño_bytes += size_in_mega_bytes_listas(vector_sensores_nl[i])
            fig.add_trace(go.Scatter(x=x_data, y=y_data, line_color=colores[i], name=nombres[i]))
        fin = time.time()
        tiempo_renderizado = fin - inicio
        tam_timestamps = size_in_mega_bytes(timestamps)
        
    #print("Tiempo de creación del gráfico: ", tiempo_renderizado)#-tiempo_preparacion)
    tamaño_total = tamaño_bytes+tam_timestamps
    #print("Tamaño total:", tamaño_total)

    fig.update_layout(clickmode='event+select',  dragmode='zoom')
    
    
    return tiempo_renderizado, tamaño_total, fig
