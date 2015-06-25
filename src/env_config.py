#!/usr/bin/python
import os
import sys
import yaml

# parses necessary base variables.


class ImportSettings(object):
    # def __init__(self, config):
    # 	self.config = config

    def openConfig(self):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, "config_template.yaml")
        with open(filename, 'r') as f:
            doc = yaml.load(f)
        return doc

    def getEnv(self):
        env = self.openConfig()["Environment"]
        return env

    def homeDir(self):  # usually a directory to store all analysis projects
        path = self.openConfig()["project_directory"]
        return path

    def genomes(self):
        supported = self.openConfig()["genomes"]
        return supported
        # return dict of genomes and their paths

    def mappingPaths(self):
        # return dict of available short-read aligner paths/modules
        aligner = self.openConfig()["Short-read_aligners"]
        return aligner

    # hardcoded for minerva args. Change this to be more flexible
    def bsubHeader(self, name, directory, project, proc, logDir, time="21:00", queue="scavenger"):
        env = "#!/bin/bash" + "\n"
        cluster = "#BSUB -m mothra" + "\n"
        queue = "#BSUB -q " + queue + "\n"
        proc = "#BSUB -n " + proc + "\n"
        Rflag = "#BSUB -R span[hosts=1]" + "\n"
        time = "#BSUB -W " + time + "\n"
        jobID = "#BSUB -J " + name + "\n"
        log = "#BSUB -o " + directory + "/" + project + \
            "/logs/" + logDir + "/" + name + ".log" + "\n"
        err = "#BSUB -e " + directory + "/" + project + \
            "/logs/" + logDir + "/" + name + ".log" + "\n"
        header = env + cluster + queue + proc + \
            Rflag + time + jobID + log + err + "\n"
        return header
# 	def openConfig(self):

# create separate setup.py-type file for pipeline setup and update
    # update genome list class to update genome dictionary


# BSUB args may be stored as dictionary or yaml entries for user input

#test = ImportSettings()
# print test.genomes()["tophat2"]["mouse"]["gtf"]
