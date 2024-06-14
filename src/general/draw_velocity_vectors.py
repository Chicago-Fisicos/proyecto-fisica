import math

import cv2

from src.general.calculate_velocity_and_acceleration import calculate_velocity_and_acceleration


# Draw velocity vectors
def draw_velocity_vectors(img, trackeo_list):
    # colour vector
    colour_velocity_vector = (255, 0, 0)
    # thickness line
    thickness = 2
    # scale vector
    velocity_scale = 0.2

    # velocities contiene (vx,vy,t) calculados a partir de la info de trackeo_list
    # accelerations contiene (ax,ay,t) calculados a partir de la info de trackeo_list
    velocities, accelerations = calculate_velocity_and_acceleration(trackeo_list)

    # se recorre ignorando el tiempo, solo se usan los valores de vx y vy
    for i in range(0, len(velocities), 3):  # Inicia en 0, avanza de 3 en 3

        vx, vy, _ = velocities[i]

        # crea una tupla (x,y), es el punto de inicio del vector velocidad en la imagen
        # Ej: trackeo_list[0][0] -> agarra la componente x de la primer tupla (x,y,t) de trackeo_list
        start_point = (int(trackeo_list[i][0]), int(trackeo_list[i][1]))

        # Al sumar la posición inicial x con la componente vx, obtenemos la coordenada x del punto final del vector., lo mismo para y
        # se multiplica con velocity_scale para que sea vea mejor en el video
        end_point = (int(trackeo_list[i][0] + vx * velocity_scale), int(trackeo_list[i][1] + vy * velocity_scale))

        # Dibuja la línea con flecha en la imagen desde start_point hasta end_point
        cv2.arrowedLine(img, start_point, end_point, colour_velocity_vector, thickness)


