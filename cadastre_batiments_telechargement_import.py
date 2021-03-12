# installation de nouveaux modules dans l'environnement python QGIS
# ouvrir une console osgeo shell (depuis menu démarrer)
# c:\> py3_env
# c:\> pip install wget

# Installations necessaires pour importer un geodataframe (geopandas) dans postgres
# py -m pip install sqlalchemy
# pip install GeoAlchemy2
# py -m pip install psycopg2-binary

import urllib.request
import os
import geopandas as gpd
import numpy as np
from sqlalchemy import create_engine


filename = 'cadastre-35-batiments-shp.zip'
url = 'https://cadastre.data.gouv.fr/data/etalab-cadastre/2020-10-01/shp/departements/35/' + filename
destFile = os.path.dirname(__file__) + '/' + filename

urllib.request.urlretrieve (url, destFile)


# Choix de colonnes à garder dans la table
columns = ["commune"]

# Chargement du shp en dataframe
# ATTENTION - prend toutes les colonnes !
gdf = gpd.read_file(
    destFile,
    usecols=columns,
    #dtype={"id":"string", "numero":int, "nom_voie":"string", "nom_commune": "string", "lon":float, "lat": float},
    sep=";"
).replace(to_replace='null', value=np.NaN)

# Instantiation de l'objet sqlalchemy.create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/generali')

# Import du dataframe dans postgres
gdf.to_postgis(
    'cadastre_batiments',
    engine,
    index=False, # Not copying over the index
    schema='public',
    if_exists='replace' # if the table already exists, replace this data
)