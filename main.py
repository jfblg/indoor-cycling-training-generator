import os

import yaml

from fit_encoder import create_workout, create_workout_step

WORKOUTS_DIR = "workouts"
WORKOUTS_FILE = "workouts.yaml"
TRAINING_PLANS_DIR = "training_plans/ftp_increase_1month"


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


def encode_workouts_to_fit_files(converted_data):
    for workout in converted_data:
        workout_steps = []
        for step in workout["steps"]:
            workout_steps.append(
                create_workout_step(
                    step_duration_ms=step["time_ms"], watts_offset=step["watts_offset"]
                )
            )
        create_workout(workout_name=workout["name"], workout_steps=workout_steps)


# TODO implement parser for training plans
# TODO generate training plan based on workouts and data from training plan. output .fit files for each workout with the names "w[number]_d[1].fit"
# TODO keep functionality to generate individual workouts from yaml file


# TODO unittest
# FIX add input validation - handling of missing keys
def generate_filenames_for_training_plan(training_plan):
    workout_file_prefix = training_plan["workout_file_prefix"]
    should_rename = training_plan["workout_rename_enabled"]
    should_index = training_plan["workout_indexing_enabled"]
    training_plan["workout_filenames"] = []
    for index, workout in enumerate(training_plan["workouts"]):
        workout_name = workout.replace(" ", "_").lower()
        filename = f"{workout_file_prefix}"
        if should_index:
            filename = f"{filename}_{index}"
        if not should_rename:
            filename = f"{filename}_{workout_name}"

        training_plan["workout_filenames"].append(filename)
    return training_plan


def filter_out_workouts(workout_data, training_plan):
    workouts = workout_data["workouts"]
    workouts_filtered = []
    for workout in workouts:
        if workout["name"] in training_plan["workouts"]:
            workouts_filtered.append(workout)

    if len(workouts_filtered) == 0:
        print("No workouts found in training plan.")
    if len(workouts_filtered) < len(training_plan["workouts"]):
        print("Some workouts not found in training plan.")
        print("Workouts found:")
        for workout in workouts_filtered:
            print(workout["name"])

    return workouts_filtered


def rename_workouts_based_on_training_plan_configuration(workouts, training_plan):
    for workout in workouts:
        workout_name = workout["name"]
        workout_index = training_plan["workouts"].index(workout_name)
        workout_filename = training_plan["workout_filenames"][workout_index]
        workout["name"] = workout_filename
    return workouts


def create_workouts_from_training_plan_for_fit_encoder(training_plan, workouts):
    training_plan_ftp = training_plan["ftp"]
    print(f"Workouts generated for FTP: {training_plan_ftp}")
    workouts_plus_ftp = {
        "ftp": training_plan_ftp,
        "workouts": workouts,
    }
    return workouts_plus_ftp


# TODO bug: if the same workout is used multiple times in the training plan, only the first occurrence will be generated as fit file
# TODO bug: if I copy multiple files to Garmin edge, only first workout appears on the device

if __name__ == "__main__":
    workouts_path = os.path.join(WORKOUTS_DIR, WORKOUTS_FILE)
    workout_data = parse_yaml(workouts_path)
    # TMP disabled
    # converted_data = prepare_data_for_fit_encoding(parsed_data)
    # encode_workouts_to_fit_files(converted_data=converted_data)

    training_plan = os.path.join(TRAINING_PLANS_DIR, "week1.yaml")
    # print(parse_yaml(training_plan))
    training_plan_with_filenames = generate_filenames_for_training_plan(
        parse_yaml(training_plan)
    )
    workouts_filtered = filter_out_workouts(workout_data, training_plan_with_filenames)
    workouts_renamed = rename_workouts_based_on_training_plan_configuration(
        workouts_filtered, training_plan_with_filenames
    )
    workouts_plus_ftp = create_workouts_from_training_plan_for_fit_encoder(
        training_plan_with_filenames, workouts_renamed
    )
    workouts_converted = prepare_data_for_fit_encoding(workouts_plus_ftp)
    encode_workouts_to_fit_files(converted_data=workouts_converted)

    print("Done.")
