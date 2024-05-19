import cv2

from src.general.calculate_velocity_and_acceleration import calculate_velocity_and_acceleration


# Draw velocity and acceleration vectors
def draw_velocity_vectors(img, trackeo_list):
    # colour vector
    colour_velocity_vector = (255, 0, 0)  # blue

    # scale vector
    velocity_scale = 0.1

    velocities, accelerations = calculate_velocity_and_acceleration(trackeo_list)

    for i, (vx, vy, _) in enumerate(velocities):
        start_point = (int(trackeo_list[i][0]), int(trackeo_list[i][1]))
        end_point = (int(trackeo_list[i][0] + vx * velocity_scale), int(trackeo_list[i][1] + vy * velocity_scale))
        cv2.arrowedLine(img, start_point, end_point, colour_velocity_vector, 2)

