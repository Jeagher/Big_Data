#!/usr/bin/env python3

#-*- coding: utf-8 -*-
from mrjob.job import MRJob

class MRWordCount(MRJob):
    def mapper(self, _, line):
        if line.split(',')[0] != 'ORDERNUMBER' : # Remoove Header line 
            yield(line.split(',')[10], int(line.split(',')[1])) # line.split(',')[10] = PRODUCTLINE , line.split(',')[1] = QUANTITYORDERED
    def reducer(self, word, counts):
        yield(word, sum(counts)) # get the number of order for each productLine 

if __name__ == '__main__':
    MRWordCount.run()