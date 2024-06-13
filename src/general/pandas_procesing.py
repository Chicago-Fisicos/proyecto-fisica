import pandas as pd
import matplotlib.pyplot as plt

#variables
RUTA_CSV = "../chipi/tablas/trackeo-suavizado-curve-fit-nuevo-origen.csv"
RUTA_OUTPUT_CSV = "./output.csv"
RUTA_CARPETA_IMAGENES = "./graficas/" #Si esta carpeta no existe da error

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
    tiempo = tabla["Time"].iloc[1:]
    # tipo de grafico y variables a usar
    plt.scatter(tiempo, velocidad)
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
    tiempo = tabla["Time"]
    # tipo de grafico y variables a usar
    plt.scatter(tiempo, posicion)
    # etiquetas
    plt.xlabel('tiempo (segundos)')
    plt.ylabel('posicion (m)')
    # titulo
    plt.title('posicion en '+coordenada+' en el tiempo')

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
    tiempo = tabla["Time"].iloc[2:]
    # tipo de grafico y variables a usar
    plt.plot(tiempo, aceleracion)
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

    # tipo de grafico y variables a usar
    plt.plot(tabla["X"], tabla["Y"])
    # etiquetas
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
    tabla_nueva["accelerationX"] = calcular_aceleracion(tabla_nueva, "X")

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

    return tabla_nueva

##################################################
#           EJEMPLO DE EJECUCION                 #
##################################################

#leor el csv
tabla_movimiento = pd.read_csv(RUTA_CSV)

#agregar datos de movimiento a la tabla
tabla_movimiento = generar_datos_movimiento_metros(tabla_movimiento)

#graficos de la coordenada x
graficar_posicion_tiempo(tabla_movimiento, "X",1,1)
graficar_velocidad_tiempo(tabla_movimiento, "X",1,1)
graficar_aceleracion_tiempo(tabla_movimiento, "X",1,1)

#graficos de la coordenada y
graficar_posicion_tiempo(tabla_movimiento, "Y",1,1)
graficar_velocidad_tiempo(tabla_movimiento, "Y",1,1)
graficar_aceleracion_tiempo(tabla_movimiento, "Y",1,1)

#graficar posicion de x respecto a y
graficar_posicion_xy(tabla_movimiento,1,1)

tabla_movimiento.to_csv(RUTA_OUTPUT_CSV)