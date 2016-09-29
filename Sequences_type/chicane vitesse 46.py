  # Chicane
  VITESSE_ENTREE_CHICANE = 42
  DISTANCE_DECLENCHEMENT_CHICANE = 45
  VITESSE_PREMIER_VIRAGE = 42
  VITESSE_CHICANE = 46
  DUREE_LIGNE_DIAGONALE_CHICANE_1 = 0.7
  DUREE_LIGNE_DIAGONALE_CHICANE_2 = DUREE_LIGNE_DIAGONALE_CHICANE_1
  DUREE_LIGNE_DIAGONALE_CHICANE_3 = DUREE_LIGNE_DIAGONALE_CHICANE_1
  DUREE_LIGNE_DIAGONALE_CHICANE_4 = DUREE_LIGNE_DIAGONALE_CHICANE_1 - 0.1
  DELTA_CAP_LIGNE_DIAGONALE = 26
  DUREE_LIGNE_DROITE_CHICANE_1 = 0.35
  DUREE_LIGNE_DROITE_CHICANE_2 = DUREE_LIGNE_DROITE_CHICANE_1
  DUREE_LIGNE_DROITE_CHICANE_3 = DUREE_LIGNE_DROITE_CHICANE_1
  DUREE_LIGNE_DROITE_CHICANE_4 = DUREE_LIGNE_DROITE_CHICANE_1

          ###########################################################
          # CHICANES              ETAPE 4
          ###########################################################

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
