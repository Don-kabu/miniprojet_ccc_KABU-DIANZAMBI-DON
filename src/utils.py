
##################################################################################
##################################################################################
#######                     main.py                                     ##########
#######                    ______________                               ##########
#######    this file is the root file of the project and        
#######    contains the root or main logic of the project               ##########
#######                                                                 ##########
##################################################################################
##################################################################################

import pandas as pd





def json_to_flat_csv(data):

    rows = []

    for key, content in data.items():

        metadata = content.get("metadata", {})
        parameters = content.get("parameters", [])

        # Extraire test_config et operating_mode séparément
        test_config = metadata.get("test_config", {})
        operating_mode = metadata.get("operating_mode", {})

        # Cas où il y a une liste de paramètres
        if isinstance(parameters, list):
            for param in parameters:
                row = {
                    "section": key,
                    "sample": metadata.get("sample", ""),
                    "project": metadata.get("project", ""),
                    "operator": metadata.get("operator", ""),
                    **test_config,
                    **operating_mode,
                    **param
                }
                rows.append(row)
        else:
            # Cas sans paramètres
            row = {
                "section": key,
                "sample": metadata.get("sample", ""),
                "project": metadata.get("project", ""),
                "operator": metadata.get("operator", ""),
                **test_config,
                **operating_mode
            }
            rows.append(row)

    # Conversion en DataFrame
    df = pd.DataFrame(rows)

    # Sauvegarde en CSV
    df.to_csv("out/output.csv", index=False, encoding="utf-8")
    return df