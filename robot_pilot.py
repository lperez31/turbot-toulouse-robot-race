#!/usr/bin/python
# encoding:utf-8

'''
Copyright 2016 Lior Perez

Ce code est distribué sous licence Apache 2.0.
L'auteur apprécierait de savoir comment vous avez utilisé ce code.
Ce serait également sympathique de partager toute modification utile que vous pourriez y apporter.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import time

# Classes
from voiture import Voiture
from sequenceur import Sequenceur
from arduino import Arduino
from asservissement import Asservissement
from myLogger import MyLogger

# Prepare le logger
myLogger = MyLogger()
logger = myLogger.logger
paramLogger = myLogger.paramLogger

# logger.info('Hello')
# paramLogger.info('Hello')

      
# Creation de la voiture
voiture = Voiture()

print "Initialisation du sequenceur"

# Initialise le sequenceur
sequenceur = Sequenceur(voiture)

# Initialise la communication avec l'Arduino
arduino = Arduino()

# Initialise la classe d'asservissement
asservissement = Asservissement(arduino, voiture)
# Donne au sequenceur la reference vers l'objet asservissement
sequenceur.asservissement = asservissement
# Donne au sequenceur la reference vers l'objet arduino
sequenceur.arduino = arduino

# Attend une seconde que tout soit bien initialise
time.sleep(1)

# Met les commandes a zero
voiture.avance(0)
voiture.tourne(0)


try:
  while True:
    arduino.litDonnees()
    sequenceur.execute()
    asservissement.execute()

except KeyboardInterrupt:
    print("W: interrupt received, stopping")
except:
    raise
finally:
    # clean up
    if asservissement.vitesse > 0:
      # Freine
      sequenceur.voiture.avance(-30)
      time.sleep(1.0)
    sequenceur.voiture.avance(0)
    time.sleep(0.5)
    myLogger.close()
    sequenceur.voiture.gpioCleanUp()
    print("Fin du programme")
    exit()
