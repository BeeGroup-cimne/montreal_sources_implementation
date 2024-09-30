import pandas as pd
import numpy as np

months_dict = {
    'Janvier': '01',
    'Février': '02',
    'Mars': '03',
    'Avril': '04',
    'Mai': '05',
    'Juin': '06',
    'Juillet': '07',
    'Août': '08',
    'Septembre': '09',
    'Octobre': '10',
    'Novembre': '11',
    'Décembre': '12'
}


def data_format_script():

    # Res
    consumptions_res_df = pd.read_excel('data/gas/Conso_Moy_m³_RTA_SCIAN (Energir).xlsx', skiprows=1, sheet_name="RES",
                                    engine='openpyxl',
                                    dtype=str)
    consumptions_res_df = consumptions_res_df[consumptions_res_df['RTA'] == 'H1K']
    df_melted = pd.melt(consumptions_res_df,
                        id_vars=['RTA', 'Type chauffage', 'Nombre de clients É'],
                        var_name='month',
                        value_name='value')
    df_melted['month'] = df_melted['month'].map(months_dict)
    df_melted['month'] = '2019-' + df_melted['month']

    # CI
    consumptions_ci_df = pd.read_excel('data/gas/Conso_Moy_m³_RTA_SCIAN (Energir).xlsx', skiprows=1, sheet_name="CI",
                                    engine='openpyxl',
                                    dtype=str)
    consumptions_ci_df = consumptions_ci_df[consumptions_ci_df['RTA'] == 'H1K']
    df_ci_melted = pd.melt(consumptions_ci_df,
                        id_vars=['RTA', 'SCIAN', 'Nombre de client HQ', 'Nombre de clients É'],
                        var_name='month',
                        value_name='value')
    df_ci_melted['month'] = df_ci_melted['month'].map(months_dict)
    df_ci_melted['month'] = '2019-' + df_ci_melted['month']

    scian_df = pd.read_excel('data/gas/Conso_Moy_m³_RTA_SCIAN (Energir).xlsx', sheet_name="SCIAN",
                                       engine='openpyxl',
                                       dtype=str)
    dict_from_df = dict(zip(scian_df['SCIAN'], scian_df['Name']))
    df_ci_melted['Mapped_Values'] = df_ci_melted['SCIAN'].map(dict_from_df)
    return df_melted, df_ci_melted


if __name__ == '__main__':
    data_format_script()
