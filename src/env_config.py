#!/usr/bin/python
import os
import yaml

# parses necessary base variables.


class ImportSettings(object):

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
        aligner = self.openConfig()["Short-read_aligners"]
        return aligner
        # return dict of available short-read aligner paths/modules

    # hardcoded for minerva args. Change this to be more flexible
    def bsubHeader(self, name, directory, project, proc,
                   logDir, time="21:00", cluster="manda", 
                   account="acc_shenl03_rna", queue="low"):
        env = "#!/bin/bash" + "\n"
        cluster = "#BSUB -m " + cluster + "\n"
        account = "#BSUB -P " + account + "\n"
        queue = "#BSUB -q " + queue + "\n"
        proc = "#BSUB -n " + proc + "\n"
        Rflag = "#BSUB -R span[hosts=1]" + "\n"
        time = "#BSUB -W " + time + "\n"
        jobID = "#BSUB -J " + name + "\n"
        log = "#BSUB -o " + directory + "/" + project + \
            "/logs/" + logDir + "/" + name + ".log" + "\n"
        err = "#BSUB -e " + directory + "/" + project + \
            "/logs/" + logDir + "/" + name + ".log" + "\n"
        header = env + cluster + account + queue + proc + \
            Rflag + time + jobID + log + err + "\n"
        return header

# create separate setup.py-type file for pipeline setup and update
    # update genome list class to update genome dictionary


# BSUB args may be stored as dictionary or yaml entries for user input
