# TP SparQL

Ce TP de 4h se décompose en deux temps:
 
  - D'abord un courte introduction au ```Web sémantique```, à [RDF](https://www.w3.org/RDF/) et à [SparQL](https://www.w3.org/TR/sparql11-query/). Le cours est celui de [Pierre-Antoine Champin](http://liris.cnrs.fr/~pchampin), MCF HDR en informatique à l'IUT de l'Université Claude Bernard Lyon 1, rattaché au laboratoire [LIRIS](https://liris.cnrs.fr).

    - [Liens vers le cours](http://liris.cnrs.fr/~pchampin/2016/lod/index.html).     
    - [TEDx Tims Berners-Lee](https://www.ted.com/talks/tim_berners_lee_the_next_web).      
    - [Non technical introduction to linked Open Data](https://www.youtube.com/watch?v=4x_xzT5eF5Q).


  - Ensuite, une séance de travaux pratiques, qui consiste à répondre aux requêtes disponibles dans le lien ci-dessous. On  utilisera le client [Yasgui](https://yasgui.triply.cc) pour exécuter des requêtes sur [DBPedia](https://wiki.dbpedia.org/develop/datasets/latest-core-dataset-releases), la base de données RDF issue d’extractions de Wikipédia.    
      - [lien vers l’énoncé du TP](http://liris.cnrs.fr/%7Epchampin/2016/ecl-sparql/)    
  
	Pour bien débuter, voici la réponse à la première requête:

	```sparql
	PREFIX dbo: <http://dbpedia.org/ontology/>
	PREFIX dbr: <http://dbpedia.org/resource/>
	SELECT ?p {
	  ?p a              dbo:Person;
	     dbo:birthPlace dbr:Lyon.
	}
	```
