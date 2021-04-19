import ftplib
import os
import subprocess
import time
import traceback

# Import des fichiers de fonctions
import fonctions_telechargement
#print(fonctions_telechargement.listFileName.__doc__)
#print(fonctions_telechargement.extractFiles.__doc__)

# Informations de connexion FTP
#ftp://ORTHO_HR_ext:Ithacah6ophai2vo@ftp3.ign.fr/ORTHOHR_1-0_RVB-0M20_JP2-E080_LAMB93_D035_2017-01-01.7z.001

host = "ftp3.ign.fr"            # adresse du serveur FTP
user = "ORTHO_HR_ext"       # votre identifiant
password = "Ithacah6ophai2vo"   # votre mot de passe


# Connexion FTP
reussite = False
nb_tentatives = 0
while (not reussite) and (nb_tentatives <= 10):
    try:
        nb_tentatives += 1
        print("Tentative n° : "+str(nb_tentatives))

        ftp = ftplib.FTP(host,user,password) # on se connecte

        dirs = fonctions_telechargement.listFileName(ftp,'/')         # listing des repertoires a la racine du ftp
        print(dirs)

        dir35 = list(filter(lambda x: x.find('D035')!=-1, dirs)) # filtrage : on ne prend que le 35
        print(dir35)

        # Récupération et écriture du dossier téléchargé
        f35 = '/' + dir35[0] # chemin du fichier à récupérer sur le ftp
        fdest = os.path.dirname(__file__) + '/' + dir35[0] # chemin du fichier à sauvegarder localement
        print("Getting " + f35 + " --> " + fdest + "...")

        with open(fdest, 'wb') as fp:
            res = ftp.retrbinary('RETR ' + f35, fp.write)
        print("done")
        ftp.quit()
        
        reussite = True
    except Exception as e:
        # affiche la stack trace (erreur produite)
        #traceback.print_exc()
        print("Erreur lors de la connexion FTP ou lors de l'écriture du dossier : " + str(e))
        print("Le script va redémarrer dans 30 secondes...")
        time.sleep(30) # Temps de latence (30 secondes) après qu'une erreur se soit produite côté serveur
        reussite = False
        
file7zPath = os.path.dirname(__file__) + '/' + dir35[0]
extractDir = os.path.dirname(__file__) + '/'
fonctions_telechargement.extractFiles(file7zPath, extractDir)