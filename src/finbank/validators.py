"""Validate the FinBank clients dataset."""

import pandas as pd


def validate_dataset(df):
    errores = []
    tipos = []

    # null check over the columns we care about
    for col in ['cliente_id', 'edad', 'ingreso_mensual', 'saldo_mora_30d', 'score_riesgo']:
        n = df[col].isnull().sum()
        if n > 0:
            errores.append('nulos en ' + col + ': ' + str(n))

    # score range check
    fuera = df[(df['score_riesgo'] < 300) | (df['score_riesgo'] >= 850)]
    score_fuera = len(fuera)
    if score_fuera > 0:
        errores.append('score fuera de rango, debe estar entre 300 y 850')

    # variable types check
    if str(df['edad'].dtype) != 'int64':
        tipos.append('edad deberia ser int64')
    if str(df['ingreso_mensual'].dtype) != 'float64':
        tipos.append('ingreso_mensual deberia ser float64')
    if str(df['saldo_mora_30d'].dtype) != 'float64':
        tipos.append('saldo_mora_30d deberia ser float64')

    return {'errores': errores, 'score_fuera_de_rango': score_fuera, 'tipos': tipos}
