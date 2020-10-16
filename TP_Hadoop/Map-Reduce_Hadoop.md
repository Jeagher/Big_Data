*Sommaire*

[[TOC]]

# Map-reduce, avec Hadoop

Étant donné notre installation, nous allons exploiter le parallélisme de votre processeur (souvent constitué de 4 cœurs, et donc susceptible de lancer 4 instructions en parallèle). Étant donné notre installation nous exploiterons 3 cœurs uniquement (1 pour le _Namenode_ et 2 pour les _Datanodes_), le dernier cœur étant à disposition de votre machine pour toutes les autres tâches.

## Préparation

La première chose à faire sur le _Terminal_ du container du nœud maître est de lancer **Hadoop** et *yarn*. On utilisera le script _start-hadoop.sh_ pour cela:
```shell
./start-hadoop.sh
```
Le résultat ressemblera à ce qui suit:
```shell
Starting namenodes on [hadoop-master]
hadoop-master: Warning: Permanently added 'hadoop-master,172.18.0.4' (ECDSA) to the list of known hosts.
hadoop-master: starting namenode, logging to /usr/local/hadoop/logs/hadoop-root-namenode-hadoop-master.out
hadoop-slave2: Warning: Permanently added 'hadoop-slave2,172.18.0.2' (ECDSA) to the list of known hosts.
hadoop-slave1: Warning: Permanently added 'hadoop-slave1,172.18.0.3' (ECDSA) to the list of known hosts.
hadoop-slave2: starting datanode, logging to /usr/local/hadoop/logs/hadoop-root-datanode-hadoop-slave2.out
hadoop-slave1: starting datanode, logging to /usr/local/hadoop/logs/hadoop-root-datanode-hadoop-slave1.out
Starting secondary namenodes [0.0.0.0]
0.0.0.0: starting secondarynamenode, logging to /usr/local/hadoop/logs/hadoop-root-secondarynamenode-hadoop-master.out

starting yarn daemons
starting resourcemanager, logging to /usr/local/hadoop/logs/yarn--resourcemanager-hadoop-master.out
hadoop-slave1: Warning: Permanently added 'hadoop-slave1,172.18.0.3' (ECDSA) to the list of known hosts.
hadoop-slave2: Warning: Permanently added 'hadoop-slave2,172.18.0.2' (ECDSA) to the list of known hosts.
hadoop-slave1: starting nodemanager, logging to /usr/local/hadoop/logs/yarn-root-nodemanager-hadoop-slave1.out
hadoop-slave2: starting nodemanager, logging to /usr/local/hadoop/logs/yarn-root-nodemanager-hadoop-slave2.out
```

## Le système de fichiers _HDFS_

_Remarque importante_ Le _Terminal_ pointe sur un système _Linux_ qui a son propre mode de stockage de fichier (appelé _ext3_). Il vous est possible de créer des répertoires, déposer des fichiers, les effacer... avec les commandes _Linux_ traditionnelles (```mkdir```, ```rm```...). Notons qu'il n'existe pas d'éditeur de texte intégré (pour écrire les scripts python), donc nous aurons recours à une astuce décrite ci-dessous. C'est sur cet espace que nous stockerons les scripts _Python_ qui seront exécutés par **Hadoop**. Par contre les fichiers volumineux (_Big Data_), ceux pour lesquels nous déploierons des algorithmes de traitement, seront stockés sur une partie de votre disque dur gérée par HDFS (_Hadoop File Distributed System_). À l'aide de commandes commençant par _```hadoop fs -``` + commande_, il est possible de créer des dossiers sur HDF, copier des fichiers depuis _Linux_ vers HDFS, et rapatrier des fichiers depuis HDFS vers Linux.  

   - Créez un dossier _wordcount_ et se déplacer dedans
   ```shell
   mkdir wordcount
   cd wordcount
   ```    
   - Télécharger depuis internet le livre _dracula_ à l'aide de la commande
   ```shell
   wget http://www.textfiles.com/etext/FICTION/dracula
   ```   
   - Verser le fichier volumineux sur l'espace HDFS (après avoir créer un répertoire pour le recevoir)
   ```shell
   hadoop fs -mkdir input
   hadoop fs -put dracula input/
   ```
   Vérifier que le fichier a bien été déposé:
   ```shell
   hadoop fs -ls input/
   ```
   ce qui donnera quelque chose comme:
   ```shell
   Found 1 items
   -rw-r--r--   2 root supergroup     844505 2020-10-16 05:02 input/dracula
   ```    
   - Supprimer le fichier _dracula_ de votre espace _Linux_ (on n'en a plus besoin!)
   ```shell
   rm dracula
   ```     

Il faut maintenant rapatrier, sur notre espace Linux, les scripts _mapper.py_ et _reducer.py_ que nous avons manipulés durant la première partie de ce TP. Pour cela, il faut ouvrir un **second _Terminal_** (laissez le premier ouvert, il va nous resservir!), et vous déplacer dans le dossier de travail qui contient les scripts _mapper.py_ et _reducer.py_, modifiés par vos soins durant la première partie. La commande suivante permet de copier ces 2 fichiers vers l'espace Linux, dans le dossier _wordcount_
```shell
docker cp mapper.py hadoop-master:/root/wordcount
docker cp reducer.py hadoop-master:/root/wordcount
``` 

Revenez alors vers le premier terminal, et vérifiez avec la commande ```ls``` que les 2 fichiers sont bien présents. Ça y est, nous sommes prêt à lancer notre premier script _map-reduce_!


## Wordcount avec Hadoop

export STREAMINGJAR='/usr/local/Hadoop/share/Hadoop/tools/lib/Hadoop-streaming-2.7.2.jar'
