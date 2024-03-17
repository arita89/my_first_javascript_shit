# services.py

import csv
import yaml
import pandas as pd
from tempfile import NamedTemporaryFile
import os
from openpyxl import Workbook

# Function to convert CSV content (as a string) to YAML string
def csv_to_yaml(csv_content, delimiter=';'):
    csv_reader = csv.DictReader(csv_content.splitlines(), delimiter=delimiter)
    yaml_data = {'sheets': []}
    current_sheet_name = ""
    sheet_structure = {}

    for row in csv_reader:
        if not row['sheet'].strip():  # Skip rows with blank sheet names, in case of trailing white spaces on actually empty rows
            continue
        if current_sheet_name != row['sheet'].strip().lower():  # Normalize sheet names
            if current_sheet_name:
                yaml_data['sheets'].append(sheet_structure)
            current_sheet_name = row['sheet'].strip().lower()  # Normalize sheet names
            sheet_structure = {
                'name': current_sheet_name,
                'color': row.get('sheet_color', 'FFFFFF'),  # Assume white as default color if not specified
                'is_optional': row['sheet_is_optional'].lower() == 'true',
                'responsibility': row['responsibility'],
                'columns': []
            }
        sheet_structure['columns'].append({
            'name_internal': row['column_name_internal'],
            'name_external': row['column_name_external'],
            'data_type': row['data_type'],
            'is_optional': row['column_is_optional'].lower() == 'true',
            'data_validation_rule_01': row['column_data_validation_rule_01'] or None,
            'data_validation_rule_02': row['column_data_validation_rule_02'] or None
        })
    yaml_data['sheets'].append(sheet_structure)
    return yaml.dump(yaml_data, sort_keys=False, default_flow_style=False, allow_unicode=True)

# Function to convert YAML string to an Excel file and return its path
def yaml_to_excel(yaml_str, excel_file_name='data.xlsx'):
    data = yaml.safe_load(yaml_str)
    temp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
    excel_file_path = temp_file.name
    temp_file.close()
    
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        for sheet in data['sheets']:
            df = pd.DataFrame({col['name_internal']: [] for col in sheet['columns']})
            df.to_excel(writer, sheet_name=sheet['name'], index=False)
            # Set the tab color
            if 'color' in sheet and sheet['color'].strip():
                writer.sheets[sheet['name']].tab_color = sheet['color'][1:]  # Remove '#' for openpyxl
    
    return excel_file_path

# Function to clean up the generated file
def cleanup_file(file_path):
    os.remove(file_path)
