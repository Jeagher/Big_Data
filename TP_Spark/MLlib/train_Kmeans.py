#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from statistics import mean
from numpy import array
from math import sqrt
from pyspark import SparkContext
from pyspark.mllib.clustering import KMeans, KMeansModel

def error(point):
	center = clusters.centers[clusters.predict(point)]
	return sum([x**2 for x in (point - center)])

if __name__ == "__main__":
	# Creation d un contexte Spark
	sc=SparkContext(appName="fire train kmeans")
	sc.setLogLevel("ERROR")

	# Lire un fichier csv et filtrer la première ligne
	data = sc.textFile('file:///root/pyspark/MLlib/modis_fire_2015_365_conus.csv')
	data = data.filter(lambda x: 'DATE' not in x).map(lambda line: line.split(","))
	data.persist()

	data = data.map(lambda x: array([float(x[4]),float(x[5])])).filter(lambda x: x[0] >50 and x[0]<42 and x[1]>-110 and x[1]<-142)
	data.collect()
	
	# Recherche des n classes
	clusters = KMeans.train(data, 10, maxIterations=10, initializationMode="random")
	# Inert    = data.map(lambda point: error(point)).reduce(lambda x, y: x + y)
	# varIntra = Inert/data.count()
	# print("Variance intraclasse = " + str(varIntra))


	# fonction lambda dans map pour "predire" tous les vecteurs
	prediction = data.map(lambda point: (clusters.predict(point),point)).combineByKey(lambda x:(x[0],x[1],1),lambda x,y:(x[0]+y[0],x[1]+y[1],x[2]+1), lambda x,y:(x[0]+y[0],x[1]+y[1],x[2]+y[2]))
	centroid = prediction.map(lambda x: (x[0],x[1][0]/x[1][2],x[1][1]/x[1][2]))
	print(centroid.collect())
	print('classe des points : ', prediction)

	sc.stop()