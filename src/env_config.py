#!/usr/bin/python
import os
import sys
import yaml

#parses necessary base variables. 
class ImportSettings(object):
	# def __init__(self, config):
	# 	self.config = config
	def openConfig(self):
		with open('config_template.yaml', 'r') as f:
			doc = yaml.load(f)
		return doc
	def getEnv(self):
		env = self.openConfig()["Environment"]
		return env
	def homeDir(self): #usually a directory to store all analysis projects
		path = self.openConfig()["project_directory"]
		return path 
	def genomes(self):
		supported = self.openConfig()["genomes"]
		return supported
		#return dict of genomes and their paths
	def mappingPaths(self):
		#return dict of available short-read aligner paths/modules
		aligner = self.openConfig()["Short-read_aligners"]
		return aligner
	def pbsHeader(self):
		header = self.openConfig()["PBS_Headers"]
		return header
		#must return string of pbs header for .pbs scripts on minerva

class ClusterSettings(object):

	def PBSdefaults(self):

#create separate setup.py-type file for pipeline setup and update
	#update genome list class to update genome dictionary


#pbs args may be stored as dictionary or yaml entries for user input

#test = ImportSettings()
#print test.genomes()["tophat2"]["mouse"]["gtf"]