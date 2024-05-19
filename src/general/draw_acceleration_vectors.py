import cv2

from src.general.calculate_velocity_and_acceleration import calculate_velocity_and_acceleration


def draw_acceleration_vectors(img, trackeo_list):
    # Colour vector
    colour_acceleration_vector = (255, 255, 0)
    # Scale vector
    acceleration_scale = 0.01

    velocities, accelerations = calculate_velocity_and_acceleration(trackeo_list)

    for i, (ax, ay, _) in enumerate(accelerations):
        start_point = (int(trackeo_list[i][0]), int(trackeo_list[i][1]))
        end_point = (int(trackeo_list[i][0] + ax * acceleration_scale), int(trackeo_list[i][1] + ay * acceleration_scale ) )
        cv2.arrowedLine(img, start_point, end_point, colour_acceleration_vector, 2)
