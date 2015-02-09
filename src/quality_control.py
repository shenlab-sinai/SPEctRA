#!/usr/bin/python
from utils import *
import re
import pysam
import os
import csv
import subprocess
from env_config import *
from analysis_framework import *

shell_splitUnique = "|cut -f1|sort -u |wc -l" #shell command to count unique reads only


settings = ImportSettings()


#add fastqc class here


class GetReads(object):
	def __init__(self,dir,genome): #pass directory to this class
		self.dir = dir
		self.genome = genome
		
	#figure out how to execute this class properly

		
	def unmapped(self):
		command = "samtools view "+self.dir+"/unmapped.bam " + shell_splitUnique
		unmapped = subprocess.check_output(command, shell=True)
		return unmapped

	def mappedTotal(self): #support all alignment outputs  in future
		command = "samtools view -F 12 "+self.dir+"/accepted_hits.bam " + shell_splitUnique
		mappedReads = subprocess.check_output(command, shell=True)

		return mappedReads

	def tophatTotal(self):
		totalReads = int(self.unmapped()) + int(self.mappedTotal())
		return totalReads
	#individual mapping rates
	def intragenic(self): 
		command = "samtools view "+self.dir+"/accepted_hits.bam -L "+ intragenicPath + " " + shell_splitUnique
		intragenic = subprocess.check_output(command, shell=True)
		return intragenic
	
	def exon(self):
		command = "samtools view -F 12"+self.dir+"/accepted_hits.bam -L "+ settings.genomes()[self.genome]["exonicPath"] + " " + shell_splitUnique
		exon = subprocess.check_output(command, shell=True)
		return exon

	def intron(self):
		command = "samtools view -F 12"+self.dir+"/accepted_hits.bam -L "+ settings.genomes()[self.genome]["intronicPath"] + " " + shell_splitUnique
		intron = subprocess.check_output(command, shell=True)
		return intron 

	def intergenic(self):
		intergenic = self.mappedTotal - self.intragenic()
		return intergenic
	
	def mitochondrial(self):
		# os.system("samtools index "+self.dir+"/accepted_hits.bam")
		# mitochondrial = pysam.Samfile(self.dir+"/accepted_hits.bam", "rb" ).count(region='MT')
		command = "samtools view -F 12 "+self.dir+"/accepted_hits.bam | grep MT "+shell_splitUnique
		mitochondrial = subprocess.check_output(command, shell=True)
		return mitochondrial
	
	def ribosomal(self):
		
		command = "samtools view -F 12 "+self.dir+"/accepted_hits.bam -L " +settings.genomes()[self.genome]["rRNApath"]+ " " + shell_splitUnique
		ribosomal = subprocess.check_output(command, shell=True)
		
		return ribosomal

class QCReport(object):
	
	def __init__(self,dir,genome): #pass directory to this class
		
		self.dir = dir
		self.genome = genome
		self.rawReads = GetReads(dir,str(self.genome))
	
	#@dd decorator
	def gatherReport(self,fileName): #computes rates 
		print "Proceeding with QC step..."
		mapping = (float(self.rawReads.mappedTotal()) / float(self.rawReads.tophatTotal()))*100
		#intragenic = self.rawReads.intragenic()/rawReads.mappedTotal()
		#exonic = self.rawReads.exon()/rawReads.mappedTotal()
		#intronic = self.rawReads.intron()/rawReads.mappedTotal()
		#intergenic = self.rawReads.intergenic()/rawReads.mappedTotal()
		chrMTrate = (float(self.rawReads.mitochondrial())/float(self.rawReads.mappedTotal()))*100
		rRNArate = (float(self.rawReads.ribosomal())/float(self.rawReads.mappedTotal()))*100
		#concatenates rates in a tab-delimted string
		## change name to pass sample name to method
		

		sample = fileName +"\t"+ str(self.rawReads.tophatTotal()).strip("\n")+"\t"+str(self.rawReads.mappedTotal()).strip("\n")+"\t"+str(self.rawReads.mitochondrial()).strip("\n")+"\t"+str(self.rawReads.ribosomal()).strip("\n")+"\t"+str(mapping)+"\t"+str(chrMTrate)+"\t"+str(rRNArate)+ "\n"#"\t"+str(self.rawReads.exon()).strip("\n")+"\t"+str(self.rawReads.intron()).strip("\n")+"\n"
		#sample = "Name" + "\t" + str(mapping) +"\t"+ str(intragenic)+ "\t" + str(exonic) + "\t" + str(intronic) + "\t"+ str(intragenic) + "\t" + str(rRNArate)+"\t"+str(chrMTrate) + "\n"
		return sample
	
	def writeReport(self,fileName):
		file = open(fileName+".qcMetrics.txt", "w") #change to relative path
		file.write("sample"+"\t"+"total_reads"+"\t"+"mapped_reads"+"\t"+"Mitochondrial_RNA_reads"+"\t"+"rRNA_reads"+"\t"+"mapping_rate"+"\t"+"Mitochondrial_RNA_rate"+"\t"+"rRNA_rate"+"\n")#"\t"+"exonic_rate"+"\t"+"intronic_rate"+"\n")
		file.write(self.gatherReport(os.path.basename(fileName)))
		file.close()


# runQC = QCReport(sys.argv[1],sys.argv[2])


runQC = QCReport(sys.argv[1],sys.argv[2])
runQC.writeReport(sys.argv[3])
