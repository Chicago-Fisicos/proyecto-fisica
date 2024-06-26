import csv

# Leer datos desde el archivo CSV
# Devuelve una lista de tuplas (x,y,t)
def read_tracking_data(file_path):
    trackeo_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Omitir el encabezado si existe
        for row in reader:
            x, y, t = float(row[0]), float(row[1]), float(row[2])
            trackeo_list.append((x, y, t))
    return trackeo_list