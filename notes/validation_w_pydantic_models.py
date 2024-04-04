from datetime import datetime

def generate_custom_validator_code(row):
    column_name = row.get('column_name_internal', '')
    validation_type = row.get('column_validation_type', '')
    val_operator = row.get('val_operator', '')
    val_formula1 = row.get('val_formula1', '')
    val_formula2 = row.get('val_formula2', '')

    # Ensure formulas are parsed as dates if they're not empty
    val_formula1_parsed = f"datetime.date({val_formula1})" if val_formula1 else "None"
    val_formula2_parsed = f"datetime.date({val_formula2})" if val_formula2 else "None"

    validator_code = ""

    if validation_type == 'date':
        if val_operator == 'between':
            validator_code = f"""
@validator('{column_name}', pre=True, always=True)
def validate_{column_name}(cls, v):
    if not ({val_formula1_parsed} <= v <= {val_formula2_parsed}):
        raise ValueError("{column_name} must be between {val_formula1} and {val_formula2}")
    return v
"""
        elif val_operator in ['gt', 'ge', 'lt', 'le']:
            operator_map = {'gt': '>', 'ge': '>=', 'lt': '<', 'le': '<='}
            comparison_op = operator_map[val_operator]
            validator_code = f"""
@validator('{column_name}', pre=True, always=True)
def validate_{column_name}(cls, v):
    if not (v {comparison_op} {val_formula1_parsed}):
        raise ValueError("{column_name} must be {val_operator} {val_formula1}")
    return v
"""

    return validator_code


def generate_list_validator_code(column_name, valid_values):
    # Convert the list of valid values into a Python list representation
    valid_values_str = str(valid_values)
    
    validator_code = f"""
@validator('{column_name}', pre=True, always=True)
def validate_{column_name}(cls, v):
    if v not in {valid_values_str}:
        raise ValueError(f'{{v}} is not a valid {column_name}')
    return v
"""
    return validator_code
