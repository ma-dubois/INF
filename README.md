# INF #

Outil permettant de créer un serveur web à partir de python et d'éxécuter des requêtes pour trouver des cours similaires à un cours en particulier.

## Obtention de cet outil ##

```shell
git clone https://github.com/ma-dubois/INF.git
```

## Introduction ##

Cet outil calcule la similarité du contenu du fichier <COURS>.txt avec tous les documents présents dans le dossier PolyHEC. Les 10 documents présentant la plus grande similarité sont retournés. Les signes de ponctuation (.,;:!?) sont ne sont pas considéré comme des mots et sont retirés. De plus, il est possible de radicaliser les mots et de supprimer les mots vides tels que 'de'. Dans le fichier elementComparison.py, on definiera les variables <stemming> et <stopWords> a True/False pour activer/désactiver la radicalisation et la suppression des mots vides respectivement.

## Configuration minimale ##

Cet outil peut être installé sur n'importe quel système UNIX.

## Dépendances ##

* Python 3.X: Le code a été développé pour fonctionner avec Python 3.

* [NLTK](http://www.nltk.org): Sur un système UNIX, on peut installer NLTK en utilisant les commandes suivantes:
```shell
sudo pip install -U nltk
sudo python -m nltk.downloader -d /usr/local/share/nltk_data all
```
* [PyStemmer](https://pypi.python.org/pypi/PyStemmer/1.0.1): 
Sur un système UNIX, on peut installer PyStemmer en utilisant les commandes suivantes:
```shell
python setup.py build
sudo python setup.py install
```
## Utilisation ##

1. Dans un terminal sur le serveur, rejoindre le dossier et lancer le serveur avec:

```shell
python serveur.py
```

Cette commande amorcera les calculs de base et lancera le serveur accessible sur localhost au port 8081. 


2. Du côté client, dans un navigateur compatible avec [jQuery](www.jquery.com), lancer la page [http://localhost:8081/index.html](http://localhost:8081/index.html)

3. Entrer le numéro d'un cours (par exemple BIA3510) dans l'invite et appuyer sur la touche Enter du clavier. Le calcul se lance sur le serveur et le résultat de la requête sera affiché dans le navigateur du client.














