#!/usr/bin/python
import numpy as np


class CalcRPKM(object):

    def __init__(self, geneLengths, countPath):
        self.geneLenghts = geneLengths
        self.countPath = countPath

    def calc(self, countPath):
        lengths = np.genfromtxt(countPath, delimiter='\t', usecols=1)
        counts = np.genfromtxt(countPath, delimiter='\t', usecols=1)
        counts = counts[0:len(counts) - 5]
        depth = np.sum(counts)
        RPM = counts / depth
        RPKM = np.true_divide(RPM, lengths)
        return RPKM
