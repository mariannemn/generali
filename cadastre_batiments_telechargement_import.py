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

# Instantiation de l'objet sqlalchemy.create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/generali')
filename = 'cadastre-35-batiments-shp.zip'
url = 'https://cadastre.data.gouv.fr/data/etalab-cadastre/2020-10-01/shp/departements/35/' + filename
destFile = os.path.dirname(__file__) + '/' + filename

urllib.request.urlretrieve (url, destFile)

# Choix de colonnes à ne pas conserver dans la table
ignoreColumns = ["nom", "type", "created", "updated"]

# Chargement du shp en geodataframe
gdf = gpd.read_file(
    filename=destFile,
    ignore_fields=ignoreColumns,
).replace(to_replace='null', value=np.NaN)

# Import du geodataframe dans postgres
gdf.to_postgis(
    'cadastre_batiments',
    engine,
    index=True,
    index_label = "id",
    schema='public',
    if_exists='replace' # if the table already exists, replace this data
)

# With remplace le try/finally et permet de fermer la connexion une fois le bloc de code terminé
with engine.connect() as con:
    con.execute('ALTER TABLE cadastre_batiments ADD PRIMARY KEY (id);')
