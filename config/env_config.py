#!/usr/bin/python
import os
import sys
import yaml

#these classes are placed in a separate pythfon script
#because they are ideally to be used for setup and to add new genomes


class ImportSettings(object):
	def __init__(self, config):
		self.config = config
	def openConfig(self):
		with open('config.yaml', 'r') as f:
			doc = yaml.load(f)
		return doc
	def getEnv(self):
		env = openConfig()[]
		return env
	def homeDir(self): #usually a directory to store all analysis projects
		path = openConfig()[]
		return path 
	def genomes(self):
		pass
		#return dict of genomes and their paths
	def mappingPaths(self):
		#return dict of available short-read aligner paths/modules
		pass
	def pbsHeader(self):
		pass
		#must return string of pbs header for .pbs scripts on minerva


#create separate setup.py-type file for pipeline setup and update
	#update genome list class to update genome dictionary


#pbs args may be stored as dictionary or yaml entries for user input