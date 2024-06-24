import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import wave

VELOCIDAD_ANTERIOR_REBOTE_INICIAL = 2.42487


def main(ruta_archivo, ruta_archivo_csv, ruta_grafico):
    # Cargar el archivo de audio
    audio, tasa_muestreo = cargar_audio(ruta_archivo)

    # Obtener el envolvente del audio para detectar los picos
    envolvente = np.abs(audio)

    # Detectar los picos (momentos de impacto)
    umbral_minimo_picos = 500
    picos, _ = find_peaks(envolvente, height=umbral_minimo_picos, distance=int(tasa_muestreo * 0.1))

    # Convertir los picos a tiempos en segundos
    tiempos = picos / tasa_muestreo

    # Guardar los tiempos en un archivo CSV con 6 decimales
    np.savetxt(ruta_archivo_csv, tiempos, delimiter=',', fmt='%.6f')

    graficar(audio, envolvente, picos, tasa_muestreo, tiempos, ruta_grafico)

    coeficiente_de_restitucion(tiempos)



def cargar_audio(ruta_archivo):
    with wave.open(ruta_archivo, 'r') as archivo:
        tasa_muestreo = archivo.getframerate()
        num_frames = archivo.getnframes()
        audio = archivo.readframes(num_frames)
        audio = np.frombuffer(audio, dtype=np.int16)
    return audio, tasa_muestreo


def graficar(audio, envolvente, picos, tasa_muestreo, tiempos, ruta_grafico):
    plt.figure(figsize=(14, 5))
    plt.plot(np.linspace(0, len(audio) / tasa_muestreo, len(audio)), envolvente)
    plt.plot(tiempos, envolvente[picos], "x")
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.title('Detección de picos en el audio')

    # Guardar la imagen del gráfico antes de mostrarla
    plt.savefig(ruta_grafico)

    plt.show()


def coeficiente_de_restitucion(tiempos):
    rebotes = len(tiempos)
    coeficientes = []
    v_antes_rebote = []
    v_antes_rebote.append(VELOCIDAD_ANTERIOR_REBOTE_INICIAL)
    v_despues_rebote = []
    for i in range(1, rebotes):
        t1 = tiempos[i - 1]
        t2 = tiempos[i]
        v_antes_rebote.append(9.8 * (t2 - (t2/2)))
        v_despues_rebote.append(9.8 * ((t2/2) - t1))
    for i in range(1, rebotes-1):
        coef = v_despues_rebote[i] / v_antes_rebote[i]
        coeficientes.append(coef)
    # Promedio del coeficiente de restitución
    coef_restitucion_promedio = np.mean(coeficientes)
    print(f'coeficientes: {coeficientes}')
    print(f'Número de rebotes detectados: {rebotes}')
    print(f'Coeficiente de restitución promedio: {coef_restitucion_promedio:.4f}')


if __name__ == "__main__":
    ruta_audio = 'videos-y-audios/input.wav'
    ruta_archivo_csv = 'tablas/tiempos_rebote.csv'
    ruta_grafico = 'graficos/grafico_picos.png'

    main(ruta_audio, ruta_archivo_csv, ruta_grafico)

