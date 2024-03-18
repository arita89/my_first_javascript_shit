from datetime import datetime
import pandas as pd

def generate_file_name(filename, extension):
    datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{filename}_{datetime_str}.{extension}"

def dataframe_to_dicts(df):
    return df.to_dict(orient="records")


# TO HANDLE EXCEL WITH MULTIPLE SHEETS

def read_excel_to_dataframes(excel_file_path):
    # Reads all sheets into a dictionary of DataFrames
    dfs = pd.read_excel(excel_file_path, sheet_name=None)
    return dfs

def convert_dfs_to_data_dicts(dfs):
    """
    Convert a dictionary of DataFrames (each representing an Excel sheet)
    into a dictionary where keys are sheet names and values are lists of dictionaries,
    with each dictionary representing a row from the respective sheet.

    Returns:
    - data_dicts: A dictionary with sheet names as keys and lists of dictionaries (rows) as values.
    """
    data_dicts = {}

    for sheet_name, df in dfs.items():
        # Convert each DataFrame to a list of dictionaries
        data_dicts[sheet_name] = dataframe_to_dicts(df)

    return data_dicts

def read_excel_to_data_dicts(excel_file_path):
    dfs = read_excel_to_dataframes(excel_file_path)
    return convert_dfs_to_data_dicts(dfs)

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