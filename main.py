import cv2
import cvzone
import numpy as np
from cvzone.ColorModule import ColorFinder

# Initialize the video
cap = cv2.VideoCapture('videos/basket-chewer-doble.MOV')

# basket-chewer-doble.MOV
hsvVals = {'hmin': 125, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 255, 'vmax': 255}



def detect_colour():
    myColorFinder = ColorFinder(True)
    while True:
        # Read the frame from the video
        success, img = cap.read()
        if not success:
            # If we've reached the end of the video, reset to the beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        img_edit, mask = myColorFinder.update(img, hsvVals)

        # Show the photo
        cv2.imshow('Detect Colour', img_edit)

        # Speed of video
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Release the video capture when done
    cap.release()
    cv2.destroyAllWindows()


def analyze_video():
    myColorFinder = ColorFinder(False)
    while True:
        success, img = cap.read()

        # Verificar si la imagen es válida antes de procesarla
        if not success:
            print("Fin del video, reiniciando...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Find the color ball
        img_color, mask = myColorFinder.update(img, hsvVals)
        # Find location of the ball
        img_contours, contours = cvzone.findContours(img, mask, minArea=800, maxArea=3000, )


        # Lista para almacenar los contornos filtrados
        filtered_contours = []

        # Filtrar contornos basados en el área
        if contours is not None:
            for cnt in contours:
                print(type(cnt))
                if isinstance(cnt, np.ndarray):
                    print("hola")
                    area = cv2.contourArea(cnt)
                    # Ajusta estos valores según lo que consideres apropiado para tu caso
                    if 1 < area < 999999:
                        print("Agrego a filtered contours")
                        filtered_contours.append(cnt)

        # Dibujar solo los contornos filtrados
        img_contours_filtered = np.zeros_like(img)
        if filtered_contours:
            print("Entro en filtered contours")
            cv2.drawContours(img, filtered_contours, -1, (0, 255, 0), 2)



        # Resize
        #img_contours = cv2.resize(img_contours, (0,0), None, 0.8, 0.8)

        # Display
        cv2.imshow('Image Contours', img)

        # Speed of video
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Liberar los recursos
    cap.release()
    cv2.destroyAllWindows()


def analyze_video_gris():
    myColorFinder = ColorFinder(False)
    while True:
        success, img = cap.read()

        if not success:
            print("Fin del video, reiniciando...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue


        # Definir la región de interés (ROI)
        height, width, _ = img.shape
        roi_top = int(height * 0.1)  # Definir el límite superior de la ROI, por ejemplo el 30% de la altura total
        roi = img[roi_top:height, :]  # ROI desde el límite superior hasta el final de la imagen



        img_color, mask = myColorFinder.update(roi, hsvVals)
        # Buscar contornos en la imagen binaria
        img_contours, contours = cvzone.findContours(roi, mask, minArea=800, maxArea=3000)

        # Lista para almacenar los contornos filtrados
        filtered_contours = []

        # Filtrar contornos basados en el área
        if contours is not None:
            for cnt in contours:
                # Acceder a los puntos del contorno a través de la clave 'cnt'
                contour_points = cnt['cnt']
                area = cnt['area']
                if 2000 < area < 3000:
                    filtered_contours.append(contour_points)

        # Dibujar solo los contornos filtrados directamente sobre la imagen original
        if filtered_contours:
            cv2.drawContours(img, filtered_contours, -1, (0, 255, 0), 2)


        # Resize
        img = cv2.resize(img, (0,0), None, 0.8, 0.8)
        # Display
        cv2.imshow('Image Contours', img)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



#detect_colour()

#analyze_video()
analyze_video_gris()

