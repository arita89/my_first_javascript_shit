from flask import Flask, send_file, request, after_this_request, jsonify
from flask_restx import Api, Resource, reqparse
from flask_cors import CORS

from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile

from werkzeug.datastructures import FileStorage
import os

from openpyxl import load_workbook
from openpyxl.worksheet.protection import SheetProtection
from dotenv import load_dotenv

import services
import utils
from models.create_models_from_csv import generate_pydantic_model
from validation_pre_ingestion import *

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(
    app, version="1.0", title="API Docs", description="A simple API documentation"
)


upload_parser = reqparse.RequestParser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)


## TRANSFORMATION ENDPOINTS
# Define the API namespace
ns = api.namespace("files_transformations", description="here all the endpoints that take a file in format x and return a format y or transformation of the same.")

@ns.route("/csv-to-yaml")
@ns.expect(upload_parser)
class CSVToYAML(Resource):
    @ns.doc("convert_csv_to_yaml")
    def post(self):
        args = upload_parser.parse_args()
        csv_file = args['file']
        original_filename = csv_file.filename.rsplit('.', 1)[0]  # Get the filename without extension
        filename = f"{original_filename}_csv_to_yaml"
        csv_content = csv_file.read().decode('utf-8-sig')
        yaml_content = services.csv_to_yaml(csv_content)
        yaml_filename = utils.generate_file_name(filename, 'yaml')  # Use the original filename to create the new filename
        
        # Generate a temporary file for the YAML
        temp_yaml_file = NamedTemporaryFile(delete=False, suffix=".yaml")
        with open(temp_yaml_file.name, 'w') as file:
            file.write(yaml_content)
        
        @after_this_request
        def cleanup(response):
            os.remove(temp_yaml_file.name)
            return response

        return send_file(temp_yaml_file.name, as_attachment=True, download_name=yaml_filename)

@ns.route("/yaml-to-excel")
@ns.expect(upload_parser)
class YAMLToExcel(Resource):
    @ns.doc("convert_yaml_to_excel")
    def post(self):
        args = upload_parser.parse_args()
        yaml_file = args['file']
        original_filename = yaml_file.filename.rsplit('.', 1)[0]  # Get the filename without extension
        filename = f"{original_filename}_yaml_to_excel"
        yaml_content = yaml_file.read().decode('utf-8')
        excel_filename = utils.generate_file_name(filename, 'xlsx')  # Use the original filename to create the new filename
        
        excel_file_path = services.yaml_to_excel(yaml_content)

        @after_this_request
        def cleanup(response):
            os.remove(excel_file_path)
            return response

        return send_file(excel_file_path, as_attachment=True, download_name=excel_filename)


@ns.route("/csv-to-pydantic-model")
@ns.expect(upload_parser)
class CSVToPydanticModel(Resource):
    @ns.doc("convert_csv_to_pydantic_model")
    def post(self):
        args = upload_parser.parse_args()
        csv_file = args['file']
        csv_content = csv_file.read().decode('utf-8-sig')

        # Generate Pydantic model code from CSV content
        pydantic_model_code = generate_pydantic_model(csv_content)

        # Generate a unique filename with the current datetime
        filename = utils.generate_file_name("model", "py")

        # Specify the directory where you want to save the file
        save_directory = "./models/history/"
        if not os.path.exists(save_directory):
            print ("directory not found, directory created")
            os.makedirs(save_directory)

        # Create the full path to the file
        file_path = os.path.join(save_directory, filename)

        # Save the generated Pydantic model code to the file
        with open(file_path, 'w') as model_file:
            model_file.write(pydantic_model_code)

        # Optional: Return the file or a message indicating success
        # return send_from_directory(directory=save_directory, filename=filename, as_attachment=True)
        # Or just return a success message
        return {'message': 'Pydantic models generated successfully', 'file_path': file_path}


## VALIDATION ENDPOINTS 
# Define the API namespace
ns_val = api.namespace("files_validations", description="here all the endpoints that take a file and validate it against certain preset rules (from another file or hardcoded)")

# add arguments to accept multiple files 
upload_parser_val = reqparse.RequestParser()
upload_parser_val .add_argument('excel_file', location='files', type=FileStorage, required=True, help='Excel file to validate')
upload_parser_val .add_argument('csv_file', location='files', type=FileStorage, required=True, help='CSV file with validation rules')

@ns_val.route("/validate-excel-sheets")
@ns_val.expect(upload_parser_val )
class ValidateExcelSheets(Resource):
    @ns_val .doc("validate_excel_sheets")
    def post(self):
        args = upload_parser_val .parse_args()
        excel_file = args['excel_file']
        csv_file = args['csv_file']

        # Read CSV content
        csv_content = csv_file.read().decode('utf-8-sig')
        required_sheets = get_required_sheets(csv_content)

        # Temporary saving the Excel file to read it
        temp_excel_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
        excel_file.save(temp_excel_file.name)

        missing_sheets = validate_excel_sheets(temp_excel_file.name, required_sheets)

        # Cleanup: Close and remove the temporary file
        temp_excel_file.close()
        os.unlink(temp_excel_file.name)

        if missing_sheets:
            # Return missing sheets
            return {'missing_sheets': missing_sheets}, 400
        else:
            return {'message': 'Excel contains all required sheets!'}, 200

@ns_val.route("/validate-excel-with-pydantic")
@ns_val.expect(upload_parser)
class ValidateExcelwithPydantic(Resource):
    @ns_val .doc("validate-excel-with-pydantic")
    def post(self):
        args = upload_parser.parse_args()
        excel_file = args['file']

        # Temporary saving the Excel file to read it
        temp_excel_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
        excel_file.save(temp_excel_file.name)

        data_dicts = utils.read_excel_to_data_dicts(temp_excel_file.name)
        valid_data, validation_errors = validate_data_with_pydantic(data_dicts)

        # Cleanup: Close and remove the temporary file
        temp_excel_file.close()
        os.unlink(temp_excel_file.name)

        if validation_errors:
            # Return missing sheets
            return {'validation_errors': validation_errors}, 400
        else:
            return {'message': 'valid_data!'}, 200


# Namespace for locking and hiding sheets
ns_lock =  api.namespace('lock', description='Endpoints related to locking and hiding Excel sheets')

# Parser for file uploads
upload_parser_lock = ns_lock.parser()
upload_parser_lock.add_argument('excel_file', location='files', type=FileStorage, required=True, help='Target Excel file')
upload_parser_lock.add_argument('source_file', location='files', type=FileStorage, required=True, help='Source CSV or Excel file to append')

@ns_lock.route('/upload-and-lock')
@ns_lock.expect(upload_parser_lock)
class UploadAndLock(Resource):
    @ns_lock.doc('upload_and_lock')
    def post(self):
        """attaches a source csv or excel to a target excel file, it hides it and locks it"""
        args = upload_parser_lock.parse_args()
        excel_file = args['excel_file']
        source_file = args['source_file']
        sheet_name = os.getenv('SHEET_NAME')
        password = os.getenv('SHEET_PASSWORD')

        source_suffix = os.path.splitext(source_file.filename)[1]
        # Ensure source_suffix is either .csv or .xlsx
        if source_suffix not in ['.csv', '.xlsx', '.xls']:
            return {'message': 'Unsupported source file type'}, 400

        # Save the uploaded files to temporary files
        excel_file_temp = NamedTemporaryFile(delete=False, suffix='.xlsx')
        source_file_temp = NamedTemporaryFile(delete=False, suffix=source_suffix )  # Respect the source file extension

        excel_file.save(excel_file_temp.name)
        source_file.save(source_file_temp.name)

        # Process and append the source file to the target Excel workbook
        message = services.append_to_excel_as_hidden_locked(source_file_temp.name, excel_file_temp.name, sheet_name, password)
        
        # Set up the cleanup after sending the file
        @after_this_request
        def cleanup(response):
            try:
                os.unlink(excel_file_temp.name)
                os.unlink(source_file_temp.name)
            except Exception as error:
                app.logger.error("Error removing temporary file: %s", error)
            return response
        
        # After processing, the temp_excel file contains the modified workbook
        if "Success" in message:
            # Prepare the modified Excel file for download
            return send_file(excel_file_temp.name, download_name='modified_workbook.xlsx', as_attachment=True)
        else:
            return {'message': message}

# Define the parser for unlocking hidden sheets
unlock_parser = ns_lock.parser()
unlock_parser.add_argument('excel_file', location='files', type=FileStorage, required=True, help='Excel file to process')
unlock_parser.add_argument('password', type=str, required=True, help='Password to unlock sheets')

@ns_lock.route('/unlock-hidden-sheets')
@ns_lock.expect(unlock_parser)
class UnlockHiddenSheets(Resource):
    @ns_lock.doc('unlock_hidden_sheets')
    def post(self):
        """Unlocks and reveals hidden sheets in the provided Excel workbook and returns it for download."""
        args = unlock_parser.parse_args()
        excel_file = args['excel_file']  # This is a FileStorage object
        password = args['password']

        # Create a temporary file
        temp_file = NamedTemporaryFile(delete=False, suffix='.xlsx')
        temp_path = temp_file.name
        excel_file.save(temp_path)

        # Attempt to unlock hidden sheets
        unlocked_sheets = services.unlock_hidden_sheets(temp_path, password)

        if unlocked_sheets:
            message = 'Unlocked sheets'
        else:
            message = 'No hidden sheets were unlocked or incorrect password provided'

        # Set up the cleanup after sending the file
        @after_this_request
        def cleanup(response):
            try:
                os.unlink(temp_path)
            except Exception as error:
                app.logger.error("Error removing temporary file: %s", error)
            return response

        # Return the file for download
        return send_file(temp_path, download_name='unlocked_workbook.xlsx', as_attachment=True)
        
# Regular Flask route for the home page
@app.route("/")
def index():
    return "Welcome to the first Shitty Flask app!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
