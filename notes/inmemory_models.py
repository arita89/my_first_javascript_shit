"""
have an Excel file where each sheet represents a different data model, 
and each column in a sheet represents a field in that model. 
The "optional" or "required" nature of each field depends on some user input 
or predefined rules.

Here’s a step-by-step approach to dynamically create a Pydantic model for each sheet:

- Read the Excel File: Use a library like pandas to read each sheet in the Excel file.

- Determine Field Types and Optionality: Based on user input or other criteria, 
determine which fields are optional and what their types should be.

- Dynamically Create Models: Use Pydantic’s create_model to create a model for each sheet, 
using the information extracted from the Excel file.

"""

import pandas as pd
from pydantic import BaseModel, create_model
from typing import Optional, Dict, Type

# Placeholder for dynamically created models
dynamic_models: Dict[str, Type[BaseModel]] = {}

# Load the Excel file
excel_file = pd.ExcelFile("your_excel_file.xlsx")


# Example function to determine field type and optionality
def get_field_type_and_optionality(column_name: str) -> tuple:
    # Example logic, replace with your own rules
    if column_name.startswith("optional_"):
        return (Optional[str], None)  # Mark as optional with default value None
    else:
        return (str, ...)  # Mark as required


# Iterate over each sheet in the Excel file
for sheet_name in excel_file.sheet_names:
    sheet_df = excel_file.parse(sheet_name)

    # Create a dictionary for the fields based on columns
    fields = {
        column: get_field_type_and_optionality(column) for column in sheet_df.columns
    }

    # Dynamically create a model for the sheet
    model = create_model(sheet_name, **fields)

    # Store the model in the dictionary
    dynamic_models[sheet_name] = model

# Now you can use the dynamically created models
# Example: Create an instance of a model for a specific sheet
sheet_model = dynamic_models["Sheet1"]  # Replace 'Sheet1' with your actual sheet name
instance = sheet_model(
    **{"your_field_name": "your_value"}
)  # Use actual field names and values
print(instance)
