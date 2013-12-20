#!/usr/bin/python

import os
import glob
import sys
import re

#Classes/methods to get data and prepare it for specified analysis tasks

class GatherData(object):
	#sort fastq samples to R1 and R2, even if multiple fastqs for one end are available
	def studySamples(self, fastq):
	
		exp = "R[1|2]"
		samples = { }
		regex = re.compile(exp)
		for line in fastq: #change to glob library function
			if regex.search(line) is not None:
				read = re.findall(exp, line)
				samples.update({line:read[0]})
		#return dictionary of values		
		return samples		

 

word = ["I_100_bc20_GTGGCC_L001_R1_001.C3H70ACXX.fastq.gz","I_100_bc20_GTGGCC_L001_R2_001.C3H70ACXX.fastq.gz","I_100_bc20_GTGGCC_L002_R1_001.C3H70ACXX.fastq.gz","I_100_bc20_GTGGCC_L002_R2_001.C3H70ACXX.fastq.gz"]

test = GatherData()

