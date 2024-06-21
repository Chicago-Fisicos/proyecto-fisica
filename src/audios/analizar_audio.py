from src.general.analizar_audio import main as analizar_audio

ruta_audio = 'videos-y-audios/input.wav'
ruta_archivo_csv = 'tablas/tiempos_rebote.csv'
ruta_grafico = 'graficos/grafico_picos.png'

analizar_audio(ruta_audio,  ruta_archivo_csv, ruta_grafico)
