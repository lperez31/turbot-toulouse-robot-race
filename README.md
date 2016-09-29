# README #

Code utilisé par le robot Turbot lors de la course "Toulouse Robot Race" 2016.

Cette course consistait à parcourir un circuit de 110 mètres de long le plus rapidement possible. Voir plan du circuit dans le fichier circuit.png.

Le robot Turbot a remporté la course en 30,61 secondes.

### Avertissement ###

Ce code n'a pas été prévu pour être distribué. Il n'a pas été nettoyé, il contient tous les ajustements de dernière minute faits pendant la compétition. Il mérite un sérieux refactoring. Je l'ai toutefois ouvert en opensource pour qu'il puisse aider d'autres amateurs de robotique. Donc n'hésitez pas à l'utiliser, mais ne vous plaignez pas si ça ne marche pas bien ! Utilisation à vos risques et péril, et bien entendu ne pas utiliser ce code dans des applications pouvant mettre en jeu la sécurité des personnes ou des biens.

### Hardware et branchements ###

Configuration hardware :

* un Raspberry Pi 3 sous Raspbian. Attention, les modèles Pi 1 et Pi 2 ne disposent pas des deux PWM hardware nécessaires au pilotage du moteur et du servomoteur.
* un Arduino. J'ai utilisé un Arduino Duemilanove, mais un autre Arduino avec suffisamment de mémoire devrait faire l'affaire. La connexion entre le Raspberry Pi et l'Arduino se fait par un câble USB (il faut autoriser si besoin la connexion série via USB dans Raspbian).
* un chassis de voiture radiocommandée, avec son moteur, son ESC (régulateur du moteur), son servomoteur de direction et sa batterie. J'ai utilisé un chassis Tamiya XV-01 avec son moteur à charbons d'origine. Branchements : ESC sur pin Raspberry Pi GPIO n°13, servomoteur sur pin Raspberry Pi GPIO n°18. Noter que les pins 13 et 18 sont les deux seules pins qui supportent le PWM sur le Raspberry Pi.
* un gyroscope Drotek MPU9250, permettant de connaitre le cap. Relié sur le bus I2C de l'Arduino (Analog 4 et Analog 5 sur l'Arduino Duemilanove).
* un télémètre à ultrasons HC-SR04. Au final je ne m'en suis quasiment pas servi car l'expérience a montré qu'on perdait très souvent le signal dès qu'on prenait de la vitesse. Branchements : trigger sur Arduino pin 7, echo sur Arduino pin 2.
* un télémètre infrarouge Sharp GP2Y0A02YK. Plage de détection 20cm à 1,5m. Branché sur Arduino analog pin 0.
* un télémètre laser Pololu VL53L0X Time-of-Flight. Plage de détection théorique, plus d'un mètre. En pratique au soleil une trentaine de cm maxi. Branché sur le bus I2C de l'Arduino (Analog 4 et Analog 5 sur l'Arduino Duemilanove).
* un bouton poussoir et sa résistance en série sur Raspberry Pi GPIO n°27
* facultatif : une led et sa résistance en série sur Raspberry Pi GPIO n°22

Tous les télémètres sont placés à l'avant, visant vers la droite, voir fichier photo_robot.jpg. En pratique, j'ai utilisé le télémètre laser pour les distances inférieures à 20cm, le télémètre infrarouge pour les distances supérieures à 20cm. Le télémètre ultrason n'a servi qu'à confirmer la détection des débuts de virage ou début de chicanes.

### Installation ###

Installer dans l'Arduino le code qui se trouve dans /Arduino/TurbotArduino/TurbotArduino.ino

Le reste du code tourne sur le Raspberry Pi, sous python 2.7.

Il faut installer au préalable :

* wiringPi (https://github.com/WiringPi/WiringPi-Python)

La librairie wiringPi permet d'utiliser les deux PWM hardware du Raspberry Pi 3.

### Lancement ###

Installer d'abord (voir chapitre suivant)

Pour lancer le code, il faut être root (à cause de la librairie wiringPi qui ne fonctionne qu'en root).

Lancer avec la commande suivante :

    sudo python robot_pilot.py

Pour les fainéants qui veulent éviter d'avoir à taper tout ça, vous pouvez utiliser la commande suivante, mais je ne suis pas sûr que ça fonctionnera sans avoir à reconfigurer certaines choses. Tentez, vous verrez bien :

    ./launcher.sh

Ce script permet également de donner les autorisations de forward X11 à root, si vous avez besoin d'afficher des images depuis python vers votre PC en ssh (pas utilisé dans mon code, mais ça peut servir).

### Utilisation ###

Une fois lancé, poser le robot sur la ligne de départ, bien aligné avec la piste. Vérifier que tout s'est bien initialisé (la led doit clignoter lentement). Attendre une dizaine de secondes que le gyroscope soit stabilisé (la led se mettra à clignoter rapidement). Cliquer sur le bouton poussoir, et c'est parti !

Mais il faudra probablement modifier plein de constantes pour que ça fonctionne avec votre robot...

### Description des fichiers ###

* robot_pilot.py : programme principal
* sequenceur.py : gestion du séquencement des actions (ligne droite pendant 2 secondes, puis ralentir et ligne droite jusqu'à ce que les télémètres mesurent plus de 80cm, etc.)
* voiture.py : gestion du moteur, du servomoteur...
* arduino.py : réception des données acquises par l'arduino
* asservissement.py : gestion de l'asservissement (asservissement de type PID). La direction est asservie au cap du gyroscope. Dans les grandes lignes droites, on y ajoute un asservissement du cap en fonction de la distance aux bordures.
* myLogger.py : librairie permettant de gérer des logs. Par défaut le programme enregistre des logs dans un fichier parametres.log. C'est un log tournant. Le dernier fichier enregistré s'appelle parametres.log, les autres sont renumérotés .log.1, .log.2, etc.

### Licence ###

Copyright 2016 Lior Perez

Ce code est distribué sous licence Apache 2.0. L'auteur apprécierait de savoir comment vous avez utilisé ce code. Ce serait également sympathique de partager toute modification utile que vous pourriez y apporter.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.