from src.fran.process_video import process_video
from src.general.detect_colour import detect_colour

# obtiene la configuracion HSV para detectar la pelota
detect_colour('video-input.mp4', 80)

#process_video()