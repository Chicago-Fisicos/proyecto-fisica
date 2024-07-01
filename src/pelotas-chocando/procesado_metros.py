import sys
import os
import importlib.util

import pandas as pd

# Ruta al archivo pandas_procesing.py
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../basket-doble/pandas_procesing.py'))

# Cargar el módulo
spec = importlib.util.spec_from_file_location("pandas_procesing", file_path)
pandas_procesing = importlib.util.module_from_spec(spec)
sys.modules["pandas_procesing"] = pandas_procesing
spec.loader.exec_module(pandas_procesing)

#variables
RUTA_CSV_BASKET_ANTES = "tablas/trackeo-basket-antes-de-choque.csv"
RUTA_CSV_BASKET_DESPUES = "tablas/trackeo-basket-despues-de-choque.csv"
RUTA_CSV_TENIS_ANTES = "tablas/trackeo-tenis-antes-de-choque.csv"
RUTA_CSV_TENIS_DESPUES = "tablas/trackeo-tenis-despues-de-choque.csv"


RUTA_OUTPUT_CSV_BASKET_ANTES = "tablas/tabla-moviento-metros-basket-antes-de-choque.csv"
RUTA_OUTPUT_CSV_BASKET_DESPUES = "tablas/tabla-moviento-metros-basket-despues-de-choque.csv"
RUTA_OUTPUT_CSV_TENIS_ANTES = "tablas/tabla-moviento-metros-tenis-antes-de-choque.csv"
RUTA_OUTPUT_CSV_TENIS_DESPUES = "tablas/tabla-moviento-metros-tenis-despues-de-choque.csv"

pandas_procesing.VALOR_PIXEL_METRO = 0.441 / 100

if __name__ == "__main__":

    #### Basket

    # antes de choque

    tabla_original = pd.read_csv(RUTA_CSV_BASKET_ANTES)
    # creo un nuevo data frame con Time,x,Y e introduzco los datos de la columna "x_nuevo_origen_suavizado" en x
    tabla_movimiento = pd.DataFrame({"Time": tabla_original["Time"],
                                     "X": tabla_original["X_nuevo_origen_suavizado"],
                                     "Y": tabla_original["Y_nuevo_origen_suavizado"]})
    tabla_movimiento = pandas_procesing.generar_datos_movimiento_metros(tabla_movimiento)
    # exportar a csv
    tabla_movimiento = tabla_movimiento.round(6)
    tabla_movimiento.to_csv(RUTA_OUTPUT_CSV_BASKET_ANTES, index=False)

    # despues de choque

    tabla_original = pd.read_csv(RUTA_CSV_BASKET_DESPUES)
    # creo un nuevo data frame con Time,x,Y e introduzco los datos de la columna "x_nuevo_origen_suavizado" en x
    tabla_movimiento = pd.DataFrame({"Time": tabla_original["Time"],
                                     "X": tabla_original["X_nuevo_origen_suavizado"],
                                     "Y": tabla_original["Y_nuevo_origen_suavizado"]})
    tabla_movimiento = pandas_procesing.generar_datos_movimiento_metros(tabla_movimiento)
    # exportar a csv
    tabla_movimiento = tabla_movimiento.round(6)
    tabla_movimiento.to_csv(RUTA_OUTPUT_CSV_BASKET_DESPUES, index=False)

    #### tenis

    # antes de choque

    tabla_original = pd.read_csv(RUTA_CSV_TENIS_ANTES)
    # creo un nuevo data frame con Time,x,Y e introduzco los datos de la columna "x_nuevo_origen_suavizado" en x
    tabla_movimiento = pd.DataFrame({"Time": tabla_original["Time"],
                                     "X": tabla_original["X_nuevo_origen_suavizado"],
                                     "Y": tabla_original["Y_nuevo_origen_suavizado"]})
    tabla_movimiento = pandas_procesing.generar_datos_movimiento_metros(tabla_movimiento)
    # exportar a csv
    tabla_movimiento = tabla_movimiento.round(6)
    tabla_movimiento.to_csv(RUTA_OUTPUT_CSV_TENIS_ANTES, index=False)

    # despues de choque

    tabla_original = pd.read_csv(RUTA_CSV_TENIS_DESPUES)
    # creo un nuevo data frame con Time,x,Y e introduzco los datos de la columna "x_nuevo_origen_suavizado" en x
    tabla_movimiento = pd.DataFrame({"Time": tabla_original["Time"],
                                     "X": tabla_original["X_nuevo_origen_suavizado"],
                                     "Y": tabla_original["Y_nuevo_origen_suavizado"]})
    tabla_movimiento = pandas_procesing.generar_datos_movimiento_metros(tabla_movimiento)
    # exportar a csv
    tabla_movimiento = tabla_movimiento.round(6)
    tabla_movimiento.to_csv(RUTA_OUTPUT_CSV_TENIS_DESPUES, index=False)




