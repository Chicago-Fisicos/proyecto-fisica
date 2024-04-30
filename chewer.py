import time
import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
from video_converter import generate_h264_video

# Define the initial color configuration for detecting color
colour_config = {'hmin': 145, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 255, 'vmax': 255}

COLOUR_BALL_TRAJECTORY = (0, 0, 255) # red
COLOUR_BALL_CONTOUR = (0, 255, 0) # green

# lower = faster, higher = slower
VIDEO_SPEED = 20

# Size of video window. Default = 1, but is very big
# 0.55 for notebook
# 0.7 for big screen
VIDEO_WINDOW_SIZE = 0.7

DATA_CSV = 'data/chewer.csv'
INPUT_VIDEO = "videos/chewer-input.MOV"
OUTPUT_VIDEO_RAW = "videos/chewer-output-raw.mp4"
OUTPUT_VIDEO_CODEC_H264 = "videos/chewer-output-h264.mp4"

def analyze_video():

    # Initialize the video capture object
    cap = cv2.VideoCapture(INPUT_VIDEO)

    # Initialize ColorFinder object for color detection
    my_color_finder = ColorFinder(False) # false becouse we don't need detect colour

    path_points = []
    path_data = []  # List to store X, Y, Time
    start_time = time.time() # Initial time of the video

    # Video export configuration
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(OUTPUT_VIDEO_RAW, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))
    
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
        # minArea y maxArea son el area min y max que debe tener un contorno para ser considerado valido
        img_contours, contours = cvzone.findContours(img, mask, minArea=300, maxArea=8000)

        # List to store filtered contours
        filtered_contours = []

        if contours is not None:
            for cnt in contours:
                contour_points = cnt['cnt']
                x, y, _, _ = cv2.boundingRect(contour_points) # for each contour get X,Y

                # mitad de la pantalla en adelante la Y debe ser menor que 500
                # o a la izquierda de la pantalla la Y debe ser menor que 320 (para recortar aro)
                if (x > 600 and y < 500) or (x > 300 and y < 320):
                    filtered_contours.append(contour_points)
                    # Calcular el centro del contorno
                    M = cv2.moments(contour_points)
                    if M["m00"] != 0:
                        center_x = int(M["m10"] / M["m00"])
                        center_y = int(M["m01"] / M["m00"])
                        current_center = (center_x, center_y)
                        # Dibujar el punto en el centro del contorno
                        cv2.circle(img, current_center, 3, (255, 0, 0), -1)
                        path_points.append(current_center)
                        # Calcular el tiempo transcurrido desde el inicio del video
                        elapsed_time = time.time() - start_time
                        # Agregar datos de coordenadas (X, Y) y tiempo a la lista
                        path_data.append((current_center[0], current_center[1], elapsed_time))

        # Draw filtered contours on the original image
        if filtered_contours:
            cv2.drawContours(img, filtered_contours, -1, COLOUR_BALL_CONTOUR, 2)

        # Draw the line that follows the path of the contour center in real-time
        if len(path_points) > 1:
            for i in range(1, len(path_points)):
                cv2.line(img, path_points[i - 1], path_points[i], COLOUR_BALL_TRAJECTORY, 2)

        # Write frame to output video
        out.write(img)

        # Resize and display the image
        img = cv2.resize(img, (0,0), None, VIDEO_WINDOW_SIZE, VIDEO_WINDOW_SIZE)
        cv2.imshow('Image Contours', img)

        # Check for quit command
        if cv2.waitKey(VIDEO_SPEED) & 0xFF == ord('q'):
            break

    # Save (X, Y, Time) to a CSV file
    with open(DATA_CSV, 'w') as f:
        f.write("X,Y,Time\n")
        for point in path_data:
            f.write(f"{point[0]},{point[1]},{point[2]}\n")

    # Release video resources
    out.release()
    cap.release()
    cv2.destroyAllWindows()

    
   # Obtener las dimensiones máximas del video original
    max_original_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    max_original_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Tamaño máximo del video original - X:", max_original_width, "Y:", max_original_height)

    # Tamaño máximo del video después de la redimensión
    max_resized_width = int(max_original_width * VIDEO_WINDOW_SIZE)
    max_resized_height = int(max_original_height * VIDEO_WINDOW_SIZE)
    print("Tamaño máximo del video redimensionado - X:", max_resized_width, "Y:", max_resized_height)

    
    generate_h264_video(OUTPUT_VIDEO_RAW, OUTPUT_VIDEO_CODEC_H264)


def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Coordenadas del clic - X:", x, "Y:", y)
        # Aquí puedes hacer lo que quieras con las coordenadas (x, y)

if __name__ == "__main__":
    analyze_video()
