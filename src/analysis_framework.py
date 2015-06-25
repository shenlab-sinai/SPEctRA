#!/usr/bin/python

import os
import glob
import sys
import re
import csv
from utils import *
from env_config import *
from commands import *

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
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"counts")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"scripts/mapping")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"scripts/QC")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"scripts/counts")#for now
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"logs/mapping")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"logs/QC")
		os.system("mkdir "+self.envDir+"/"+self.projDir+"/"+"logs/counts")
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
	def mergeDir(self):
		data = self.openConfig()['mapping']['merge_directory_path']
		return data
	def readCount(self):
		countMethod = self.openConfig()['count']
		return countMethod

class GatherData(object):
	#sort fastq samples to R1 and R2, even if multiple fastqs for one end are available
	util = Utility()
	def mergeReplicates(self,sampledir, repDir=None,mergeFile=None,):
		
		sample = glob.glob(sampledir+"/*.fastq*")

		if mergeFile is not None:

			paths = csv.reader(open(mergeFile,'r'), delimiter='\t')
			replicates={}
			for row in paths:
				replicates[row[0]]=row[1:]
			if replicates.get(os.path.basename(sampledir)) is not None:
			 	sample2 = glob.glob(replicates[os.path.basename(sampledir)][0]+"/*.fastq.gz")
			 	sample = sample+sample2

		return sample


	def studySamples(self, fastq): #need to sort values 

		exp = "R[1|2]"
		samples = { }
		regex = re.compile(exp)
		for line in fastq: #change to glob library function
			if regex.search(line) is not None:
				read = re.findall(exp, line)
				samples.update({line:read[0]})
			if regex.search(line) is None:
				samples.update({line:"R1"})
		#return dictionary of values
		return samples
	#these functions parse R1 and R2 data and return a string 
	def read1(self,fastq):
		R1 = ",".join(sorted([str(x) for x in self.util.findKey(self.studySamples(fastq),'R1')]))
		if R1 is None:
			R1 = self.studySamples(fastq)
		return R1

	def read2(self,fastq):
		R2 = ",".join(sorted([str(x) for x in self.util.findKey(self.studySamples(fastq),'R2')]))
		return R2
	#def pairwise(self) ...future parsing of pairwise combinations. Not this sprint

class ScriptWriter(object):
	util = Utility()
	fastqs = GatherData()
	
	def writeMappingScript(self,userInput,mergeFile=None): #writes mapping script #flexible for csv 
		
		inputs = UserInputsConfigFile(userInput)
		# star command in one script, himem
		#mkdir and change script location to more generalized directory name
		
		

		########################### resolve STAR later ##################################################
		# if inputs.aligner() == "STAR": #opens a single STAR mapping.lsf mapScript (himem queues only)
		# 	if settings.getEnv()["cluster"] is not 'None': 
		# 		mapScript = open(settings.homeDir()+"/"+inputs.projName()+"/"+"scripts/mapping/"+inputs.projName()+".STAR.mapping.lsf", "w")
		# 		mapScript.write(settings.lsfHeader(inputs.projName()+".STAR",settings.homeDir(),inputs.projName(),str(inputs.proc()),queue="himem_24hr")+"\n")
				
		for line in self.util.subDirectories(inputs.fastQdir()):
			
			#sample = glob.glob(inputs.fastQdir()+"/"+line+"/*.fastq.gz") #change to function call
			sample = self.fastqs.mergeReplicates(inputs.fastQdir()+"/"+line,inputs.mergeDir(),mergeFile)
			basedir = settings.homeDir()+"/"+inputs.projName()
			outdir = basedir+"/mapping/"+line+"."+ inputs.aligner()

			

			align = Mapping(self.fastqs.read1(sample),inputs.proc(), outdir,settings.genomes()[inputs.genome()][inputs.aligner()],fastqR2=self.fastqs.read2(sample))
			count = Counting(settings.genomes()[inputs.genome()]['tophat2']['gtf'],basedir+"/counts/"+line+"."+"htseq_counts"+".txt")
			countStrand = "no"
			

			if inputs.strand() == "fr-secondstrand":
				align = Mapping(self.fastqs.read1(sample),inputs.proc(), outdir,settings.genomes()[inputs.genome()][inputs.aligner()],libType="fr-secondstrand",fastqR2=self.fastqs.read2(sample)) 
				countStrand = "yes"
			
			########################### resolve STAR later ##################################################
			# if inputs.aligner() == "STAR": #opens a single STAR mapping.lsf mapScript (himem queues only)
			# 	if settings.getEnv()["cluster"] is not 'None':
			# 		mapScript.write("mkdir "+outdir+"\n") 
			# 		mapScript.write("cd "+outdir+"\n")
			# 		mapScript.write(str(align.STAR()+"\n"))

			if inputs.aligner() == "tophat2": #logic for tophat alignment...
				if settings.getEnv()["cluster"] is not None: #...on a cluster such as minerva
					mapScript = open(settings.homeDir()+"/"+inputs.projName()+"/"+"scripts/mapping/"+line+".tophat2.mapping.lsf", "w") #change to relative path
					#insert.lsf headers
					mapScript.write(settings.bsubHeader(inputs.projName()+"."+line,settings.homeDir(),inputs.projName(),str(inputs.proc()),"mapping"))
					#insert load modules

					#hardcoded env modules
					mapScript.write("module load python/2.7.6"+"\n"+"module load py_packages/2.7"+"\n")

					mapScript.write("module load samtools"+"\n"+"module load " + settings.mappingPaths()['bowtie2'] +"\n"+"module load " + settings.mappingPaths()['tophat2'] +"\n")
					#bowtie Index
					mapScript.write("export BOWTIE2_INDEXES="+settings.genomes()[inputs.genome()][inputs.aligner()]['index'] +"\n")
					mapScript.write(str(align.tophat()+"\n"))


					#launch qc bsub < here
					qcScriptPath = settings.homeDir()+"/"+inputs.projName()+"/"+"scripts/QC/"+line+".QC.lsf"
					qcScript = open(qcScriptPath, "w")
					qcScript.write(settings.bsubHeader(inputs.projName()+"."+line,settings.homeDir(),inputs.projName(),"1","QC",time="10:00",))
					qcScript.write("module load python/2.7.6"+"\n"+"module load py_packages/2.7"+"\n"+"module load samtools"+"\n")
					qcScript.write("python "+os.path.dirname(os.path.realpath(__file__))+"/quality_control.py " + outdir + " " + inputs.genome()+ " " + basedir+"/QC/"+line+"\n")

					mapScript.write("bsub < " + qcScriptPath +"\n")

					countScriptPath = settings.homeDir()+"/"+inputs.projName()+"/"+"scripts/counts/"+line+".counts.lsf" 
					countScript = open(countScriptPath, "w")
					countScript.write(settings.bsubHeader(inputs.projName()+"."+line,settings.homeDir(),inputs.projName(),"1","counts",time="24:00",))
					countScript.write("module load python/2.7.6"+"\n"+"module load py_packages/2.7"+"\n"+"module load samtools"+"\n")
					countScript.write("cd "+outdir+"\n")
					countScript.write(str(count.htseqcounts(outdir+"/accepted_hits.bam", countStrand))+"\n")
					mapScript.write("bsub < " + countScriptPath +"\n")

				if settings.getEnv()["server"] is not None:
					
					mapScript = open(settings.homeDir()+"/"+inputs.projName()+"/"+"scripts/mapping/"+line+".tophat2.mapping.sh", "w")
					mapScript.write("export BOWTIE2_INDEXES="+settings.genomes()[inputs.genome()][inputs.aligner()]['index'] +"\n")
					mapScript.write(str(align.tophat()+"\n"))


					qcScriptPath = settings.homeDir()+"/"+inputs.projName()+"/"+"scripts/QC/"+line+".QC.sh"
					qcScript = open(qcScriptPath, "w")
					qcScript.write("python "+os.path.dirname(os.path.realpath(__file__))+"/quality_control.py " + outdir + " " + inputs.genome()+ " " + basedir+"/QC/"+line+"\n")
					mapScript.write("./" + qcScriptPath +"\n")

					countScriptPath = settings.homeDir()+"/"+inputs.projName()+"/"+"scripts/counts/"+line+".counts.sh" 
					countScript = open(countScriptPath, "w")
					countScript.write("cd "+outdir+"\n")
					countScript.write(str(count.htseqcounts(outdir+"/accepted_hits.bam", countStrand))+"\n")
					mapScript.write("./" + countScriptPath +"\n")


					#mapScript.write("python "+os.path.dirname(os.path.realpath(__mapScript__))+"/quality_control.py " + outdir + " " + inputs.genome()+ " " + basedir+"/QC/"+line+"\n") 
					

					#launch mapping bsub < here
					#mapScript.write("cd "+outdir+"\n")
					#mapScript.write(str(count.htseqcounts(outdir+"/accepted_hits.bam", countStrand))+"\n")
		qcScript.close()
		countScript.close()
		mapScript.close()

	def writeCounterScript(self):
		pass

