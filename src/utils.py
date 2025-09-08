import pandas as pd








def extract_important_data(data):
    structured_result = {}
    
    for test_name, test_data in data.items():
        metadata = test_data.get('metadata', {})
        test_config = metadata.get('test_config', {})
        operating_mode = test_data.get('metadata', {}).get('operating_mode', {})
        
        sample_id = metadata.get('sample', '')
        antenna_position = test_config.get('Antenna position', '')
        dut_orientation = test_config.get('DUT Orientation', '')
        mode = operating_mode.get("Mode")
        
        # Extraire les paramètres uniques (sans name)
        parameters_list = test_data.get('parameters', [])
        parameters_list[0].pop("name")
        parameters_list[0].pop("filename")
        unique_params = parameters_list[0]
        measurements_data = []
        measurements = test_data.get('measurements', {})
        
        for measurement_type, measurement_info in measurements.items():
            headers = measurement_info.get('headers', [])
            rows = measurement_info.get('rows', [])
            measurement_used = measurement_type.split('/')[0]
            
            for row in rows:
                # Créer une entrée standardisée
                measurement_entry = {
                    'measurement_type': measurement_used,
                    'frequency_mhz': row.get('Frequency (MHz)', ''),
                    'sr': row.get('SR', ''),
                    'Measure': '',
                    'Limit': '',
                    'Margin': '',
                    'polarization': row.get('Polarization', ''),
                    'correction_db': row.get('Correction (dB)', ''),
                    'veridict' : ''
                }
                
                # Remplir les valeurs selon le type de mesure
                if measurement_used == 'CISPR.AVG':
                    measurement_entry['Measured'] = row.get('CISPR.AVG (dBµV/m)', '')
                    measurement_entry['Limit'] = row.get('Lim.Avg (dBµV/m)', '')
                    measurement_entry['Margin'] = row.get('CISPR.AVG-Lim.Avg (dB)', '')
                elif measurement_used == 'Peak':
                    measurement_entry['Measured'] = row.get('Peak (dBµV/m)', '')
                    measurement_entry['Limit'] = row.get('Lim.Q-Peak (dBµV/m)', '') or row.get('Lim.Peak (dBµV/m)', '')
                    measurement_entry['Margin'] = row.get('Peak-Lim.Q-Peak (dB)', '') or row.get('Peak-Lim.Peak (dB)', '')
                elif measurement_used == 'Q-Peak':
                    measurement_entry['Measure'] = row.get('Q-Peak (dBµV/m)', '')
                    measurement_entry['Limit'] = row.get('Lim.Q-Peak (dBµV/m)', '')
                    measurement_entry['Margin'] = row.get('Q-Peak-Lim.Q-Peak (dB)', '')
                
                measurement_entry['veridict']  =  "PASS" if measurement_entry['Margin']>= 0 else "FAIL"
                    
                measurements_data.append(measurement_entry)
        
        # Structurer le résultat final
        structured_result[test_name] = {
            'sample_id': sample_id,
            'antenna_position': antenna_position,
            'mode' : mode,
            'dut_orientation': dut_orientation,
            'parameters': unique_params,
            'measurements': measurements_data,
            'has_measurements': bool(measurements)

        }
    
    return structured_result






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





