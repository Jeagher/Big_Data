#!/usr/bin/env python
from statistics import mean
import sys

# spark-submit --deploy-mode client --master local[2] movie_request.py --sort=rating --genre=action 

from pyspark import SparkContext

if __name__ == "__main__":

  # Creation d'un contexte spark
  sc = SparkContext(appName="Spark movie")
  sc.setLogLevel("ERROR")

  # Lecture des fichiers csv
  movies = sc.textFile("hdfs:///user/root/input/movies.csv") # movieId,title,genres
  ratings = sc.textFile("hdfs:///user/root/input/ratings.csv") # userId,movieId,rating,timestamp

  # Gestion des paramètres, utilisation simplifiée des --
  sortby_dic = {"--sort=popularity":"pop","--sort=rating":"rat"}
  sortby = ''
  genre = ''
  if len(sys.argv) > 1 :
    for elt in sys.argv :
      if elt in ["--sort=popularity","--sort=rating"] :
        sortby = sortby_dic[elt]
      elif "--genre=" in elt:
        genre = elt[8:]
    print('_____________________________________________________________________________________________________________________________')
    print(sys.argv)
    print(f"sortby : {sortby}, genre : {genre}")
  
  # Split des Lignes et filtre sur la ligne de Header 
  movies_rows = movies.filter(lambda x: 'movieId' not in x).map(lambda line: line.split(","))
  ratings_rows = ratings.filter(lambda x: 'movieId' not in x).map(lambda line: line.split(","))
  movies_rows.persist()
  ratings_rows.persist()

  # Mapping des infos intéréssantes : rating : (movieId,rating); movie : (movieId,(title,genres))
  ratings_rows = ratings_rows.map(lambda row: (row[1], row[2]))
  movies_rows = movies_rows.map(lambda row: (row[0], (row[1],row[2])))

  # Filter on movies containing selected genre
  if genre != '':
    movies_rows = movies_rows.filter(lambda x: genre in x[1][1].lower())

  # Join on movie_Id key, # output (movie_id, ((movie_name,genre),rating)))
  # Then createCombiner() if first encounter of the key in the partition create the accumulator ((movie_name,genre),rating,1))
  # if the key has been seen, mergeValue with the first accumulator ((movie_name,genre),sum_ratings,popularity)
  # Then combine accumulators across the partitions (movie_id,((movie_name,genre),sum_ratings,popularity))  
  fulljoin = movies_rows.join(ratings_rows).combineByKey(lambda x:(x[0],float(x[1]),1), lambda x,y : (x[0],x[1]+float(y[1]),x[2]+1), lambda x,y :(x[0],x[1]+y[1],x[2]+y[2]))
  fulljoin = fulljoin.map(lambda row: (row[1][0][1],(row[1][0][0],row[1][1]/row[1][2],row[1][2]))) # (genre,(movie_name,avg_rating,popularity))

  def get_movie_by_merge_value(x,y):
    if sortby == "pop" :
        if x[3][2] > y[2] :
          return (x[0]+y[1],x[1]+y[2],x[2]+1,x[3])
        return (x[0]+y[1],x[1]+y[2],x[2]+1,(y[0],y[1],y[2]))
    else : # by default sort by rating 
      if  x[3][1] > y[1] :
        return (x[0]+y[1],x[1]+y[2],x[2]+1,x[3])
      return (x[0]+y[1],x[1]+y[2],x[2]+1,(y[0],y[1],y[2]))

  def get_movie_by_merge_combiner(x,y):
    if sortby == "pop" :
        if x[3][2] > y[3][2] :
          return (x[0]+y[0],x[1]+y[1],x[2]+y[2],x[3])
        return (x[0]+y[0],x[1]+y[1],x[2]+y[2],y[3])
    else : # By default sort by rating
      if x[3][1] > y[3][1] :
        return (x[0]+y[0],x[1]+y[1],x[2]+y[2],x[3])
      return (x[0]+y[0],x[1]+y[1],x[2]+y[2],y[3])

  # Create Accumulator (rating,popularity,1,(movie_name,movie_avg_rating,popularity))
  # MergeVale with the first accumulator in partition, keep best movie (score or popularity) in every merge
  #  Then combine accumulator across the partitions (genre,(sum_avg_ratings,popularity,nb_movies,(best_movie,avg_rating,popularity)))
  fulljoin = fulljoin.combineByKey(lambda x:(x[1],x[2],1,(x[0],x[1],x[2])), lambda x,y :get_movie_by_merge_value(x,y), lambda x,y: get_movie_by_merge_combiner(x,y))

  fulljoin = fulljoin.map(lambda row: (row[0],{"genre_rating":round(row[1][0]/row[1][2],1),"genre_popularity":row[1][1],"best_genre_movie":row[1][3][0],
                                               "best_movie_rating":round(row[1][3][1],1),"best_movie_popularity":row[1][3][2]}))
  

  if sortby == 'pop' : 
      fulljoin = fulljoin.sortBy(ascending=False, keyfunc=lambda x: x[1]["genre_popularity"])
  else : # By default sort by rating
    fulljoin = fulljoin.sortBy(ascending=False, keyfunc=lambda x: x[1]["genre_rating"])
    
  # Stockage du resultat sur HDFS 
  # ne pas oublier "hadoop fs -rm -r -f sortie" entre 2 exécutions!
  fulljoin.saveAsTextFile("sortie")

  # Arret du contexte Spark
  sc.stop()