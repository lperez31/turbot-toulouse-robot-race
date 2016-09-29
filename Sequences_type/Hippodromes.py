  # Hippodromes
  
  programme = [
          {
            'instruction' : 'attendreGyroStable',
            'conditionFin' : 'attendreGyroStable'
          },
          {
            'instruction' : 'setCap',
            'conditionFin' : 'immediat'
          },
          {
            'label' : 'debutLigneDroite',
            'instruction' : 'ligneDroite',
            'vitesse' : 55,
            'conditionFin' : 'duree',
            'duree' : 1.0
          },
          {
           'instruction' : 'ligneDroiteTelemetre',
            'vitesse' : 55,
#            'conditionFin' : 'telemetre',
#            'distSupA' : 80
            'conditionFin' : 'duree',
            'duree' : 3.0
          },
          {
           'instruction' : 'ligneDroiteTelemetre',
            'vitesse' : 25,
#            'conditionFin' : 'telemetre',
#            'distSupA' : 80
            'conditionFin' : 'duree',
            'duree' : 1.0
          },                
          {
            'instruction' : 'tourne',
            'positionRoues' : -100,
            'vitesse' : 25,
            'conditionFin' : 'cap',
            'capFinalMini' : 90,  # En relatif par rapport au cap initial
            'capFinalMaxi' : 210  # En relatif par rapport au cap initial
          },
          {
            'instruction' : 'ajouteCap',
            'cap' : 180,
            'conditionFin' : 'immediat',
          },
          {
            'instruction' : 'ligneDroite',
            'vitesse' : 55,
            'conditionFin' : 'duree',
            'duree' : 4.0
          },
          {
            'instruction' : 'tourne',
            'positionRoues' : -100,
            'vitesse' : 25,
            'conditionFin' : 'cap',
            'capFinalMini' : 90,  # En relatif par rapport au cap initial
            'capFinalMaxi' : 210  # En relatif par rapport au cap initial
          },
          {
            'instruction' : 'ajouteCap',
            'cap' : 180,
            'conditionFin' : 'immediat',
            'nextLabel' : 'debutLigneDroite'
          }
        ]
