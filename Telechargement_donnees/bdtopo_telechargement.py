# Librairies
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
#ftp://BDTOPO_V3_NL_ext:Ohp3quaz2aideel4@ftp3.ign.fr/BDTOPO_3-0_2020-12-15/BDTOPO_3-0_TOUSTHEMES_SHP_LAMB93_D016_2020-12-15.7z

host = "ftp3.ign.fr"            # adresse du serveur FTP
user = "BDTOPO_V3_NL_ext"       # votre identifiant
password = "Ohp3quaz2aideel4"   # votre mot de passe


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
        dirs2 = fonctions_telechargement.listFileName(ftp,dirs[-1])   # listing des sous-repertoires du dernier repertoire
        print(dirs2)
        dir35 = list(filter(lambda x: x.find('35')!=-1, dirs2)) # filtrage : on ne prend que le 35
        print(dir35)

        # Récupération et écriture du dossier téléchargé
        f35 = '/' + dirs[-1] + '/' + dir35[0] # chemin du fichier à récupérer sur le ftp
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