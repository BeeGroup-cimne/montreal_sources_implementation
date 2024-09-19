# Buildings description

The building data source includes both detailed geometric information and specific building attributes, such as type,
size, number of floors, use (residential, commercial, industrial), age, and any other relevant characteristics.

## Gathering tool

This data source comes in GeoJSON file format and contains the geometric polygon and all information about the building.

#### RUN import application

To run the import application, execute the python script with the following parameters:

```bash
python3 -m gather -so buildings -f <file> -n <namespace> -u <user_importing> -tz <file_timezone> -st <storage>
```

## Raw Data Format

The data imported will be stored:

#### Buidings

````json
{
  "buildings": {
    "geojson": [
      {
        "type": "Feature",
        "properties": {
          "OBJECTID": 15,
          "OBJECTID_12_13_14_15": 15,
          "ID_UEV": "02028167",
          "CIVIQUE_DE": " 9101",
          "CIVIQUE_FI": " 9101",
          "NOM_RUE": "avenue \u00c9mile-Legault  (ANJ)",
          "SUITE_DEBU": " ",
          "MUNICIPALI": "50",
          "ETAGE_HORS": 1,
          "NOMBRE_LOG": 1,
          "ANNEE_CONS": 1986,
          "CODE_UTILI": "1000",
          "LETTRE_DEB": " ",
          "LETTRE_FIN": " ",
          "LIBELLE_UT": "Logement",
          "CATEGORIE_": "R\u00e9gulier",
          "MATRICULE8": "0053-71-4922-1-000-0000",
          "SUPERFICIE": 347,
          "SUPERFIC_1": 105,
          "NO_ARROND_": "REM09",
          "sum_etage_hors": 0.9999985619115167,
          "sum_nombre_log": 0.9999985619115167,
          "sum_superficie": 346.9995009832963,
          "sum_superfic_1": 104.99984900070925,
          "Polygon_Count": 1,
          "OBJECTID_1": 15,
          "Join_Count": 1,
          "TARGET_FID": 15,
          "CODEID": 34,
          "NOM": "Anjou",
          "NOM_OFFICI": "Anjou",
          "CODEMAMH": "REM09",
          "CODE_3C": "ANJ",
          "NUM": 9,
          "ABREV": "AJ",
          "TYPE": "Arrondissement",
          "COMMENT": " ",
          "DATEMODIF": "2022-08-24",
          "Shape_Length_1": 52.51830175251459,
          "Shape_Area_1": 105.04579975719392,
          "OBJECTID_12": 15,
          "Join_Count_1": 2,
          "TARGET_FID_1": 15,
          "g_objectid": 885669,
          "g_co_mrc": "66023",
          "g_code_mun": "66023",
          "g_arrond": "REM09",
          "g_anrole": "2022",
          "g_usag_pre": "R\u00e9sidentiel",
          "g_no_lot": "1110849",
          "g_nb_poly_": 1,
          "g_utilisat": "1000",
          "g_id_provi": "66023005371563250000000",
          "g_sup_tota": 347.47,
          "g_descript": "R\u00f4le d'\u00e9valuation",
          "g_nb_logem": 1,
          "g_nb_locau": 0,
          "g_shape_le": 0.00095737,
          "g_shape_ar": 4e-08,
          "g_dat_acqu": "2023-03-13 00:00:00.0000000",
          "g_dat_char": "2023-05-05 00:00:00.0000000",
          "Shape_Length_12": 83.75510476795777,
          "Shape_Area_12": 347.4450521314864,
          "OBJECTID_12_13": 15,
          "Join_Count_12": 1,
          "TARGET_FID_12": 15,
          "CFSAUID": "H1K",
          "DGUID": "2021A0011H1K",
          "PRUID": "24",
          "PRNAME": "Quebec / Qu\u00e9bec",
          "LANDAREA": 6.1714,
          "Shape_Length_12_13": 10419.034643627045,
          "Shape_Area_12_13": 6360028.451001342,
          "OBJECTID_12_13_14": 15,
          "Join_Count_12_13": 4,
          "TARGET_FID_12_13": 15,
          "COUNT_": 1,
          "COUNT_FC": 1,
          "Shape_Length_12_13_14": 43.59948210853762,
          "Shape_Area_12_13_14": 104.71946656302781,
          "OBJECTID_12_13_14_15_16": 15,
          "Join_Count_12_13_14": 2,
          "TARGET_FID_12_13_14": 15,
          "Step1_singlemore40sqm_NewHieght": 7,
          "Shape_Length_12_13_14_15": 0.0004821583415461357,
          "Shape_Area_12_13_14_15": 1.086863101972509e-08,
          "ORIG_FID": 15,
          "AREA_NEW": 105,
          "ORIG_FID_1": null,
          "MBG_Width": 7.1763380817171125,
          "MBG_Length": 14.885736706574077,
          "MBG_Orientation": 122.30351500269066,
          "Shape_Length": 44.12403746058595,
          "Shape_Area": 106.82429209641087,
          "BuidingCategory": null,
          "BuildingVolume": null,
          "AspectRatio": null,
          "SurfacetoVolumeRatio": null,
          "TotalFloorArea": null,
          "FloorNu_Calculated": null
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": "[[-73.55196434629887, 45.61807146664603], [-73.5520134721315, 45.618016864503865], [-73.55185207250884, 45.61794535679895], [-73.55180294786413, 45.617999958871835], [-73.55196434629887, 45.61807146664603]]"
        }
      }
    ]
  }
}
````

## Harmonization

The harmonization of the data will be done with the following mapping:

#### Building=>

| Origin                  | Harmonization                       |
|-------------------------|-------------------------------------|
| beginLifespanVersion    | s4bldg:Building-startState          | 
| conditionOfConstruction | s4bldg:Building-state               |
| beginning               | s4bldg:Building-startConstruction   |
| end                     | s4bldg:Building-endConstruction     |
| endLifespanVersion      | s4bldg:Building-endState            |
| informationSystem       | s4bldg:Building-cadasterDetailedUrl |
| reference               | s4bldg:Building-cadastralId         |
| currentUse              | s4bldg:Building-mainUse             |
| numberOfBuildingsUnits  | s4bldg:Building-buildingUnits       |
| numberOfDwellings       | s4bldg:Building-dwellings           |
| officialAreaReference   | saref:Measurement-type              |
| value                   | saref:Measurement-value             |
| value_uom               | saref:UnitOfMeasure-unit            |

