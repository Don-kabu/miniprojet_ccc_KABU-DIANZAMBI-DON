import pandas as pd
import Parser
from docx import Document
from docx.shared import Pt, Inches,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json
from datetime import datetime
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import config







def getdata(rawdata):
    blocks = Parser.find_all_blocks(rawdata)
    data = []
    for block in blocks:
        blockdata = {}
        blockdata["test_name"]=Parser.extract_name_test(block)
        blockdata["metadata"] = Parser.extract_metadata(block)
        blockdata["parameters"] = Parser.extract_test_parameters_block(block)
        blockdata["measurements"] = Parser.extract_measurement_tables(block)

        data.append(blockdata)
    data = Parser.normalize_data(data)
    return data













# the function that returns a cleaned data or important data or best data format for output
def get_cleaned_data(data):
    data=Parser.normalize_data(data)
    result = []
    for block in data :
        result.append(getblockdata(block))
    result.append({
        "headers":[
            "Section",
            "Frequency(MHz)",
            "SR",
            "Polarization",
            "Correction(dB)",
            "Mesure(dBµV/m)",
            "Limite(dBµV/m)",
            "Marge(dB)",
            "Verdict"
        ]
    })
    return result








# this function gets block important data for output
def getblockdata(block):
    result={}
    try:
        result["header"]=  f"{block['test_name']}-{block['metadata']['test_config']['DUT Orientation']}-Mode{block['metadata']['operating_mode']['Mode']}-{block['metadata']['operating_mode']['Conclusion']} \n tests :{''.join([k['name'] for k in block['parameters'] ])}"
        result["table"]=[]

        for k in block["measurements"].keys():
            detector =k.split("/")[0]

            for i in block["measurements"][k]["rows"]:
                d = [a for a in i.values()]+[detector]
                result["table"].append(d+["PASS" if d[-4]*-1 >=0 else "FAIL"])
        
        # produire le veridict de la section
        for i in result["table"]:
            if i[-1] =="FAIL":
                result["verdict"]="FAIL"
                break
            else:
                result["verdict"]="PASS"
    except:
        pass

    return result












def get_filename_from_path(path):
    return path.split("/")[-1].split(".")[0]







def export_to_csv(data,filename):
    measurements_list = []

    for test_name, test_data in data.items():
        if test_data['has_measurements'] and test_data['measurements']:
            for measurement in test_data['measurements']:
                measurement_row = {
                    'test_name': test_name,
                    'sample_id': test_data['sample_id'],
                    'antenna_position': test_data['antenna_position'],
                    'dut_orientation': test_data['dut_orientation'],
                    'measurement_type': measurement['measurement_type'],
                    'frequency_mhz': measurement['frequency_mhz'],
                    'sr': measurement['sr'],
                    'Measure': measurement.get('Measure', ''),
                    'Limit': measurement['Limit'],
                    'Margin': measurement['Margin'],
                    'polarization': measurement['polarization'],
                    'correction_db': measurement['correction_db'],
                    'veridict': measurement['veridict'],
                    'Measured': measurement.get('Measured', '')
                }
                measurements_list.append(measurement_row)

    # Créer le DataFrame et exporter en CSV
    if measurements_list:
        df = pd.DataFrame(measurements_list)
        df.to_csv(f'out/out_{filename}.csv', index=False, encoding='utf-8')
        return True
    else:
        return False







def getdataframe(json_data):
    # Définir les noms de colonnes pour le DataFrame final
    final_columns = [
        "Section", 
        "Frequency (MHz)", 
        "SR", 
        "Polarization", 
        "Correction (dB)", 
        "Mesure(dBµV/m)", 
        "Limite (dBµV/m)", 
        "Marge (dB)", 
        "Detector",
        "Verdict"
    ]
    
    all_data = []
    
    for item in json_data[:-2]:
        try:
            header = item["header"].split(" ")[0]
            table = item["table"]
        except:
            continue

        if table:
            for row in table:
                # Extraire les valeurs du tableau
                frequency = row[0]
                sr = row[1]
                mesure = row[2]
                limite = row[3]
                marge = row[4]
                polarization = row[5]
                correction = row[6]
                detector = row[7]  # Non utilisé dans le format final demandé
                row_verdict = row[8]
                
                # Créer une nouvelle ligne avec le format demandé
                new_row = [
                    header,          # Section
                    frequency,       # Frequency (MHz)
                    sr,              # SR
                    polarization,    # Polarization
                    correction,      # Correction (dB)
                    mesure,          # Mesure(dBµV/m)
                    limite,          # Limite (dBµV/m)
                    marge,           # Marge (dB)
                    detector,
                    row_verdict      # Verdict
                ]
                
                all_data.append(new_row)
        else:
            all_data.append(["" for i in range(10)])
    
    # Créer le DataFrame
    df = pd.DataFrame(all_data, columns=final_columns)
    return df


