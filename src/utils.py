#!/usr/bin/python
import os
import glob
import sys
import re
import ConfigParser

#python class to manage auxilary file/string manipulation
class Utility(object):
	#iterates through a directory and lists subdirectories, use with glob method too
	def subDirectories(self,dir):
		return [name for name in os.listdir(dir)
           if os.path.isdir(os.path.join(dir, name))]
	def openFile(self,dir,fileName): #opens file, read only
		openFile = open(dir+"/"+fileName,"rb")
		return openFile
	def findKey(self,input_dict, value): #dict search method, find key based on value, returns  all in list
		return {k for k, v in input_dict.items() if v == value}
	def batchQsub(self,directory): #launch qsub scripts into the respective queue
		for line in glob.glob(directory +"/*.pbs"):
			os.system("qsub " + line)