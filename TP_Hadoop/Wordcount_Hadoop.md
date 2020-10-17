**Sommaire**

[[_TOC_]]

# Map-reduce, avec Hadoop

Étant donné l'installation que nous venons de faire, nous allons exploiter le parallélisme de votre processeur (souvent constitué de 4 cœurs, et donc susceptible de lancer 4 instructions en parallèle). Parmi ces 4 cœurs, nous n'en exploiterons que 3 (1 pour le _Namenode_ et 2 pour les _Datanodes_), le dernier cœur étant à disposition de votre machine pour toutes les autres tâches.

## Lancement du _daemon_ **Hadoop**

La première chose à faire sur le _Terminal_ du container du nœud maître est de lancer **Hadoop** et *yarn*. On exécutera le script _start-hadoop.sh_ pour cela:
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

> **Remarque importante** Le _Terminal_ pointe sur un système _Linux_ qui a son propre mode de stockage de fichier (appelé _ext3_). Il est alors possible de créer des dossiers, déposer des fichiers, les effacer... avec les commandes _Linux_ traditionnelles (```mkdir```, ```rm```...). Notons qu'il n'existe pas d'éditeur de texte intégré (pour écrire les scripts _Python_), donc nous aurons recours à une astuce décrite ci-dessous. C'est sur cet espace que nous stockerons les scripts _Python map-reduce_ qui seront exécutés par **Hadoop**. Par contre, les fichiers volumineux, ceux pour lesquels nous déploierons des algorithmes de traitement, seront stockés sur une partie de votre disque dur gérée par _HDFS_ (_Hadoop Distributed File System_). À l'aide de commandes commençant par _```hadoop fs -``` + commande_, il sera possible de créer des dossiers sur _HDFS_, copier des fichiers depuis _Linux_ vers _HDFS_, et rapatrier des fichiers depuis _HDFS_ vers Linux.  

Laissez-vous guider...

   - Depuis le _Terminal_, créez un dossier _wordcount_ et déplacez-vous dedans
   ```shell
   mkdir wordcount
   cd wordcount
   ```    
   - Téléchargez depuis internet le livre _dracula_ à l'aide de la commande
   ```shell
   wget http://www.textfiles.com/etext/FICTION/dracula
   ```   
   - Versez ce fichier volumineux sur l'espace HDFS (après avoir créer un dossier pour le recevoir)
   ```shell
   hadoop fs -mkdir input
   hadoop fs -put dracula input/
   ```
   Vérifiez que le fichier a bien été déposé:
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
Retenez la syntaxe, car elle vous sera utile plus tard, pour rapatrier les nouveaux scripts _Python_ que vous aurez développés.

Revenez alors vers le premier terminal, et vérifiez avec la commande ```ls``` que les 2 fichiers sont bien présents. Il faut maintenant rendre ces 2 scripts exécutables:
```shell
chmod +x mapper.py
chmod +x reducer.py
``` 
Souvenez-vous de cette manip., car il faudra aussi la faire sur vos nouveaux scripts.

Ça y est, nous sommes prêts à lancer notre premier script _map-reduce_!


## _Wordcount_ avec **Hadoop**

À partir du premier _Terminal_, nous allons donc lancer les scripts permettant de compter le nombre de mots sur le fichier du livre _dracula_.

  - Tout d'abord, stockez le lien vers la librairie permettant de programmer avec _Python_ dans une variable système
  ```shell
  export STREAMINGJAR='/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar'
  ```    
  Je vous rappelle que _**Hadoop** map-reduce_ fonctionne avec le langage **Java** ; il faut donc utiliser une bibliothèque capable de transformer des instructions _Python_ en instruction **Java**. C'est le rôle de cette bibliothèque (on appelle cela un _wrapper_).    
  - Ensuite, lancez le _job_ a proprement parlé avec l'instruction suivante:
  ```shell
  hadoop jar $STREAMINGJAR \
     -input input/dracula \
     -output sortie \
     -mapper mapper.py \
     -reducer reducer.py \
     -file mapper.py \
     -file reducer.py
  ``` 
  Les options ```-file``` permettent de copier les fichiers associés sur tous les 3 nœuds du cluster.
  Le résultat du comptage de mots est stocké dans le dossier _sortie_ sous _HDFS_. Vous pouvez voir son contenu en lançant la commande:
  ```shell
  hadoop fs -ls sortie/
  ```
  qui donnera quelque chose comme
  ```shell
  Found 2 items
  -rw-r--r--   2 root supergroup          0 2020-10-16 06:58 sortie/_SUCCESS
  -rw-r--r--   2 root supergroup         25 2020-10-16 06:58 sortie/part-00000
  ```
  Le premier fichier _\_SUCCESS_ est un fichier vide, dont la présence indique que le _job_ s'est terminé avec succès. Le second fichier _part-00000_ contient le résultat de l'algorithme. Vous pouvez les dernières lignes du fichier avec la commande :
  ```shell
  hadoop fs -tail sortie/part-00000
  ```
  ou tout le fichier de résultat:
  ```shell
  hadoop fs -cat sortie/part-00000
  ```
  Le résultat devrait être exactement le même que lors de la première partie du TP.

  *Remarque - N'oubliez pas!* : Entre 2 exécutions, il faut soit utiliser un nouveau nom pour le dossier _sortie_, soit le supprimer de la manière suivante:
  ```shell
  hdfs fs -rm -r -f sortie
  ``` 

  La présence d'un seul fichier ```part-0000x```  montre qu'un seul nœud a été utilisé pour le _reducer_ (le nombre de nœuds est estimé par le _Namenode_). Il est possible de forcer ne nombre de _reducer_:
  ```shell
  hadoop jar $STREAMINGJAR \
     -D mapred.reduce.tasks=2 \
     -input input/dracula \
     -output sortie \
     -mapper mapper.py \
     -reducer reducer.py \
     -file mapper.py \
     -file reducer.py
  ```

## Monitoring des _jobs_
