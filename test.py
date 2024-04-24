# Importa las bibliotecas necesarias
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# Construye el analizador de argumentos y analiza los argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="videos/basket-chewer-doble.MOV")
ap.add_argument("-b", "--buffer", type=int, default=64, help="tamaño máximo del buffer")
args = vars(ap.parse_args())

# Define los rangos de color para la pelota (ajusta estos valores según sea necesario)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# Inicializa el buffer de puntos para el seguimiento de la pelota
pts = deque(maxlen=args["buffer"])

# Inicializa el video stream
if args.get("video", False):
    vs = cv2.VideoCapture(args["video"])
else:
    vs = VideoStream(src=0).start()

# Bucle principal
while True:
    # Lee el frame actual
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    # Si no se lee un frame, termina el bucle
    if frame is None:
        break

    # Redimensiona el frame, aplica un desenfoque y convierte a espacio de color HSV
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Construye una máscara para el color "verde"
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Encuentra contornos en la máscara y encuentra el contorno más grande
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # Si se encontraron contornos, encuentra el centroide
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Dibuja el centroide y el radio de la pelota
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # Muestra el frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # Si se presiona 'q', termina el bucle
    if key == ord("q"):
        break

# Limpieza
cv2.destroyAllWindows()
vs.stop() if args.get("video", False) else vs.release()
