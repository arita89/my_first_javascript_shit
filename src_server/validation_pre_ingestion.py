# validation_pre_ingestion.py

import pandas as pd
import csv
from io import StringIO

from datetime import date, datetime
from models import models_current
from typing import Dict, List, Any, Tuple
from pydantic import ValidationError, BaseModel
from utils import *

## VALIDATE REQUIRED SHEETS
def get_required_sheets(csv_content: str) -> List[str]:
    """
    from a certain reference csv - to be required as input? 
    the list of required sheets is created 
    """
    required_sheets = set()
    csv_reader = csv.DictReader(StringIO(csv_content), delimiter=';')
    for row in csv_reader:
        if row['sheet_is_optional'].strip().upper() == 'FALSE':
            required_sheets.add(row['sheet'])
    return list(required_sheets)

def validate_excel_sheets(excel_path: str, required_sheets: List[str]) -> List[str]:
    xls = pd.ExcelFile(excel_path)
    existing_sheets = xls.sheet_names
    
    missing_sheets = [sheet for sheet in required_sheets if sheet not in existing_sheets]
    return missing_sheets

## VALIDATE WITH PYDANTIC MODELS - REQUIRED COLUMNS, TYPE, RANGE, REGEX
def get_model_by_sheet(sheet_name: str):
    # Iterate over all items in the models_current
    for name, obj in vars(models_current).items():
        # Ensure the object is a Pydantic model and has the __sheet_name__ attribute
        if isinstance(obj, type) and issubclass(obj, BaseModel) and hasattr(obj, '__sheet_name__'):
            if obj.__sheet_name__ == sheet_name:
                return obj
    return None

def validate_data_with_pydantic(data_dicts: Dict[str, List[Dict[str, Any]]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Validate data for each Excel sheet against its corresponding Pydantic model.
    
    Args:
        data_dicts : A dictionary where keys are sheet names 
            and values are lists of dictionaries, each representing a row from the sheet.

    Returns:
        valid_data, errors : A tuple containing two lists,
            one for valid data and another for errors. Each error includes the sheet name,
            the row data that failed validation, and the validation errors.
    """
    valid_data = []
    errors = []

    # Iterate over the sheet names and their corresponding data
    for sheet_name, data_list in data_dicts.items():
        model = get_model_by_sheet(sheet_name)
        if not model:
            errors.append({'sheet': sheet_name, 'error': 'No matching Pydantic model found'})
            continue

        for data in data_list:
            try:
                model_instance = model(**data)
                valid_data.append(model_instance.dict(exclude_unset=True))
            except ValidationError as e:
                errors.append({'sheet': sheet_name, 'row': data, 'errors': e.errors()})

    return valid_data, errors

## MORE COMPLEX AND AD HOC VALIDATION RULES