import pandas as pd
import numpy as np

#variables
RUTA_CSV = "tablas/tabla-moviento-metros.csv"
RUTA_OUTPUT_CSV = "tablas/tabla-moviento-error.csv"

def main():
    # Importar datos de csv
    tabla_movimiento = pd.read_csv(RUTA_CSV)

    promedio_teorico_X = np.mean(tabla_movimiento["pos_X_teorica"].iloc[1:])
    promedio_teorico_Y = np.mean(tabla_movimiento["pos_Y_teorica"].iloc[1:])

    a_sumar = (promedio_teorico_X - tabla_movimiento["X"].iloc[1:])**2
    b_sumar = (promedio_teorico_Y - tabla_movimiento["Y"].iloc[1:])**2

    desvio_estandar_x = np.abs(np.sum(a_sumar)/tabla_movimiento.iloc[1:].size)
    desvio_estandar_y = np.abs(np.sum(b_sumar)/tabla_movimiento.iloc[1:].size)

    desvio_medicion = 0.01**2

    delta_e_x = np.sqrt(desvio_estandar_x + desvio_medicion)
    delta_e_y = np.sqrt(desvio_estandar_y + desvio_medicion)

    print(promedio_teorico_X)
    print(promedio_teorico_Y)
    print(delta_e_x)
    print(delta_e_y)

    tabla_error= pd.DataFrame()

    tabla_error["X"] = tabla_movimiento["X"].iloc[1:]
    tabla_error["Y"] = tabla_movimiento["Y"].iloc[1:]

    tabla_error["error_X"] = delta_e_x/tabla_error["X"]
    tabla_error["error_Y"] = delta_e_y/tabla_error["Y"]

    tabla_error = tabla_error.round(4)
    tabla_error.to_csv(RUTA_OUTPUT_CSV, index=False)

if __name__ == "__main__":
    main()