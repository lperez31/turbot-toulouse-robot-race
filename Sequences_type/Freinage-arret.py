
          ###########################################################
          # FREINAGE PUIS ARRET
          ###########################################################


          {
            'instruction' : 'ligneDroite',              # Freinage
            'vitesse' : -30,
            'conditionFin' : 'duree',
            'duree' : 0.5
          },
          {
            'instruction' : 'ligneDroite',              # Arrêt
            'vitesse' : 0,
            'conditionFin' : 'duree',
            'duree' : 1.5
          }
