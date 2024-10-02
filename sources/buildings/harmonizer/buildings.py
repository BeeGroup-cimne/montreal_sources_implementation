import json
import os

import utils
from neo4j import GraphDatabase
import settings
import morph_kgc
import pandas as pd
import rdflib

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

def harmonize_buildings(data, **kwargs):
    config = utils.utils.read_config(settings.conf_file)
    # df_geometry = pd.DataFrame(data)
    morph_config = '\n[DataSource1]\nmappings:sources/buildings/harmonizer/mapping.yaml\nfile_path: {d_file}\n'

    data = json.load(open("data/buildings/montreal_buildings_H1K.geojson"))

    with open("data/buildings/data.json", "w") as d_file:
        json.dump({"buildings": {"geojson": data['features']}}, d_file)

    json_data = json.load(open("data/buildings/data.json"))
    df_geometry = pd.json_normalize(json_data['buildings']['geojson'])

    df_geometry['geometry.coordinates'] = df_geometry['geometry.coordinates'].apply(
        lambda x: ' '.join([str(item) for item in x]))

    with open("sources/buildings/harmonizer/temp.json", "w") as d_file:
        json.dump({"buildings": {"geojson": df_to_formatted_json(df_geometry, sep=".")}}, d_file)

    # Load data
    g_rdflib = morph_kgc.materialize(morph_config.format(d_file=d_file.name))
    os.unlink("sources/buildings/harmonizer/temp.json")
    neo = GraphDatabase.driver(**config['neo4j'])
    content = g_rdflib.serialize(format="ttl")
    content = content.replace('\\"', "&apos;")
    content = content.replace("'", "&apos;")

    with neo.session() as s:
        response = s.run(f"""CALL n10s.rdf.import.inline('{content}','Turtle')""")
        print(response.single())

    # harmonize one building roof
    morph_config = '\n[DataSource1]\nmappings:sources/buildings/harmonizer/mapping_building_physics.yaml\nfile_path: {d_file}\n'

    data = json.load(open("data/buildings/montreal_buildings_H1K.geojson"))

    with open("data/buildings/data.json", "w") as d_file:
        json.dump({"buildings": {"geojson": data['features'][0]}}, d_file)

    json_data = json.load(open("data/buildings/data.json"))
    df_geometry = pd.json_normalize(json_data['buildings']['geojson'])

    with open("sources/buildings/harmonizer/temp.json", "w") as d_file:
        json.dump({"buildings": {"geojson": df_to_formatted_json(df_geometry, sep=".")}}, d_file)

    # Load data
    g_rdflib = morph_kgc.materialize(morph_config.format(d_file=d_file.name))
    os.unlink("sources/buildings/harmonizer/temp.json")
    neo = GraphDatabase.driver(**config['neo4j'])
    content = g_rdflib.serialize(format="ttl")
    content = content.replace('\\"', "&apos;")
    content = content.replace("'", "&apos;")

    with neo.session() as s:
        response = s.run(f"""CALL n10s.rdf.import.inline('{content}','Turtle')""")
        print(response.single())