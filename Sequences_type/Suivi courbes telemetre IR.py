	# Suivi courbes au telemetre IR
	VITESSE_SUIVI_COURBE_TELEMETRE_IR = 25
	DISTANCE_SUIVI_COURBE_TELEMETRE_IR = 60
	DUREE_SUIVI_COURBE_TELEMETRE_IR = 180

          {
            'instruction' : 'attendreGyroStable', # Attend stabilisation du gyro
            'conditionFin' : 'attendreGyroStable'
          },

          ###########################################################
          # SUIVI COURBES AU TELEMETRE IR
          ###########################################################

          {
           'instruction' : 'suiviCourbeTelemetre',               # Suivi courbes telemetre
            'vitesse' :     VITESSE_SUIVI_COURBE_TELEMETRE_IR,
            'distance' :     DISTANCE_SUIVI_COURBE_TELEMETRE_IR,
            'conditionFin' : 'duree',
            'duree' :    DUREE_SUIVI_COURBE_TELEMETRE_IR         # Fin au bout de n secondes
          },