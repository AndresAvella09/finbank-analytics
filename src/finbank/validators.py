"""Validate the FinBank clients dataset."""

import pandas as pd


def validate_dataset(df):
    errors = []
    missing = [c for c in ['cliente_id', 'edad', 'ingreso_mensual', 'saldo_mora_30d', 'score_riesgo', 'tipo_cliente', 'activo'] if c not in df.columns]
    for c in missing:
        errors.append({'type': 'missing_column', 'column': c, 'message': 'columna faltante: ' + c})

    # null check over every column of the dataset
    for col in df.columns:
        n = df[col].isnull().sum()
        if n > 0:
            errors.append({'type': 'nulls', 'column': col, 'message': 'nulos en ' + col + ': ' + str(n)})

    # score range check
    if 'score_riesgo' in df.columns:
        fuera = df[(df['score_riesgo'] < 300) | (df['score_riesgo'] > 850)]
        if len(fuera) > 0:
            errors.append({'type': 'score_range', 'column': 'score_riesgo', 'message': 'score fuera de rango, debe estar entre 300 y 850'})

    # variable types check
    if 'edad' in df.columns and str(df['edad'].dtype) != 'int64':
        errors.append({'type': 'wrong_type', 'column': 'edad', 'message': 'edad deberia ser int64'})
    if 'ingreso_mensual' in df.columns and str(df['ingreso_mensual'].dtype) not in ('int64', 'float64'):
        errors.append({'type': 'wrong_type', 'column': 'ingreso_mensual', 'message': 'ingreso_mensual deberia ser int64 o float64'})
    if 'saldo_mora_30d' in df.columns and str(df['saldo_mora_30d'].dtype) != 'float64':
        errors.append({'type': 'wrong_type', 'column': 'saldo_mora_30d', 'message': 'saldo_mora_30d deberia ser float64'})

    return {'errors': errors}
