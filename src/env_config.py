#!/usr/bin/python
import os
import sys
import yaml

#parses necessary base variables. 
class ImportSettings(object):
	# def __init__(self, config):
	# 	self.config = config
	def openConfig(self):
		dir = os.path.dirname(__file__)
		filename = os.path.join(dir, "config_template.yaml")
		with open(filename, 'r') as f:
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
	def pbsHeader(self,name,directory,proc,time="24:00:00", nodes ="1",queue="small_24hr"): #hardcoded for minerva args. Change this to be more flexible
		env = "#!/bin/bash"+"\n"
		acc = "" #PBS -A acc_80"+"\n"
		queue= "#PBS -q "+queue+"\n"
		proc = "#PBS -l nodes="+nodes+":ppn="+proc+"\n"
		time = "#PBS -l walltime="+time+"\n"
		jobID = "#PBS -N "+name+"\n"
		log = "#PBS -o "+directory+"/logs/mapping/"+ name+".log"+"\n"
		err = "#PBS -e "+directory+"/logs/mapping/"+ name+".log"+"\n"
		header = env + acc+queue+proc + time + jobID + log + err + "\n"
		return header  
# 	def openConfig(self):

#create separate setup.py-type file for pipeline setup and update
	#update genome list class to update genome dictionary


#pbs args may be stored as dictionary or yaml entries for user input

#test = ImportSettings()
#print test.genomes()["tophat2"]["mouse"]["gtf"]
