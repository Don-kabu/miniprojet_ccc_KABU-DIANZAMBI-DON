
import re
from typing import Dict, Any







def normalize_value(key: str, value: str):
    """Normalise seulement les données numériques avec unités, ignore les dates."""
    if not isinstance(value, str):
        return value


    # garder Polarization tel quel
    if value in ["Vertical", "Horizontal"]:
        return value

    # garder les dates (présence de / et :)
    if re.search(r"\d{1,2}/\d{1,2}/\d{4}", value) and ":" in value:
        return value

    # détecter RBW et garder texte standard
    if "rbw" in key.lower():
        value = value.lower().replace(" ", "")
        if "9khz" in value:
            return "9 kHz"
        if "120khz" in value:
            return "120 kHz"
        if "1mhz" in value:
            return "1 MHz"
        return value

    # remplacer virgule par point pour parsing
    candidate = value.replace(",", ".")

    # extraire uniquement la partie numérique
    clean_val = re.sub(r"[^\d\.\-]", "", candidate)

    # si pas de chiffre → retourner texte brut
    if not re.search(r"\d", clean_val):
        return value

    try:
        num = float(clean_val)
    except ValueError:
        return value

    key_lower = key.lower()

    # fréquence
    if "frequency" in key_lower:
        return round(num, 5) if num < 10 else round(num, 3)

    # valeurs en dB
    if "db" in key_lower:
        return round(num, 2)

    # valeurs simples → int si possible
    return int(num) if num.is_integer() else num





# normalisation des valeurs numerique 
def normalize_data(data):
    """normalise toutes les valeurs numériques avec unités."""
    if isinstance(data, dict):
        return {k : normalize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_data(item) for item in data]
    elif isinstance(data, str):
        return normalize_value("", data)
    else:
        return data
    
