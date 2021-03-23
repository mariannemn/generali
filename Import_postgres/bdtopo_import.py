import ftplib
import os
import subprocess
import geopandas as gpd
import numpy as np
from sqlalchemy import create_engine

# Instantiation de l'objet sqlalchemy.create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/generali')

# Choix de colonnes à ne pas conserver dans la table
ignoreColumns = ["NATURE", "ETAT", "DATE_CREAT", "DATE_MAJ", "DATE_APP", "DATE_CONF", "ID_SOURCE", "PREC_PLANI", "PREC_ALTI", "ORIGIN_BAT", "APP_FF"]

# Chargement du shp en geodataframe
gdf = gpd.read_file(
    'C:/M2_SIGAT/S2/Generali/Python/Automatisation/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D035_2020-12-15/BDTOPO/1_DONNEES_LIVRAISON_2021-01-00019/BDT_3-0_SHP_LAMB93_D035-ED2020-12-15/BATI/BATIMENT.shp',
    ignore_fields=ignoreColumns,
).replace(to_replace='null', value=np.NaN)

# Import du geodataframe dans postgres
gdf.to_postgis(
    'bd_topo',
    engine,
    index=False,
    schema='public',
    if_exists='replace' # si la table existe deja, on la remplace
)

# Requete pour que le champ id soit la cle primaire
# With remplace le try/finally et permet de fermer la connexion une fois le bloc de code terminé
with engine.connect() as con:
    con.execute('ALTER TABLE bd_topo ADD PRIMARY KEY ("ID");')