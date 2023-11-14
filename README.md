# Projet Pokémon API

Auteur : Julien DEVIENNE-OUSMER

## Objectif

Le projet Pokémon API vise à fournir une API permettant la gestion des données relatives à des Pokémon, incluant certaines caractéristiques de base, leurs types, et leurs compétences.

## Mise en place

### Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre système :

- Python (version ⩾ 3.11 de préférence)
- FastAPI (version ⩾ 0.104.0 de préférence)

### Installation

1. Clonez le repository :

```bash
git clone https://github.com/julienousmer/fastap-api-pokemon.git
cd fastap-api-pokemon
```

2. Activer l'environnement virtuel Python

```bash
.\venv\Scripts\activate
```
Vous devez ici voir dans votre terminal le préfix : **(venv)**

3. Installer les dépendances
   
```bash
pip install -r requirements.txt
```

4. Lancer l'API

```bash
uvicorn main:app --reload
```

L'API sera accessible à l'adresse http://localhost:8000 pour une utilisation locale.

## Base de données 

### Création des tables

1. Table Pokemon
   
```
CREATE TABLE "Pokemon" (
	"pokedex_id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"size"	REAL,
	"weight"	REAL,
	"basic_stats"	INTEGER,
	"image"	TEXT UNIQUE,
	"types"	INT ,
	"skills"	INT ,
	FOREIGN KEY("types") REFERENCES "Type"("id"),
	FOREIGN KEY("skills") REFERENCES "Skill"("id"),
	PRIMARY KEY("pokedex_id" AUTOINCREMENT)
)
```

2. Table Skill

```
CREATE TABLE "Skill" (
    "id"    INTEGER NOT NULL UNIQUE,
    "name"    TEXT NOT NULL UNIQUE,
    "description"    TEXT,
    "power"    INTEGER,
    "accuracy"    INTEGER,
    "life_max"    INTEGER COLLATE UTF16CI,
    "type_name"    TEXT COLLATE UTF16CI,
    FOREIGN KEY("type_name") REFERENCES "Type"("name"),
    PRIMARY KEY("id" AUTOINCREMENT)
)
```
3. Table Type
```
CREATE TABLE "Type" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
)
```

### Diagramme du schéma de données

![image](https://github.com/julienousmer/fastap-api-pokemon/assets/95275157/32705971-0210-4295-8810-cb303bfe53c8)

NB : J'ai choisi suite à une discussion avec mon professeur lors du lancement de ce projet d'utiliser pour les relations 
entre les pokémons ainsi que leur(s) type(s) et compétence(s) respectives d'utiliser une list d'entier, qui récupère les id des compétences et types attribués au pokémon.
Ce choix m'a été conseillé par M. Aunim pour pouvoir attribuer 1 à n types et compétences à chacun des pokémons.




