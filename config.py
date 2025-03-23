ENV = "development"
DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = 0 #vider le cache
SECRET_KEY="maCleSuperSecurisee" # pour les sessions

#Configuration du serveur web
WEB_SERVER = {
 "host": "localhost", #@IP du serveur web
 "port":8080 #port du serveur
}
