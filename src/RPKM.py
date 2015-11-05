#!/usr/bin/python
import numpy as np


class CalcRPKM(object):

    def __init__(self, genomes, countPath):
        self.genomes = genomes
        self.countPath = countPath

    def calc(self, countPath):
        lengths = np.genfromtxt(
            self.genomes["geneLenghts"], delimiter='\t', usecols=1)
        counts = np.genfromtxt(countPath, delimiter='\t', usecols=1)
        counts = counts[0:len(counts) - 5]
        depth = np.sum(counts)
        RPM = counts / depth
        RPKM = np.true_divide(RPM, lengths)
        return RPKM

    def writeRPKM(self, RPKM, fileName):
        file = open(fileName + ".RPKM.txt", "w")
        file.write(RPKM)
        file.close()
