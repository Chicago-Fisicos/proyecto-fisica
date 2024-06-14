import pandas as pd


def separar_datos_por_choque(csv_file, tiempo_choque):
    df = pd.read_csv(csv_file)

    # Crear la nueva columna "choque"
    df['choque'] = df['Time'].apply(lambda x: 'antes' if x < tiempo_choque else 'despues')

    # Guardar el archivo CSV con la nueva columna
    df.to_csv(csv_file, index=False)

    # Dividir el DataFrame en dos basado en el valor de la columna 'choque'
    df_antes = df[df['choque'] == 'antes'].copy()  # Crear una copia para evitar SettingWithCopyWarning
    df_despues = df[df['choque'] == 'despues'].copy()  # Crear una copia para evitar SettingWithCopyWarning

    # Eliminar la columna 'choque' para mantener el formato original del archivo
    #df.drop(columns=['choque'], inplace=True)
    df_antes.drop(columns=['choque'], inplace=True)
    df_despues.drop(columns=['choque'], inplace=True)

    # Definir nombres de archivo para los archivos de salida
    archivo_antes = f'{csv_file.replace(".csv", "")}-antes-de-choque.csv'
    archivo_despues = f'{csv_file.replace(".csv", "")}-despues-de-choque.csv'

    # Guardar los DataFrames en archivos CSV
    df.to_csv(csv_file, index=False)
    df_antes.to_csv(archivo_antes, index=False)
    df_despues.to_csv(archivo_despues, index=False)


if __name__ == "__main__":
    TRACKEO_ORIGINAL_BASKET = "tablas/trackeo-original-basket.csv"
    TRACKEO_ORIGINAL_TENIS = "tablas/trackeo-original-tenis.csv"

    # Agregar la columna 'choque' y obtener el DataFrame modificado
    separar_datos_por_choque(TRACKEO_ORIGINAL_BASKET, 0.68)
    separar_datos_por_choque(TRACKEO_ORIGINAL_TENIS, 0.7)
