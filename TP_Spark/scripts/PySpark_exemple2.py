#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pyspark import SparkContext

if __name__ == "__main__":

	# Creation d un contexte Spark
	sc=SparkContext(appName="Text line count")
	sc.setLogLevel("ERROR") # Valid log levels include: ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

	lines = sc.textFile("README.md")
	lineLengths = lines.map(lambda s: len(s))
	# lineLengths.persist()
	totalLength = lineLengths.reduce(lambda a, b: a + b)
	print(totalLength)

	# Arret du contexte Spark
	sc.stop()