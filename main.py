import yaml

from fit_encoder import create_workout, create_workout_step


def parse_yaml(file_path):
    """Parses a YAML file and returns a dictionary."""
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None
    except FileNotFoundError:
        print("File not found.")
        return None


# TODO unittest
def time_to_milliseconds(time_str):
    """Converts time in 'MM:SS' format to milliseconds."""
    try:
        minutes, seconds = map(int, time_str.split(":"))
        return (minutes * 60 + seconds) * 1000
    except ValueError:
        print("Invalid time format. Expected 'MM:SS'.")
        return None


# TODO unittest
def ftp_percent_to_watts(ftp_percentage, ftp):
    """Converts % FTP value to absolute watts."""
    if not ftp_percentage.endswith("%"):
        raise ValueError("Invalid input: FTP percentage must contain '%'")
    try:
        percentage = float(ftp_percentage.strip("%")) / 100
        return round(percentage * ftp)
    except ValueError:
        print("Invalid FTP percentage format.")
        return None


# TODO unittest
def prepare_data_for_fit_encoding(parsed_data):
    """Converts percentage watts and time. Remove unused."""
    converted_data = []  # list of workouts
    ftp = parsed_data["ftp"]
    for workout in parsed_data["workouts"]:
        converted_workout = {"name": "", "steps": []}
        converted_workout["name"] = workout["name"]
        for step in workout["steps"]:
            converted_step = {}
            converted_step["time_ms"] = time_to_milliseconds(step["time"])
            converted_step["watts_offset"] = (
                ftp_percent_to_watts(step["ftp_percentage"], ftp) + 1000
            )  # Offset of 1000 required for custom Watts in .fit file
            converted_workout["steps"].append(converted_step)
        converted_data.append(converted_workout)
    return converted_data


def create_workouts(converted_data):
    for workout in converted_data:
        workout_steps = []
        for step in workout["steps"]:
            workout_steps.append(
                create_workout_step(
                    step_duration_ms=step["time_ms"], watts_offset=step["watts_offset"]
                )
            )
        create_workout(workout_name=workout["name"], workout_steps=workout_steps)


# TODO output to the correct directory

# Example usage
file_path = "training_data.yaml"
parsed_data = parse_yaml(file_path)
# print(parsed_data)
converted_data = prepare_data_for_fit_encoding(parsed_data)
create_workouts(converted_data=converted_data)
