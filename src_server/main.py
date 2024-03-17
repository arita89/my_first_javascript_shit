from flask import Flask, send_file, request, after_this_request
from flask_restx import Api, Resource, fields, reqparse
from flask_cors import CORS

from tempfile import NamedTemporaryFile
import shutil

from werkzeug.datastructures import FileStorage
import yaml
import pandas as pd
import os

import services
import utils

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



# Regular Flask route for the home page
@app.route("/")
def index():
    return "Welcome to the first Shitty Flask app!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
