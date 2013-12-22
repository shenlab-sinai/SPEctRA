#!/usr/bin/python
import os
import glob
import sys
import re

#python class to manage auxilary file/string manipulation
class Utility(object):
	#iterates through a directory and lists subdirectories, use with glob method too
	def subDirectories(self,dir):
		return [name for name in os.listdir(dir)
           if os.path.isdir(os.path.join(dir, name))]
	def openFile(self,dir,fileName):
		openFile = open(dir+"/"+fileName,"rb")
		return openFile
	def mappedBam(self): #get generic mapped reads filename (different from STAR and Tophat2), may move outside of utils class
		pass
	def findKey(self,input_dict, value): #dict search method
		return {k for k, v in input_dict.items() if v == value}
