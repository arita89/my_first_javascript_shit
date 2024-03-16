from flask import Flask, send_file, request, after_this_request
from flask_restx import Api, Resource, fields, reqparse
from flask_cors import CORS

from tempfile import NamedTemporaryFile
import shutil

from werkzeug.datastructures import FileStorage
import yaml
import pandas as pd
import os

app = Flask(__name__)
CORS(app)
api = Api(
    app, version="1.0", title="API Docs", description="A simple API documentation"
)


upload_parser = reqparse.RequestParser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)

# Define the API namespace
ns = api.namespace("yaml2excel", description="List of all endpoints")


# Function to convert YAML to Excel
def yaml_to_excel(yaml_file, excel_file):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

        # Create a temporary file
        temp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
        excel_file_path = temp_file.name
        temp_file.close()  # Close the file so pandas can write to it

        # Use pandas to convert the dictionary to an Excel file
        with pd.ExcelWriter(excel_file_path) as writer:
            for category, items in data.items():
                df = pd.DataFrame(items)
                df.to_excel(writer, sheet_name=category, index=False)

        # Ensure the temporary file is deleted after the request
        @after_this_request
        def remove_file(response):
            os.remove(excel_file_path)
            return response

        # Send the file
        return send_file(excel_file_path, as_attachment=True, download_name="data.xlsx")


@ns.route("/generate-excel")
@ns.expect(upload_parser)
class GenerateExcel(Resource):
    @ns.doc("generate_excel")
    def post(self):
        args = upload_parser.parse_args()
        yaml_file = args["file"]  # This is a FileStorage instance

        # Convert YAML content to Python dictionary
        data = yaml.safe_load(yaml_file)

        # Use a temporary file to avoid saving the Excel file locally
        with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            with pd.ExcelWriter(tmp.name) as writer:
                for category, items in data.items():
                    df = pd.DataFrame(items)
                    df.to_excel(writer, sheet_name=category, index=False)
            # No need to manually delete, Python cleans up the temporary file

            # Rewind the file to send it correctly
            tmp.seek(0)
            return send_file(
                tmp.name, as_attachment=True, download_name=f"{yaml_file.filename}.xlsx"
            )


# Regular Flask route for the home page
@app.route("/")
def index():
    return "Welcome to the first Shitty Flask app!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
