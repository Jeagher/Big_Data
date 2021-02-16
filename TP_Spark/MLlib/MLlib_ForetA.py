from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import RandomForest
from pyspark import SparkContext

if __name__ == "__main__":

	sc=SparkContext(appName="Parallelize")

	data = [LabeledPoint(0.0, [0.0]), 
			LabeledPoint(0.0, [1.0]),
			LabeledPoint(1.0, [2.0]),
			LabeledPoint(1.0, [3.0])]

	# distribution de la table
	trainingData=sc.parallelize(data)
	trainingData.collect()
	# Estimation du modele
	model = RandomForest.trainClassifier(trainingData, 2, {}, 3, seed=42)
	model.numTrees()
	model.totalNumNodes()

	# "Affichage" de la foret
	print model.toDebugString()
	# Preevision d un eechantillon
	rdd = sc.parallelize([[3.0], [1.0]]) 
	model.predict(rdd).collect()

	sc.stop()