import pandas as pd

#variables
RUTA_CSV = "../chipi/tablas/trackeo-original-nuevo-origen.csv"
RUTA_OUTPUT_CSV = "./output.csv"

VALOR_PIXEL_METRO = 0.447 / 100

def parsear_a_metros(valorPixel):
    return valorPixel * VALOR_PIXEL_METRO

def calcular_velocidad(tabla, columna):
    # Asegurarse de que los datos son flotantes para la operación
    tabla[columna] = tabla[columna].astype(float)
    tabla["Time"] = tabla["Time"].astype(float)

    # Calcular la diferencia entre filas consecutivas
    delta_posicion = tabla[columna].diff().fillna(0)
    delta_tiempo = tabla["Time"].diff().fillna(0)

    # Evitar la división por cero
    velocidad = delta_posicion / delta_tiempo.replace(0, 1)

    return velocidad

def calcular_aceleracion(tabla,columna):
    # Asegurarse de que los datos son flotantes para la operación
    velocidad="velocity"+columna
    tabla["Time"] = tabla["Time"].astype(float)
    tabla[velocidad] = tabla[velocidad].astype(float)

    # Calcular la diferencia entre filas consecutivas
    delta_velocidad = tabla[velocidad].diff().fillna(0)
    delta_tiempo = tabla["Time"].diff().fillna(0)

    # Evitar la división por cero
    aceleracion = round(delta_velocidad / delta_tiempo.replace(0, 1),2)
    return aceleracion

tabla_movimiento = pd.read_csv(RUTA_CSV)

tabla_movimiento["X"]= tabla_movimiento["X"].apply(parsear_a_metros)
tabla_movimiento["Y"]= tabla_movimiento["Y"].apply(parsear_a_metros)

tabla_movimiento["velocityX"] = calcular_velocidad(tabla_movimiento, "X")
tabla_movimiento["velocityY"] = calcular_velocidad(tabla_movimiento, "Y")

tabla_movimiento["accelerationY"] = calcular_aceleracion(tabla_movimiento, "Y")

tabla_movimiento.to_csv(RUTA_OUTPUT_CSV, index=False)