# py -m pip install pandas
# py -m pip install sqlalchemy


# Librairies
import os
import urllib.request


# Telechargement du fichier compresse adresses-35.csv (BAN)
filename = 'adresses-35.csv.gz'
url = 'https://adresse.data.gouv.fr/data/ban/adresses/latest/csv/' + filename
destFile = os.path.dirname(__file__) + '/' + filename

urllib.request.urlretrieve(url, destFile) # effectue le telechargement