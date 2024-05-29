import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


# Definir una función de segundo grado para el ajuste
def func(x, a, b, c):
    return a * x**2 + b * x + c

def suavizar(csv_original, csv_suavizado):
    # Leer el archivo CSV
    df = pd.read_csv(csv_original)

    # Extraer columnas X, Y y Time
    X = df['X'].values
    Y = df['Y'].values
    Time = df['Time'].values

    # Ajustar la función a los datos, omitiendo la primera fila
    params_x, _ = curve_fit(func, Time[1:], X[1:])
    params_y, _ = curve_fit(func, Time[1:], Y[1:])

    # Generar valores suavizados usando la función ajustada
    X_smooth = func(Time, *params_x)
    Y_smooth = func(Time, *params_y)

    # Mantener la primera fila como (0, 0)
#    X_smooth[0] = 0
#    Y_smooth[0] = 0

    # Redondear los números a cuatro dígitos decimales
    X_smooth = np.round(X_smooth, 4)
    Y_smooth = np.round(Y_smooth, 4)

    # Crear una nueva tabla con los valores suavizados
    df_smooth = pd.DataFrame({
        'X': X_smooth,
        'Y': Y_smooth,
        'Time': Time
    })

    # Guardar la nueva tabla en un archivo CSV
    df_smooth.to_csv(csv_suavizado, index=False)



def graficar(csv_original, csv_suavizado):
    # Leer los archivos CSV
    df1 = pd.read_csv(csv_original)
    df2 = pd.read_csv(csv_suavizado)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))

    # Graficar los datos del segundo archivo
    plt.plot(df2['X'], df2['Y'], label='Suavizado', color='red', linestyle='-', linewidth=10)

    # Graficar los datos del primer archivo
    plt.plot(df1['X'], df1['Y'], label='Original', color='blue', linestyle='-', linewidth=4)

    # Etiquetas y título
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Gráfica de X e Y para ambos archivos')
    plt.legend()

    # Guardar la gráfica como una imagen
    plt.savefig("grafica.png")

    # Mostrar la gráfica
    plt.show()

