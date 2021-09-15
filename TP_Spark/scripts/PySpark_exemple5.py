#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
from pyspark import SparkContext

if __name__ == "__main__":
	
	sc=SparkContext(appName="baby example")
	sc.setLogLevel("ERROR") # Valid log levels include: ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

	baby_names = sc.textFile("file:///root/pyspark/baby_names_2013.csv")    # en local
	#baby_names = sc.textFile("hdfs:///user/root/input/baby_names_2013.csv")  # sur HDFS

	rows = baby_names.filter(lambda x: 'County' not in x).map(lambda line: line.split(","))
	rows.persist()

	namesToCounties = rows.map(lambda n: (str(n[1]), str(n[2]))).groupByKey()
	res1 = namesToCounties.map(lambda x : {x[0]: list(x[1])}).collect()
	print(res1[:10])
	# => [{'GRIFFIN': ['ERIE', 'ONONDAGA', 'NEW YORK', 'ERIE', ...}, {...}]

	namesNumber = rows.map(lambda n: (str(n[1]), int(n[4]) ) ).reduceByKey(lambda v1,v2: v1 + v2).collect()
	print(namesNumber[:10])
	# => [('GRIFFIN', 20), ('KALEB', 24), ('JOHNNY', 25), ('NAYELI', 11), ('ERIN', 58) ...

	sc.stop()