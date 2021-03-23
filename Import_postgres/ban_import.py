# Librairies
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Choix de colonnes à garder dans la table
columns = ["id", "numero", "nom_voie", "nom_commune", "lon", "lat"]

# Chargement du CSV en dataframe
filename = 'adresses-35.csv.gz'
destFile = os.path.dirname(__file__) + '/' + filename

df = pd.read_csv(
    destFile,
    usecols=columns,
    #dtype={"id":"string", "numero":int, "nom_voie":"string", "nom_commune": "string", "lon":float, "lat": float},
    sep=";"
).replace(to_replace='null', value=np.NaN)

# Instantiation de l'objet sqlalchemy.create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/generali')

# Import du dataframe dans postgres
df.to_sql(
    'ban',
    engine,
    index=False, # Not copying over the index
    schema='public',
    if_exists='replace' # if the table already exists, replace this data
)