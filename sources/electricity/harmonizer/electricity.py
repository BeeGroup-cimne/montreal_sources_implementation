import hashlib
import json
import os
import tempfile
from functools import partial
import utils
from neo4j import GraphDatabase

import settings
import morph_kgc
import pandas as pd
import rdflib
from utils.data_transformations import fuzzy_dictionary_match, fuzz_params
def df_to_formatted_json(df, sep="."):
    """
    The opposite of json_normalize
    """
    result = []
    for idx, row in df.iterrows():
        parsed_row = {}
        for col_label, v in row.items():
            keys = col_label.split(sep)

            current = parsed_row
            for i, k in enumerate(keys):
                if i == len(keys) - 1:
                    current[k] = v
                else:
                    if k not in current.keys():
                        current[k] = {}
                    current = current[k]
        result.append(parsed_row)
    return result

def harmonize_electricity(data, **kwargs):
    config = utils.utils.read_config(settings.conf_file)
    # df_geometry = pd.DataFrame(data)
    morph_config = '\n[DataSource1]\nmappings:sources/electricity/harmonizer/mapping.yaml\nfile_path: {d_file}\n'

    df = pd.read_csv('data/electricity/DonneesconsommationMTL.csv', dtype=object)

    # data = json.load(open("data/PostalCodes/bcn_postal_codes.geojson"))

    df.drop(['kWh_Moyen', 'kWh_std', 'pctIntervals', 'nbClients'], inplace=True, axis=1)

    df = df[df['CP3'] == 'H1K']

    freq = "PT15M"
    user = "MON"

    df.dropna(subset=['kWh'], inplace=True)
    df.dropna(subset=['CP3'], inplace=True)
    df.dropna(subset=['Secteur'], inplace=True)
    df['id'] = df['CP3'] + ' ' + df['Secteur']

    df = df.groupby('id', group_keys=False).apply(lambda x: x.sample(2)).reset_index(drop=True)

    df["electricityId"] = df['id'].apply(lambda x: (x + '-electricity').encode("utf-8"))
    df["electricityId"] = df['electricityId'].apply(lambda x: hashlib.sha256(x).hexdigest())

    # Load static data
    with open("sources/electricity/harmonizer/temp.json", "w") as d_file:
        json.dump({"electricity": df_to_formatted_json(df, sep=".")}, d_file)

    g_rdflib = morph_kgc.materialize(morph_config.format(d_file=d_file.name))
    os.unlink("sources/electricity/harmonizer/temp.json")
    neo = GraphDatabase.driver(**config['neo4j'])
    content = g_rdflib.serialize(format="ttl")
    content = content.replace('\\"', "&apos;")
    content = content.replace("'", "&apos;")

    with neo.session() as s:
        response = s.run(f"""CALL n10s.rdf.import.inline('{content}','Turtle')""")
        print(response.single())

    df['date'] = pd.to_datetime(df['DateInterval'])
    df['date'] = df['date'].dt.tz_convert("America/Toronto")
    df['start'] = df['date'].astype(int) // 10 ** 9
    df['end'] = df['date'].apply(lambda x: (x + pd.offsets.Minute(15))).astype(int) // 10 ** 9
    df["bucket"] = (df['start'].apply(int) // settings.ts_buckets) % settings.buckets
    df['isReal'] = True
    df.rename(columns={'kWh': 'value'}, inplace=True)

    # Load dynamic data


