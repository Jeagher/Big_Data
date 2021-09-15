#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pyspark import SparkContext

if __name__ == "__main__":

	# Creation d un contexte Spark
	sc=SparkContext(appName="Parallelize")
	sc.setLogLevel("ERROR") # Valid log levels include: ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

	data = [1, 2, 3, 4, 5]
	distData = sc.parallelize(data)

	# Arret du contexte Spark
	sc.stop()
