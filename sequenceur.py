# encoding:utf-8

# Librairies tierces
import time
import os

# Mes classes
from voiture import Voiture
from asservissement import Asservissement
from arduino import Arduino

class Sequenceur:

  # General
  # CONST_NOMBRE_MESURES_DEPASSEMENT_DISTANCE = 1000 # Nombre de mesures consecutives du telemetre avant de considerer qu'un depassement de distance est effectif
  DUREE_DEPASSEMENT_TELEMETRE = 0.1       # Temps en secondes pendant lequel le telemetre doit mesurer un depassement avant de considerer qu'un depassement est effectif
  DISTANCE_DEPASSEMENT_TELEMETRE_IR = 1  # TODO: remettre ? Distance min mesuree par le telemetre IR pour confirmer depassement

  # Premiere ligne droite
  VITESSE_PREMIERE_LIGNE_DROITE = 50    # 45 pendant 4.8 fonctionne
  DUREE_PREMIERE_LIGNE_DROITE = 4.15     # 4.5 lors des essais à 33s
  DISTANCE_BORDURE_PREMIERE_LIGNE_DROITE = 30

  # Ligne droite avant 180°
  VITESSE_LIGNE_DROITE_AVANT_180 = 25
  DISTANCE_DECLENCHEMENT_180 = 80

  # Virage 180°
  POSITION_ROUES_180_DEBUT = 70
  POSITION_ROUES_180_FIN = 25     # Initialement 30 ou 35, mais ca passe trop pres
  VITESSE_180_DEBUT = 30
  VITESSE_180_FIN = 38
  DUREE_LIGNE_DROITE_PENDANT_180 = 0.3

  # Ligne droite apres premier virage 180°
  VITESSE_LIGNE_DROITE_APRES_PREMiER_VIRAGE = 45
  DISTANCE_BORDURE_APRES_PREMIER_VIRAGE = 30
  DUREE_LIGNE_DROITE_SANS_SUIVI_BORDURE_APRES_PREMIER_VIRAGE = 1
  DUREE_LIGNE_DROITE_APRES_PREMIER_VIRAGE = 2.5  # Auparavant 2.5         

  # Chicane
  VITESSE_ENTREE_CHICANE = 25
  DISTANCE_DECLENCHEMENT_CHICANE = 60
  VITESSE_PREMIER_VIRAGE = 42

  VITESSE_CHICANE = 40
  DUREE_LIGNE_DIAGONALE_CHICANE_1 = 0.7  # 0.9 lors des essais du soir
  DUREE_LIGNE_DIAGONALE_CHICANE_2 = 0.7  # 0.6 lors des essais du soir
  DUREE_LIGNE_DIAGONALE_CHICANE_3 = 0.85  # 0.8 lors des essais du soir
  DUREE_LIGNE_DIAGONALE_CHICANE_4 = 0.75  # 0.6 lors des essais du soir

  #VITESSE_ENTREE_CHICANE = 25
  #DISTANCE_DECLENCHEMENT_CHICANE = 20
  #VITESSE_PREMIER_VIRAGE = 25
  #VITESSE_CHICANE = 25

  #VITESSE_CHICANE = 46
  #DUREE_LIGNE_DIAGONALE_CHICANE_1 = 1.1
  #DUREE_LIGNE_DIAGONALE_CHICANE_2 = 0.7
  #DUREE_LIGNE_DIAGONALE_CHICANE_3 = 0.7
  #DUREE_LIGNE_DIAGONALE_CHICANE_4 = 0.6
  #DELTA_CAP_LIGNE_DIAGONALE = 27
  #DUREE_LIGNE_DROITE_CHICANE_1 = 0.35
  #DUREE_LIGNE_DROITE_CHICANE_2 = DUREE_LIGNE_DROITE_CHICANE_1
  #DUREE_LIGNE_DROITE_CHICANE_3 = DUREE_LIGNE_DROITE_CHICANE_1
  #DUREE_LIGNE_DROITE_CHICANE_4 = DUREE_LIGNE_DROITE_CHICANE_1

  DELTA_CAP_LIGNE_DIAGONALE = 27
  DUREE_LIGNE_DROITE_CHICANE_1 = 0.40
  DUREE_LIGNE_DROITE_CHICANE_2 = DUREE_LIGNE_DROITE_CHICANE_1 - 0.05
  DUREE_LIGNE_DROITE_CHICANE_3 = DUREE_LIGNE_DROITE_CHICANE_1 + 0.25
  DUREE_LIGNE_DROITE_CHICANE_4 = DUREE_LIGNE_DROITE_CHICANE_1 - 0.05

  # Ligne droite après chicane sans telemetre pour stabilisation
  VITESSE_LIGNE_DROITE_SORTIE_CHICANE = 45
  DUREE_LIGNE_DROITE_SORTIE_CHICANE = 1.0
  # Ligne droite au telemetre apres chicane
  VITESSE_LIGNE_DROITE_APRES_CHICANE = 50
  DISTANCE_BORDURE_LIGNE_DROITE_APRES_CHICANE = 30
  DUREE_LIGNE_DROITE_APRES_CHICANE = 2.7

  # Derniere ligne droite suivi bordure
  VITESSE_DERNIERE_LIGNE_DROITE = 55
  DISTANCE_BORDURE_DERNIERE_LIGNE_DROITE = 40
  DUREE_LIGNE_DROITE_SANS_SUIVI_BORDURE_APRES_DERNIER_VIRAGE = 1   # On commence par une ligne droite au cap
  DUREE_DERNIERE_LIGNE_DROITE = 4.7                                # On poursuit par un suivi bordure

  # Acceleration finale
  VITESSE_DERNIERE_LIGNE_DROITE_CAP = 60
  DUREE_DERNIERE_LIGNE_DROITE_CAP = 1.7

  # Ralentissement ligne droite finale suivi bordure
  VITESSE_RALENTISSEMENT_FINAL = 40
  DISTANCE_BORDURE_RALENTISSEMENT_FINAL = 30
  DUREE_RALENTISSEMENT_FINAL = 1.0

  # Suivi courbes au telemetre IR
  VITESSE_SUIVI_COURBE_TELEMETRE_IR = 25
  DISTANCE_SUIVI_COURBE_TELEMETRE_IR = 60
  DUREE_SUIVI_COURBE_TELEMETRE_IR = 180

  # Durees d'appui sur le bouton poussoir
  DUREE_APPUI_COURT_REDEMARRAGE = 2   # Nombre de secondes d'appui sur le poussoir pour reinitialiser le programme
  DUREE_APPUI_LONG_SHUTDOWN = 10     # Nombre de secondes d'appui sur le poussoir pour eteindre le raspberry

  programme = [

          ###########################################################
          # Attente stabilisation gyro - ETAPE 0
          ###########################################################

          {
            'instruction' : 'attendreGyroStable', # Attend stabilisation du gyro
            'conditionFin' : 'attendreGyroStable'
          },
          {
            'label' : 'attendBouton',          
            'instruction' : 'tourne',        # Attend l'appui sur le bouton
            'positionRoues' : 0,
            'vitesse' : 0,
            'conditionFin' : 'attendBouton'
          },
          {
            'instruction' : 'setCap',             # Cap asuivre = cap actuel
            'conditionFin' : 'immediat'
          },

          ###########################################################
          # PREMIERE LIGNE DROITE        ETAPE 1
          ###########################################################
          
          {
            'label' :        'debutLigneDroite',         # Ligne droite avec suivi bordure
            'instruction' :  'ligneDroiteTelemetre',
            'vitesse'  :      VITESSE_PREMIERE_LIGNE_DROITE,
            'distance' :      DISTANCE_BORDURE_PREMIERE_LIGNE_DROITE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_PREMIERE_LIGNE_DROITE
          },

          {
            'instruction' :  'tourne',    # Freine
            'positionRoues' : 0,
            'vitesse'  :      -30,
            'conditionFin' : 'duree',
            'duree' :         0.5
          },
          
          ############ TEST
          #{
          #  'instruction' :  'ligneDroiteTelemetre',
          #  'vitesse'  :      40, # Max 55 ? 45 plus raisonnable...
          #  'recalageCap' :   False,
          #  'distance' :      40,
          #  'antiProche' :    False,
          #  'conditionFin' : 'duree',
          #  'duree' :         4,  # Fin quand distance telemetre s'envole
          #  'activationDistanceIntegrale' : False,
          #  'nextLabel' :     'arret'
          #},


          ###########################################################
          # VIRAGE 180°                  ETAPE 2
          ###########################################################

          {
           'instruction' : 'ligneDroite',               # Ligne droite au cap
            'vitesse' :     VITESSE_LIGNE_DROITE_AVANT_180,
            'conditionFin' : 'telemetre',
            'distSupA' :    DISTANCE_DECLENCHEMENT_180  # Fin quand distance telemetre s'envole
          },

          {
            'instruction' : 'tourne',                   # Commence le virage 180°
            'positionRoues' : POSITION_ROUES_180_DEBUT,
            'vitesse' : VITESSE_180_DEBUT,
            'conditionFin' : 'cap',
            'capFinalMini' : 60,  # En relatif par rapport au cap initial, pour la gauche : 180 300, pour la droite 60 180
            'capFinalMaxi' : 180,  # En relatif par rapport au cap initial
          },

          {
            'instruction' : 'ajouteCap',
            'cap' : 90,
            'conditionFin' : 'immediat',
          },
          
          {
           'instruction' : 'ligneDroite',               # Ligne droite au cap
            'vitesse' :     VITESSE_180_DEBUT,
            'conditionFin' : 'duree',
            'duree' :    DUREE_LIGNE_DROITE_PENDANT_180
          },
          
          {
            'instruction' : 'tourne',                   # Puis finit le virage 180°
            'positionRoues' : POSITION_ROUES_180_FIN,
            'vitesse' : VITESSE_180_FIN,
            'conditionFin' : 'cap',
            'capFinalMini' : 60,  # En relatif par rapport au cap initial
            'capFinalMaxi' : 180 # En relatif par rapport au cap initial
          },


          {
            'instruction' : 'ajouteCap',
            'cap' : 90,
            'conditionFin' : 'immediat',
          },

          ###########################################################
          # LIGNE DROITE AVEC SUIVI BORDURE      ETAPE 3
          ###########################################################

          {
            'instruction' :  'ligneDroite',               # Ligne droite sans suivi bordure pour sortir proprement du virage
            'vitesse'  :      VITESSE_LIGNE_DROITE_APRES_PREMiER_VIRAGE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DROITE_SANS_SUIVI_BORDURE_APRES_PREMIER_VIRAGE
          },

          {
            'label' :        'debutLigneDroiteSortieVirage',         # Ligne droite avec suivi bordure sans recalage de cap
            'instruction' :  'ligneDroiteTelemetre',
            'recalageCap' :   False,
            'activationDistanceIntegrale' : True,
            'vitesse'  :      VITESSE_LIGNE_DROITE_APRES_PREMiER_VIRAGE,
            'distance' :      DISTANCE_BORDURE_APRES_PREMIER_VIRAGE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DROITE_APRES_PREMIER_VIRAGE
          },

          ###########################################################
          # CHICANES              ETAPE 4
          ###########################################################
          {
            'instruction' :  'tourne',    # Freine
            'positionRoues' : 0,
            'vitesse'  :      -5,
            'conditionFin' : 'duree',
            'duree' :         0.3
          },

          {
           'instruction' : 'ligneDroite',               # Ligne droite
            'vitesse' :     VITESSE_ENTREE_CHICANE,
            'conditionFin' : 'telemetre',
            'distSupA' :    DISTANCE_DECLENCHEMENT_CHICANE     # Fin quand distance telemetre s'envole
          },

          # PREMIERE CHICANE
          {
            'instruction' : 'ajouteCap',                # 1ere diagonale a droite
            'cap' : DELTA_CAP_LIGNE_DIAGONALE,
            'conditionFin' : 'immediat',
          },
          {
           'instruction' : 'ligneDroite',               
            'vitesse' :     VITESSE_PREMIER_VIRAGE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DIAGONALE_CHICANE_1
          },
          {
            'instruction' : 'ajouteCap',
            'cap' : -DELTA_CAP_LIGNE_DIAGONALE,
            'conditionFin' : 'immediat',
          },

          {
           'instruction' : 'ligneDroite',               # Ligne droite chicane
            'vitesse' :     VITESSE_CHICANE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DROITE_CHICANE_1
          },

          # DEUXIEME CHICANE
          {
            'instruction' : 'ajouteCap',                # 2e diagonale a gauche
            'cap' : -DELTA_CAP_LIGNE_DIAGONALE,
            'conditionFin' : 'immediat',
          },
          {
           'instruction' : 'ligneDroite',               
            'vitesse' :     VITESSE_CHICANE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DIAGONALE_CHICANE_2
          },
          {
            'instruction' : 'ajouteCap',
            'cap' : +DELTA_CAP_LIGNE_DIAGONALE,
            'conditionFin' : 'immediat',
          },

          {
           'instruction' : 'ligneDroite',               # Ligne droite chicane
            'vitesse' :     VITESSE_CHICANE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DROITE_CHICANE_2
          },

          # TROISIEME CHICANE
          {
            'instruction' : 'ajouteCap',                # 3eme diagonale a droite
            'cap' : DELTA_CAP_LIGNE_DIAGONALE,
            'conditionFin' : 'immediat',
          },
          {
           'instruction' : 'ligneDroite',               
            'vitesse' :     VITESSE_CHICANE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DIAGONALE_CHICANE_3
          },
          {
            'instruction' : 'ajouteCap',
            'cap' : -DELTA_CAP_LIGNE_DIAGONALE,
            'conditionFin' : 'immediat',
          },

          {
           'instruction' : 'ligneDroite',               # Ligne droite chicane
            'vitesse' :     VITESSE_CHICANE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DROITE_CHICANE_3
          },

          # QUATRIEME CHICANE
          {
            'instruction' : 'ajouteCap',                # 4e diagonale a gauche
            'cap' : -DELTA_CAP_LIGNE_DIAGONALE,
            'conditionFin' : 'immediat',
          },
          {
           'instruction' : 'ligneDroite',               
            'vitesse' :     VITESSE_CHICANE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DIAGONALE_CHICANE_4
          },
          {
            'instruction' : 'ajouteCap',
            'cap' : DELTA_CAP_LIGNE_DIAGONALE,
            'conditionFin' : 'immediat',
          },

          {
           'instruction' : 'ligneDroite',               # Ligne droite chicane (TODO: verifier si c'est utile)
            'vitesse' :     VITESSE_CHICANE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DROITE_CHICANE_4
          },

          ###########################################################
          # LIGNE DROITE APRES CHICANE        ETAPE 5
          ###########################################################
          
          {
            'label' :        'debutLigneDroite',         # Ligne droite avec suivi bordure
            'instruction' :  'ligneDroiteTelemetre',
            'vitesse'  :      VITESSE_LIGNE_DROITE_APRES_CHICANE,
            'distance' :      DISTANCE_BORDURE_LIGNE_DROITE_APRES_CHICANE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DROITE_APRES_CHICANE
          },

          {
            'instruction' :  'tourne',    # Freine
            'positionRoues' : 0,
            'vitesse'  :      -30,
            'distance' :      DISTANCE_BORDURE_LIGNE_DROITE_APRES_CHICANE,
            'conditionFin' : 'duree',
            'duree' :         0.5
          },

          ###########################################################
          # SECOND VIRAGE 180°                  ETAPE 6
          ###########################################################

          {
           'instruction' : 'ligneDroite',               # Ligne droite au cap
            'vitesse' :     VITESSE_LIGNE_DROITE_AVANT_180,
            'conditionFin' : 'telemetre',
            'distSupA' :    DISTANCE_DECLENCHEMENT_180  # Fin quand distance telemetre s'envole
          },

          {
            'instruction' : 'tourne',                   # Commence le virage 180°
            'positionRoues' : POSITION_ROUES_180_DEBUT,
            'vitesse' : VITESSE_180_DEBUT,
            'conditionFin' : 'cap',
            'capFinalMini' : 60,  # En relatif par rapport au cap initial, pour la gauche : 180 300, pour la droite 60 180
            'capFinalMaxi' : 180,  # En relatif par rapport au cap initial
          },

          {
            'instruction' : 'ajouteCap',
            'cap' : 90,
            'conditionFin' : 'immediat',
          },
          
          {
           'instruction' : 'ligneDroite',               # Ligne droite au cap
            'vitesse' :     VITESSE_180_DEBUT,
            'conditionFin' : 'duree',
            'duree' :    DUREE_LIGNE_DROITE_PENDANT_180 + 0.1 # Ajout car il y a un devers
          },
          
          {
            'instruction' : 'tourne',                   # Puis finit le virage 180°
            'positionRoues' : POSITION_ROUES_180_FIN,
            'vitesse' : VITESSE_180_FIN,
            'conditionFin' : 'cap',
            'capFinalMini' : 60,  # En relatif par rapport au cap initial
            'capFinalMaxi' : 180 # En relatif par rapport au cap initial
          },


          {
            'instruction' : 'ajouteCap',
            'cap' : 90,
            'conditionFin' : 'immediat',
          },

          ###########################################################
          # LIGNE DROITE AVEC SUIVI BORDURE      ETAPE 7
          ###########################################################

          {
            'instruction' :  'ligneDroite',  # Ligne droite au cap pour sortir proprement du virage
            'vitesse'  :      VITESSE_DERNIERE_LIGNE_DROITE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DROITE_SANS_SUIVI_BORDURE_APRES_DERNIER_VIRAGE
          },

          {
            'instruction' :  'ligneDroiteTelemetre',  # Ligne droite avec suivi bordures
            'vitesse'  :      VITESSE_DERNIERE_LIGNE_DROITE,
            'distance' :      DISTANCE_BORDURE_DERNIERE_LIGNE_DROITE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_DERNIERE_LIGNE_DROITE
          },

          {
            'instruction' : 'ajouteCap',        # Hack pour corriger un biais
            'cap' : -2,
            'conditionFin' : 'immediat',
          },

          {
            'instruction' :  'ligneDroite',  # Ligne droite au cap
            'vitesse'  :      VITESSE_DERNIERE_LIGNE_DROITE_CAP,
            'conditionFin' : 'duree',
            'duree' :         DUREE_DERNIERE_LIGNE_DROITE_CAP
          },

          {
            'instruction' :  'tourne',    # Freine
            'positionRoues' : 0,
            'vitesse'  :      -10,
            'conditionFin' : 'duree',
            'duree' :         0.3
          },

          {
            'instruction' :  'ligneDroiteTelemetre',  # Ligne droite avec suivi bordures
            'vitesse'  :      VITESSE_RALENTISSEMENT_FINAL,
            'distance' :      DISTANCE_BORDURE_RALENTISSEMENT_FINAL,
            'conditionFin' : 'duree',
            'duree' :         DUREE_RALENTISSEMENT_FINAL
          },


          {
            'instruction' :  'tourne',    # Freine
            'positionRoues' : 0,
            'vitesse'  :      -30,
            'distance' :      DISTANCE_BORDURE_PREMIERE_LIGNE_DROITE,
            'conditionFin' : 'duree',
            'duree' :         0.5
          },
          
          {
           'instruction' : 'ligneDroite',               # Ligne droite au cap
            'vitesse' :     VITESSE_LIGNE_DROITE_AVANT_180,
            'conditionFin' : 'telemetre',
            'distSupA' :    DISTANCE_DECLENCHEMENT_180  # Fin quand distance telemetre s'envole
          },



          ###########################################################
          # FREINAGE PUIS ARRET
          ###########################################################

          {
            'label' :       'arret',
            'instruction' : 'tourne',              # Freinage
            'vitesse' : -30,
            'positionRoues' : 0,
            'conditionFin' : 'duree',
            'duree' : 0.5
          },
          {
            'instruction' : 'tourne',                   # Arrêt avec roues a 0
            'vitesse' : 0,
            'positionRoues' : 0,
            'conditionFin' : 'duree',
            'duree' : 1.5,
            'nextLabel' : 'attendBouton'                # Retour au début
          }
  ]

  sequence = 0
  debut = True
  timeDebut = 0
  programmeCourant = {}
  voiture = None
  asservissement = None
  last_mesure_depassement = False
  time_debut_depassement = 0
  last_mesure_telemetre1 = 0

  timer_led = 0
  vitesse_clignote_led = 10
  led_clignote = True
  last_led = 0

  timer_bouton = 0
  last_bouton = 1     # 1 = bouton relache, 0 = bouton appuye
  flag_appui_court = False  # Passe a True quand un appui court (3 secondes) a ete detecte

  def __init__(self, voiture):
    self.voiture = voiture

  def execute(self):

    # Fait clignoter la led
    if self.led_clignote:
      if time.time() > self.timer_led + self.vitesse_clignote_led:
        self.timer_led = time.time()
        self.last_led = 0 if self.last_led else 1
        self.voiture.setLed(self.last_led)
    else:
      self.voiture.setLed(1)

    # Verifie appui court (3 sec) ou long (10 sec) sur bouton
    if self.voiture.getBoutonPoussoir() == 0:
      if self.last_bouton == 1:
        self.timer_bouton = time.time()
      else:
        if time.time() > self.timer_bouton + self.DUREE_APPUI_COURT_REDEMARRAGE:
          # Arrete la voiture
          self.voiture.avance(0)
          self.voiture.tourne(0)
          self.vitesse_clignote_led = 0.3
          self.led_clignote = True
          self.flag_appui_court = True
        if time.time() > self.timer_bouton + self.DUREE_APPUI_LONG_SHUTDOWN:
          # Appui long: shutdown Raspberry Pi
          os.system('sudo shutdown -h now')
          pass
      self.last_bouton = 0
    else:
      self.last_bouton = 1
      if self.flag_appui_court:
        # Si on a detecte un appui court avant la relache du bouton
        self.flag_appui_court = False
        # Retourne a la sequence du debut
        for i in range(len(self.programme)):
          if 'label' in self.programme[i]:
            if self.programme[i]['label'] == 'attendBouton':
              # On a trouve la prochaine sequence
              self.sequence = i
              self.debut = True

    if self.debut:
      # Premiere execution de l'instruction courante
      self.programmeCourant = self.programme[self.sequence]
      instruction = self.programmeCourant['instruction']
      print "********** Nouvelle instruction *********** ", instruction
      self.timeDebut = time.time()
      self.debut = False
      self.arduino.annuleRecalageCap()
      self.asservissement.cumulErreurCap = 0
      self.last_mesure_depassement = False

      # Fait du cap courant le cap a suivre
      if instruction == 'setCap':
        self.asservissement.setCapTarget()

      # Programme la vitesse de la voiture
      if instruction == 'ligneDroite' or instruction == 'ligneDroiteTelemetre' or instruction == 'tourne' or instruction == 'suiviCourbeTelemetre':
        vitesse = self.programmeCourant['vitesse']
        print "Vitesse : ", vitesse
        self.voiture.avance(vitesse)
        self.asservissement.setVitesse(vitesse)

      # Positionne les roues pour l'instruction 'tourne'
      if instruction == 'tourne':
        positionRoues = self.programmeCourant['positionRoues']
        print "Position roues : ", positionRoues
        self.voiture.tourne(positionRoues)

      # Ajoute une valeur a capTarget pour l'instruction 'ajouteCap'
      if instruction == 'ajouteCap':
        self.asservissement.ajouteCap(self.programmeCourant['cap'])

      # Indique a la classe d'asservissement si elle doit asservir, et selon quel algo
      if instruction == 'ligneDroite':
        self.asservissement.initLigneDroite()
      elif instruction == 'ligneDroiteTelemetre':
        
        recalageCap = False
        if 'recalageCap' in self.programmeCourant:
          recalageCap = self.programmeCourant['recalageCap']

        activationDistanceIntegrale = False
        if 'activationDistanceIntegrale' in self.programmeCourant:
          activationDistanceIntegrale = self.programmeCourant['activationDistanceIntegrale']
        
        antiProche = False
        if 'antiProche' in self.programmeCourant:
          antiProche = self.programmeCourant['antiProche']
          # Surtout pas de correction integrale avec la protection antiProche
          activationDistanceIntegrale = False
        
        self.asservissement.initLigneDroiteTelemetre(self.programmeCourant['distance'], recalageCap, activationDistanceIntegrale, antiProche)
      
      elif instruction == 'suiviCourbeTelemetre':
        self.asservissement.initCourbeTelemetre(self.programmeCourant['distance'])
      else:
        self.asservissement.annuleLigneDroite()

    else:
      # Partie qui s'execute en boucle tant que la condition de fin n'est pas remplie
      pass

    # Verifie s'il faut passer a l'instruction suivante
    finSequence = False # Initialise finSequence
    # Recupere la condition de fin
    conditionFin = self.programmeCourant['conditionFin']
    # Verifie si la condition de fin est atteinte
    if conditionFin == 'attendreGyroStable':
      if self.arduino.gyroX != 0.0:
        # Si l'arduino a bien reussi a acquerir le gyro, le dit a travers la vitesse de clignotement de la led
        self.vitesse_clignote_led = 1.5
      finSequence = self.arduino.checkGyroStable()
    elif conditionFin == 'cap':
      capFinalMini = self.programmeCourant['capFinalMini']
      capFinalMaxi = self.programmeCourant['capFinalMaxi']
      if self.asservissement.checkDeltaCapAtteint(capFinalMini, capFinalMaxi):
        finSequence = True
    elif conditionFin == 'duree':
      if (time.time() - self.timeDebut) > self.programmeCourant['duree']:
        finSequence = True
    elif conditionFin == 'immediat':
      finSequence = True
    elif conditionFin == 'telemetre':
      if self.arduino.bestTelemetrePourDetectionVirage() > self.programmeCourant['distSupA']:
        #if self.last_mesure_depassement:
        #  if self.last_mesure_telemetre1 != self.arduino.telemetre1:
        #    print "Telemetre1 : ", self.arduino.telemetre1, " Distance a depasser : ", self.programmeCourant['distSupA']
        #    self.last_mesure_telemetre1 = self.arduino.telemetre1
        #  # Verifie si depassement du telemetre1 pendant longtemps + confirmation par telemetre IR
        #  if (time.time() > self.time_debut_depassement + self.DUREE_DEPASSEMENT_TELEMETRE) and (self.arduino.telemetreIR > self.DISTANCE_DEPASSEMENT_TELEMETRE_IR):
            finSequence = True
        #else:
        #  self.time_debut_depassement = time.time()
        #self.last_mesure_depassement = True
      #else:
      #  self.last_mesure_depassement = False
    elif conditionFin == 'attendBouton':
      self.vitesse_clignote_led = 0.3
      self.led_clignote = True
      if self.voiture.getBoutonPoussoir() == 0:
        self.led_clignote = False
        finSequence = True

    if finSequence:
      # Si le champ nextLabel est defini, alors il faut chercher le prochain element par son label
      if 'nextLabel' in self.programmeCourant:
        nextLabel = self.programmeCourant['nextLabel']
        for i in range(len(self.programme)):
          if 'label' in self.programme[i]:
            if self.programme[i]['label'] == nextLabel:
              # On a trouve la prochaine sequence
              self.sequence = i
      else:
      # Si le champ nextLabel n'est pas defini, on passe simplement a l'element suivant
        self.sequence += 1
      self.debut = True
      