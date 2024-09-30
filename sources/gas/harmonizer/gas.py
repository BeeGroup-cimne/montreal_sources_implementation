import json
import os
import tempfile
from functools import partial
import utils
from neo4j import GraphDatabase
import hashlib

import settings
import morph_kgc
import pandas as pd
import data_format_script
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

def harmonize_gas(data, **kwargs):
    config = utils.utils.read_config(settings.conf_file)
    # df_geometry = pd.DataFrame(data)
    morph_config = '\n[DataSource1]\nmappings:sources/gas/harmonizer/mapping.yaml\nfile_path: {d_file}\n'

    freq = "P1M"
    user = "MON"

    res_df, ci_df = data_format_script().data_format_script()

    #res

    res_df.dropna(subset=['value'], inplace=True)
    res_df.dropna(subset=['RTA'], inplace=True)
    res_df.dropna(subset=['Type chauffage'], inplace=True)
    res_df['id'] = res_df['RTA'] + '_res_' + res_df['Type chauffage']

    # df = df.groupby('id', group_keys=False).apply(lambda x: x.sample(2)).reset_index(drop=True)

    res_df["gasId"] = res_df['id'].apply(lambda x: (x + '-gas').encode("utf-8"))
    res_df["gasId"] = res_df['gasId'].apply(lambda x: hashlib.sha256(x).hexdigest())

    # Load res static data
    with open("sources/gas/harmonizer/temp.json", "w") as d_file:
        json.dump({"gas": df_to_formatted_json(res_df, sep=".")}, d_file)

    g_rdflib = morph_kgc.materialize(morph_config.format(d_file=d_file.name))
    os.unlink("sources/gas/harmonizer/temp.json")
    neo = GraphDatabase.driver(**config['neo4j'])
    content = g_rdflib.serialize(format="ttl")
    content = content.replace('\\"', "&apos;")
    content = content.replace("'", "&apos;")

    with neo.session() as s:
        response = s.run(f"""CALL n10s.rdf.import.inline('{content}','Turtle')""")
        print(response.single())


    res_df['date'] = pd.to_datetime(res_df['month'], format='%Y-%m')
    res_df['start'] = res_df['date'].astype(int) // 10 ** 9
    res_df['end'] = res_df['date'].apply(lambda x: (x + pd.offsets.MonthEnd())).astype(int) // 10 ** 9
    res_df["bucket"] = (res_df['start'].apply(int) // settings.ts_buckets) % settings.buckets
    res_df['isReal'] = True
    res_df.rename(columns={'kWh': 'value'}, inplace=True)

    # Load res dynamic data




    ci_df.dropna(subset=['value', 'RTA', 'SCIAN'], inplace=True)
    ci_df['id'] = ci_df['RTA'] + '_ci_' + ci_df['SCIAN']
    ci_df["gasId"] = ci_df['id'].apply(lambda x: (x + '-gas').encode("utf-8"))
    ci_df["gasId"] = ci_df['gasId'].apply(lambda x: hashlib.sha256(x).hexdigest())

    # Load ci static data
    with open("sources/gas/harmonizer/temp.json", "w") as d_file:
        json.dump({"gas": df_to_formatted_json(ci_df, sep=".")}, d_file)

    g_rdflib = morph_kgc.materialize(morph_config.format(d_file=d_file.name))
    os.unlink("sources/gas/harmonizer/temp.json")
    neo = GraphDatabase.driver(**config['neo4j'])
    content = g_rdflib.serialize(format="ttl")
    content = content.replace('\\"', "&apos;")
    content = content.replace("'", "&apos;")

    with neo.session() as s:
        response = s.run(f"""CALL n10s.rdf.import.inline('{content}','Turtle')""")
        print(response.single())

    # Load ci dynamic data