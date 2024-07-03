import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leer el archivo CSV
data = pd.read_csv('tablas/tabla-moviento-metros-practico.csv')

# Variables
altura_aro = 3.05
altura_tiro_pelota = 2.81
g = 9.81
velocidad_inicial_x = 4.064
velocidad_inicial_y = 4.858

# Calcular el tiempo relativo
tiempo = data['Time'] - data['Time'].iloc[0]

# Obtener el último valor de X trackeado
ultimo_x_trackeado = data['X'].iloc[-1]

# Encontrar el tiempo correspondiente a ese último valor de X trackeado
tiempo_maximo = tiempo[data['X'] <= ultimo_x_trackeado].max()

# Filtrar los tiempos hasta el tiempo máximo
tiempo_filtrado = tiempo[tiempo <= tiempo_maximo]

# Calcular las posiciones x(t) y y(t) usando el tiempo filtrado
y_t = altura_tiro_pelota + velocidad_inicial_y * tiempo_filtrado - 0.5 * g * (tiempo_filtrado ** 2)
x_t = velocidad_inicial_x * tiempo_filtrado

# Redondear los valores para mejorar la legibilidad
tiempo_filtrado = round(tiempo_filtrado, 4)
y_t = round(y_t, 4)
x_t = round(x_t, 4)

x_t_lim = x_t
y_t_lim = y_t

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(x_t_lim, y_t_lim, label='Predicción', color='blue')
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.title('Predicción de tiro al aro')

Y_trackeado = data['Y'] + 2.81
X_trackeado = data['X']
plt.plot(X_trackeado, Y_trackeado, label='Tiro trackeado', color='red')

plt.scatter([3.472, 3.972], [3.05, 3.05], color='green', label='Aro de basquet')
# Agregar líneas verticales
plt.plot([3.472, 3.472], [3.05, 0], linestyle='--', color='green')
plt.plot([3.972, 3.972], [3.05, 0], linestyle='--', color='green')

plt.ylim(2, 5)
plt.legend()
plt.grid(True)
plt.savefig("graficos/prediccion-vs-trackeado.png")
plt.show()
