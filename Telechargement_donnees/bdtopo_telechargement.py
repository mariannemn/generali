# ESSAYER DE TELECHARGER UNIQUEMENT LA COUCHE BATIMENT

import ftplib
import os
import subprocess
import geopandas as gpd
import numpy as np
from sqlalchemy import create_engine

#ftp://BDTOPO_V3_NL_ext:Ohp3quaz2aideel4@ftp3.ign.fr/BDTOPO_3-0_2020-12-15/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D016_2020-12-15.7z

host = "ftp3.ign.fr"            # adresse du serveur FTP
user = "BDTOPO_V3_NL_ext"       # votre identifiant
password = "Ohp3quaz2aideel4"   # votre mot de passe


def listFileName(con, rep):
    cmd = con.cwd(rep)
    fileList = []
    cmd = ftp.dir(fileList.append) # on recupere le listing
    res = []
    for l in fileList:
        t = l.split(' ')
        res.append(t[-1])
    return res

# Connexion FTP
try:
    ftp = ftplib.FTP(host,user,password) # on se connecte

    dirs = listFileName(ftp,'/')         # listing des repertoires a la racine du ftp
    print(dirs)
    dirs2 = listFileName(ftp,dirs[-1])   # listing des sous-repertoires du dernier repertoire
    print(dirs2)
    dir35 = list(filter(lambda x: x.find('35')!=-1, dirs2)) # filtrage : on ne prend que le 35
    print(dir35)
except Exception as e:
    print("Erreur lors de la connexion FTP : " + e)

# Ecriture du dossier téléchargé
try:
    f35 = '/' + dirs[-1] + '/' + dir35[0] # chemin du fichier à récupérer sur le ftp
    fdest = os.path.dirname(__file__) + '/' + dir35[0] # chemin du fichier à sauvegarder localement
    print("Getting " + f35 + " --> " + fdest + "...")
    with open(fdest, 'wb') as fp:
        res = ftp.retrbinary('RETR ' + f35, fp.write)
    print("done")
    ftp.quit()
except Exception as e:
    print("Erreur lors de l'écriture du dossier' : " + e)


# Decompression du fichier - si on n'a pas uniquement la couche des batiments il faut dezipper le fichier
def extractfiles(zipname, dirPath):
    cmd = ["C:/Program Files/7-Zip/7z.exe", "-aoa", "-o"+dirPath, "x", zipname]
    system = subprocess.Popen(cmd)
    return(system.communicate())

file7zPath = os.path.dirname(__file__) + '/' + dir35[0]
extractDir = os.path.dirname(__file__) + '/'
extractfiles(file7zPath, extractDir)