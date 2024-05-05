import csv

INPUT = "data/chipi.csv"
OUTPUT = "data/chipi_parse.csv"

origen_x = 1218
origen_y = 443
mul_x = -1
mul_y = -1

def generar_archivo_nuevo(input, output):
    with open(input, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Ignorar la primera fila que contiene los encabezados
        datos = list(reader)

    nuevos_datos = []
    for x, y, tiempo in datos:
        new_x, new_y = change_origen(x,y)
        nuevos_datos.append((str(new_x), str(new_y), tiempo))

    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["X", "Y", "Time"])
        writer.writerows(nuevos_datos)

def change_origen(x,y):
    x = int(x)
    y = int(y)
    new_x = mul_x * (x- origen_x)
    new_y = mul_y * (y- origen_y)
    return (new_x, new_y)


if __name__ == "__main__":
    generar_archivo_nuevo(INPUT, OUTPUT)