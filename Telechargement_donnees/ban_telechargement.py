# py -m pip install pandas
# py -m pip install sqlalchemy

# installation geopandas
# télécharger gdal et fiona (en .whl) à cette URL :
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona
# dans l'invite de commande :
# py -m pip install Downloads\GDAL-3.2.2-cp39-cp39-win_amd64.whl
# py -m pip install Downloads\Fiona-1.8.18-cp39-cp39-win_amd64.whl
# py -m pip install geopandas


# Librairies
import os
import urllib.request
import subprocess


# Telechargement du fichier compresse adresses-35.csv (BAN)
filename = 'adresses-35.csv.gz'
url = 'https://adresse.data.gouv.fr/data/ban/adresses/latest/csv/' + filename
destFile = os.path.dirname(__file__) + '/' + filename

urllib.request.urlretrieve(url, destFile) # effectue le telechargement


# Decompression du fichier - a voir si possible de l'importer via pandas sans decompresser le fichier
#file7zPath = os.path.dirname(__file__) + '/' + "adresses-35.csv.gz"
#extractDir = os.path.dirname(__file__) + '/'
#extractFiles(file7zPath, extractDir)