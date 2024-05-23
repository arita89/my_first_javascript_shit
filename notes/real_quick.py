import requests
import os

# Define the FastAPI endpoint
url = "http://127.0.0.1:8081/processfile/"

# Define the input file path and output folder
input_file_path = "path/to/your/input_file.xlsx"
output_folder = "path/to/save/processed_files/"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Upload the file and get the processed file
with open(input_file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the original file name
        original_filename = os.path.basename(input_file_path)
        # Define the output file path
        output_file_path = os.path.join(output_folder, f"validated_{original_filename}")

        # Save the processed file
        with open(output_file_path, "wb") as output_file:
            output_file.write(response.content)
        
        print(f"Processed file saved to {output_file_path}")
    else:
        print(f"Failed to process file. Status code: {response.status_code}")
        print(response.text)
