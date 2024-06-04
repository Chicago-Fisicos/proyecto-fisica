import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment


def m4a_to_wav():
    # Ruta del archivo de audio .m4a
    input_file = "../audios/Golf1.m4a"

    # Ruta donde guardar el archivo de audio convertido
    output_file = "Golf1.wav"

    # Convertir el archivo de audio .m4a a WAV
    audio = AudioSegment.from_file(input_file, format="m4a")
    audio.export(output_file, format="wav")


def detect_audio_sound():
    # Cargar el archivo de audio
    audio_file = "Golf1.wav"

    # Utilizar librosa para cargar el archivo de audio y extraer sus características
    y, sr = librosa.load(audio_file)

    # Calcular el espectrograma del audio
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

    # Mostrar el espectrograma
    plt.figure(figsize=(10, 5))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma')
    plt.show()


if __name__ == "__main__":
    m4a_to_wav()
