*Sommaire*

[[TOC]]

# TP Hadoop

Ce TP fait suite au cours sur le _framework_ libre et open source appelé [__Hadoop__](https://Hadoop.apache.org), développé et maintenu par la [Fondation Apache](https://www.apache.org).

*Remarque* :
> Pour ce TP, vous devez savoir ouvrir un _Terminal_ sur votre machine, quelque soit le système d'exploitation (_Windows_, _Linux_, ou _Mac OS X_). Sous _Windows 10_, vous pourrez utiliser le programme _Windows powershell_ qui est très similaires au _Terminal_ de _Linux_ et de _Mac OS X_. 
Vous devez aussi savoir naviguer dans vos dossiers à l'aide de la commande ```cd```. Typiquement :
```shell
cd c:\Users\stephane\TP_Hadoop # Windows
cd ~\stephane\TP_Hadoop        # Mac, linux
```
Si vous souhaitez remonter d'un niveau dans la hiérarchie des dossiers: ```cd ..```.


## Installer **git** pour Windows (si requis)

Avant de commencer, il faut vérifier que **git** (un gestionnaire de version de fichier) est bien installé sur votre machine. **git** est disponible par défaut sur les machines *Mac OS X* et *Linux* et *Windows 10* (à vérifier). Pour vérifier, lancez la commande suivante dans un _Terminal_
```shell
git --version
```
S'il est absent, alors installez-le grâce à ce lien : [git-scm](https://git-scm.com/download/win). Lors de l'installation, validez les choix par défaut qui vous sont proposés.


## TP 1ière partie - _wordcount_ en local

Suivez alors les consignes concernant la première partie du TP, qui consistent a exécuter l'algorithme _map-reduce_ de comptage de mots, sur le fichier contenant un livre (_Dracula_) au format texte: [Wordcount_Local.md](./Wordcount_Local.md).

## Installer **Hadoop** via *Docker*

Pour installer **Hadoop** sur votre machine, suivez les consignes du fichier [Install_Docker_Hadoop.md](./Install_Docker_Hadoop.md).

## TP 2ième partie - _Map-Reduce_ avec Hadoop

Ensuite, suivez les consignes permettant de lancer le comptage de mots en tant que _job map-reduce_ : [Wordcount_Hadoop.md](./Wordcount_Hadoop.md).

Enfin, répondez aux exercices de cet énoncé : [Enonce_TP_Hadoop.md](./Enonce_TP_Hadoop.md).

