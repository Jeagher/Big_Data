#!/usr/bin/env python3

#-*- coding: utf-8 -*-
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWordCount(MRJob):
    def mapper1(self, _, line):
        if line.split(',')[0] != 'ORDERNUMBER': # Remoove Header line
            if line.split(',')[10] == 'Trucks and Buses':
                yield ([line.split(',')[20],line.split(',')[13]], float(line.split(',')[4]))
                # line.split(',')[20] = Country,  line.split(',')[13] = CustomName,  line.split(',')[4] = Sales
    def reducer1(self, name_country, counts):
        yield(name_country, sum(counts)) 
    # Output : ["Country","CustomerName"]   sum
    
    def mapper2(self, name_country, count):
        country = name_country[0]
        customer = name_country[1]
        yield(country, [count, customer])
    # Output : "Country"     ["sums","Customer"]
    
    def reducer2(self, country, tupple):
        yield(country, max(tupple,key= lambda x:x[0])) # Get the shop with the beast CA for each country
        
    def steps(self):
        return [
            MRStep(mapper=self.mapper1, reducer=self.reducer1),
            MRStep(mapper=self.mapper2, reducer=self.reducer2)
        ]

if __name__ == '__main__':
    MRWordCount.run()