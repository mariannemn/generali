# Essayer d'automatiser les installations des librairies ? > a voir avec Hadrien
# py -m pip install pandas
# py -m pip install sqlalchemy

# Librairies
import os
import urllib.request
import subprocess
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


# Telechargement du fichier compresse adresses-35.csv (BAN)
filename = 'adresses-35.csv.gz'
url = 'https://adresse.data.gouv.fr/data/ban/adresses/latest/csv/' + filename
destFile = os.path.dirname(__file__) + '/' + filename

urllib.request.urlretrieve(url, destFile) # effectue le telechargement


# Decompression du fichier - a voir si possible de l'importer via pandas sans decompresser le fichier
def extractfiles(zipname, dirPath):
    cmd = ["C:/Program Files/7-Zip/7z.exe", "-aoa", "-o"+dirPath, "x", zipname]
    system = subprocess.Popen(cmd)
    return(system.communicate())

file7zPath = os.path.dirname(__file__) + '/' + "adresses-35.csv.gz"
extractDir = os.path.dirname(__file__) + '/'
extractfiles(file7zPath, extractDir)


# Choix de colonnes à garder dans la table
columns = ["id", "numero", "nom_voie", "nom_commune", "lon", "lat"]

# Chargement du CSV en dataframe
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