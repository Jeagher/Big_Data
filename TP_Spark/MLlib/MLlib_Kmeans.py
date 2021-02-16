from pyspark.mllib.clustering import KMeans 
from numpy import array
from math import sqrt
from pyspark import SparkContext

# Qualite de la classification
def error(point):
	center = clusters.centers[clusters.predict(point)]
	return sum([x**2 for x in (point - center)])

if __name__ == "__main__":

	sc=SparkContext(appName="Parallelize")

	# Lire et "distribuer" les donnees
	data = sc.textFile("file:///root/pyspark/MLlib/kmeans_data.txt")
	parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))
	parsedData.collect()

	# Recherche des 2 classes
	clusters = KMeans.train(parsedData, 2, maxIterations=10, runs=10, initializationMode="random")
	Inert    = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
	varIntra = Inert/parsedData.count()
	print("Variance intraclasse = " + str(varIntra))

	 # fonction lambda dans map pour "predire" tous les vecteurs
	prediction = parsedData.map(lambda point: clusters.predict(point)).collect()
	print('classe des points : ', prediction)

	sc.stop()