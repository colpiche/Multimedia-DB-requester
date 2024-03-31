# Multimedia DB requester

Script Python mettant en oeuvre un prototype de système de description et de recherche d'images par le contenu. La base étudiée est disponible à l'adresse [https://cedric.cnam.fr/~ferecatu/BDMM/TP/Base10000.zip](https://cedric.cnam.fr/~ferecatu/BDMM/TP/Base10000.zip).


## Installation

- Cloner le repo
- `cd Multimedia-DB-requester`
- `pip install -r requirements.txt`

## Architecture du programme

Le script est composé des fichiers suivants :
 - `main.py` : fichier à exécuter
 - `python_database\IndexDatabase.py` : classe gérant l'indexation de la base de données (récupération de la liste des fichier, requêtes de calculs de descripteurs, écriture des descripteurs dans des fichiers)
 - `python_database\JPicture.py` : classe utilitaire opérant différentes tâches sur les images (calcul des histogrammes, normalisation, conversion en niveaux de gris...) 
 - `python_database\QBE.py` : classe traitant les requêtes de recherche par similarité visuelle (comparaison des descripteurs, génération des fichiers HTML de sortie...)

## Usage

### Indexation de la base

Etapes pour procéder à l'indexation de la base de données :
 - Modification de la variable `DB_PATH` du fichier `main.py` : chemin du dossier contenant les images à indexer. Ce dossier doit contenir un fichier nommé `Base10000_files.txt` dans lequel sont inscrit les noms de fichiers des images à analyser (un par ligne). Les images en question doivent être placées dans un sous-dossier `images`
 - Décommenter la ligne 28 (`index_db.index()`)
 - Exécuter le script `main.py`

Les résultats de l'indexation de la base de données sont des fichiers placés dans le dossier `$DB_PATH\histograms` et nommés selon le nom de la base et le type d'histogramme calculé. Chaque fichier contient l'ensemble des histogrammes du même type pour toutes les images de la base.
Chaque ligne d'un fichier représente l'histogramme d'une image où toutes les valeurs sont separées par des espaces et où les listes multidimensionnelles ont été aplaties. Exemple de ligne pour un descripteur HistRGB_2x2x2 : `0.93618774 4.0690105E-5 0.0011189779 2.339681E-4 0.014129639 0.0 0.016082764 0.03220622`

### Exécution d'une requête de recherche par similarité

L'exécution d'une requête s'effectue aussi par le fichier `main.py`. Avant son exécution il convient de modifier les variables suivantes :
 - `DESCRIPTORS_PATH` : chemin du dossier contenant les fichiers stockant les descripteurs des images
 - `IMAGE_NAME` : nom du fichier sur lequel effectuer la requête
 - `DESCRIPTOR_FILE_NAME` : nom du fichier dans lequel est stocké un type de descripteur pour toutes les images de la base (fichier généré lors de l'indexation de la base)
 - `NB_RESULTS` : nombre de résultats de requête à afficher

Le résultat de la requête est un fichier HTML placé dans le dossier `$DB_PATH\requests`, nommé selon l'image sur laquelle a été effectuée la requête et le descripteur étudié.
