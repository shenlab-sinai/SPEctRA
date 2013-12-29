#!/usr/bin/python
import os
import sys
import yaml

class ImportSettings(object):
	def __init__(self, config):
		self.config = config
	def openConfig(self):
		with open('config.yaml', 'r') as f:
			doc = yaml.load(f)
		return doc
	def getEnv(self):
		pass
	def homeDir(self):
		pass 
	def genomes(self):
		pass
		#return dict of genomes and their paths
	def paths(self):
		#return dict of available short-read aligner paths
		pass