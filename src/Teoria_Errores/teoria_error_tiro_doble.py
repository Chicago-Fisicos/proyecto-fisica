import csv
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

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
    c_x = list_errors[2][1]
    c_y= list_errors[2][3]
    error_c_x = list_errors[2][2]
    error_c_y = list_errors[2][4]

    return c_x*PIXEL_METROS, c_y*PIXEL_METROS, error_c_x*PIXEL_METROS, error_c_y*PIXEL_METROS

def calcular_valor_c(gravedad, vx):
    c = (-1*gravedad)/((vx**2)*2)
    return c

def calcular_error_total_c():
    c_x, c_y, error_c_x, error_c_y = calculate_error_c_curve_fit()
    error_c_total = np.sqrt(error_c_x ** 2 + error_c_y ** 2)
    return error_c_total

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

def calculate_error_gravedad (c, error_c, Vx, error_Vx):
    #gravedad = -2*c*(Vx**2)

    derivada_g_c = -2*(Vx**2)
    derivada_g_v = -4*c*Vx

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
    Vx = data['velocityX'].iloc[1]

    return Xf,Xi,Tf,Ti,Vx

def calculate_g_prom ():
    # Leer los datos del archivo CSV
    data = pd.read_csv(PATH_TABLA_MOV_METROS)

    # Extraer de las columnas
    acceleration = data['accelerationY'].iloc[3:]
    g_prom = np.abs(np.mean(acceleration))
    return g_prom

def calculate_error_velocidad_y(Xf,Xi,Tf, Ti, g_prom, error_x, error_g, error_t):
    # Vy =  (d/t) + (g*(1/2)*(t))
    t= Tf-Ti
    d= Xf-Xi

    derivada_Vy_d = 1 / t
    derivada_Vy_g = 0.5 * t
    derivada_Vy_t = (-d / (t ** 2)) + (0.5 * g_prom)

    error_velocidad_y = np.sqrt((derivada_Vy_d ** 2) * (error_x ** 2) + (derivada_Vy_g ** 2) * (error_g ** 2) + (derivada_Vy_t ** 2) * (error_t ** 2) )
    return error_velocidad_y

def plot_error_gravity(g_prom, error_gravedad):
    plt.errorbar([0], [g_prom], yerr=[error_gravedad], fmt='o', label='Gravedad con error')
    plt.xlabel('Index')
    plt.ylabel('Gravedad (m/s^2)')
    plt.title('Gravedad con su error')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_error_velocity_x(Vx, error_Vx):
    plt.errorbar([0], [Vx], yerr=[error_Vx], fmt='o', label='Velocidad en X con error')
    plt.xlabel('Index')
    plt.ylabel('Velocidad en X (m/s)')
    plt.title('Velocidad en X con su error')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_error_velocity_y(Vy, error_Vy):
    plt.errorbar([0], [Vy], yerr=[error_Vy], fmt='o', label='Velocidad en Y con error')
    plt.xlabel('Index')
    plt.ylabel('Velocidad en Y (m/s)')
    plt.title('Velocidad en Y con su error')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    # Calculate_time_error
    error_time = calculate_time_error()
    print(f'El error del tiempo es: {error_time}')

    # Calculate_c_error
    error_c_total = calcular_error_total_c()
    print(f'El error de C segun curve fit en metros es: {error_c_total}')

    # Calculate_X_error
    error_x = calculate_error_x()
    print(f'El error de X es: {error_x}')

    # data
    Xf, Xi, Tf, Ti, Vx = extraer_datos()
    print(f'Xf es: {Xf}')
    print(f'Xi es: {Xi}')
    print(f'Tf es: {Tf}')
    print(f'Ti es: {Ti}')
    print(f'Vx es: {Vx}')

    # calculate gravity(prom)
    g_prom = calculate_g_prom()
    print(f'El G promedio es: {g_prom}')

    # calculate C
    c_total = calcular_valor_c(g_prom, Vx)
    print(f'El valor C en metros es: {c_total}')

    # Calculate_error_velocity_x
    error_Vx = calculate_error_velocidad_x(Xf, Xi, Tf, Ti)
    print(f'El error de Vx es: {error_Vx}')

    # calculate error gravity
    error_gravedad = calculate_error_gravedad(c_total, error_c_total, Vx, error_Vx)
    print(f'El error de G es: {error_gravedad}')

    # calculate error in velocity_y
    error_velocidad_y = calculate_error_velocidad_y(Xf, Xi, Tf, Ti, g_prom, error_x, error_gravedad, error_time)
    print(f'El error de Vy es: {error_velocidad_y}')

    #Generar tabla

    tabla_de_Errores = pd.DataFrame({'Gravedad Promedio': [g_prom]})
    tabla_de_Errores['Gravedad Error'] = error_gravedad
    tabla_de_Errores['Gravedad Promedio + Error'] = g_prom + error_gravedad
    tabla_de_Errores['Gravedad Promedio - Error'] = g_prom - error_gravedad
    tabla_de_Errores.round(2).to_csv('Tabla_de_Errores_Tiro_Doble.csv',index=False)

    # Generate plots
    #plot_error_gravity(g_prom, error_gravedad)
    #plot_error_velocity_x(Vx, error_Vx)
    #Vy = (Xf - Xi) / (Tf - Ti) + g_prom * 0.5 * (Tf - Ti)
    #plot_error_velocity_y(Vy, error_velocidad_y)

if __name__ == "__main__":
    main()
