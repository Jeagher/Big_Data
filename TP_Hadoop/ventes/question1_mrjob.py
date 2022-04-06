#!/usr/bin/env python3

#-*- coding: utf-8 -*-
from mrjob.job import MRJob
import csv

class MRWordCount(MRJob):
    def mapper(self, _, line):
        if line.split(',')[0] != 'ORDERNUMBER' : # Remoove Header line 
            yield(line.split(',')[10], 1) # line.split(',')[10] = PRODUCTLINE
    def reducer(self, word, counts):
        yield(word, sum(counts)) # Count the number of time each product line is in the dataset 

if __name__ == '__main__':
    MRWordCount.run()