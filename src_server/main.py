from flask import Flask, send_file, request
from flask_restx import Api, Resource, fields, reqparse
from flask_cors import CORS

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

    with pd.ExcelWriter(excel_file) as writer:
        for category, items in data.items():
            df = pd.DataFrame(items)
            df.to_excel(writer, sheet_name=category, index=False)


@ns.route("/generate-excel")
@ns.expect(upload_parser)
class GenerateExcel(Resource):
    @ns.doc("generate_excel")
    def post(self):
        args = upload_parser.parse_args()
        yaml_file = args["file"]  # This is a FileStorage instance
        filename_wo_ext = os.path.splitext(yaml_file.filename)[
            0
        ]  # Extract the filename without extension
        excel_file = f"{filename_wo_ext}.xlsx"  # Use the original name with .xlsx

        # Read the content of the YAML file
        yaml_content = yaml_file.read()

        # Convert YAML content to Python dictionary
        data = yaml.safe_load(yaml_content)

        # Use pandas to convert the dictionary to an Excel file
        with pd.ExcelWriter(excel_file) as writer:
            for category, items in data.items():
                df = pd.DataFrame(items)
                df.to_excel(writer, sheet_name=category, index=False)

        return send_file(
            excel_file, as_attachment=True, download_name=f"{filename_wo_ext}.xlsx"
        )


# Regular Flask route for the home page
@app.route("/")
def index():
    return "Welcome to the first Shitty Flask app!"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
