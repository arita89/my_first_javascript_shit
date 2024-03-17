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
    #print ("READING CSV FILE")
    csv_reader = csv.DictReader(StringIO(csv_content), delimiter=';')
    fields = []
    for row in csv_reader:
        py_type = type_mapping(row['column_validation_format'])
        validation = validation_mapping(row['column_validation_type'], row['column_validation_details'])

        # Constructing each field line.
        field_line = f"    {row['column_name_internal']}: {py_type} = Field(..., {validation})"
        fields.append(field_line)

    # Joining all field lines to form the body of the Pydantic model class.
    fields_body = "\n".join(fields)

    # Forming the complete model class as a string.
    model_code = f"""
from pydantic import BaseModel, Field
import datetime

class TemplateModel(BaseModel):
{fields_body}
    """
    #print ("PYDANTIC MODEL BUILT")
    #print (model_code.strip())
    return model_code.strip()

