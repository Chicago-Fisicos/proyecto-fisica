import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


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

    # Ajustar la función cuadrática a los datos de X
    params_x, _ = curve_fit(func, np.arange(len(X)), X)

    # Ajustar la función cuadrática a los datos de Y
    params_y, _ = curve_fit(func, np.arange(len(Y)), Y)

    # Aplicar el filtro de Savitzky-Golay a los datos de X e Y
    window_length = 5  # Longitud de la ventana, debe ser impar
    polyorder = 2  # Orden del polinomio, usualmente 2 o 3

    X_suavizado = savgol_filter(X, window_length, polyorder)
    Y_suavizado = savgol_filter(Y, window_length, polyorder)

    # Redondear los números a cuatro dígitos decimales
    X_suavizado = np.round(X_suavizado, 4)
    Y_suavizado = np.round(Y_suavizado, 4)

    # Crear una nueva tabla con los valores suavizados
    df_suavizado = pd.DataFrame({
        'X': X_suavizado,
        'Y': Y_suavizado,
        'Time': Time
    })

    # Guardar la nueva tabla en un archivo CSV
    df_suavizado.to_csv(csv_suavizado, index=False)


def graficar(csv_original, csv_suavizado):
    # Leer los archivos CSV
    df1 = pd.read_csv(csv_original)
    df2 = pd.read_csv(csv_suavizado)

    # Crear la figura y los ejes
    plt.figure(figsize=(10, 6))

    # Graficar los datos del segundo archivo
    plt.plot(df2['X'], df2['Y'], label='Suavizado', color='red', linestyle='-', linewidth=10)

    # Graficar los datos del primer archivo
    plt.plot(df1['X'], df1['Y'], label='Original', color='blue', linestyle='-', linewidth=3)

    # Etiquetas y título
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Gráfica de X e Y para ambos archivos')
    plt.legend()

    # Guardar la gráfica como una imagen
    plt.savefig("grafica.png")

    # Mostrar la gráfica
    plt.show()

