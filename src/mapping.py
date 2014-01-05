#!/usr/bin/python

import os
import pysam


#executes mapping tool of choice
#use separate class to parse input params
class Mapping(object):
	def __init__(self,fastqR1,proc,outdir,genome,libType="fr-unstranded",fastqR2 = ""):
		self.fastqR1 = fastqR1
		self.fastqR2 = fastqR2
		self.libType = libType
		self.proc = proc
		self.genome = genome
		self.outdir = outdir
	
	def tophat(self):
		#parse tophat specific parameters
		#command: tophat2 --library-type fr-unstranded --no-novel-juncs --b2-very-sensitive -p 16 -G  $GTF -o $OUTDIR $BOWTIE_INDEX $SAMPLE (must be list)
		command = "tophat2 --library-type %s --no-novel-juncs --b2-very-sensitive -p %s -G %s -o %s %s  %s %s " % (self.libType, self.proc,self.genome["gtf"],self.outdir,self.genome["index"],self.fastqR1,self.fastqR2)
		return command
	def STAR(self): #unique pbs/.sh script due to himmem requirements
		#parse STAR specific parametsrs
		#command: STAR --genomeDir /scratch/purusi01/hg19_star_ercc  --readFilesIn /scratch/purusi01/test_10M.fastq  --runThreadN 8
		command = "STAR --genomeDir %s --readFilesIn fastqs --readFilesCommand zcat --runThread %s" % (self.genome["path"],self.proc,)
 		return command
 	#def shortreadalinger(self) add as needed

class Auxilery(object): #post alignment manipulation 

	#figure out how to execute tasks (via script, at end of mapping or separate job)
	def tophat(self):
 		
 		tophat_prep=""
 		return tophat_prep #indexBam
 		pass
 	def STAR(self):
 		pass
 		#sortSam
 		#convertSamtoBam
 		#indexBam
