# encoding:utf-8

import logging
import time
logger = logging.getLogger('mainLogger')
paramLogger = logging.getLogger('csvFile')

class Asservissement:

  # PID
  # Le coeff proportionnel reel depend de la vitesse
  COEFF_PROPORTIONNEL_POUR_VITESSE_NOMINALE = 1.0 # 0.7
  COEFF_PROPORTIONNEL_POUR_VITESSE_MIN = 2.0 # 2.0
  VITESSE_NOMINALE = 45
  VITESSE_MIN = 25
  COEFF_INTEGRAL = 0.064 # 0.05. Sinon 0.1 avant multiplication par environ 2,7 de la vitesse d'acquisition gyro 
  COEFF_AMORTISSEMENT_INTEGRAL = 1.0 # Attention, c'est l'amortissement. Inutilise.
  COEFF_DERIVEE = 3.9
  MAX_CUMUL_ERREUR_CAP = 200   # Cumul max des erreurs de cap pour le calcul integral (en degres)

  # PID suivi de bordure au telemetre
  COEFF_SUIVI_LIGNE_P = 0.13
  AMPLIFICATEUR_P_ANTI_PROCHE = 3 # Coeff multiplicateur pour P quand on est en mode anti proche
  COEFF_SUIVI_LIGNE_I = 0.1 * COEFF_SUIVI_LIGNE_P
  MAX_CUMUL_ERREUR_DISTANCE = 4 / COEFF_SUIVI_LIGNE_I    # Cumul max des erreurs de distance pour le calcul integral (en cm), avec N/COEFF_I, N est en degres (correction max I)
  MAX_CORRECTION_CAP_TELEMETRE = 10  # Correction de cap maxi lors du suivi de bordure au telemetre (en degres)

  # Autres constantes
  DELTA_T_SUIVI_COURBES = 0.1
  COEFF_DERIVEE_TELEMETRE_COURBES = 0.8
  COEFF_ERREUR_TELEMETRE_COURBES = 0.5

  arduino = None
  voiture = None
  capTarget = 0.0
  ligneDroite = False
  ligneDroiteTelemetre = False
  activationDistanceIntegrale = False
  antiProche = False
  recalageAutoCap = False
  suiviCourbesTelemetre = False
  distance_ligne_droite_telemetre = 40
  distance_courbes_telemetre = 40
  vitesse = 0
  calculCapSuiviCourbesEnCours = False
  timeLastCalculSuiviCourbe = time.time()
  mesureTelemetrePourSuiviCourbe = 0.0
  lastCapASuivrePourSuiviCourbe = 0.0
  capTargetSuiviCourbe = 0.0
  lastErreurCap = 0.0

  cumulErreurCap = 0.0
  cumulErreurDistanceBordure = 0.0

  def __init__(self, arduino, voiture):
    self.arduino = arduino
    self.voiture = voiture

  # A appeler lorsqu'on demarre un asservissement de ligne droite
  def initLigneDroite(self):
    self.ligneDroite = True
    self.ligneDroiteTelemetre = False
    self.suiviCourbesTelemetre = False
    self.recalageAutoCap = False
    self.cumulErreurCap = 0

  # A appeler lorsqu'on demarre un asservissement de ligne droite au telemetre
  # recalageCap indique si on doit recaler automatiquement le cap
  def initLigneDroiteTelemetre(self, distance, recalageCap, activationDistanceIntegrale, antiProche):
    self.ligneDroite = True
    self.ligneDroiteTelemetre = True
    self.suiviCourbesTelemetre = False
    self.recalageAutoCap = recalageCap
    self.distance_ligne_droite_telemetre = distance
    self.cumulErreurCap = 0.0
    self.cumulErreurDistanceBordure = 0.0
    self.activationDistanceIntegrale = activationDistanceIntegrale
    self.antiProche = antiProche

  # A appeler lorsqu'on demarre un asservissement de courbe au telemetre
  def initCourbeTelemetre(self, distance):
    self.ligneDroite = False
    self.ligneDroiteTelemetre = False
    self.suiviCourbesTelemetre = True
    self.distance_courbes_telemetre = distance
    self.calculCapSuiviCourbesEnCours = False
    self.cumulErreurCap = 0.0
    self.cumulErreurDistanceBordure = 0.0

  # A appeler lorsqu'on modifie la vitesse (permet au coefficient P d'etre plus eleve quand on roule moins vite)
  def setVitesse(self, vitesse):
    self.vitesse = vitesse

  # A appeler lorsqu'on demarre un asservissement autre que la ligne droite
  def annuleLigneDroite(self):
    self.ligneDroite = False
    self.ligneDroiteTelemetre = False
    self.recalageAutoCap = False

  # Definit le cap a suivre au cap courant
  def setCapTarget(self):
    target = self.arduino.getCap()
    print 'Cap Target : ', target
    self.capTarget = target

  # Ajoute deltaCap au cap a suivre
  def ajouteCap(self, deltaCap):
    self.capTarget = (self.capTarget + deltaCap) % 360
    print "Nouveau cap : ", self.capTarget

  # Verifie si le cap est compris entre capTarget+capFinalMini et capTarget+capFinalMaxi
  def checkDeltaCapAtteint(self, capFinalMini, capFinalMaxi):
    absoluteCapMini = (self.capTarget + capFinalMini) % 360
    absoluteCapMaxi = (self.capTarget + capFinalMaxi) % 360

    ecartCapMini = (((self.arduino.getCap() - absoluteCapMini) + 180) % 360 ) - 180
    ecartCapMaxi = (((self.arduino.getCap() - absoluteCapMaxi) + 180) % 360 ) - 180

    if (ecartCapMini > 0 and ecartCapMaxi < 0):
      print "--------------- Fin de virage ----------------"
      print "CapTarget : ", self.capTarget, "Cap : ", self.arduino.getCap(), " Ecart cap mini : ", ecartCapMini, " Ecart cap maxi : ", ecartCapMaxi
      print "----------------------------------------------"

    return (ecartCapMini > 0 and ecartCapMaxi < 0)   

  # Execute l'asservissement
  def execute(self):

    arduino = self.arduino
    if arduino.nouvelleDonneeGyro:

      arduino.nouvelleDonneeGyro = False

      capASuivre = 0.0
      positionRoues = 0

      # Si on doit asservir selon la ligne droite
      if self.ligneDroite or self.suiviCourbesTelemetre:

        # Si on doit faire une ligne droite
        if self.ligneDroite:
          capASuivre = self.capTarget

          #######################################
          # Asservissement ligne droite telemetre
          #######################################   
          if self.ligneDroiteTelemetre:
            # Calcule le cap a suivre en fonction de la distance du telemetre (uniquement si la valeur du telemetre est bonne)
            mesureDistance = arduino.bestTelemetrePourSuiviBordure() # Utilise exclusivement ultrason et lidar
            p = self.COEFF_SUIVI_LIGNE_P / 3 # On asservit mollement
            i = self.COEFF_SUIVI_LIGNE_I / 3
            autoriseRecalage = True
            if (mesureDistance > 200):  # TODO si besoin ne faire l'asservissement que si mesureDistance est à +-25cm de la consigne
              # Si on n'a pas de bonne mesure, alors on utilise le telemetre IR
              mesureDistance = self.arduino.telemetreIR
              p = self.COEFF_SUIVI_LIGNE_P / 3   # Asservissement beaucoup plus mou avec telemetre IR
              i = self.COEFF_SUIVI_LIGNE_I / 3
              autoriseRecalage = False
            erreurDistance = mesureDistance - self.distance_ligne_droite_telemetre

            # Si on est en mode antiProche, ne prendre en compte que les erreurs de distance négatives (trop proches)
            amplificateurPAntiProche = 1
            if self.antiProche:
              if erreurDistance > 0:
                erreurDistance = 0
                amplificateurPAntiProche = self.AMPLIFICATEUR_P_ANTI_PROCHE

            correctionProportionnelle = erreurDistance * self.COEFF_SUIVI_LIGNE_P * amplificateurPAntiProche

            self.cumulErreurDistanceBordure += max(min(erreurDistance, 10), -10) # Inutile de cumuler trop vite quand on est vraiment trop loin 
            # Maintient le cumul des erreurs à une valeur raisonnable
            self.cumulErreurDistanceBordure = max(min(self.cumulErreurDistanceBordure, self.MAX_CUMUL_ERREUR_DISTANCE), -self.MAX_CUMUL_ERREUR_DISTANCE)

            print "Cumul erreur distance: ", self.cumulErreurDistanceBordure
            if self.activationDistanceIntegrale:
              correctionIntegrale = self.cumulErreurDistanceBordure * self.COEFF_SUIVI_LIGNE_I
            else:
              correctionIntegrale = 0

            correctionCap = max( min( correctionProportionnelle + correctionIntegrale, self.MAX_CORRECTION_CAP_TELEMETRE), -self.MAX_CORRECTION_CAP_TELEMETRE)
            capASuivre = (capASuivre + correctionCap ) % 360

            # Execute le calcul de la derive du cap si c'est demande
            if self.recalageAutoCap and autoriseRecalage:
              arduino.executeRecalageCap(self.capTarget)

          print "bestTelemetre: ", arduino.bestTelemetre, "Telemetre1: ", arduino.telemetre1, " TelemetreIR: ", arduino.telemetreIR
          print "bestTelemetrePourDetectionVirage: ", arduino.bestTelemetrePourDetectionVirage()
          print "Cap Target : ", self.capTarget, " Cap A suivre : ", capASuivre

        # Si on doit suivre les courbes selon le telemetre
        elif self.suiviCourbesTelemetre:
          capASuivre = self.calculeCapSuiviCourbes()

        ###############################
        # Effectue l'asservissement PID
        ###############################
        erreurCap = (((arduino.getCap() - capASuivre) + 180) % 360 ) - 180
        print "Erreur cap : ", erreurCap      
        self.cumulErreurCap = (self.cumulErreurCap / self.COEFF_AMORTISSEMENT_INTEGRAL) + erreurCap
        # Maintient le cumul des erreurs à une valeur raisonnable
        self.cumulErreurCap = max(min(self.cumulErreurCap, self.MAX_CUMUL_ERREUR_CAP), -self.MAX_CUMUL_ERREUR_CAP)
        print "Cumul erreur cap : ", self.cumulErreurCap, " time : ", time.time()
        # Calcul de D
        correctionDerivee = -self.COEFF_DERIVEE * (erreurCap - self.lastErreurCap)
        self.lastErreurCap = erreurCap

        coeff_proportionnel = self.COEFF_PROPORTIONNEL_POUR_VITESSE_MIN  + ( (self.vitesse - self.VITESSE_MIN) * (self.COEFF_PROPORTIONNEL_POUR_VITESSE_NOMINALE - self.COEFF_PROPORTIONNEL_POUR_VITESSE_MIN) / (self.VITESSE_NOMINALE - self.VITESSE_MIN) )
        positionRoues = min(max( int( -(coeff_proportionnel * erreurCap) - (self.COEFF_INTEGRAL * self.cumulErreurCap) + correctionDerivee ), -100), 100)
        print "Position roues : ", positionRoues
        self.voiture.tourne(positionRoues)

        # Loggue cap, cap corrige, roulis, tangage, telemetre, instruction==ligne droite, instruction==ligne droite telemetre, cap Target, cap a suivre (apres correction telemetre), positionRoues
        paramLogger.info(str(arduino.gyroX) + ',' + str(arduino.getCap()) + ',' + str(arduino.gyroY) + ',' + str(arduino.gyroZ) + ',' + str(arduino.telemetre1) + ',' + str(self.ligneDroite) + ',' + str(self.ligneDroiteTelemetre) + ',' + str(self.capTarget) + ',' + str(capASuivre) + ',' + str(positionRoues) + ',' + str(arduino.telemetreIR) + ',' + str(arduino.telemetreLidar) + ',' + str(arduino.bestTelemetrePourSuiviBordure()) + ',' + str(arduino.bestTelemetrePourDetectionVirage()))

    if arduino.nouvelleDonneeTelemetre1:
      # Loggue cap, cap corrige, roulis, tangage, telemetre, instruction==ligne droite, instruction==ligne droite telemetre, cap Target, cap a suivre (apres correction telemetre), positionRoues
      paramLogger.info(str(arduino.gyroX) + ',' + str(arduino.getCap()) + ',' + str(arduino.gyroY) + ',' + str(arduino.gyroZ) + ',' + str(arduino.telemetre1) + ',' + str(self.ligneDroite) + ',' + str(self.ligneDroiteTelemetre) + ',' + str(self.capTarget) + ',' + '' + ',' + '' + ',' + str(arduino.telemetreIR) + ',' + str(arduino.telemetreLidar)  + ',' + str(arduino.bestTelemetrePourSuiviBordure()) + ',' + str(arduino.bestTelemetrePourDetectionVirage()))
      arduino.nouvelleDonneeTelemetre1 = False
      # print "Telemetre1 : ", "{:4.1f}".format(self.arduino.telemetre1), " TelemetreIR : ", "{:4.1f}".format(self.arduino.telemetreIR), " Lidar : ", self.arduino.telemetreLidar, " Best: ", self.arduino.bestTelemetre
      #print "functionBest : ", "{:4.1f}".format(self.arduino.bestTelemetrePourSuiviBordure()), " TelemetreIR : ", "{:4.1f}".format(self.arduino.telemetreIR), " Lidar : ", self.arduino.telemetreLidar, " Best: ", self.arduino.bestTelemetre
      #print "bestForVirage : ", "{:4.1f}".format(self.arduino.bestTelemetrePourDetectionVirage())

  # Calcule le cap a suivre pour le suivi de courbes au telemetre
  def calculeCapSuiviCourbes(self):
    arduino = self.arduino
    print "Enter calcul suivi courbes"
    if self.calculCapSuiviCourbesEnCours == False:
      print "Premiere mesure"
      # Premiere mesure
      self.timeLastCalculSuiviCourbe = time.time()
      self.mesureTelemetrePourSuiviCourbe = arduino.telemetreIR
      self.calculCapSuiviCourbesEnCours = True
      print "Arduino cap : ", arduino.getCap()
      capASuivre = arduino.getCap()
      self.capTargetSuiviCourbe = capASuivre
    
    elif time.time() > (self.timeLastCalculSuiviCourbe + self.DELTA_T_SUIVI_COURBES):
      # C'est le moment de recaler le cap de suivi de courbes
      print "Recalage suivi courbes"
      print "Arduino telemetreIR : ", arduino.telemetreIR
      print "Mesure telemetre ancienne : ", self.mesureTelemetrePourSuiviCourbe
      deltaTelemetre = arduino.telemetreIR - self.mesureTelemetrePourSuiviCourbe
      print "----- deltaTelemetre : ", deltaTelemetre
      correctionCapDerivee = deltaTelemetre * self.COEFF_DERIVEE_TELEMETRE_COURBES
      correctionCapDistance = (arduino.telemetreIR - self.distance_courbes_telemetre) * self.COEFF_ERREUR_TELEMETRE_COURBES
      correctionCapDerivee = max(min(correctionCapDerivee, 5), -5)
      correctionCapDistance = max(min(correctionCapDistance, 5), -5)
      print "correctionCapDerivee : ", correctionCapDerivee
      print "correctionCapDistance : ", correctionCapDistance
      # if (arduino.telemetreIR - self.distance_courbes_telemetre) > 0:
      #  correctionCapDerivee = 0
      capASuivre = self.capTargetSuiviCourbe + correctionCapDerivee + correctionCapDistance 

      self.mesureTelemetrePourSuiviCourbe = arduino.telemetreIR
      print "Cap actuel : ", arduino.getCap(), " Cap a suivre : ", capASuivre
      self.capTargetSuiviCourbe = capASuivre
    
      #if (arduino.telemetreIR - self.distance_courbes_telemetre) < -10:
      #  capASuivre = arduino.getCap() - 15
      #elif (arduino.telemetreIR - self.distance_courbes_telemetre) > 10:
      #  capASuivre = arduino.getCap() + 15

    else:
      capASuivre = self.capTargetSuiviCourbe

    return capASuivre
  