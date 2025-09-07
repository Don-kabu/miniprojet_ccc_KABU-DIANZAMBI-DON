
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

text=docx2txt.process("input/Raw DATA 01.doc")

with open("output.txt","w") as f:
    f.write(text)
# Les titres possibles
titles = [
    r"CISPR\.AVG/Lim\.Avg \(2\)",
    r"Peak/Lim\.Q-Peak \(2\)",
    r"Q-Peak/Lim\.Q-Peak \(2\)",
    r"Peak/Lim\.Peak \(2\)"
]

# Regex pour capturer un bloc complet par titre
pattern = re.compile(
    r"(?s)(?P<title>" + "|".join(titles) + r")"
    r".*?(?:Vertical|Horizontal)\s*\d+\.\d+\s*"
    r"\n\n\n"
)

result = {}

for match in pattern.finditer(text):
    title = match.group("title").strip()[:-3].strip()
    block = match.group()

    # Découper en lignes
    lines = [l.strip() for l in block.splitlines() if l.strip()]

    # En-têtes = lignes entre le titre et la première ligne numérique
    headers = []
    data_lines = []
    found_data = False
    for l in lines[1:]:  # skip le titre
        if not found_data and not re.match(r"^-?\d", l) and l not in ("Vertical", "Horizontal"):
            headers.append(l.replace("Â",""))
        else:
            found_data = True
            data_lines.append(l)

    rows = []
    row = []
    for val in data_lines:
        row.append(val.strip().replace(",","."))
        if len(row) == len(headers):
            # Vérification : dernière = nombre, avant-dernière = polarization
            if (row[-2] in ("Vertical", "Horizontal")
                and re.match(r"^-?\d+(\.\d+)?$", row[-1])):
                rows.append(dict(zip(headers, row)))
            row = []  # reset

    result[title] = rows






import pandas as pd

# Dataset fourni
data = result

rows = []

for section, entries in data.items():
    for idx, entry in enumerate(entries, start=1):
        # Colonnes mesure, limite, marge
        mesure_key = next((k for k in entry if "(dBµV/m)" in k and "Lim" not in k), None)
        limite_key = next((k for k in entry if "Lim" in k and "(dBµV/m)" in k), None)
        marge_key = next((k for k in entry if "Lim" in k and "-" in k), None)

        mesure = float(entry[mesure_key])
        limite = float(entry[limite_key])
        marge = float(entry[marge_key])

        verdict = "PASS" if marge >= 0 else "FAIL"

        # Formatage fréquence et dB
        freq = float(entry["Frequency (MHz)"])
        freq_str = f"{freq:.5f}" if freq < 10 else f"{freq:.3f}"
        mesure_str = f"{mesure:.2f}"
        limite_str = f"{limite:.2f}"
        marge_str = f"{marge:.2f}"

        # Polarization
        polar = entry.get("Polarization", "")
        if polar not in ["Vertical", "Horizontal"]:
            polar = "Unknown"

        # RBW (détection automatique)
        rbw = entry.get("RBW", "")
        if rbw not in ["9kHz", "120kHz", "1MHz"]:
            rbw = "Unknown"

        row = {
            "section": section,
            "index": idx,
            "frequency (MHz)": freq_str,
            "mesure (dBµV/m)": mesure_str,
            "limite (dBµV/m)": limite_str,
            "marge (dB)": marge_str,
            "verdict_ligne": verdict,
            "Polarization": polar,
            "Correction (dB)": f"{float(entry.get('Correction (dB)',0)):.2f}",
            "RBW": rbw
        }
        rows.append(row)

# DataFrame final
# df = pd.DataFrame(rows)












import json

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