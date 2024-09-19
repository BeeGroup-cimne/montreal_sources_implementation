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

def harmonize_rta(data, **kwargs):
    config = utils.utils.read_config(settings.conf_file)
    # df_geometry = pd.DataFrame(data)
    morph_config = '\n[DataSource1]\nmappings:sources/RTA/harmonizer/mapping.yaml\nfile_path: {d_file}\n'


    data = json.load(open("data/RTA/Montreal.geojson"))

    with open("data/RTA/data.json", "w") as d_file:
        json.dump({"rta": {"geojson": data['features']}}, d_file)

    json_data = json.load(open("data/RTA/data.json"))
    df_geometry = pd.json_normalize(json_data['rta']['geojson'])

    df_geometry['geometry.coordinates'] = df_geometry['geometry.coordinates'].apply(
        lambda x: ' '.join([str(item) for item in x]))


    with open("sources/RTA/harmonizer/temp.json", "w") as d_file:
        json.dump({"rta": {"geojson": df_to_formatted_json(df_geometry, sep=".")}}, d_file)

    g_rdflib = morph_kgc.materialize(morph_config.format(d_file=d_file.name))
    os.unlink("sources/RTA/harmonizer/temp.json")
    neo = GraphDatabase.driver(**config['neo4j'])
    content = g_rdflib.serialize(format="ttl")
    content = content.replace('\\"', "&apos;")
    content = content.replace("'", "&apos;")
    with neo.session() as s:
        response = s.run(f"""CALL n10s.rdf.import.inline('{content}','Turtle')""")
        print(response.single())
