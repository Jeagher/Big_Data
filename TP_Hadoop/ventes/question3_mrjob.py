#!/usr/bin/env python3

#-*- coding: utf-8 -*-
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWordCount(MRJob):
    def mapper(self, _, line):
        if line.split(',')[0] != 'ORDERNUMBER' :  # Remoove Header line 
            yield(line.split(',')[10]+'  '+line.split(',')[9],float(line.split(',')[4]))  
            # line.split(',')[10] = PRODUCTLINE ,  line.split(',')[4] = SALES,  line.split(',')[9] = Year
            # ('productline year',sales)
    def reducer(self, product_year, sales):
        yield(product_year, round(sum(sales),2)) # Get total sales for every product for each year 

if __name__ == '__main__':
    MRWordCount.run()