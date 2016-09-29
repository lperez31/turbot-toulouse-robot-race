  # Premiere ligne droite
  VITESSE_PREMIERE_LIGNE_DROITE = 25
  DUREE_PREMIERE_LIGNE_DROITE = 3.0
  DISTANCE_BORDURE_PREMIERE_LIGNE_DROITE = 30

  # Ligne droite avant 180°
  VITESSE_LIGNE_DROITE_AVANT_180 = 25
  DISTANCE_DECLENCHEMENT_180 = 50

  # Virage 180°
  POSITION_ROUES_180_DEBUT = 44
  POSITION_ROUES_180_FIN = 21
  VITESSE_180_DEBUT = 25
  VITESSE_180_FIN = 25
  DUREE_180_DEBUT = 0.5
  CAP_MIN_180_FIN = 150 # Virage 180 à droite : min 150, max 270 - A gauche : min 90, max 210
  CAP_MAX_180_FIN = 270

  # Ligne droite apres premier virage 180°
  VITESSE_LIGNE_DROITE_APRES_PREMiER_VIRAGE = 25
  DISTANCE_BORDURE_APRES_PREMIER_VIRAGE = 30
  DUREE_LIGNE_DROITE_APRES_PREMIER_VIRAGE = 2

          ###########################################################
          # Attente stabilisation gyro - ETAPE 0
          ###########################################################


          {
            'instruction' : 'attendreGyroStable', # Attend stabilisation du gyro
            'conditionFin' : 'attendreGyroStable'
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
            'distance' :      DUREE_PREMIERE_LIGNE_DROITE,
            'conditionFin' : 'duree',
            'duree' :         DISTANCE_BORDURE_PREMIERE_LIGNE_DROITE
          },

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
            'instruction' : 'tourne',                   # Commence par tourner fort
            'positionRoues' : POSITION_ROUES_180_DEBUT,
            'vitesse' : VITESSE_180_DEBUT,
            'conditionFin' : 'duree',
            'duree' :         DUREE_180_DEBUT
          },
          {
            'instruction' : 'tourne',                   # Puis finit le virage 180°
            'positionRoues' : POSITION_ROUES_180_FIN,
            'vitesse' : VITESSE_180_FIN,
            'conditionFin' : 'cap',
            'capFinalMini' : CAP_MIN_180_FIN,  # En relatif par rapport au cap initial
            'capFinalMaxi' : CAP_MAX_180_FIN  # En relatif par rapport au cap initial
          },

          {
            'instruction' : 'ajouteCap',
            'cap' : 180,
            'conditionFin' : 'immediat',
          },

          ###########################################################
          # LIGNE DROITE AVEC SUIVI BORDURE      ETAPE 3
          ###########################################################

          {
            'label' :        'debutLigneDroite',         # Ligne droite avec suivi bordure
            'instruction' :  'ligneDroiteTelemetre',
            'vitesse'  :      VITESSE_LIGNE_DROITE_APRES_PREMiER_VIRAGE,
            'distance' :      DISTANCE_BORDURE_APRES_PREMIER_VIRAGE,
            'conditionFin' : 'duree',
            'duree' :         DUREE_LIGNE_DROITE_APRES_PREMIER_VIRAGE
          },