# validation_pre_ingestion.py

import pandas as pd
from pydantic import ValidationError
from datetime import date, datetime
from models.model_current import TemplateModel

def read_excel_to_dataframes(excel_file_path):
    # Reads all sheets into a dictionary of DataFrames
    dfs = pd.read_excel(excel_file_path, sheet_name=None)
    return dfs

def dataframe_to_dicts(df):
    return df.to_dict(orient="records")

def convert_dfs_to_data_dicts(dfs):
    """
    Convert a dictionary of DataFrames (each representing an Excel sheet)
    into a list of data dictionaries, including the sheet name with each record.

    Parameters:
    - dfs (dict): A dictionary where keys are sheet names and values are DataFrames.

    Returns:
    - List[dict]: A list of dictionaries with each dictionary representing a row from any sheet,
                  including the sheet name under the key 'sheet_name'.
    """
    all_data_dicts = []

    # Iterate through each sheet's DataFrame
    for sheet_name, df in dfs.items():
        # Convert the DataFrame to a list of dictionaries
        data_dicts = dataframe_to_dicts(df)
        
        # Add the sheet name to each dictionary
        for data_dict in data_dicts:
            data_dict['sheet_name'] = sheet_name
        
        # Extend the main list with these modified dictionaries
        all_data_dicts.extend(data_dicts)

    return all_data_dicts

def serialize_dates(obj):
    """ all date objects are converted to strings immediately after validation and before they are serialized to JSON"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (datetime, date)):
                # Convert datetime/date objects to string
                obj[key] = value.isoformat()
            elif isinstance(value, dict) or isinstance(value, list):
                obj[key] = serialize_dates(value)
    elif isinstance(obj, list):
        obj = [serialize_dates(item) if isinstance(item, (dict, list)) else item for item in obj]
    return obj

def validate_data_with_pydantic(data_dicts):
    valid_data = []
    errors = []

    for data in data_dicts:
        try:
            # Ensure the data is in the correct format for Pydantic validation
            model_instance = TemplateModel(**data)
            validated_data = model_instance.dict()
            # Serialize all datetime/date objects to strings
            validated_data = serialize_dates(validated_data)
            valid_data.append(validated_data)
        except ValidationError as e:
            errors.append(e.errors())  # Store structured errors for reporting

    return valid_data, errors