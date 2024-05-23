
from openpyxl import load_workbook
from io import BytesIO

def load_excel_file(file_bytes):
    try:
        wb = load_workbook(filename=BytesIO(file_bytes))
        return wb
    except KeyError as e:
        print(f"Error: {e}")
        # Handle the specific case where drawing1.xml is missing
        if "cl/drawings/drawing1.xml" in str(e):
            print("The file appears to be missing a drawing component.")
        return None

# Example usage with your BytesIO transformation
file_bytes = your_bytes_io_transformation_function(your_file)
workbook = load_excel_file(file_bytes)
