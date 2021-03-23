# Librairies
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Choix de colonnes à garder dans la table
columns = ["id_mutation", "date_mutation", "valeur_fonciere", "id_parcelle", "code_type_local", "type_local", "nombre_pieces_principales", "longitude", "latitude"]

# Chargement du CSV en dataframe
filename = '35.csv.gz'
destFile = os.path.dirname(__file__) + '/' + filename

df = pd.read_csv(
    destFile,
    usecols=columns,
    #dtype={"id":"string", "numero":int, "nom_voie":"string", "nom_commune": "string", "lon":float, "lat": float},
    sep=","
).replace(to_replace='null', value=np.NaN)

# Instantiation de l'objet sqlalchemy.create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/generali')

# Import du dataframe dans postgres
df.to_sql(
    'dvf',
    engine,
    index=True,
    index_label="id",  # ajout d'un champ id
    schema='public',
    if_exists='replace' # si la table existe deja, on la remplace
)