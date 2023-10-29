import json

# Function to read a JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Function to empty a JSON file
def empty_json_file(file_path):
    with open(file_path, 'w') as f:
        json.dump({}, f)

# Function to fill a JSON file with data
def fill_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)
