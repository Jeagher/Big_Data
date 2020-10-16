*Sommaire*

[[TOC]]

# Installation de **Hadoop** via _Docker_

Les étapes pour installer **Hadoop** via _Docker_ sont largement adaptées de la page de [Lilia Sfaxi](https://insatunisia.github.io/TP-BigData/), elles-mêmes reposant sur le projet [github de Kai LIU](https://github.com/kiwenlau/Hadoop-cluster-docker).

## Installation de *Docker*

Pour installer *Docker*, merci de suivre les consignes disponibles ici [Docker](https://docs.docker.com/desktop/), en fonction de votre système d'exploitation. Cette étape installe un application appelée _Docker Desktop_, qui aura l'allure suivante, une fois les consignes ci-dessous exécutées:

<center class=correction><img src="figures/Docker_capture.png" style="width:50%"/></center>

## Installation d'un _Namenode_ et de deux _Datanode_

Nous allons utiliser tout au long de ce TP trois contenaires représentant respectivement un nœud maître (_Namenode_) et deux nœuds esclaves (_Datanodes_).

1. Depuis un _Terminal_, télécharger l'image docker depuis [_dockerhub_](https://hub.docker.com):
```shell
docker pull liliasfaxi/spark-Hadoop:hv-2.7.2
```
Ce container contient une distribution _Linux/Ubuntu_, et les librairies nécessaires pour utiliser **Hadoop**.

1. Créez les trois contenaires à partir de l'image téléchargée. Pour cela:

     1. Créez un réseau qui permettra de relier les trois contenaires:
     ```shell
     docker network create --driver=bridge hadoop
     ```   
     1. Créer et lancer les trois contenaires (les instructions -p permettent de faire un mapping entre les ports de la machine hôte et ceux du contenaire):
     ```shell
     docker run -itd --net=hadoop -p 50070:50070 -p 8088:8088 -p 7077:7077 -p 16010:16010 \
              --name hadoop-master --hostname hadoop-master \
              liliasfaxi/spark-hadoop:hv-2.7.2
  
     docker run -itd -p 8040:8042 --net=hadoop \
              --name hadoop-slave1 --hostname hadoop-slave1 \
              liliasfaxi/spark-hadoop:hv-2.7.2
  
     docker run -itd -p 8041:8042 --net=hadoop \
              --name hadoop-slave2 --hostname hadoop-slave2 \
              liliasfaxi/spark-hadoop:hv-2.7.2
     ```    
     1. Entrez dans le contenaire master pour commencer à l'utiliser
     ```shell
     docker exec -it hadoop-master bash
     ```
     Le résultat de cette exécution sera le suivant:
     ```shell
     root@hadoop-master:~#
     ```

Après cette dernière instruction, vous êtes entré dans un environnement, entièrement indépendant de votre machine. Il s'agit du ```shell``` (_Linux/Ubuntu_) du nœud maître. Effaçons dès-à-présent les fichiers qui ne nous seront pas nécessaires avec la commande ```rm```:
```shell
rm purchases.txt purchases2.txt run-wordcount.sh
```
Le résultat de la commande ```ls``` (liste les fichiers et dossiers du dossier en cours) ressemblera à ce qui suit:
```shell
hdfs start-hadoop.sh  start-kafka-zookeeper.sh
```

