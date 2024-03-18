# Function to convert CSV content (as a string) to YAML string
        # TODO DELETE ONCE THE OTHER WORKS
def csv_to_yaml_old(csv_content, delimiter=';'):
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

def csv_to_yaml(csv_content, delimiter=';'):
    csv_reader = csv.DictReader(csv_content.splitlines(), delimiter=delimiter)
    yaml_data = {'sheets': []}

    for row in csv_reader:
        if not row['sheet'].strip():  # Skip rows with blank sheet names
            continue

        sheet_name = row['sheet'].strip().lower()  # Normalize sheet names
        
        # Find or create the sheet structure
        sheet_structure = next((item for item in yaml_data['sheets'] if item['name'] == sheet_name), None)
        if sheet_structure is None:
            print ("Creating sheet structure")
            sheet_structure = {
                'name': sheet_name,
                'color': row.get('sheet_color', 'FFFFFF'),  # Default color if not specified
                'is_optional': row['sheet_is_optional'].lower() == 'true',
                'responsibility': row['responsibility'],
                'columns': []
            }
            yaml_data['sheets'].append(sheet_structure)
        else:
            print ("Found sheet structure")
        
        # Prepare column details, handling "na" or missing validation info
        column_details = {key.replace("column_", "", 1): (value if value.lower() != 'na' else None) for key, value in row.items() if key.startswith('column_')}
        sheet_structure['columns'].append(column_details)

    return yaml.dump(yaml_data, sort_keys=False, default_flow_style=False, allow_unicode=True)

# Function to convert YAML string to an Excel file and return its path
# TODO DELETE ONCE THE OTHER WORKS
def yaml_to_excel_old(yaml_str):
    data = yaml.safe_load(yaml_str)
    temp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
    excel_file_path = temp_file.name
    temp_file.close()
    
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        for sheet in data['sheets']:
            sheet_name = sheet['name'][:31].strip()  # Ensure valid Excel sheet name
            df = pd.DataFrame(columns=[col['name_internal'] for col in sheet['columns']])
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Apply sheet tab color
            if 'color' in sheet:
                color_code = sheet['color'].lstrip('#')
                apply_sheet_colors(writer, sheet_name, color_code)

    return excel_file_path

def apply_conditional_formatting(worksheet, column_letter):
    """
    Applies conditional formatting to mark cells in red if they're empty.

    Parameters:
    - worksheet: The openpyxl worksheet object to which the conditional formatting will be applied.
    - column_letter: The letter of the column to apply the conditional formatting to.
    """
    red_fill = PatternFill(start_color="FFEE1111", end_color="FFEE1111", fill_type="solid")
    # Example rule: mark cells red if they're blank (empty)
    worksheet.conditional_formatting.add(f'{column_letter}2:{column_letter}1048576',
                                         CellIsRule(operator='equal', formula=['""'], stopIfTrue=True, fill=red_fill))
    
#THIS WORKS
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

# Extend your existing upload parser configuration 
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Excel file to validate')
@ns.route("/validate-excel")
@ns.expect(upload_parser)
class ValidateExcel(Resource):
    @ns.doc("validate_excel_data")
    def post(self):
        args = upload_parser.parse_args()
        excel_file = args['file']
        
        # Temporary saving file to read it
        temp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
        excel_file.save(temp_file.name)

        # Process the file for validation
        dfs = read_excel_to_dataframes(temp_file.name)
        print (dfs)
        data_dicts = convert_dfs_to_data_dicts(dfs)
        valid_data, errors = validate_data_with_pydantic(data_dicts)

        # Cleanup the temporary file
        os.remove(temp_file.name)

        if errors:
            # Return validation errors
            return {'validation_errors': errors}, 400
        else:
            # Placeholder for further processing of valid_data, such as database ingestion
            return {'message': 'Excel data is valid!', 'valid_data': [data.dict() for data in valid_data]}, 200