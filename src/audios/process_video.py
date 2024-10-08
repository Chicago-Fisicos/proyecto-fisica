import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
from moviepy.editor import VideoFileClip, AudioFileClip

# Import your custom modules
from src.general.change_origin_parse_table import change_origin_trackeo, cambiar_origen_a_coordenadas_especificas
from src.general.draw_acceleration_vectors import draw_acceleration_vectors
from src.general.draw_cartesian_axes import draw_cartesian_axes
from src.general.draw_velocity_vectors import draw_velocity_vectors
from src.general.suavizar_tabla import suavizar_curve_fit, suavizar_savitzky, graficar

# Size of video window. Default = 1, but is very big
# 0.55 for notebook
# 0.7 for big screen
VIDEO_WINDOW_SIZE = 0.7  # NO CAMBIARLO PORQUE MODIFICA EL TAMAÑO DEL EJE DE COORDENADAS

TRACKEO_ORIGINAL = 'tablas/trackeo-original.csv'
TRACKEO_ORIGINAL_NUEVO_ORIGEN = 'tablas/trackeo-original-nuevo-origen.csv'

TRACKEO_SUAVIZADO_CURVE_FIT = "tablas/trackeo-suavizado-curve-fit.csv"
TRACKEO_SUAVIZADO_CURVE_FIT_NUEVO_ORIGEN = "tablas/trackeo-suavizado-curve-fit-nuevo-origen.csv"
NOMBRE_GRAFICO_CURVE_FIT = "graficos/curve_fit.png"

TRACKEO_SUAVIZADO_SAVITZKY = "tablas/trackeo-suavizado-savitzky.csv"
TRACKEO_SUAVIZADO_SAVITZKY_NUEVO_ORIGEN = "tablas/trackeo-suavizado-savitzky-nuevo-origen.csv"
NOMBRE_GRAFICO_SAVITZKY = "graficos/savitzky.png"

INPUT_VIDEO = "videos/input.mp4"
OUTPUT_VIDEO = "videos/output_no_audio.mp4"
FINAL_OUTPUT_VIDEO = "videos/output_with_audio.mp4"

######################### VARIABLES EDITABLES #########################
colour_config = {'hmin': 0, 'smin': 0, 'vmin': 212, 'hmax': 179, 'smax': 255, 'vmax': 255}

COLOUR_BALL = (0, 80, 255)
COLOUR_BALL_TRAJECTORY = (0, 0, 255)  # red

# ancho de la linea roja
BALL_CIRCLE_WIDTH = 2

# lower = faster, higher = slower
VIDEO_SPEED = 1


#######################################################################

def process_video():
    # Initialize the video capture object
    cap = cv2.VideoCapture(INPUT_VIDEO)

    # Initialize ColorFinder object for color detection
    my_color_finder = ColorFinder(False)  # false because we don't need to detect colour

    center_points = []
    trackeo_list = []  # List to store X, Y, Time

    # Get video info
    fps = get_fps(cap)
    frame_width, frame_height = get_frame_dimensions(cap)
    out = cv2.VideoWriter(OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(frame_width), int(frame_height)))
    print("Tamaño del video original - X:", frame_width, "Y:", frame_height)
    print("Tamaño del video redimensionado - X:", frame_width * VIDEO_WINDOW_SIZE, "Y:",
          frame_height * VIDEO_WINDOW_SIZE)

    # Crear una ventana para mostrar el video
    cv2.namedWindow('Image Contours')

    # Establecer la función de devolución de llamada del clic del ratón
    cv2.setMouseCallback('Image Contours', click_event)

    while True:
        success, img = cap.read()

        if not success:
            print("End of video")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break

        img_color, mask = my_color_finder.update(img, colour_config)
        # minArea y maxArea son el área min y max que debe tener un contorno para ser considerado válido
        img_contours, contours = cvzone.findContours(img, mask, minArea=1000, maxArea=10000)

        # List to store filtered contours
        filtered_contours = []

        if contours is not None:
            for cnt in contours:
                contour_points = cnt['cnt']
                x, y, _, _ = cv2.boundingRect(contour_points)

                if (868 < x < 1190 and y < 700):
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
        # if filtered_contours:
        #     cv2.drawContours(img, filtered_contours, -1, COLOUR_BALL_CONTOUR, 2)

        # for point in trackeo_list:
        #     current_center = (point[0], point[1])
        #     cv2.circle(img, current_center, BALL_CIRCLE_WIDTH, COLOUR_BALL, -1)

        # Draw the line that follows the path of the contour center in real-time
        if len(center_points) > 1:
            for i in range(1, len(center_points)):
                cv2.line(img, center_points[i - 1], center_points[i], COLOUR_BALL_TRAJECTORY, BALL_CIRCLE_WIDTH)

        # Guarda video nuevo
        out.write(img)

        # Resize and display the image
        img = cv2.resize(img, (0, 0), None, VIDEO_WINDOW_SIZE, VIDEO_WINDOW_SIZE)
        cv2.imshow('Image Contours', img)

        # Check for quit command
        if cv2.waitKey(VIDEO_SPEED) & 0xFF == ord('q'):
            break

    # Save (X, Y, Time) to a CSV file
    with open(TRACKEO_ORIGINAL, 'w') as f:
        f.write("X,Y,Time\n")
        for point in trackeo_list:
            x = round(point[0], 4)
            y = round(point[1], 4)
            time = round(point[2], 4)
            f.write(f"{x},{y},{time}\n")

    cambiar_origen_a_coordenadas_especificas(TRACKEO_ORIGINAL, 658, 700)
    '''
    # Cambio el origen del trackeo original
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

    # Add audio back to the processed video using moviepy
    add_audio_to_video(INPUT_VIDEO, OUTPUT_VIDEO, FINAL_OUTPUT_VIDEO)


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


def add_audio_to_video(input_video_path, output_video_no_audio_path, final_output_video_path):
    video = VideoFileClip(output_video_no_audio_path)
    audio = AudioFileClip(input_video_path)

    # Ensure the audio is correctly synchronized
    audio = audio.subclip(0, video.duration)

    final_video = video.set_audio(audio)
    final_video.write_videofile(final_output_video_path, codec='libx264', audio_codec='aac')


if __name__ == "__main__":
    process_video()
