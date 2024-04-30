import csv

INPUT = "data/chewer.csv"
OUTPUT = "data/chewer_parse.csv"

def generar_archivo_nuevo(input, output):
    with open(input, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Ignorar la primera fila que contiene los encabezados
        datos = list(reader)

    nuevos_datos = []
    for x, y, tiempo in datos:
        y_nuevo = -(int(y)-756)
        nuevos_datos.append((x, str(y_nuevo), tiempo))

    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["X", "Y", "Time"])
        writer.writerows(nuevos_datos)

generar_archivo_nuevo(INPUT, OUTPUT)
