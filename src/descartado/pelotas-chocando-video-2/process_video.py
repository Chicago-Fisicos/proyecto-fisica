import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
from src.general.change_origin_parse_table import change_origin_trackeo
from src.general.draw_acceleration_vectors import draw_acceleration_vectors
from src.general.draw_cartesian_axes import draw_cartesian_axes
from src.general.draw_velocity_vectors import draw_velocity_vectors
from src.general.suavizar_tabla import suavizar_curve_fit, suavizar_savitzky, graficar


# Size of video window. Default = 1, but is very big
# 0.55 for notebook
# 0.7 for big screen
VIDEO_WINDOW_SIZE = 0.7  # NO CAMBIARLO PORQUE MODIFICA EL TAMAÑO DEL EJE DE COORDENADAS

TRACKEO_ORIGINAL_BASKET = 'tablas/trackeo-original-basket.csv'
TRACKEO_ORIGINAL_TENIS = 'tablas/trackeo-original-tenis.csv'
'''
TRACKEO_ORIGINAL = 'tablas/trackeo-original.csv'
TRACKEO_ORIGINAL_NUEVO_ORIGEN = 'tablas/trackeo-original-nuevo-origen.csv'

TRACKEO_SUAVIZADO_CURVE_FIT = "tablas/trackeo-suavizado-curve-fit.csv"
TRACKEO_SUAVIZADO_CURVE_FIT_NUEVO_ORIGEN = "tablas/trackeo-suavizado-curve-fit-nuevo-origen.csv"
NOMBRE_GRAFICO_CURVE_FIT = "graficos/curve_fit.png"

TRACKEO_SUAVIZADO_SAVITZKY = "tablas/trackeo-suavizado-savitzky.csv"
TRACKEO_SUAVIZADO_SAVITZKY_NUEVO_ORIGEN = "tablas/trackeo-suavizado-savitzky-nuevo-origen.csv"
NOMBRE_GRAFICO_SAVITZKY = "graficos/savitzky.png"
'''

INPUT_VIDEO = "videos/input.MOV"
OUTPUT_VIDEO = "videos/output.mp4"

######################### VARIABLES EDITABLES #########################
colour_config = {'hmin': 8, 'smin': 124, 'vmin': 0, 'hmax': 40, 'smax': 255, 'vmax': 255}

COLOUR_BALL_BASKET = (0, 80, 255)
COLOUR_BALL_TENIS = (51, 255, 100)

# tamaño puntos
BALL_CIRCLE_WIDTH = 5

# lower = faster, higher = slower
VIDEO_SPEED = 1

# Definimos el área mínima y máxima esperada para cada tipo de pelota
MIN_AREA_BASKETBALL = 500
MAX_AREA_BASKETBALL = 3000
MIN_AREA_TENNIS = 50
MAX_AREA_TENNIS = 300
#######################################################################

def process_video():

    # Initialize the video capture object
    cap = cv2.VideoCapture(INPUT_VIDEO)

    # Initialize ColorFinder object for color detection
    my_color_finder = ColorFinder(False)  # false because we don't need to detect colour

    # Get video info
    fps = get_fps(cap)
    frame_width, frame_height = get_frame_dimensions(cap)
    out = cv2.VideoWriter(OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(frame_width), int(frame_height)))
    print("Tamaño del video original - X:", frame_width, "Y:", frame_height)
    print("Tamaño del video redimensionado - X:", frame_width * VIDEO_WINDOW_SIZE, "Y:", frame_height * VIDEO_WINDOW_SIZE)

    # Crear una ventana para mostrar el video
    cv2.namedWindow('Image Contours')

    # Establecer la función de devolución de llamada del clic del ratón
    cv2.setMouseCallback('Image Contours', click_event)

    trackeo_list_basket = []
    trackeo_list_tenis = []

    while True:
        success, img = cap.read()

        if not success:
            print("End of video")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break

        img_color, mask = my_color_finder.update(img, colour_config)
        # minArea y maxArea son el área min y max que debe tener un contorno para ser considerado válido
        img_contours, contours = cvzone.findContours(img, mask, minArea=10, maxArea=5000)

        if contours:
            for cnt in contours:
                contour_points = cnt['cnt']
                x, y, _, _ = cv2.boundingRect(contour_points)

                if 314 < x < 1700 and 170 < y < 800:
                    area = cnt['area']
                    current_center = cnt['center']
                    current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
                    current_time_sec = current_time_ms / 1000

                    if MIN_AREA_BASKETBALL <= area <= MAX_AREA_BASKETBALL:
                        trackeo_list_basket.append((*current_center, current_time_sec))
                        cv2.circle(img, current_center, 3, COLOUR_BALL_BASKET, -1)
                    elif MIN_AREA_TENNIS <= area <= MAX_AREA_TENNIS:
                        trackeo_list_tenis.append((*current_center, current_time_sec))
                        cv2.circle(img, current_center, 3, COLOUR_BALL_TENIS, -1)

        for point in trackeo_list_basket:
            current_center = (point[0], point[1])
            cv2.circle(img, current_center, BALL_CIRCLE_WIDTH, COLOUR_BALL_BASKET, -1)

        for point in trackeo_list_tenis:
            current_center = (point[0], point[1])
            cv2.circle(img, current_center, BALL_CIRCLE_WIDTH, COLOUR_BALL_TENIS, -1)

        out.write(img)
        img = cv2.resize(img, (0, 0), None, VIDEO_WINDOW_SIZE, VIDEO_WINDOW_SIZE)
        cv2.imshow('Image Contours', img)

        if cv2.waitKey(VIDEO_SPEED) & 0xFF == ord('q'):
            break

    with open(TRACKEO_ORIGINAL_BASKET, 'w') as f:
        f.write("X,Y,Time\n")
        for point in trackeo_list_basket:
            x = round(point[0], 4)
            y = round(point[1], 4)
            time = round(point[2], 4)
            f.write(f"{x},{y},{time}\n")

    with open(TRACKEO_ORIGINAL_TENIS, 'w') as f:
        f.write("X,Y,Time\n")
        for point in trackeo_list_tenis:
            x = round(point[0], 4)
            y = round(point[1], 4)
            time = round(point[2], 4)
            f.write(f"{x},{y},{time}\n")

    # Cambio el origen del trackeo original
    '''
    change_origin_trackeo(TRACKEO_ORIGINAL, TRACKEO_ORIGINAL_NUEVO_ORIGEN)

    # Suavizo el trackeo original
    suavizar_curve_fit(TRACKEO_ORIGINAL, TRACKEO_SUAVIZADO_CURVE_FIT)
    suavizar_savitzky(TRACKEO_ORIGINAL, TRACKEO_SUAVIZADO_SAVITZKY)

    # Cambio el origen de los trackeos suavizados
    change_origin_trackeo(TRACKEO_SUAVIZADO_CURVE_FIT, TRACKEO_SUAVIZADO_CURVE_FIT_NUEVO_ORIGEN)
    change_origin_trackeo(TRACKEO_SUAVIZADO_SAVITZKY, TRACKEO_SUAVIZADO_SAVITZKY_NUEVO_ORIGEN)

    # Grafico el trackeo original y el suavizado (ambos con el nuevo origen)
    graficar(TRACKEO_ORIGINAL_NUEVO_ORIGEN, TRACKEO_SUAVIZADO_CURVE_FIT_NUEVO_ORIGEN, NOMBRE_GRAFICO_CURVE_FIT)
    graficar(TRACKEO_ORIGINAL_NUEVO_ORIGEN, TRACKEO_SUAVIZADO_SAVITZKY_NUEVO_ORIGEN, NOMBRE_GRAFICO_SAVITZKY)
    '''
    # Release video resources
    out.release()
    cap.release()
    cv2.destroyAllWindows()


def click_event(event, x, y, flags, params):
    # ESTO MUESTRA EL X,Y DEL VIDEO ORIGINAL!!! SIN REDIMENSION
    if event == cv2.EVENT_LBUTTONDOWN:
        # hacemos una division en x,y porque el video fue redimensionado
        # es decir, fue multiplicado por VIDEO_WINDOW_SIZE, por lo tanto se achicó la resolucion
        # esto se hizo para que entre el video en la pantalla.
        # al dividir, estamos obteniendo el pixel original
        print("Coordenadas del click - X:", x / VIDEO_WINDOW_SIZE, "Y:", y / VIDEO_WINDOW_SIZE)


def get_fps(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("FPS del video:", fps)
    return fps

def get_frame_dimensions(cap):
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return frame_width, frame_height


if __name__ == "__main__":
    process_video()
