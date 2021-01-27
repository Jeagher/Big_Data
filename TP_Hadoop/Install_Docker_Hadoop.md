**Sommaire**

[[_TOC_]]

# Installation de **Hadoop** via _Docker_

Les étapes pour installer **Hadoop** via _Docker_ sont largement adaptées de la page de [Lilia Sfaxi](https://insatunisia.github.io/TP-BigData/), elles-mêmes reposant sur le projet [github de Kai LIU](https://github.com/kiwenlau/Hadoop-cluster-docker).

---
## Installation de *Docker* et des nœuds

Pour installer *Docker*, merci de suivre les [consignes disponibles ici](https://docs.docker.com/desktop/), en fonction de votre système d'exploitation (lisez les _System requirements_ pour vérifier que votre machine est adaptée). Si votre machine est trop ancienne, ou avec peu d'espace disque ou mémoire RAM, il y a de bonnes chances que l'installation ne fonctionne pas. Si c'est le cas, 

 - soit vous pouvez travailler avec votre voisin,    
 - soit vous pouvez aller directement à la seconde partie du TP, et réaliser les exercices en local (sans **Hadoop**).


Nous allons utiliser tout au long de ce TP trois contenaires représentant respectivement un nœud maître (le _Namenode_) et deux nœuds esclaves (les _Datanodes_).

1. Depuis un _Terminal_, téléchargez l'image docker depuis [_dockerhub_](https://hub.docker.com) (volume à télécharger : 1.76 GB!) :
```shell
docker pull liliasfaxi/spark-hadoop:hv-2.7.2
```
Ce container contient une distribution _Linux/Ubuntu_, et les librairies nécessaires pour utiliser **Hadoop**. Ce container ne contient pas _Python_, mais nous verrons comment l'installer _a posteriori_.

2. Créez les trois contenaires à partir de l'image téléchargée. Pour cela:

     a. Créez un réseau qui permettra de relier les trois contenaires:
     ```shell
     docker network create --driver=bridge hadoop
     ```   
     b. Créez et lancez les trois contenaires (les instructions `-p` permettent de faire un _mapping_ entre les ports de la machine hôte et ceux du contenaire):
     ```shell
     docker run -itd --net=hadoop -p 50070:50070 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/spark-hadoop:hv-2.7.2

     docker run -itd -p 8040:8042 --net=hadoop --name hadoop-slave1 --hostname hadoop-slave1 liliasfaxi/spark-hadoop:hv-2.7.2

     docker run -itd -p 8041:8042 --net=hadoop --name hadoop-slave2 --hostname hadoop-slave2 liliasfaxi/spark-hadoop:hv-2.7.2
     ```     
   **Remarque** Sur certaines machines, la première ligne de commande ne s’exécute pas correctement. L'erreur provient sans doute du port `50070` que doit déjà être utilisé par une autre application installée sur votre machine. Vous pouvez alors supprimer ce port de la première ligne de commande :
   ```shell
   docker run -itd --net=hadoop -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/spark-hadoop:hv-2.7.2
   ```

---
## Préparation au TP

1. Entrez dans le contenaire `hadoop-master` pour commencer à l'utiliser
 ```shell
 docker exec -it hadoop-master bash
 ```
 Le résultat de cette exécution sera le suivant:
 ```shell
 root@hadoop-master:~#
 ```
 Il s'agit du ```shell``` ou du ```bash``` (_Linux/Ubuntu_) du nœud maître. Nous allons en profiter pour installer _Python2.7_ (version requise pour la version d'**Hadoop** installée):
 ```shell
 apt-get update
 apt-get install python2.7
 ```

2. Cette installation de _Python_ doit aussi être réalisée sur les _Datanodes_. Quittez le contenaire `hadoop-master`
 ```shell
 exit
 ```
 Puis, enchaînez les commandes suivantes (une par une) pour le container `hadoop-slave1` :
 ```shell
 docker exec -it hadoop-slave1 bash
 ```
 Puis
 ```shell
 apt-get update
 apt-get install python2.7
 exit
 ```
 et pour le container `hadoop-slave2`
 ```shell
 docker exec -it hadoop-slave2 bash
 ```
 Puis
 ```shell
 apt-get update
 apt-get install python2.7
 exit
 ```

3. Enfin, entrez à nouveau dans le container `hadoop-master` dans lequel nous allons lancer les _jobs_ :
 ```shell
 docker exec -it hadoop-master bash
 ```  
 Effacez les fichiers inutiles pour la suite avec la commande ```rm```:
 ```shell
 rm purchases2.txt run-wordcount.sh start-kafka-zookeeper.sh
 ```
 La commande ```ls```, qui liste les fichiers et dossiers du dossier en cours, doit faire état des fichiers suivants :
 ```shell
 hdfs start-hadoop.sh purchases.txt
 ```
 Le fichier _purchases.txt_ nous sera utile dans la seconde partie du TP.

**Remarque** Ces étapes de configuration ne doivent être réalisées qu'une seule fois. Pour relancer le cluster (une fois qu'on a fermer et relancer son ordinateur p. ex.), il suffira 

  1. de lancer l'application ```Docker Desktop```, qui lance les _daemon Docker_.   
  1. de lancer la commande suivante :
   ```shell
   docker start hadoop-master hadoop-slave1 hadoop-slave2
   ```

Vous pouvez alors entrer dans le _Namenode_ :
```shell
docker exec -it hadoop-master bash
```
