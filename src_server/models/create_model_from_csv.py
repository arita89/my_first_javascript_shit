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
    csv_reader = csv.DictReader(StringIO(csv_content), delimiter=';')
    fields = []
    for row in csv_reader:
        py_type = type_mapping(row['column_validation_format'])
        validation = validation_mapping(row['column_validation_type'], row['column_validation_details'])
        is_optional = row.get('column_is_optional', 'TRUE').strip().upper() == 'TRUE'

        # Adjusting default based on column optionality
        default = "None" if is_optional else "..."
        
        # Constructing each field line with the adjusted default
        field_line = f"    {row['column_name_internal']}: Optional[{py_type}] = Field({default}, {validation})" if is_optional else f"    {row['column_name_internal']}: {py_type} = Field({default}, {validation})"
        fields.append(field_line)

    fields_body = "\n".join(fields)

    model_code = f"""
from pydantic import BaseModel, Field
from typing import Optional
import datetime

class TemplateModel(BaseModel):
{fields_body}
    """
    return model_code.strip()
