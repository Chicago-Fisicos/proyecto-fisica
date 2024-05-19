def calculate_velocity_and_acceleration(points):
    velocities = []
    accelerations = []
    for i in range(1, len(points)):
        x1, y1, t1 = points[i - 1]
        x2, y2, t2 = points[i]

        dt = t2 - t1
        if dt == 0:
            continue

        vx = (x2 - x1) / dt
        vy = (y2 - y1) / dt
        velocities.append((vx, vy, t2))

    for i in range(1, len(velocities)):
        vx1, vy1, t1 = velocities[i - 1]
        vx2, vy2, t2 = velocities[i]

        dt = t2 - t1
        if dt == 0:
            continue

        ax = (vx2 - vx1) / dt
        ay = (vy2 - vy1) / dt
        accelerations.append((ax, ay, t2))

    return velocities, accelerations
