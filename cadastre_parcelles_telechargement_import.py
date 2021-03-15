# installation de nouveaux modules dans l'environnement python QGIS
# ouvrir une console osgeo shell (depuis menu démarrer)
# c:\> py3_env
# c:\> pip install wget

import urllib.request
import os
import geopandas as gpd
import numpy as np
from sqlalchemy import create_engine

# Instantiation de l'objet sqlalchemy.create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/generali')

# Téléchargement des données via un protocole HTTP
filename = 'cadastre-35-parcelles-shp.zip'
url = 'https://cadastre.data.gouv.fr/data/etalab-cadastre/latest/shp/departements/35/' + filename
destFile = os.path.dirname(__file__) + '/' + filename

urllib.request.urlretrieve (url, destFile)

# Choix de colonnes à ne pas conserver dans la table
ignoreColumns = ["prefixe", "section", "created", "updated"]

# Chargement du shp en geodataframe
gdf = gpd.read_file(
    filename=destFile,
    ignore_fields=ignoreColumns,
).replace(to_replace='null', value=np.NaN)

# Import du geodataframe dans postgres
gdf.to_postgis(
    'cadastre_parcelles',
    engine,
    index=False, # il y a deja un id dans la donnee
    schema='public',
    if_exists='replace' # si la table existe deja, on la remplace
)

# Requete pour que le champ id soit la cle primaire
# With remplace le try/finally et permet de fermer la connexion une fois le bloc de code terminé
with engine.connect() as con:
    con.execute('ALTER TABLE cadastre_parcelles ADD PRIMARY KEY (id);')