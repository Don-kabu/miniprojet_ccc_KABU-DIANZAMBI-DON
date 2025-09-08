# KABU DIANZAMBI DON 


# Mini-Projet CCC – Automatisation du traitement des RAW DATA

##  Objectif
Ce projet permet d’automatiser la **transformation de données brutes (RAW DATA)** issues de tests CEM en documents normalisés et exploitables.  
Il prend en entrée des fichiers Word de mesures brutes et génère automatiquement des résultats :
- Tableaux homogènes et lisibles,
- Calculs métier (marges, verdicts PASS/FAIL, verdict global),
- Exports multi-formats (Word, CSV, JSON),
- Rapport final formaté pour l’exploitation et la conformité.

## ⚙️ Installation

1. **Cloner le projet et entrer dans le dossier**
   ```bash
   git clone https://github.com/Don-kabu/miniprojet_ccc_KABU-DIANZAMBI-DON.git

   cd MINIPROJET_CCC_KABU-DIANZAMBI-DON
    ```


## Installer les dépendances

pip install -r requirements.txt

## Utilisation

### Configurer le fichier d’entrée

Ouvrir src/config.py

### Modifier le paramètre INPUTFILE en mettant le chemin vers votre fichier RAW.
Exemple par défaut :

INPUTFILE = "input/RAW DATA 02.doc"


### execution du projet

python src/main.py


Résultats générés
Tous les fichiers de sortie se trouvent dans le dossier out/ :

out/out_(nomfichier).csv → Résultats tabulés au format CSV

out/(nomfichier)_IMPORTANT.json → Résumé des informations essentielles

out/(nomfichier)_FULL.json → Résultats complets en JSON

out/Processed_(nomfichier).docx → Rapport final Word formaté

# Structure du projet
```bash
MINIPROJET_CCC_KABU-DIANZAMBI-DON/
├─ input/                  # Fichiers RAW en entrée
├─ out/                    # Résultats générés
│   ├─ *.csv
│   ├─ *_IMPORTANT.json
│   ├─ *_FULL.json
│   └─ Processed_*.docx
├─ src/                    # Code source
│   ├─ config.py           # Configuration principale (INPUTFILE)
│   ├─ main.py             # Point d'entrée du programme
│   ├─ Parser.py           # Parsing des données RAW
│   ├─ rules.py            # Logique métier (marges, verdicts)
│   ├─ writter.py          # Génération Word/CSV
│   └─ utils.py            # Outils (hash, logs, etc.)
├─ tests/                  # Tests unitaires
├─ requirements.txt        # Dépendances Python
└─ README.md               # Documentation
```

## Exemple rapide
# Modifier src/config.py
```bash
INPUTFILE = "input/RAW DATA 01.doc"
```
# Lancer le script
```bash
    python src/main.py
```

# Vérifier les résultats dans /out
```bash
Résultats générés
Tous les fichiers de sortie se trouvent dans le dossier out/ :

. out/out_(nomfichier).csv → Résultats tabulés au format CSV

. out/(nomfichier)_IMPORTANT.json → Résumé des informations essentielles

. out/(nomfichier)_FULL.json → Résultats complets en JSON

. out/Processed_(nomfichier).docx → Rapport final Word formaté
```