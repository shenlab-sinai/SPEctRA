#!/usr/bin/python
import os
import glob

# python class to manage auxilary file/string manipulation


class Utility(object):
    # iterates through a directory and lists subdirectories, use with glob
    # method too

    def subDirectories(self, dir):
        return [name for name in os.listdir(dir)
                if os.path.isdir(os.path.join(dir, name))]

    def openFile(self, dir, fileName):  # opens file, read only
        openFile = open(dir + "/" + fileName, "rb")
        return openFile

    # dict search method, find key based on value, returns  all in list
    def findKey(self, input_dict, value):
        return {k for k, v in input_dict.items() if v == value}

    # launch qsub scripts into the respective queue
    def batchQsub(self, directory):
        for line in glob.glob(directory + "/*.pbs"):
            os.system("qsub " + line)

    # launch qsub scripts into the respective queue
    def batchBsub(self, directory):
        for line in glob.glob(directory + "/*.lsf"):
            os.system("bsub <" + line)

    def chmodAll(self, directory):
        for line in glob.glob(directory + "*.sh"):
            os.system("chmod u+x " + line)
