import json
import csv

def json_to_flat_csv(data):
    """
    Transforme un fichier JSON de tests en un CSV plat avec metadata, test_config,
    parameters et measurements.
    """

    # Colonnes de base
    base_cols = [
        "Test name", "Sample", "Project", "Operator",
        "Antenna position", "DUT Orientation", 
        "Housing connected to the ground plane", 
        "Configuration of the power return line LV",
        "Operating Mode", "Conclusion"
    ]

    # Colonnes parameters
    param_cols = [
        "Parameter name", "Step", "Preamp", "Setup", 
        "RBW", "Dynamic", "Span", "Ref_level", 
        "VBW", "RF Att", "Sweep time", "Maxhold"
    ]

    # Colonnes measurements
    measure_cols = set()
    for test in data.values():
        measurements = test.get("measurements", {})
        for measure_data in measurements.values():
            measure_cols.update(measure_data.get("headers", []))
    measure_cols = list(measure_cols)

    # Toutes les colonnes
    all_cols = base_cols + param_cols + measure_cols

    with open("out/output.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_cols)
        writer.writeheader()

        for test_name, test_data in data.items():
            metadata = test_data.get("metadata", {})
            test_config = metadata.get("test_config", {})
            operating_mode = metadata.get("operating_mode", {})
            parameters = test_data.get("parameters", [])
            measurements = test_data.get("measurements", {})

            if not parameters:
                parameters = [{}]

            for param in parameters:
                row = {
                    "Test name": test_name,
                    "Sample": metadata.get("sample", ""),
                    "Project": metadata.get("project", ""),
                    "Operator": metadata.get("operator", ""),
                    "Antenna position": test_config.get("Antenna position", ""),
                    "DUT Orientation": test_config.get("DUT Orientation", ""),
                    "Housing connected to the ground plane": test_config.get("Housing connected to the ground plane", ""),
                    "Configuration of the power return line LV": test_config.get("Configuration of the power return line LV", ""),
                    "Operating Mode": operating_mode.get("Mode", ""),
                    "Conclusion": operating_mode.get("Conclusion", ""),
                    "Parameter name": param.get("name", ""),
                    "Step": param.get("step", ""),
                    "Preamp": param.get("preamp", ""),
                    "Setup": param.get("setup", ""),
                    "RBW": param.get("rbw", ""),
                    "Dynamic": param.get("dynamic", ""),
                    "Span": param.get("span", ""),
                    "Ref_level": param.get("ref_level", ""),
                    "VBW": param.get("vbw", ""),
                    "RF Att": param.get("rf_att", ""),
                    "Sweep time": param.get("sweep_time", ""),
                    "Maxhold": param.get("maxhold", "")
                }

                # Ajouter les mesures
                if measurements:
                    for measure_name, measure_data in measurements.items():
                        rows = measure_data.get("rows", [])
                        if rows:
                            for measure_row in rows:
                                row_copy = row.copy()
                                for col in measure_cols:
                                    row_copy[col] = measure_row.get(col, "")
                                writer.writerow(row_copy)
                        else:
                            for col in measure_cols:
                                row[col] = ""
                            writer.writerow(row)
                else:
                    for col in measure_cols:
                        row[col] = ""
                    writer.writerow(row)

# Exemple d'utilisation
