import pandas as pd


def agregar_columna_choque(csv_file, tiempo_choque):
    df = pd.read_csv(csv_file)

    # Crear la nueva columna "choque"
    df['choque'] = df['Time'].apply(lambda x: 'antes' if x < tiempo_choque else 'despues')

    # Guardar el archivo CSV con la nueva columna (sobreescribir el original)
    df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    TRACKEO_ORIGINAL_BASKET = "tablas/trackeo-original-basket.csv"
    TRACKEO_ORIGINAL_TENIS = "tablas/trackeo-original-tenis.csv"

    agregar_columna_choque(TRACKEO_ORIGINAL_BASKET, 0.68)
    agregar_columna_choque(TRACKEO_ORIGINAL_TENIS, 0.7)
