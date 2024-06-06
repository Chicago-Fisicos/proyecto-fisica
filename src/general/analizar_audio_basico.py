import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import csv

MOSTRAR_SOLO_X_MAYOR_A_0 = True  # default = False
UMBRAL_MINIMO = 0  # default = 0


def analizar_audio(ruta_audio):
    # Cargar el archivo de audio
    audio = AudioSegment.from_file(ruta_audio)

    # Obtener las muestras de audio
    muestras = audio.get_array_of_samples()

    # Obtener la tasa de muestreo del audio
    tasa_muestreo = audio.frame_rate

    # Crear un vector de tiempo
    duracion = len(muestras) / tasa_muestreo
    tiempo = np.linspace(0, duracion, len(muestras))

    # Obtener el valor absoluto de las muestras
    if MOSTRAR_SOLO_X_MAYOR_A_0:
        muestras = np.abs(muestras)

    # Descartar valores de amplitud menores que un cierto umbral y asignarles cero
    muestras = descartar_menores_que(muestras, umbral=UMBRAL_MINIMO)

    # Detectar los picos
    picos, _ = detectar_picos(tiempo, muestras)

    # Exportar los picos a un archivo CSV
    exportar_picos_a_csv(picos, 'picos.csv')

    # Graficar la forma de onda del audio y los picos
    graficar(duracion, muestras, tiempo, picos)


def descartar_menores_que(muestras, umbral):
    muestras_filtradas = np.where(np.abs(muestras) < umbral, 0, muestras)
    return muestras_filtradas


def detectar_picos(tiempo, muestras):
    # Detectar los picos en las muestras
    picos, _ = find_peaks(muestras)

    # Convertir los índices de los picos en coordenadas de tiempo
    tiempos_picos = tiempo[picos]

    return tiempos_picos, picos


def exportar_picos_a_csv(picos, nombre_archivo):
    # Escribir las coordenadas de los picos en un archivo CSV
    with open(nombre_archivo, mode='w', newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerow(['Tiempo (s)'])
        for pico in picos:
            escritor_csv.writerow([pico])


def graficar(duracion, muestras, tiempo, picos):
    picos_enteros = picos.astype(int)  # Convertir los índices de picos a enteros
    plt.figure(figsize=(14, 6))
    plt.plot(tiempo, muestras)
    plt.plot(tiempo[picos_enteros], muestras[picos_enteros], "x", color='red')  # Graficar los picos
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Forma de onda del audio con picos')

    # Configurar el número de marcas de tiempo en el eje x
    intervalo_tiempo = 0.5
    marcas_tiempo = np.arange(0, duracion + intervalo_tiempo, intervalo_tiempo)
    plt.xticks(marcas_tiempo)
    plt.show()



if __name__ == "__main__":
    ruta_audio = '../audios/Golf2.m4a'
    analizar_audio(ruta_audio)
