import math

import cv2
import numpy as np

from src.general.calculate_velocity_and_acceleration import calculate_velocity_and_acceleration


def draw_acceleration_vectors(img, trackeo_list):
    # Colour vector
    colour_acceleration_vector = (0, 143, 57)
    # thickness line
    thickness = 2
    # Length of acceleration vectors
    acceleration_length = 70  # Adjust this value to set the desired length of the acceleration vectors

    # velocities contiene (vx,vy,t) calculados a partir de la info de trackeo_list
    # accelerations contiene (ax,ay,t) calculados a partir de la info de trackeo_list
    velocities, accelerations = calculate_velocity_and_acceleration(trackeo_list)

    # se recorre ignorando el tiempo, solo se usan los valores de vx y vy
    for i in range(1, len(accelerations), 2):
        ax, ay, _ = accelerations[i]

        # Normalizar la aceleración para obtener la dirección
        acceleration_magnitude = math.sqrt(ax ** 2 + ay ** 2)
        if acceleration_magnitude == 0:
            # Evitar dividir por cero
            ax_normalized = ay_normalized = 0
        else:
            ax_normalized = ax / acceleration_magnitude
            ay_normalized = ay / acceleration_magnitude

        # crea una tupla (x,y), es el punto de inicio del vector velocidad en la imagen
        # Ej: trackeo_list[0][0] -> agarra la componente x de la primer tupla (x,y,t) de trackeo_list
        start_point = (int(trackeo_list[i][0]), int(trackeo_list[i][1]))

        # Al sumar la posición inicial x con la componente vx, obtenemos la coordenada x del punto final del vector., lo mismo para y
        # se multiplica con acceleration_scale para que sea vea mejor en el video
        end_point = (int(trackeo_list[i][0] + ax_normalized * -acceleration_length), int(trackeo_list[i][1] + ay_normalized * -acceleration_length) )
        cv2.arrowedLine(img, start_point, end_point, colour_acceleration_vector, thickness)
