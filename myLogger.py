import logging
from logging.handlers import RotatingFileHandler

class MyLogger:

	file_handler = None
	logger = None
	paramLogger = None

	def __init__(self):

		# Creation de l'objet logger qui va nous servir a ecrire dans les logs
		# Note : logger sert a logger l'execution du programme, paramLogger sert a enregistrer les parametres mesures dans un fichier csv
		logger = logging.getLogger('mainLogger')
		paramLogger = logging.getLogger('csvFile')

		# Indique quel niveau de logs on veut voir apparaitre
		paramLogger.setLevel(logging.DEBUG)
		logger.setLevel(logging.INFO)

		# Creation de formatteurs qui vont ajouter le temps a chaque log et le niveau de log
		formatter1 = logging.Formatter('%(created)f,%(message)s')
		formatter2 = logging.Formatter('%(created)f :: %(levelname)s :: %(message)s')

		# Creation d'un file handler pour ecrire dans un fichier
		file_handler = RotatingFileHandler('parametres.log', 'a', 0, 100000)
		# Passe au fichier suivant
		file_handler.doRollover()
		# Initialise les parametres de logging du fichier
		file_handler.setLevel(logging.DEBUG)
		file_handler.setFormatter(formatter1)
		paramLogger.addHandler(file_handler)

		# Creation du logger pour les messages d'execution du programme
		stream_handler = logging.StreamHandler()
		stream_handler.setLevel(logging.DEBUG)
		stream_handler.setFormatter(formatter2)
		logger.addHandler(stream_handler)

		self.file_handler = file_handler
		self.logger = logger
		self.paramLogger = paramLogger

	def close(self):
		self.file_handler.close()