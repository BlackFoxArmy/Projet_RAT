# RAT Project - MGS
#### Maxime Chasson - Sacha Perrin - Grégoire Matthieu
## READ ME

### Installation : 

Prérequis : 

- Python 3
- Mettre à jour python si besoin (pip install --upgrade pip)
- Mettre à jour la machine Linux (apt-get update)
- Installer le Packages (mss)
- Installer le Packages (requests)
- Installer le Packages (pynput)

### Étape 1 : 
- Une fois que l'installation des prérequis est faite, il va falloir modifier   l'ip et le port dans les fichiers serveur.py et backdoor.py (mettre l'ip de ma machine attaquante | le port est aux choix)

### Étape 2 : 

- Ensuite, il suffit de lancer le notre serveur.py et attendre que notre vicitme lance le backdoor.py

- Si tout ce passe bien et que tout est bien configurer, la machine devrait se connecter à notre machine attaquante 

### Étape 3 : 

- Dans notre cas, nous avons réalisé les tests sur un réseau local. Dans le cas d'une réel utilisation, les deux machines (attaquantes et victimes) doivent être dans le même réseau. Par exemple un wifi public.

### Étape 4 : 

- Une fois toutes les étapes précédentes réalisés, le controle de la machine est récupéré et on peut utiliser les commandes que l'on souhaite sur la machine victime.