import os
import numpy as np
import pandas as pd
import yaml
from processing.core.Processing import Processing
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import *
from qgis.utils import *

# filter by one RTA
Processing.run("native:selectbylocation", {
    'INPUT': '/Users/jose/PycharmProjects/montreal_sources_implementation/data/buildings/MS_1_July23_23_40_3_MGB.geojson',
    'PREDICATE': [6],
    'INTERSECT': '/Users/jose/PycharmProjects/montreal_sources_implementation/data/RTA/Montreal.geojson|subset="CFSAUID" = \'H1K\'',
    'METHOD': 0})
