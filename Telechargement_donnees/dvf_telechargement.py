# Librairies
import os
import urllib.request

# Telechargement du fichier compresse 35.csv (DVF)
filename = '35.csv.gz'

# Comment faire pour ne prendre que la derniere annee ?
url = 'https://cadastre.data.gouv.fr/data/etalab-dvf/latest/csv/2020/departements/' + filename
destFile = os.path.dirname(__file__) + '/' + filename

urllib.request.urlretrieve(url, destFile) # effectue le telechargement