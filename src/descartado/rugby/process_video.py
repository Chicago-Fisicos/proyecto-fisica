import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
from src.general.change_origin_parse_table import change_origin_trackeo

# Size of video window. Default = 1, but is very big
# 0.55 for notebook
# 0.7 for big screen
VIDEO_WINDOW_SIZE = 0.7# NO CAMBIARLO PORQUE MODIFICA EL TAMAÑO DEL EJE DE COORDENADAS

TRACKEO = 'trackeo-original.csv'
TRACKEO_NEW_ORIGIN = "trackeo-mod.csv"

INPUT_VIDEO = "video-input.mp4"
OUTPUT_VIDEO = "video-output.mp4"

######################### VARIABLES EDITABLES #########################
colour_config = {'hmin': 74, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 124, 'vmax': 191}

COLOUR_BALL_TRAJECTORY = (0, 0, 255)  # red
COLOUR_BALL_CONTOUR = (0, 255, 0)  # green

# ancho de la linea roja
BALL_LINE_WIDTH = 2

# lower = faster, higher = slower
VIDEO_SPEED = 20


#######################################################################


def process_video():
    # Initialize the video capture object
    cap = cv2.VideoCapture(INPUT_VIDEO)

    # Initialize ColorFinder object for color detection
    my_color_finder = ColorFinder(False)  # false because we don't need to detect colour

    center_points = []
    trackeo_list = []  # List to store X, Y, Time

    # Video export configuration
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

    # Crear una ventana para mostrar el video
    cv2.namedWindow('Image Contours')

    # Establecer la función de devolución de llamada del clic del ratón
    cv2.setMouseCallback('Image Contours', click_event)

    # Obtener las dimensiones máximas del video original
    max_original_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    max_original_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Tamaño máximo del video original - X:", max_original_width, "Y:", max_original_height)

    # Tamaño máximo del video después de la redimensión
    max_resized_width = int(max_original_width * VIDEO_WINDOW_SIZE)
    max_resized_height = int(max_original_height * VIDEO_WINDOW_SIZE)
    print("Tamaño máximo del video redimensionado - X:", max_resized_width, "Y:", max_resized_height)

    while True:
        success, img = cap.read()

        if not success:
            print("End of video")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break

        img_color, mask = my_color_finder.update(img, colour_config)
        # minArea y maxArea son el area min y max que debe tener un contorno para ser considerado valido
        img_contours, contours = cvzone.findContours(img, mask, minArea=300, maxArea=8000)

        # List to store filtered contours
        filtered_contours = []

        if contours is not None:
            for cnt in contours:
                contour_points = cnt['cnt']
                x, y, _, _ = cv2.boundingRect(contour_points)  # for each contour get X,Y

                # mitad de la pantalla en adelante la Y debe ser menor que 500
                # o a la izquierda de la pantalla la Y debe ser menor que 320 (para recortar aro)
                #if (y < 540 and x > 360) or (x>100 and y<200):
                #if (50 < y < 343) and (x>500):
                if ((68 < y < 531) and (x>700)) or (y<307 and 498<x<700):
                    filtered_contours.append(contour_points)

                    # Calcular el centro del contorno
                    M = cv2.moments(contour_points)
                    if M["m00"] != 0:
                        center_x = int(M["m10"] / M["m00"])
                        center_y = int(M["m01"] / M["m00"])
                        current_center = (center_x, center_y)
                        # Dibujar el punto en el centro del contorno
                        cv2.circle(img, current_center, 3, (255, 0, 0), -1)
                        center_points.append(current_center)

                        # Agregar datos de coordenadas (X, Y) y tiempo a la lista
                        current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
                        current_time_sec = current_time_ms / 1000
                        trackeo_list.append((current_center[0], current_center[1], current_time_sec))

        # Dibuja contorno de la pelota
        if filtered_contours:
            cv2.drawContours(img, filtered_contours, -1, COLOUR_BALL_CONTOUR, 2)

        # Draw the line that follows the path of the contour center in real-time
        if len(center_points) > 1:
            for i in range(1, len(center_points)):
                cv2.line(img, center_points[i - 1], center_points[i], COLOUR_BALL_TRAJECTORY, BALL_LINE_WIDTH)

        # Guarda video nuevo
        out.write(img)

        # Resize and display the image
        img = cv2.resize(img, (0, 0), None, VIDEO_WINDOW_SIZE, VIDEO_WINDOW_SIZE)
        cv2.imshow('Image Contours', img)

        # Check for quit command
        if cv2.waitKey(VIDEO_SPEED) & 0xFF == ord('q'):
            break
        # fin while true

    # Save (X, Y, Time) to a CSV file
    with open(TRACKEO, 'w') as f:
        f.write("X,Y,Time\n")
        for point in trackeo_list:
            x = round(point[0] * VIDEO_WINDOW_SIZE, 4)
            y = round(point[1] * VIDEO_WINDOW_SIZE, 4)
            time = round(point[2], 4)
            f.write(f"{x},{y},{time}\n")

    change_origin_trackeo(TRACKEO, TRACKEO_NEW_ORIGIN)

    # Release video resources
    out.release()
    cap.release()
    cv2.destroyAllWindows()


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Coordenadas del click - X:", x/VIDEO_WINDOW_SIZE, "Y:", y/VIDEO_WINDOW_SIZE)


if __name__ == "__main__":
    process_video()