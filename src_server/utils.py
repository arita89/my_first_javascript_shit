from datetime import datetime

def generate_file_name(filename, extension):
    datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{filename}_{datetime_str}.{extension}"