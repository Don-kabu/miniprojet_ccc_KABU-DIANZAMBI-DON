
##################################################################################
##################################################################################
#######                     main.py                                     ##########
#######                    ______________                               ##########
#######    this file is the root file of the project and        
#######    contains the root or main logic of the project               ##########
#######                                                                 ##########
##################################################################################
##################################################################################

import docx2txt
import re
import json

text=docx2txt.process("input/Raw DATA 01.doc")
from typing import Dict, Any





def fix_encoding(data):
    """
    Corrige les problèmes d'encodage 'Âµ' → 'µ'
    dans un dictionnaire 
    """
    if isinstance(data, dict):
        return {fix_encoding(k): fix_encoding(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [fix_encoding(item) for item in data]
    elif isinstance(data, str):
        corrections = {
            "Âµ": "µ",
        }
        for wrong, right in corrections.items():
            data = data.replace(wrong, right)
        return data
    else:
        return data




def normalize_value(key: str, value: str):
    """Normalise seulement les données numériques avec unités, ignore les dates."""
    if not isinstance(value, str):
        return value

    val = fix_encoding(value)

    # garder Polarization tel quel
    if val in ["Vertical", "Horizontal"]:
        return val

    # garder les dates (présence de / et :)
    if re.search(r"\d{1,2}/\d{1,2}/\d{4}", val) and ":" in val:
        return val

    # détecter RBW et garder texte standard
    if "rbw" in key.lower():
        val = val.lower().replace(" ", "")
        if "9khz" in val:
            return "9 kHz"
        if "120khz" in val:
            return "120 kHz"
        if "1mhz" in val:
            return "1 MHz"
        return val

    # remplacer virgule par point pour parsing
    candidate = val.replace(",", ".")

    # extraire uniquement la partie numérique
    clean_val = re.sub(r"[^\d\.\-]", "", candidate)

    # si pas de chiffre → retourner texte brut
    if not re.search(r"\d", clean_val):
        return val

    try:
        num = float(clean_val)
    except ValueError:
        return val

    key_lower = key.lower()

    # fréquence
    if "frequency" in key_lower:
        return round(num, 5) if num < 10 else round(num, 3)

    # valeurs en dB
    if "db" in key_lower:
        return round(num, 2)

    # valeurs simples → int si possible
    return int(num) if num.is_integer() else num

def normalize_data(data):
    """Corrige encodage + normalise toutes les valeurs numériques avec unités."""
    if isinstance(data, dict):
        return {fix_encoding(k): normalize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_data(item) for item in data]
    elif isinstance(data, str):
        return normalize_value("", data)
    else:
        return data