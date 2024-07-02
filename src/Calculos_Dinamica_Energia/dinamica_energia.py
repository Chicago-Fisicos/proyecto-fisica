import pandas as pd
import numpy as np

INPUT = '../basket-doble/tablas/tabla-moviento-metros.csv'
ERROR_X = 0.010953579323673152 #Calculado el tiro doble teorria de error
MASA_PELOTA_BASQUET = 0.62

def calcular_pendiente_recta_ajustada ():
    # Leer los datos del archivo CSV
    data = pd.read_csv(INPUT)

    # Extraer las columnas de tiempo y velocidad en x
    t = data['Time'].iloc[1:]
    velocidad_x = data['velocityX'].iloc[1:]

    # Ajustar una línea a los datos (velocidad en x en función del tiempo)
    A,B = np.polyfit(t, velocidad_x, 1)

    # Calcular la matriz de covarianza
    cov_matrix = np.cov(t, velocidad_x)
    cov_ab = cov_matrix[0, 1]  # Covarianza entre t y velocidad_x

    # Calcular el error estándar para A y B
    n = len(t)  # Número de observaciones
    error_A = np.sqrt((1 / n) * (cov_matrix[1, 1] / cov_matrix[0, 0] - (A ** 2)))

    return A, B, error_A

def calcular_fx():
    pendiente_x, ordenada , errorA = calcular_pendiente_recta_ajustada()

    Fx = 0.62 * pendiente_x

    return Fx

def calcular_fuerza_aire_promedio ():
     Fx = calcular_fx()
     delta_x, delta_y = calcular_deltas()
     fuerza_aire_prom = Fx*delta_x
     return fuerza_aire_prom

def calcular_deltas():
    # Leer los datos del archivo CSV
    data = pd.read_csv(INPUT)

    # Extraer las columnas de posición en x y y
    x = data['X'].iloc[1:]
    y = data['Y'].iloc[1:]

    # Calcular las diferencias de posición (dx y dy)
    delta_x = np.sum(np.diff(x))
    delta_y = np.sum(np.diff(y))

    return delta_x, delta_y

def calcular_delta_energia_mecanica():
    # Leer los datos del archivo CSV
    data = pd.read_csv(INPUT)

    # Extraer las columnas de posición en x y y
    energia_mecanica = data['Energia_mecanica'].iloc[1:]

    # Calcular las diferencias de posición (dx y dy)
    delta_energia_mecanica = np.sum(np.diff(energia_mecanica))

    return delta_energia_mecanica

def calcular_integrales_x():
   # Calcular las integrales como Fx*delta_x y Fy*delta_y
   delta_x, delta_y = calcular_deltas()
   Fx = calcular_fx()
   integral_Fx_dx =  Fx * delta_x

   return integral_Fx_dx

def calcular_fy () :
  integral_Fx_dx = calcular_integrales_x()
  delta_x, delta_y = calcular_deltas()
  delta_energia_mecanica = calcular_delta_energia_mecanica()
  Fy = (delta_energia_mecanica - integral_Fx_dx ) / delta_y
  return Fy

def calcular_modulo_fuerzas():
    Fx= calcular_fx ()
    Fy= calcular_fy ()
    modulo= np.linalg.norm([Fx, Fy])

    return modulo

def calcular_error_fx ():
    A,B, error_A = calcular_pendiente_recta_ajustada()
    derivada_Fx_m = A
    derivada_Fx_a = MASA_PELOTA_BASQUET
    dm = 0.005

    error_fx = np.sqrt((derivada_Fx_m ** 2) * (dm ** 2) + (derivada_Fx_a ** 2) * (error_A ** 2))
    return error_fx


def calcular_error_fy (dy, Fx, dx , dem, dFx):

    derivada_Fy_dem = 1 / dy
    derivada_Fy_dy = Fx * dx / dy ** 2 - dem / dy ** 2
    derivada_Fy_Fx = -dx / dy
    derivada_Fy_dx = -Fx / dy

    error_fy = np.sqrt((derivada_Fy_dem ** 2) * ( dem ** 2) + (derivada_Fy_dy ** 2) * (ERROR_X ** 2) + (derivada_Fy_Fx ** 2) * (dFx ** 2) + (derivada_Fy_dx ** 2) * (ERROR_X ** 2))
    return error_fy
def main():
    # Calcular pendiente recta ajustada
    A, B , errorA = calcular_pendiente_recta_ajustada()
    # Calcular las fuerzas no conservativas
    Fx = calcular_fx()
    Fy = calcular_fy()
    # Calcular las integrales y los desplazamientos
    delta_x, delta_y = calcular_deltas()
    integral_Fx_dx = calcular_integrales_x()
    # Calcular la variación de la energía mecánica
    delta_energia_mecanica = calcular_delta_energia_mecanica()
    # Calcular modulo de las fuerzas
    modulo = calcular_modulo_fuerzas()

    # Calcular error Fx
    error_fx = calcular_error_fx()

    # Calcular error Fy
    error_fy = calcular_error_fy(delta_y, Fx, delta_x , delta_energia_mecanica, error_fx)

    # Imprimir los resultados finales
    print(f'Pendiente (A): {A}')
    print(f'Intersección (B): {B}')
    print(f'Fx: {Fx}')
    print(f'Delta x: {delta_x}')
    print(f'Fy: {Fy}')
    print(f'Delta y: {delta_y}')
    print(f'int_fx_dx: {integral_Fx_dx}')
    print(f'Delta energía mecánica: {delta_energia_mecanica}')
    print(f'Módulo de fuerzas: {modulo}')
    print(f'Error Fx: {error_fx}')
    print(f'Error Fy: {error_fy}')

if __name__ == "__main__":
    main()