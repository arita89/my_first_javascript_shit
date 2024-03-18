from flask import Flask, send_file, request, after_this_request, jsonify
from flask_restx import Api, Resource, reqparse
from flask_cors import CORS

from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile

from werkzeug.datastructures import FileStorage
import os

import services
import utils
#from models.create_model_from_csv import generate_pydantic_model
from models.create_models_from_csv import generate_pydantic_model
from validation_pre_ingestion import read_excel_to_dataframes, dataframe_to_dicts, convert_dfs_to_data_dicts, validate_data_with_pydantic

app = Flask(__name__)
CORS(app)
api = Api(
    app, version="1.0", title="API Docs", description="A simple API documentation"
)


upload_parser = reqparse.RequestParser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)

# Define the API namespace
ns = api.namespace("yaml2excel", description="List of all endpoints")

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

# Regular Flask route for the home page
@app.route("/")
def index():
    return "Welcome to the first Shitty Flask app!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
