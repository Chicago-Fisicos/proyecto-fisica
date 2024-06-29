import csv
import os
import numpy as np
import pandas
import pandas as pd

PATH_ERROR_C_CURVE_FIT = '../basket-doble/tablas/error_segun_curve_fit.csv'
# calculada con curve fit pero en metros
PATH_TABLA_MOV_METROS = '../basket-doble/tablas/tabla-moviento-metros.csv'
CANT_FRAMES = 29.5235
MEASUREMENT_ERROR_METROS = 0.01
PIXEL_METROS = 0.00447

def calculate_time_error():
    return 1 / CANT_FRAMES

def file_exists(file_path):
    return os.path.isfile(file_path)

def read_errors_curve_fit(file_path):
    errors_list = []
    if not file_exists(file_path):
        print(f"El archivo no existe en la ruta: {file_path}")
        return errors_list
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Omitir el encabezado si existe
            for row in reader:
                variable, x, error_x, y, error_y = row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4])
                errors_list.append((variable, x, error_x, y, error_y))
    except ValueError as ve:
        print(f"Error de valor: {ve}")
    except Exception as e:
        print(f"Se produjo un error al leer el archivo: {e}")
    return errors_list

def calculate_error_c_curve_fit():
    list_errors = read_errors_curve_fit(PATH_ERROR_C_CURVE_FIT)
    c= list_errors[2][3]
    error_c = list_errors[2][4]
    return c*PIXEL_METROS, error_c*PIXEL_METROS

def calculate_error_x():
    error_x = np.sqrt((PIXEL_METROS**2) + (MEASUREMENT_ERROR_METROS**2))
    return error_x

def calculate_error_velocidad_x (Xf,Xi,Tf,Ti):
    # V = d/t

    error_x = calculate_error_x()
    error_t = calculate_time_error()
    t = Tf - Ti
    d = Xf - Xi
    error_d = error_x
    derivadaVx_d = 1/t
    derivadaVx_t = -d/(t**2)

    error_Vx = np.sqrt((derivadaVx_d**2) * (error_d**2) + (derivadaVx_t**2) * (error_t**2))
    return error_Vx

def calculate_error_gravedad (c, error_c, error_Vx):
    #gravedad = -2*c*(error_Vx**2)

    derivada_g_c = -4*error_Vx
    derivada_g_v = -4*c

    error_gravedad = np.sqrt( (derivada_g_c**2) * (error_c**2) + (derivada_g_v**2) * (error_Vx**2) )

    return error_gravedad

def extraer_datos ():
    # Leer los datos del archivo CSV
    data = pd.read_csv(PATH_TABLA_MOV_METROS)

    # Extraer de las columnas
    Xf = data['X'].iloc[-1]
    Xi = data['X'].iloc[1]
    Tf = data['Time'].iloc[-1]
    Ti = data['Time'].iloc[1]

    return Xf,Xi,Tf,Ti

def calculate_g_prom ():
    # Leer los datos del archivo CSV
    data = pd.read_csv(PATH_TABLA_MOV_METROS)

    # Extraer de las columnas
    acceleration = data['accelerationY'].iloc[3:]
    g_prom = np.abs(np.mean(acceleration))
    return g_prom

def main():
    # Calculate_time_error
    error_time = calculate_time_error()
    print(f'El error del tiempo es: {error_time}')

    # Calculate_c_error
    c, error_c = calculate_error_c_curve_fit()
    print(f'C segun curve fit en metros es: {c}')
    print(f'El error de C segun curve fit en metros es: {error_c}')

    # Calculate_X_error
    error_x = calculate_error_x()
    print(f'El error de X es: {error_x}')

    # data
    Xf, Xi, Tf, Ti = extraer_datos()
    print(f'Xf es: {Xf}')
    print(f'Xi es: {Xi}')
    print(f'Tf es: {Tf}')
    print(f'Ti es: {Ti}')

    # Calculate_error_velocidad_x (Xf,Xi,Tf,Ti)
    error_Vx = calculate_error_velocidad_x(Xf, Xi, Tf, Ti)

    #calcular error de gravedad
    error_gravedad = calculate_error_gravedad(c, error_c, error_Vx)
    print(f'El error de G es: {error_gravedad}')

    # calcular gravedad promedio
    g_prom = calculate_g_prom()
    print(f'El G promedio es: {g_prom}')

    #Generar tabla

    tabla_de_Errores = pd.DataFrame({'Gravedad Promedio': [g_prom]})
    tabla_de_Errores['Gravedad Error'] = error_gravedad
    tabla_de_Errores['Gravedad Promedio + Error'] = g_prom + error_gravedad
    tabla_de_Errores['Gravedad Promedio - Error'] = g_prom - error_gravedad
    tabla_de_Errores.round(2).to_csv('Tabla_de_Errores.csv',index=False)

if __name__ == "__main__":
    main()
