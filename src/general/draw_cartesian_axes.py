import cv2


def draw_cartesian_axes(img, origin_x, origin_y, end_line_eje_x, end_line_eje_y):
    # grosor en pixeles de la linea
    thikness = 2

    # permite controlar el tamaño de la punta de la flecha
    tip_length_factor_eje_x = 0.02
    tip_length_factor_eje_y = 0.04

    # Eje x
    cv2.arrowedLine(img, (0, origin_y), (end_line_eje_x, origin_y), (0, 0, 0), thikness,
                    tipLength=tip_length_factor_eje_x)
    # Eje y
    cv2.arrowedLine(img, (origin_x, 0), (origin_x, end_line_eje_y), (0, 0, 0), thikness,
                    tipLength=tip_length_factor_eje_y)

    # Eje x con flecha apuntando hacia la izquierda
    cv2.arrowedLine(img, (end_line_eje_x, origin_y), (0, origin_y), (0, 0, 0), thikness,
                    tipLength=tip_length_factor_eje_x)
    # Eje y con flecha apuntando hacia arriba
    cv2.arrowedLine(img, (origin_x, end_line_eje_y), (origin_x, 0), (0, 0, 0), thikness,
                    tipLength=tip_length_factor_eje_y)

    # Agrega nombres a los ejes
    cv2.putText(img, "eje x", (origin_x + 50, origin_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), thikness)
    cv2.putText(img, "eje y", (origin_x - 65, 0 + origin_y - 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), thikness)

