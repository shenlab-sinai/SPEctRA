#!/usr/bin/python

import os
import glob
import sys
import re
from utils import *
from env_config import *
#Classes/methods to get data and prepare it for specified analysis tasks
#R wrappers relevent to this class

project = ImportSettings().homeDir()



class ProjectEnv(object): #creates project folders (relative paths) before project execution
	def __init__(self,projDir,envDir):
		self.projDir = projDir
		self.envDir = envDir
	
	def test(self): #makes project directory 

		#os.system("cd "+envDir) #replace envDir with general dir from config
		print "mkdir "+self.projDir
		print "mkdir "+self.projDir+"/"+"scripts"
		#this will not work


	def makeProj(self): #makes project directory 

		#os.system("cd "+envDir) #replace envDir with general dir from config
		os.system("mkdir "+self.envDir+"/"+self.projDir)
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"scripts")
		#this will not work
	def startMappingEnv(self): #add logic to match user input of desired tasks 
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"  mapping")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"QC")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"scripts/mapping")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"scripts/other")#for now
	#os.system("mkdir "+self.projDir+"/"+"differential_analysis") Add new method to do this later




class UserInputsConfigFile(object): #parses user submitted YAML file ( single command line options should be placed elswhere)

	def openConfig(self):
		with open('../pipeline_start_template.yaml', 'r') as f:
			doc = yaml.load(f)
		return doc
	def projName(self):
		project = self.openConfig()['project_Name']
		return project
	def proc(self):
		procNum = self.openConfig()['mapping']['proc']
		return procNum
	def genome(self):
		ref = self.openConfig()['mapping']['genome']
		return ref
	def strand(self):
		pairedStrand = self.openConfig()['mapping']['strand']
		return pairedStrand

class GatherData(object):
	#sort fastq samples to R1 and R2, even if multiple fastqs for one end are available
	util = Utility()
	def studySamples(self, fastq): #need to sort values 
	
		exp = "R[1|2]"
		samples = { }
		regex = re.compile(exp)
		for line in fastq: #change to glob library function
			if regex.search(line) is not None:
				read = re.findall(exp, line)
				samples.update({line:read[0]})
		#return dictionary of values		
		return samples		
	#these functions parse R1 and R2 data and return a string 
	def read1(self,fastq):
		R1 = ",".join([str(x) for x in self.util.findKey(self.studySamples(fastq),'R1')])
		return R1

	def read2(self,fastq):
		R2 = ",".join([str(x) for x in self.util.findKey(self.studySamples(fastq),'R2')])
		return R2
	#def pairwise(self) ...future parsing of pairwise combinations. Not this sprint









#word = ["I_100_bc20_GTGGCC_L001_R1_001.C3H70ACXX.fastq.gz","I_100_bc20_GTGGCC_L001_R2_001.C3H70ACXX.fastq.gz","I_100_bc20_GTGGCC_L002_R1_001.C3H70ACXX.fastq.gz","I_100_bc20_GTGGCC_L002_R2_001.C3H70ACXX.fastq.gz"]





# util = Utility()
# test = GatherData()
# for line in util.subDirectories("/home/immanuel/Desktop/"):
# 	print test.read1(glob.glob("/home/immanuel/Desktop/"+line+"/*.bed"))