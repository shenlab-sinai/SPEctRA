#!/usr/bin/python
import sys
import numpy as np


class CalcRPKM(object):

    def __init__(self, genomes, countPath):
        self.genomes = genomes
        self.countPath = countPath

    def calc(self):
        lengths = np.genfromtxt(
            self.genomes, delimiter='\t', usecols=1)
        counts = np.genfromtxt(self.countPath, delimiter='\t', usecols=1)
        counts = counts[0:len(counts) - 5]
        depth = np.sum(counts)
        RPM = counts / depth
        RPKM = np.true_divide(RPM, lengths)
        return RPKM

    def writeRPKM(self, RPKM, fileName):
        np.savetxt(fileName + ".RPKM.txt", RPKM, delimiter="\t")


compute = CalcRPKM(sys.argv[1], sys.argv[2])
compute.writeRPKM(compute.calc(), sys.argv[3])
