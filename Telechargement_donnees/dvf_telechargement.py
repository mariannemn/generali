# Librairies
import os
import urllib.request
import datetime
import traceback


# Telechargement du fichier compresse 35.csv (DVF)
filename = '35.csv.gz'

now = datetime.datetime.now()
year = str(now.year)
reussite = False
nb_tentatives = 0

while (not reussite) and (nb_tentatives <= 10):
    try:
      # est-ce que j'ai le dernier fichier ?  
      url_index = 'https://cadastre.data.gouv.fr/data/etalab-dvf/latest/csv/'+ year +'/departements/'
      destFile_index_test = os.path.dirname(__file__) + '/' + 'index_dvf_test.html'
      destFile_index = os.path.dirname(__file__) + '/' + 'index_dvf.html'
      urllib.request.urlretrieve(url_index, destFile_index_test)
      if (os.path.exists(destFile_index)):  
          with open(destFile_index, 'r') as file:
            data_index = file.read()  
          with open(destFile_index_test, 'r') as file:
            data_index_test = file.read()  
          reussite = data_index_test == data_index
      # si non, je telecharge...
      if (not reussite):      
          print('pas la dernière version')
          url = 'https://cadastre.data.gouv.fr/data/etalab-dvf/latest/csv/'+ year +'/departements/' + filename
          print(url)
          
          destFile = os.path.dirname(__file__) + '/' + filename
          if (os.path.exists(destFile)):
              os.unlink(destFile)
          urllib.request.urlretrieve(url, destFile) # effectue le telechargement
          reussite = True
          os.unlink(destFile_index)  
          os.rename(destFile_index_test, destFile_index)
      else:
          os.unlink(destFile_index_test)
    except Exception as e:
      # affiche la stack trace (erreur produite)
      #traceback.print_exc()
      year = str(int(year) - 1)
      reussite = False
