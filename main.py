import yaml

def parse_yaml(file_path):
    """Parses a YAML file and returns a dictionary."""
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None
    except FileNotFoundError:
        print("File not found.")
        return None

# TODO function which converts time in 4:30 to miliseconds
# TODO function which converts % FTP value to absolute value
# TODO rework fit_encoder, so that it can be efficiently called to create list of workout steps
# TODO output to the correct directory

# Example usage
file_path = "training_data.yaml"
parsed_data = parse_yaml(file_path)
print(parsed_data)
