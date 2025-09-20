# -*- coding: utf-8 -*-

import re
import docx2txt
from typing import List, Dict, Any
import config
from rules import normalize_data



# le donnees brut qui viennent directement du fichier de RAW DATA.
text = docx2txt.process("input/RAW DATA 02.doc")

# fixage manuel de l'encodage , suppression du caractere "Â"
text = text.replace("Â","")




# la fonction qui extrait les tables des mesures du block de text brut .
def extract_measurement_tables(text: str) -> Dict[str, Any]:

    # Regex pour capturer un tableau depuis son titre jusqu'au 2ème 'Vertical|Horizontal + nombre'
    results = {}
    for match in config.MESURE_DATA_PATTERN.finditer(text):
        title = match.group("title").strip()  # enlever (2) et espaces
        body = match.group("body").strip().splitlines()
        
        # Nettoyage des lignes vides
        body = [line.strip() for line in body if line.strip()]

        # Le premier bloc = en-têtes
        headers = []
        data = []
        
        # On considère que les lignes non numériques = en-têtes
        for line in body:
            if not re.match(r"^[\d\.\-]+$", line) and line not in ("Vertical", "Horizontal"):
                headers.append(line)
            else:
                break
        # Données brutes (les nombres et valeurs texte)
        raw_values = body[len(headers):]
        # Regroupement par "nombre de colonnes"
        num_cols = len(headers)
        rows = [raw_values[i:i+num_cols] for i in range(0, len(raw_values), num_cols)]
        # Construction en dictionnaires
        for row in rows:
            if len(row) == num_cols:
                data.append(dict(zip(headers, row)))
        results[title] = {
            "headers": headers,
            "rows": data
        }
    return results










def extract_test_parameters_block(block: str) -> Dict[str, str]:
    """
    Extrait les paramètres d'un seul bloc de test et les retourne sous forme de dictionnaire.
    Le bloc doit contenir les champs standards (name, filename, step, ...).
    """
    match = config.TEST_PARAMETERS_BLOCK_PATTERN.finditer(block)
    if not match:
        return []
    else:
        test_params = [value.groupdict() for keys,value in enumerate(match) ]
    return test_params
    








def extract_name_test(text: str):
    """
    Extrait uniquement la ligne qui suit 'Name test:'.
    """
    pattern = re.compile(r"Name test:\s*([^\n\r]+)")
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None










def parse_test_config(config_text: str) -> Dict[str, str]:
    """
    Transforme le champ Test Configuration en dictionnaire.
    Exemple:
    "Antenna position:in front, DUT Orientation:axis X"
    => {"Antenna position": "in front", "DUT Orientation": "axis X"}
    """
    params = {}
    for part in config_text.split(","):
        if ":" in part:
            key, value = part.split(":", 1)
            params[key.strip()] = value.strip()
        else:
            # cas où il n'y a pas de ':', on garde brut
            part = part.strip().split(" ")
            params[part[0]] = part[1] if len(part) > 1 else ""
    return params








def extract_metadata(text: str) -> Dict[str, str]:
    """
    Extrait les métadonnées du bloc (Sample, Project, Operator, Test Configuration, Operating mode).
    """
    match = config.META_DATA_PATTERN.search(text)
    if not match:
        return {}
    meta = {k: v.strip() for k, v in match.groupdict().items()}
    meta["test_config"] = parse_test_config(meta["test_config"])
    meta["operating_mode"] = parse_test_config(meta["operating_mode"])
    return meta








def find_all_blocks(text: str) -> List[str]:
    """
    Trouve tous les blocs de test dans le texte.
    Un bloc commence par 'EQ/MR' et se termine avant le prochain 'EQ/MR' ou la fin du texte.
    """
    return config.BLOCK_PATTERN.findall(text)





