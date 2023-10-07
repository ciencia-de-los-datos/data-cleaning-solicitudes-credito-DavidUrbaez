"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import numpy as np
import pandas as pd


def clean_data():
    def clean_money_amount(str_amount):
        if "$" in str_amount:
            str_amount = str_amount.replace(".00", "").replace(",", "").replace("$ ", "")
        return int(str_amount)

    df = pd.read_csv("solicitudes_credito.csv", sep=";", index_col=0)

    df['fecha_de_beneficio'] = pd.to_datetime(df['fecha_de_beneficio'], dayfirst=True, format='mixed')

    df['sexo'] = df['sexo'].str.strip().str.lower()

    df['tipo_de_emprendimiento'] = df['tipo_de_emprendimiento'].str.lower()

    df['idea_negocio'] = (
        df['idea_negocio'].str.lower()
        .str.replace("-", "_")
        .str.replace(" ", "_")
        .str.strip(" _-")
    )

    df['barrio'] = (
        df['barrio'].str.lower()
        # .str.replace("san jose de la cima no. ", "san jose de la cima no. XXXX")  # Check
        # .str.replace("el salado ", "el salado XXXXX")  # Check
        .str.replace("antonio nariño", "santonio nariño XXXX")  # Check
        # .str.strip(" _-")  # Check
        .str.replace(" ", "_").str.replace("-", "_")
        .str.replace(r"[áéíóúñ¿]", "*", regex=True)
        # .str.replace("belen", "bel*n") # Check
        .str.replace("andalucia", "andaluc*a")
        .str.replace("boyaca", "boyac*")
        .str.replace("'campo_valdes_no._1'", 'campo_vald*s_no.1', regex=False)
    )

    df['estrato'] = df['estrato'].astype(int)

    df["monto_del_credito"] = df["monto_del_credito"].apply(clean_money_amount).astype(int)

    df['línea_credito'] = (
        df['línea_credito'].str.lower()
        .str.strip(" _-")
        .str.replace(' ', '_').str.replace('-', '_')
        # .str.replace("soli_diaria", "solidaria")  # ¿?
    )

    # df = df.drop("comuna_ciudadano", axis=1)
    df = df.dropna(axis=0)
    df = df.drop_duplicates()

    return df


clean_data()
