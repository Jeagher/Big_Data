#!/usr/bin/env python3

# python question5_mrjob.py -r inline <sales_data_sample.csv > resultInline.txt

# The idea is to get the shop with the best CA and only 1 sale during the year for each year and each product line 

#-*- coding: utf-8 -*-
from itertools import count
from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np 

class MRWordCount(MRJob):
    def mapper1(self, _, line):
        if line.split(',')[0] != 'ORDERNUMBER': # Remoove Header line
            yield ((line.split(',')[13],line.split(',')[10],line.split(',')[9]), [1,float(line.split(',')[4])])
                # line.split(',')[13] = CUSTOMNAME, line.split(',')[10] = PRODUCTLINE ,  line.split(',')[9] = Year,  line.split(',')[4] = Sales
    def reducer1(self, key_tuple, value_tuple):
        
        def func(x): # Custom sum function for a 2d iterable
            S0=0
            S1=0
            for elt in x : 
                S0+=elt[0]
                S1+=elt[1]
            return S0,S1

        yield(key_tuple, func(value_tuple)) 
    # Output : ["CUSTOMNAME","PRODUCTLINE","Year"], [count,Total_Sales]
    
    def mapper2(self, key_tuple, value_tuple):
        
        count = value_tuple[0]
        if count == 1 :
            customName = key_tuple[0]
            productLine = key_tuple[1]
            year = key_tuple[2]
            totalSales = value_tuple[1]
            yield([productLine,year], [customName, totalSales])
        # Output : [productLine,year], [customName, totalSales]
    
    def reducer2(self, key_tuple, value_tuple):
        yield(key_tuple, max(value_tuple,key= lambda x:x[1])) # Get the CustomName with maximum sales for each country 
        
    def steps(self):
        return [
            MRStep(mapper=self.mapper1, reducer=self.reducer1),
            MRStep(mapper=self.mapper2, reducer=self.reducer2)
        ]

if __name__ == '__main__':
    MRWordCount.run()