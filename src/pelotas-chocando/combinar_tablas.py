import pandas as pd


def combinar_tablas(csv_a_modificar, csv_a_borrar):

    # Cargar los dos CSVs
    df_a_modificar = pd.read_csv(csv_a_modificar)
    df_a_borrar = pd.read_csv(csv_a_borrar)

    # Renombrar las columnas de df2 para que coincidan con el nombre deseado en df_a_modificar
    df_a_borrar.rename(columns={'X': 'X_nuevo_origen_suavizado', 'Y': 'Y_nuevo_origen_suavizado'}, inplace=True)

    # Merge los dataframes basados en la columna 'Time'
    df_merged = pd.merge(df_a_modificar, df_a_borrar[['X_nuevo_origen_suavizado', 'Y_nuevo_origen_suavizado', 'Time']], on='Time')

    columnas = ['Time', 'X', 'Y', 'X_nuevo_origen', 'Y_nuevo_origen', 'X_nuevo_origen_suavizado',
                'Y_nuevo_origen_suavizado']
    df_merged = df_merged[columnas]

    # Guardar el resultado en un nuevo CSV
    df_merged.to_csv(csv_a_modificar, index=False)





