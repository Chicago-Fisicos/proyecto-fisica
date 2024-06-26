import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#variables
RUTA_CSV = "tablas/trackeo-suavizado-curve-fit-nuevo-origen.csv"
RUTA_OUTPUT_CSV = "tablas/tabla-moviento-metros.csv"
RUTA_CARPETA_IMAGENES = "graficos/" #Si esta carpeta no existe da error

### este valor se calcula a partir comparar la medida de un objeto en el video y en la realidad
### debe ser calculado para cada video
VALOR_PIXEL_METRO = 0.447 / 100

def parsear_a_metros(valorPixel):
    """
    Multiplica el valor dado `valorPixel` por la constante `VALOR_PIXEL_METRO` y devuelve el resultado.

    Args:
        valorPixel (float): El valor a multiplicar.

    Returns:
        float: El resultado de la multiplicación.
    """
    return valorPixel * VALOR_PIXEL_METRO

def calcular_velocidad(tabla, columna):
    """
    Calcula la velocidad de un objeto basándose en la tabla y columna dadas.

    Args:
        tabla (pandas.DataFrame): La tabla que contiene los datos.
        columna (str): El nombre de la columna que contiene los datos de posición.

    Returns:
        pandas.Series: La velocidad del objeto en el tiempo.
    """
    # Asegurarse de que los datos son flotantes para la operación
    tabla[columna] = tabla[columna].astype(float)
    tabla["Time"] = tabla["Time"].astype(float)

    # Calcular la diferencia entre filas consecutivas
    delta_posicion = tabla[columna].diff().fillna(0)
    delta_tiempo = tabla["Time"].diff().fillna(0)

    # Evitar la división por cero
    velocidad = delta_posicion / delta_tiempo.replace(0, 1)

    return velocidad


def calcular_aceleracion(tabla, columna):
    """
    Calcula la aceleración de una columna dada en un DataFrame calculando la diferencia en velocidad entre filas consecutivas y dividiéndola por la diferencia en tiempo entre filas consecutivas.

    Args:
        tabla (pandas.DataFrame): El DataFrame que contiene los datos.
        columna (str): El nombre de la columna para la cual se calculará la aceleración.
    Returns:
        aceleracion (pandas.Series): Un objeto Series que contiene los valores de aceleración calculados para cada fila.
    """
    # Asegurarse de que los datos son flotantes para la operación
    velocidad = "velocity" + columna
    tabla["Time"] = tabla["Time"].astype(float)
    tabla[velocidad] = tabla[velocidad].astype(float)

    # Calcular la diferencia entre filas consecutivas
    delta_velocidad = tabla[velocidad].diff().fillna(0)
    delta_tiempo = tabla["Time"].diff().fillna(0)

    # Evitar la división por cero
    aceleracion = round(delta_velocidad / delta_tiempo.replace(0, 1), 2)
    return aceleracion


def graficar_velocidad_tiempo(tabla, coordenada, guardar_grafica=None, mostrar_grafica=None):
    """
    Genera un gráfico de dispersión de velocidad contra tiempo para una coordenada dada.

    Args:
        tabla (pandas.DataFrame): El DataFrame que contiene los datos.
        coordenada (str): El nombre de la columna para la cual se calculará la velocidad.
        guardar_grafica (bool, opcional): Si es True, guarda el gráfico como una imagen. Por defecto es None.
        mostrar_grafica (bool, opcional): Si es True, muestra el gráfico. Por defecto es None.

    Returns:
        None
    """

    vel_coor = "velocity" + coordenada
    velocidad = tabla[vel_coor].iloc[1:]
    velocidad_teorica = tabla["vel_"+coordenada+"_teorica"].iloc[1:]
    tiempo = tabla["Time"].iloc[1:]
    # tipo de grafico y variables a usar
    fig , ax = plt.subplots()
    ax.plot(tiempo, velocidad_teorica, color="blue", label="teorica")
    ax.plot(tiempo, velocidad, color="red", label="real")
    ax.legend()
    # etiquetas
    plt.xlabel('tiempo (segundos)')
    plt.ylabel('velocidad (m/s)')
    # titulo
    plt.title('velocidad en '+coordenada+' en el tiempo')

    if guardar_grafica:
        plt.savefig(RUTA_CARPETA_IMAGENES + "velocidad_tiempo_" + coordenada + ".png")
    if mostrar_grafica:
        plt.show()


def graficar_posicion_tiempo(tabla, coordenada, guardar_grafica=None, mostrar_grafica=None):
    """
    Genera un gráfico de dispersión de posición contra tiempo para una determinada coordenada en un DataFrame.

    Args:
        tabla (pandas.DataFrame): El DataFrame que contiene los datos.
        coordenada (str): El nombre de la columna para la que se dibujará la posición.
        guardar_grafica (bool, opcional): Si es True, guarda el gráfico como una imagen. Defaults a None.
        mostrar_grafica (bool, opcional): Si es True, muestra el gráfico. Defaults a None.

    Returns:
        None
    """
    posicion = tabla[coordenada]
    posicion_teorica = tabla["pos_"+coordenada+"_teorica"]
    tiempo = tabla["Time"]
    # tipo de grafico y variables a usar
    fig, ax = plt.subplots()
    ax.plot(tiempo, posicion_teorica, color='blue', label='teorica')
    ax.scatter(tiempo, posicion, color='red', label='real')
    ax.legend()
    # etiquetas
    plt.xlabel('tiempo (segundos)')
    plt.ylabel('posicion (m)')
    # titulo
    plt.title('posicion en '+coordenada+' en el tiempo')
    #plt.ylim(-1, 5)

    if guardar_grafica:
        plt.savefig(RUTA_CARPETA_IMAGENES + "posicion_tiempo_" + coordenada + ".png")
    if mostrar_grafica:
        plt.show()


def graficar_aceleracion_tiempo(tabla, coordenada, guardar_grafica=None, mostrar_grafica=None):
    """
    Genera un gráfico de aceleración en el tiempo para una coordenada dada en un DataFrame de pandas.

    Args:
        tabla (pandas.DataFrame): El DataFrame que contiene los datos.
        coordenada (str): El nombre de la columna para la cual calcular la aceleración.
        guardar_grafica (bool, opcional): Si es True, guarda el gráfico como una imagen. Defaults a None.
        mostrar_grafica (bool, opcional): Si es True, muestra el gráfico. Defaults a None.

    Returns:
        None
    """
    accCoor = "acceleration" + coordenada
    aceleracion = tabla[accCoor].iloc[2:]
    aceleracion_teorica = tabla["acc_"+coordenada+"_teorica"].iloc[2:]
    tiempo = tabla["Time"].iloc[2:]
    fig, ax = plt.subplots()
    # tipo de grafico y variables a usar
    ax.plot(tiempo, aceleracion_teorica, color="blue", label="teorica")
    ax.plot(tiempo, aceleracion, color="red", label="real")
    ax.legend()
    # etiquetas
    plt.xlabel('tiempo (segundos)')
    plt.ylabel('aceleracion (m/s^2)')
    # titulo
    plt.title('aceleracion en '+coordenada+' en el tiempo')

    if guardar_grafica:
        plt.savefig(RUTA_CARPETA_IMAGENES + "aceleracion_tiempo_" + coordenada + ".png")
    if mostrar_grafica:
        plt.show()

def graficar_posicion_xy(tabla, guardar_grafica=None, mostrar_grafica=None):
    """
    Grafica la posición de la nave en el eje X contra el eje Y en un DataFrame de pandas.

    Args:
        tabla (pandas.DataFrame): El DataFrame que contiene los datos.
        guardar_grafica (bool, opcional): Si es True, guarda el gráfico como una imagen. Defaults a None.
        mostrar_grafica (bool, opcional): Si es True, muestra el gráfico. Defaults a None.

    Returns:
        None
    """
    fig, ax = plt.subplots()

    # tipo de grafico y variables a usar
    ax.plot(tabla["X"], tabla["Y"], color="red", label="real")
    ax.plot(tabla["pos_X_teorica"], tabla["pos_Y_teorica"], color="blue", label="teorica")    # etiquetas
    plt.xlabel('posicion en el eje X (m)')
    plt.ylabel('posicion en el eje Y (m)')
    # titulo
    plt.title('Posicion')

    if guardar_grafica:
        plt.savefig(RUTA_CARPETA_IMAGENES + "posicion_xy.png")
    if mostrar_grafica:
        plt.show()

def agregar_datos_movimiento(tabla):
    """
        Agrega columnas de velocidad y aceleración a una tabla de datos.

        Args:
            tabla (pandas.DataFrame): La tabla de datos a la que se le agregarán las columnas.

        Returns:
            pandas.DataFrame: La nueva tabla con columnas adicionales para X, Y, velocityX, velocityY, accelerationY y accelerationX.
        """
    tabla_nueva = tabla.copy()
    tabla_nueva["velocityX"] = calcular_velocidad(tabla_nueva, "X")
    tabla_nueva["velocityY"] = calcular_velocidad(tabla_nueva, "Y")
    tabla_nueva["accelerationY"] = calcular_aceleracion(tabla_nueva, "Y")

    return tabla_nueva

def generar_datos_teoricos(tabla):
    tabla_nueva = tabla.copy()
    tabla_nueva = generar_datos_x_teorica(tabla_nueva)
    tabla_nueva = generar_datos_y_teorica(tabla_nueva)

    return tabla_nueva

def generar_datos_movimiento_metros(tabla):
    """
    Genera nuevos datos para el movimiento en metros.

    Args:
        tabla (pandas.DataFrame): La tabla de entrada.

    Returns:
        pandas.DataFrame: La nueva tabla con columnas adicionales para X e Y, velocityX, velocityY, accelerationY y accelerationX.
    """
    tabla_nueva = tabla.copy()
    tabla_nueva["X"] = tabla_nueva["X"].apply(parsear_a_metros)
    tabla_nueva["Y"] = tabla_nueva["Y"].apply(parsear_a_metros)
    tabla_nueva = agregar_datos_movimiento(tabla_nueva)

    tabla_nueva =  generar_datos_teoricos(tabla_nueva)
    return tabla_nueva

def velocidad_inicial_x_teorica(tabla):
    """
    Calcula la velocidad inicial en el eje x teórico.

    Args:
        tabla (pandas.DataFrame): La tabla de datos.

    Returns:
        float: La velocidad inicial en el eje x teórico.
    """
    delta_t = tabla["Time"].iloc[-1] - tabla["Time"].iloc[0]
    delta_x = tabla["X"].iloc[-1] - tabla["X"].iloc[0]
    return delta_x / delta_t

def velocidad_inicial_y_teorica(tabla):
    """
    Calcula la velocidad inicial en el eje y teórica.

    Args:
        tabla (pandas.DataFrame): La tabla de datos.

    Returns:
        float: La velocidad inicial en el eje y teórica.
    """
    t = tabla["Time"].iloc[-1] - tabla["Time"].iloc[0]
    y_final = tabla["Y"].iloc[-1]
    y_inicial = tabla["Y"].iloc[0]
    g = 9.81

    return (y_final - y_inicial + g * (t ** 2) * 0.5)/t

def calcular_posicion_x(x_inicial, v_inicial, t):
    """
        Calcula la posición en el eje x dada la posición inicial, la velocidad inicial y el tiempo.
        Siguiendo un movimiento rectilineo y uniforme.
        Parameters:
            x_inicial (float): La posicion inicial en el eje x.
            v_inicial (float): La velocidad inicial en el eje x.
            t (float): Tiempo.
        Returns:
            float: La posición en el eje x después del tiempo t.
        """
    return (x_inicial + v_inicial * t).round(6)

def calcular_posicion_y(y_inicial, v_inicial, t):
    """
    Calculate the position in the y-axis given the initial position, initial velocity, and time.
    Siguiendo un movimiento uniformemente variado.

    Parameters:
        y_inicial (float): La posicion inicial en el eje y.
        v_inicial (float): La velocidad inicial en el eje y.
        t (float): El tiempo.

    Returns:
        float: La posición en el eje x después del tiempo t.
    """
    g = 9.81
    return (y_inicial + v_inicial * t - 0.5 * g * (t ** 2)).round(6)

def generar_datos_x_teorica(tabla):
    tabla_nueva = tabla.copy()
    x_inicial = tabla_nueva["X"].iloc[0]
    v_inicial = velocidad_inicial_x_teorica(tabla_nueva)
    tiempo = tabla_nueva["Time"]-tabla_nueva["Time"].iloc[0]
    tabla_nueva["pos_X_teorica"] = calcular_posicion_x(x_inicial, v_inicial, tiempo)
    tabla_nueva["vel_X_teorica"] = v_inicial
    return tabla_nueva


def calcular_velocidad_y(v_inicial, tiempo):
    return (v_inicial - 9.81 * tiempo).round(6)


def generar_datos_y_teorica(tabla):
    tabla_nueva = tabla.copy()
    y_inicial = tabla_nueva["Y"].iloc[0]
    v_inicial = velocidad_inicial_y_teorica(tabla_nueva)
    tiempo = tabla_nueva["Time"] - tabla_nueva["Time"].iloc[0]
    tabla_nueva["pos_Y_teorica"] = calcular_posicion_y(y_inicial, v_inicial, tiempo)
    tabla_nueva["vel_Y_teorica"] = calcular_velocidad_y(v_inicial, tiempo)
    tabla_nueva["acc_Y_teorica"] = -9.81

    return tabla_nueva

def energia_cinetica(tabla):
    velocidad_x : float = pd.to_numeric(tabla["velocityX"], errors="coerce")
    velocidad_y : float = pd.to_numeric(tabla["velocityY"], errors="coerce")

    return 0.5 * 0.62 * ((np.sqrt(velocidad_x** 2 + velocidad_y ** 2)) ** 2)

def energia_potencial(tabla):
    pos_y : float = pd.to_numeric(tabla["Y"], errors="coerce")
    return 9.81 * 0.62 * pos_y

def generar_datos_energia(tabla):
    tabla_nueva = tabla.copy()
    tabla_nueva["Energia_cinetica"] = energia_cinetica(tabla_nueva)
    tabla_nueva["Energia_potencial"] = energia_potencial(tabla_nueva)
    tabla_nueva["Energia_mecanica"] = tabla_nueva["Energia_cinetica"] + tabla_nueva["Energia_potencial"]
    return tabla_nueva

def graficar_energia(tabla,guardar_grafica=None, mostrar_grafica=None):

    # Crear una figura con dos líneas para representar las energías
    fig, ax = plt.subplots()

    tiempo = tabla["Time"].iloc[1:]
    cinetica = tabla["Energia_cinetica"].iloc[1:]
    potencial = tabla["Energia_potencial"].iloc[1:]
    mecanica = tabla["Energia_mecanica"].iloc[1:]
    mecanica_teorica = 13.6756

    ax.plot(tiempo, cinetica, color="blue", label="Energía cinética")
    ax.plot(tiempo, potencial, color="red", label="Energía potencial")
    ax.plot(tiempo, mecanica, color="green", label="Energía mecánica")
    ax.axhline(y=mecanica_teorica, color="purple", label="Energía mecánica teórica")

    ax.legend()

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Energía (J)")

    plt.title("Cambio de Energía en el Tiempo")

    # Mostrar la figura
    if mostrar_grafica:
        plt.show()
    if guardar_grafica:
        fig.savefig(RUTA_CARPETA_IMAGENES + "energia_mecanica.png")


def main():
    ##################################################
    #           EJEMPLO DE EJECUCION                 #
    ##################################################
    MOSTRAR_GRAFICOS = False
    # Importar datos de csv
    tabla_movimiento = pd.read_csv(RUTA_CSV)
    # agregar datos de movimiento a la tabla
    tabla_movimiento = generar_datos_movimiento_metros(tabla_movimiento)
    # graficos de la coordenada x
    graficar_posicion_tiempo(tabla_movimiento, "X", 1, MOSTRAR_GRAFICOS)
    graficar_velocidad_tiempo(tabla_movimiento, "X", 1, MOSTRAR_GRAFICOS)
    # graficos de la coordenada y
    graficar_posicion_tiempo(tabla_movimiento, "Y", 1, MOSTRAR_GRAFICOS)
    graficar_velocidad_tiempo(tabla_movimiento, "Y", 1, MOSTRAR_GRAFICOS)
    graficar_aceleracion_tiempo(tabla_movimiento, "Y", 1, MOSTRAR_GRAFICOS)
    # graficar posicion de x respecto a y
    graficar_posicion_xy(tabla_movimiento, 1, MOSTRAR_GRAFICOS)
    # generar datos de energia
    tabla_movimiento = generar_datos_energia(tabla_movimiento)
    # graficar energia
    graficar_energia(tabla_movimiento, 1, MOSTRAR_GRAFICOS)
    # exportar a csv
    tabla_movimiento = tabla_movimiento.round(6)
    tabla_movimiento.to_csv(RUTA_OUTPUT_CSV, index=False)

if __name__ == "__main__":
    main()

