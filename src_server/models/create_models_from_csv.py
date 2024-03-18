from typing import List
import csv
from io import StringIO
from datetime import datetime

def type_mapping(csv_type: str):
    """Maps CSV column types to Python types."""
    return {
        'int': 'int',
        'float': 'float',
        'char': 'str',
        'date': 'datetime.date',
    }.get(csv_type, 'str')

def validation_mapping(validation_type: str, details: str):
    """Generates Pydantic validator strings based on CSV validation details."""
    if validation_type == 'range':
        #print (details.strip('[]').split('-'))
        start, end = details.strip('[]').split('-')
        return f"ge={start}, le={end}"
    elif validation_type in ['min', 'max']:
        value = details[1:]
        operator = 'ge' if '>' in details else 'le'
        return f"{operator}={value}"
    elif validation_type == 'list':
        options = details.split(',')
        options_formatted = ", ".join([f'"{opt}"' for opt in options])  # Formatting options without f-string
        return f"values=[{options_formatted}]"
    return ''

def generate_pydantic_model(csv_content: str) -> str:
    models_code = "from pydantic import BaseModel, Field\nfrom typing import Optional\nimport datetime\nimport enum\n\n"
    sheets_schema = {}

    csv_reader = csv.DictReader(StringIO(csv_content), delimiter=';')
    for row in csv_reader:
        sheet_name = row['sheet']
        if sheet_name not in sheets_schema:
            sheets_schema[sheet_name] = []
        
        py_type = type_mapping(row['column_validation_format'])
        validation = validation_mapping(row['column_validation_type'], row['column_validation_details'])
        is_optional = row['column_is_optional'].strip().upper() == 'TRUE'
        
        field_definition = {
            'name': row['column_name_internal'],
            'type': py_type,
            'validation': validation,
            'optional': is_optional
        }
        sheets_schema[sheet_name].append(field_definition)

    for sheet_name, columns in sheets_schema.items():
        class_name = ''.join(word.capitalize() for word in sheet_name.split('_')) + 'Model'
        fields_code = []
        for column in columns:
            field_type = f"Optional[{column['type']}]" if column['optional'] else column['type']
            validation_code = f", {column['validation']}" if column['validation'] else ""
            fields_code.append(f"    {column['name']}: {field_type} = Field(default=None{validation_code})")
        fields_code_str = "\n".join(fields_code)
        model_code = f"class {class_name}(BaseModel):\n{fields_code_str}\n\n"
        models_code += model_code
    return models_code.strip()
