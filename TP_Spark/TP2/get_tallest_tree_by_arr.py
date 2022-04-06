#!/usr/bin/env python
import sys

#IDBASE;LIBELLEFRANCAIS;GENRE;ESPECE;ADRESSE;TYPEEMPLACEMENT;DOMANIALITE;
# ARRONDISSEMENT;COMPLEMENTADRESSE;NUMERO;IDEMPLACEMENT;CIRCONFERENCE EN CM;HAUTEUR EN M;
# STADEDEVELOPPEMENT;PEPINIERE;VARIETE OU CULTIVAR;DATEPLANTATION;REMARQUABLE;Geo point

from pyspark import SparkContext

if __name__ == "__main__":

	# Creation d'un contexte spark
	sc = SparkContext(appName="Spark Count")
	sc.setLogLevel("ERROR")
	
	# Lecture du fichier du csv
	rows = sc.textFile(sys.argv[1])
	rows = rows.filter(lambda x: 'ESPECE' not in x).map(lambda line: line.split(";"))
	rows.persist()

	# Regroupement par tailles et adresse gps
	tree = rows.filter(lambda row: row[12] != '' and 'PARIS' in row[7]).map(lambda row: (row[7], (row[4], float(row[12])))).reduceByKey(lambda x,y: x if(x[1] > y[1]) else y)
	# tree = max(tree.collect(),key=lambda x:x[1])
	# rdd = sc.parallelize([tuple])
	# Stockage du resultat sur HDFS 
	# ne pas oublier "hadoop fs -rm -r -f sortie" entre 2 exécutions!
	tree.saveAsTextFile("sortie")
	
	# Arret du contexte Spark
	sc.stop()