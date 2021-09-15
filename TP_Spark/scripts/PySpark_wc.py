#!/usr/bin/env python3

import sys
from pyspark import SparkContext

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print("Usage: PySpark_wc <file>", file=sys.stderr)
		sys.exit(-1)

	# Creation d'un contexte spark
	sc = SparkContext(appName="Spark Count")
	sc.setLogLevel("ERROR") # Valid log levels include: ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN

	lines = sc.textFile(sys.argv[1])
	counts = lines.flatMap(lambda x: x.split(' ')) \
				  .map(lambda x: (x, 1)) \
				  .reduceByKey(lambda v1,v2 : v1 + v2)

	# Stockage du resultat sur HDFS 
	# ne pas oublier "hadoop fs -rm -r -f sortie" entre 2 executions
	#count.saveAsTextFile("sortie")

	# Affichage
	output = counts.collect()
	for (word, count) in output:
		print("%s: %i" % (word, count))
	
	# Arret du contexte Spark
	sc.stop()
	
