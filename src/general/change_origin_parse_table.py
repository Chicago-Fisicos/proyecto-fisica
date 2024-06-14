import csv
import pandas as pd

# los calculos chinos los hizo Jere,
# si estás leyendo esto y tenés dudas habla con él


def change_origin_trackeo(input, output, mul_x=-1, mul_y=-1):

    with open(input, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Ignorar la primera fila que contiene los encabezados
        datos = list(reader)

    # Obtener el primer valor de X y de Y
    origen_x = float(datos[0][0])
    origen_y = float(datos[0][1])
    origen = (origen_x, origen_y)

    lista_trackeo_mod = []
    nuevos_datos = []
    for x, y, tiempo in datos:
        new_x, new_y = change_origen_single(x, y, origen, mul_x, mul_y)
        nuevos_datos.append((str(new_x), str(new_y), tiempo))

    with open(output, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y", "Time"])
        writer.writerows(nuevos_datos)



def change_origen_single(x, y, origen, mul_x=-1, mul_y=-1):
    x = float(x)
    y = float(y)
    new_x = round(mul_x * (x - origen[0]), 4)
    new_y = round(mul_y * (y - origen[1]), 4)

    # fix -0.0 number
    if new_x == -0.0:
        new_x = 0.0
    if new_y == -0.0:
        new_y = 0.0
    return new_x, new_y


def cambiar_origen_a_coordenadas_especificas(csv_file, nuevo_origen_x, nuevo_origen_y):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file)

    # Calcular las nuevas coordenadas
    df['X_nuevo_origen'] = df['X'] - nuevo_origen_x
    df['Y_nuevo_origen'] = (df['Y'] - nuevo_origen_y) * -1

    # Guardar el archivo CSV con las nuevas columnas
    df.to_csv(csv_file, index=False)



if __name__ == "__main__":
    INPUT = "../chipi/trackeo-original.csv"
    OUTPUT = "../chipi/trackeo-mod.csv"
    #change_origin_trackeo(INPUT, OUTPUT)

    TRACKEO_ORIGINAL_BASKET = "trackeo-original-basket.csv"
    NUEVO_ORIGEN_X = 200  # Ejemplo de nueva coordenada X del origen
    NUEVO_ORIGEN_Y = 100  # Ejemplo de nueva coordenada Y del origen
    #transformar_origen(TRACKEO_ORIGINAL_BASKET, NUEVO_ORIGEN_X, NUEVO_ORIGEN_Y)
