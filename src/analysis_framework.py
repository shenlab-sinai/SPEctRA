#!/usr/bin/python

import os
import glob
import sys
import re
from utils import *
from env_config import *
from mapping import *

#Classes/methods to get data and prepare it for specified analysis tasks
#R wrappers relevent to this class

settings = ImportSettings()


class SetProjectEnv(object): #creates project folders (relative paths) before project execution
	def __init__(self,envDir,projDir):
		self.projDir = projDir
		self.envDir = envDir
	def makeProj(self): #makes project directory 
		os.system("mkdir "+self.envDir+"/"+self.projDir)
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"scripts")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"logs")
	def startMappingEnv(self): #add logic to match user input of desired tasks 
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"mapping")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"QC")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"scripts/mapping")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"logs/mapping")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"scripts/other")#for now
	#os.system("mkdir "+self.projDir+"/"+"differential_analysis") Add new method to do this later

class UserInputsConfigFile(object): #parses user submitted YAML file ( single command line options should be placed elswhere)
	def __init__(self,inputYaml):
	 	self.inputYaml = inputYaml
	def openConfig(self):
		with open(str(self.inputYaml), 'r') as f:
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
	def aligner(self):
		mapper = self.openConfig()['mapping']['aligner']
		return mapper
	def fastQdir(self):
		data = self.openConfig()['mapping']['fastQ_directory_path']
		return data
	def readCount(self):
		countMethod = self.openConfig()['count']
		return countMethod
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

class ScriptWriter(object):
	util = Utility()
	fastqs = GatherData()
	
	def writeMappingScript(self,userInput): #writes mapping script
		
		inputs = UserInputsConfigFile(userInput)
		# star command in one script, himem
		#mkdir and change script location to more generalized directory name
		
		if inputs.aligner() == "STAR": #opens a single STAR mapping pbs file (himem queues only)
			if settings.getEnv()["cluster"] is not 'None': 
				file = open(settings.homeDir()+"/"+inputs.projName()+"/"+"scripts/mapping/"+inputs.projName()+".STAR.mapping.pbs", "w")
				file.write(settings.pbsHeader(inputs.projName()+".STAR",settings.homeDir(),inputs.projName(),str(inputs.proc()),queue="himem_24hr")+"\n")
				
		for line in self.util.subDirectories(inputs.fastQdir()):
			
			sample = glob.glob(inputs.fastQdir()+"/"+line+"/*.fastq.gz")
			basedir = settings.homeDir()+"/"+inputs.projName()
			outdir = basedir+"/mapping/"+line+"."+ inputs.aligner()

			

			align = Mapping(self.fastqs.read1(sample),inputs.proc(), outdir,settings.genomes()[inputs.genome()][inputs.aligner()],fastqR2=self.fastqs.read2(sample))
			
			if inputs.strand() == "fr-secondstrand":
				align = Mapping(self.fastqs.read1(sample),inputs.proc(), outdir,settings.genomes()[inputs.genome()][inputs.aligner()],libType="fr-secondstrand",fastqR2=self.fastqs.read2(sample)) 
			
			if inputs.aligner() == "STAR": #opens a single STAR mapping pbs file (himem queues only)
				if settings.getEnv()["cluster"] is not 'None':
					file.write("mkdir "+outdir+"\n") 
					file.write("cd "+outdir+"\n")
					file.write(str(align.STAR()+"\n"))

			if inputs.aligner() == "tophat2": #logic for tophat alignment...
				if settings.getEnv()["cluster"] is not 'None': #...on a cluster such as minerva
					file = open(settings.homeDir()+"/"+inputs.projName()+"/"+"scripts/mapping/"+line+".tophat2.mapping.pbs", "w") #change to relative path
					#insert pbs headers
					file.write(settings.pbsHeader(inputs.projName()+"."+line,settings.homeDir(),inputs.projName(),str(inputs.proc())))
					#insert load modules

					#hardcoded env modules
					file.write("module load python/2.7.3"+"\n"+"module load pysam/0.6"+"\n"+"module load pyyaml/3.10"+"\n")

					file.write("module load samtools"+"\n"+"module load " + settings.mappingPaths()['bowtie2'] +"\n"+"module load " + settings.mappingPaths()['tophat2'] +"\n")
					#bowtie Index
					file.write("export BOWTIE2_INDEXES="+settings.genomes()[inputs.genome()][inputs.aligner()]['index'] +"\n")
					file.write(str(align.tophat()+"\n"))
					#insert post-processing
					#insert QC 
					file.write("python "+os.path.dirname(os.path.realpath(__file__))+"/quality_control.py " + outdir + " " + inputs.genome()+ " " + basedir+"/QC/"+line) #uncomment this when you fix this class
		file.close()

	def writeCounterScript(self):
		pass

