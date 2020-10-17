**Sommaire**

[[_TOC_]]

# Wordcount, en local

Nous allons ici faire fonctionner l'algorithme _map-reduce_ qui compte les mots d'un fichier texte, en local, _i.e._ sans exploiter le parallélisme massif du framework **Hadoop**. Le programme est constitué de deux scripts _Python_ qui sont appelés successivement selon la méthode décrite ci-dessous. Il s'agit ici surtout de comprendre la logique algorithmique.


---
## Récupération et lancement des scripts _Python_

Pour récupérer le scripts, suivez les consignes:

  - Ouvrez un _Terminal_ et déplacez-vous dans votre dossier de travail (avec la commande ```cd```). Tapez la commande permettant de récupérer les fichiers nécessaires à ce TP.   
  ```shell
  git clone https://gitlab.ec-lyon.fr/sderrode/s9_mod21_bigdata_tp.git
  ```
  Constatez, dans un gestionnaire de fichiers, que cette commande a permis de rapatrier des fichiers répartis dans 2 dossiers : _TP\_Hadoop_ et _TP\_SparQL_. Nous allons ici travailler sur le dossier _TP\_Hadoop_.

  - Dans le _Terminal_, déplacez-vous dans le dossier _wordcount_, en lançant successivement les 3 commandes suivantes :
  ```shell
  cd s9_mod21_bigdata_tp
  cd TP_Hadoop
  cd wordcount
  ```
  ou plus simplement :    
  ```shell
  cd s9_mod21_bigdata_tp/TP_Hadoop/wordcount
  ```

  La commande ```ls``` permet de lister le contenu du dossier. Vous pouvez observer la présence des 2 fichiers _mapper.py_ et _reducer.py_, ainsi que du livre _Dracula_ (libre de droit, téléchargé à partir de [cette adresse](http://www.textfiles.com/etext/FICTION/dracula)).

  - Lancez la commande suivante et observez le résultat:
  ```shell
  cat dracula | python mapper.py
  ```

  - Lancez ensuite la commande entière et observez le résultat:
  ```shell
  cat dracula | python mapper.py | sort | python reducer.py 
  ```


----
## Exercice 1 - Amélioration du *wordcount*

Pour stocker le résultat dans un fichier appelé _result.txt_, on lancera
```shell
cat dracula | python mapper.py | sort | python reducer.py > results.txt
```

Ouvrez ce fichier avec votre éditeur de texte préféré, et regardez les premières lignes. On constate de nombreux problèmes:

  - les signes de ponctuation associés aux mots;
  - les mots commençant par une majuscule sont distingués des mots commençant par une minuscule. 

Pour régler ces problèmes, veuillez

  1. Modifier les scripts _Python_ précédents pour qu'ils ne distinguent plus les mots qui comportent des majuscules et les mêmes mots qui n'en comportent pas.    
  1. Modifier la version précédente, de telle manière que les signes de ponctuation ne soient plus pris en compte (consultez Internet pour trouver un moyen de supprimer les signes de ponctuation d'une chaîne de caractères représentant un mot).
