# automatically build sqlalchemy models 

import pandas as pd

# Example DataFrame with additional attributes for each column
data_attributes = {
    'column_name': ['id', 'name', 'age', 'email', 'hire_date'],
    'data_type': ['int64', 'object', 'int64', 'object', 'datetime64[ns]'],
    'is_primary_key': [True, False, False, False, False],
    'is_nullable': [False, True, True, False, True],
    'is_unique': [True, False, False, True, False],
    'is_index': [True, False, True, True, False],
}

df_attributes = pd.DataFrame(data_attributes)

# Mapping from pandas dtype to SQLAlchemy type strings
dtype_mapping = {
    'object': 'String',
    'int64': 'Integer',
    'float64': 'Float',
    'bool': 'Boolean',
    'datetime64[ns]': 'DateTime',
}

# Function to generate SQLAlchemy model class definitions with column attributes
def print_sqlalchemy_model_with_attributes(df_attributes, table_name):
    model_str = f"class {table_name.capitalize()}(Base):\n"
    model_str += f"    __tablename__ = '{table_name.lower()}'\n"
    
    for _, row in df_attributes.iterrows():
        column_name = row['column_name']
        sqlalchemy_type = dtype_mapping.get(row['data_type'], 'String')
        primary_key = "primary_key=True" if row['is_primary_key'] else ""
        nullable = f"nullable={row['is_nullable']}"
        unique = "unique=True" if row['is_unique'] else ""
        index = "index=True" if row['is_index'] else ""
        
        # Combine attributes, filtering out empty strings
        attributes = ", ".join(filter(None, [sqlalchemy_type, primary_key, nullable, unique, index]))
        
        model_str += f"    {column_name} = Column({attributes})\n"
    
    print(model_str)

# Example usage
print_sqlalchemy_model_with_attributes(df_attributes, 'Employee')
