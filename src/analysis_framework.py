#!/usr/bin/python

import os
import glob
import sys
import re
from utils import *

#Classes/methods to get data and prepare it for specified analysis tasks
#R wrappers relevent to this class


class ProjectEnv(object): #creates project folders (relative paths) before project execution
	def __init__(self,projDir):
		self.projDir = projDir
	def makeProj(self): #makes project directory 
		os.system("cd "+envDir) #replace envDir with general dir from config
		os.system("mdkr "+self.projDir)
	
		#this will not work
	def startEnv(self): #add logic to match user input of desired tasks 
		os.system("cd "+self.projDir)
		os.system("mkdir mapping")
		os.system("mkdir QC")
		os.system("mkdir scripts")
		os.system("mkdir scripts/mapping")
		os.system("mkdir scripts/other")#for now
		os.system("mkdir differential_analysis")

class GatherUserInputs(object):
	def proc(self):
		pass
	def genome(self):
		pass
	def strand(self):
		pass


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

#word = ["I_100_bc20_GTGGCC_L001_R1_001.C3H70ACXX.fastq.gz","I_100_bc20_GTGGCC_L001_R2_001.C3H70ACXX.fastq.gz","I_100_bc20_GTGGCC_L002_R1_001.C3H70ACXX.fastq.gz","I_100_bc20_GTGGCC_L002_R2_001.C3H70ACXX.fastq.gz"]





# util = Utility()
# test = GatherData()
# for line in util.subDirectories("/home/immanuel/Desktop/"):
# 	print test.read1(glob.glob("/home/immanuel/Desktop/"+line+"/*.bed"))