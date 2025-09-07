# -*- coding: utf-8 -*-

import re
import docx2txt
from typing import List, Dict, Any
from config import MESURE_DATA_PATTERN,TEST_PARAMETERS_BLOCK_PATTERN,BLOCK_PATTERN,META_DATA_PATTERN
import json
from rules import fix_encoding,normalize_data
from utils import json_to_flat_csv

text = docx2txt.process("input/RAW DATA 02.doc")


def extract_measurement_tables(text: str) -> Dict[str, Any]:

    # Regex pour capturer un tableau depuis son titre jusqu'au 2ème 'Vertical|Horizontal + nombre'
    results = {}
    for match in MESURE_DATA_PATTERN.finditer(text):
        title = match.group("title").strip().replace("Â","")  # enlever (2) et espaces
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
    match = TEST_PARAMETERS_BLOCK_PATTERN.finditer(block)
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
    match = META_DATA_PATTERN.search(text)
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
    return BLOCK_PATTERN.findall(text)




def makedata(rawdata):
    blocks = find_all_blocks(rawdata)
    data = {}
    a = 0
    for i, block in enumerate(blocks, 1):
        test_name = extract_name_test(block)
        data[test_name] = {}
        data[test_name]["metadata"] = extract_metadata(block)
        data[test_name]["parameters"] = extract_test_parameters_block(block)
        data[test_name]["measurements"] = extract_measurement_tables(block)


    # data["measurements"] = extract_measurement_tables(rawdata)

    data = normalize_data(fix_encoding(data))
    with open("out/output.json","w",encoding="utf-8") as file:
        json.dump(data,file,indent=4,ensure_ascii=False)
    return data

# makedata(text)
data = json_to_flat_csv(makedata(text))
print(data)