import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from pydub import AudioSegment



def main(ruta_archivo):

    # Cargar el archivo de audio
    audio, tasa_muestreo = cargar_audio(ruta_archivo)

    # Normalizar el audio (opcional, dependiendo del caso)
    # audio = audio / np.max(np.abs(audio))

    # Obtener el envolvente del audio para detectar los picos
    envolvente = np.abs(audio)

    # Detectar los picos (momentos de impacto)
    umbral_minimo_picos = 1000
    picos, _ = find_peaks(envolvente, height=umbral_minimo_picos, distance=tasa_muestreo * 0.1)

    # Convertir los picos a tiempos en segundos
    tiempos = picos / tasa_muestreo

    graficar(audio, envolvente, picos, tasa_muestreo, tiempos)

    coeficiente_de_restitucion(tiempos)


def cargar_audio(ruta_archivo):
    audio = AudioSegment.from_file(ruta_archivo)
    muestras = np.array(audio.get_array_of_samples())
    tasa_muestreo = audio.frame_rate
    return muestras, tasa_muestreo


def graficar(audio, envolvente, picos, tasa_muestreo, tiempos):
    plt.figure(figsize=(14, 5))
    plt.plot(np.linspace(0, len(audio) / tasa_muestreo, len(audio)), envolvente)
    plt.plot(tiempos, envolvente[picos], "x")
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Detección de picos en el audio')
    plt.show()


def coeficiente_de_restitucion(tiempos):
    rebotes = len(tiempos)
    coeficientes = []
    for i in range(1, rebotes):
        t1 = tiempos[i - 1]
        t2 = tiempos[i]
        coef = np.sqrt(t2 / t1)
        coeficientes.append(coef)

    # Promedio del coeficiente de restitución
    coef_restitucion_promedio = np.mean(coeficientes)
    print(f'Número de rebotes detectados: {rebotes}')
    print(f'Coeficiente de restitución promedio: {coef_restitucion_promedio:.4f}')


if __name__ == "__main__":
    ruta_audio = '../audios/Golf2.m4a'
    main(ruta_audio)
