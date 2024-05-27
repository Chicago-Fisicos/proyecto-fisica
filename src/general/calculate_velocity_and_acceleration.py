from src.general.change_origin_parse_table import change_origen_single


def calculate_velocity_and_acceleration(trackeo_list):
    velocities = []
    accelerations = []

    for i in range(1, len(trackeo_list)):

        # Para cada par de puntos consecutivos, se extraen las coordenadas (x, y, t)

        origen_x1 = float(trackeo_list[i - 1][0])
        origen_y1 = float(trackeo_list[i - 1][1])
        origen1 = (origen_x1, origen_y1)

        #se modifican los valores para que coincidan con el archivo trackeo_mod
        x1, y1 = change_origen_single(trackeo_list[i - 1][0], trackeo_list[i - 1][1], origen1)
        x2, y2 = change_origen_single(trackeo_list[i][0], trackeo_list[i][1], origen1)

        # Se calcula el dt entre los dos puntos.
        t1 = trackeo_list[i-1][2]
        t2 = trackeo_list[i][2]

        dt = t2 - t1

        # Si es cero, se omite la iteración para evitar la división por cero.
        if dt == 0:
            continue

        # Se calculan las velocidades en x y en y, se almacenan los valores

        vx = (x2 - x1) / dt
        vy = (y2 - y1) / dt
        velocities.append((vx, vy, t2))

    for i in range(1, len(velocities)):

        # Para cada par de puntos consecutivos en velocities, se extraen las coordenadas (x, y, t)
        vx1, vy1, t1 = velocities[i - 1]
        vx2, vy2, t2 = velocities[i]

        # Se calcula el dt entre los dos puntos.
        dt = t2 - t1

        # Si es cero, se omite la iteración para evitar la división por cero.
        if dt == 0:
            continue

        ## Se calculan las aceleraciones en x y en y, se alamacenan los valores
        ax = 0 / dt
        #ax = (vx2 - vx1) / dt
        ay = (vy2 - vy1) / dt
        accelerations.append((ax, ay, t2))

    return velocities, accelerations
