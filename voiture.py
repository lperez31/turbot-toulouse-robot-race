# encoding:utf-8

import wiringpi
import RPi.GPIO as GPIO

class Voiture:

  TRIM_DIRECTION = 12

  GPIO_BOUTON_POUSSOIR = 27
  GPIO_LED_ROUGE = 22

  duty_cycle_moteur_neutre = 75.0  # PWM ï¿½ envoyer au moteur pour qu'il ne tourne pas
  duty_cycle_moteur_max = 100.0     # PWM max du moteur
  echelle_vitesse = 100.0    # Vitesse max
  duty_cycle_direction_neutre = 76.0 # PWM ï¿½ envoyer au servo pour qu'il soit au neutre
  duty_cycle_debattement_direction = 12.0 # Dï¿½battement de direction (doit ï¿½tre infï¿½rieur ï¿½ duty_cycle_direction_neutre)
  echelle_debattement_direction = 100.0 # Direction max

  # Initialise les sorties PWM
  def __init__(self):

    # use BCM GPIO numbers
    wiringpi.wiringPiSetupGpio()

    # enable PWM0
    wiringpi.pinMode(18,2)
    wiringpi.pwmSetMode(0)
    wiringpi.pwmSetClock(400)
    wiringpi.pwmSetRange(1048)
  # wiringpi.pwmWrite(18, 75)  # 75=valeur approximative du neutre

    # enable PWM1
    wiringpi.pinMode(13,2)
    wiringpi.pwmSetMode(0)
    wiringpi.pwmSetClock(400)
    wiringpi.pwmSetRange(1024)
  # wiringpi.pwmWrite(13, 75)  # 75=valeur approximative du neutre

    # Choisit la numerotation des pins en "GPIO numbers"
    GPIO.setmode(GPIO.BCM)
    # Initialise entree bouton poussoir
    GPIO.setup(self.GPIO_BOUTON_POUSSOIR, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # set a port/pin as an input  
    # Initialise sortie led
    GPIO.setup(self.GPIO_LED_ROUGE, GPIO.OUT)       # set a port/pin as an output  


    # Arrête la voiture et met les roues au neutre
    self.tourne(0)
    self.avance(0)

  # Fait avancer (vitesse comprise entre 0 et echelle_vitesse)
  def avance(self, vitesse):
    pwm_val = int(((vitesse / self.echelle_vitesse) * (self.duty_cycle_moteur_max - self.duty_cycle_moteur_neutre)) + self.duty_cycle_moteur_neutre)
    wiringpi.pwmWrite(13, pwm_val)
    # print "Duty cycle: " + str(pwm_val)

  # Fait tourner (direction comprise entre -echelle_debattement_direction et echelle_debattement_direction)
  def tourne(self, direction):
    # Applique une exponentielle
    sign = 1 if direction > 0 else -1      
    direction = sign * (abs(direction) ** 0.7) * 4
    trim_pwm = (-self.TRIM_DIRECTION / self.echelle_debattement_direction) * self.duty_cycle_debattement_direction
    pwm_val = int(((-direction / self.echelle_debattement_direction) * self.duty_cycle_debattement_direction) + trim_pwm + self.duty_cycle_direction_neutre)
    wiringpi.pwmWrite(18, pwm_val)
    # print "Duty cycle: " + str(pwm_val)

  # Allume ou eteint la led
  def setLed(self, etat):
    GPIO.output(self.GPIO_LED_ROUGE, etat)

  # Recupere le statut du bouton poussoir
  def getBoutonPoussoir(self):
    return GPIO.input(self.GPIO_BOUTON_POUSSOIR)

  # Libere les GPIO (a appeler en quittant le programme)
  def gpioCleanUp(self):
    GPIO.cleanup()