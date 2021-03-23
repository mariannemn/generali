# Fonction qui liste les noms de fichiers (connexion FTP)
def listFileName(con, rep):
    '''La fonction listFileName(con, rep) prend en entrée une méthode de connection et un répertoire. Elle permet de lister les répertoires contenus.'''
    cmd = con.cwd(rep)
    fileList = []
    cmd = ftp.dir(fileList.append) # on recupere le listing
    res = []
    for l in fileList:
        t = l.split(' ')
        res.append(t[-1])
    return res


# Fonction de decompression d'un fichier zip
def extractFiles(zipname, dirPath):
    '''La fonction extractFiles permet de dézipper des fichiers 7-Zip.'''
    cmd = ["C:/Program Files/7-Zip/7z.exe", "-aoa", "-o"+dirPath, "x", zipname]
    system = subprocess.Popen(cmd)
    return(system.communicate())