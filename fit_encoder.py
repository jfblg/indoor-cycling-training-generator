import datetime
import os
import random
from typing import List

from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.workout_message import WorkoutMessage
from fit_tool.profile.messages.workout_step_message import WorkoutStepMessage
from fit_tool.profile.profile_type import (
    FileType,
    Intensity,
    Manufacturer,
    Sport,
    SubSport,
    WorkoutStepDuration,
    WorkoutStepTarget,
)

# --- Constants ---
OUTPUT_DIRECTORY = "output"

# --- Functions ---

def ensure_output_directory_exists(directory: str) -> None:
    """Checks if the output directory exists, and creates it if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_workout_step(
    step_duration_ms: int, 
    watts_offset: int
) -> WorkoutStepMessage:
    """Creates a single workout step message for a .fit file."""
    step = WorkoutStepMessage()
    step.workout_step_name = "Step"
    step.intensity = Intensity.OTHER
    step.duration_type = WorkoutStepDuration.TIME
    step.duration_time = step_duration_ms
    step.target_type = WorkoutStepTarget.POWER_3S
    step.target_value = 0
    step.custom_target_value_low = 0
    step.custom_target_value_high = 0
    step.custom_target_power_low = watts_offset
    step.custom_target_power_high = watts_offset
    return step

def create_workout(
    workout_name: str, 
    workout_steps: List[WorkoutStepMessage], 
    creation_time: datetime.datetime
) -> None:
    """
    Creates a complete .fit workout file from a list of steps.

    Args:
        workout_name: The name of the workout.
        workout_steps: A list of `WorkoutStepMessage` objects.
        creation_time: The precise time of creation for the file ID.
    """
    # 1. Create File ID Message
    file_id_message = FileIdMessage()
    file_id_message.type = FileType.WORKOUT
    file_id_message.manufacturer = Manufacturer.GARMIN.value
    file_id_message.product = 0
    file_id_message.time_created = round(creation_time.timestamp() * 1000)
    file_id_message.serial_number = random.randint(0, 0xFFFFFFFF)

    # 2. Create Workout Message
    workout_message = WorkoutMessage()
    workout_message.workout_name = workout_name
    workout_message.sport = Sport.CYCLING
    workout_message.sub_sport = SubSport.INDOOR_CYCLING
    workout_message.num_valid_steps = len(workout_steps)

    # 3. Build the .fit file
    builder = FitFileBuilder(auto_define=True, min_string_size=50)
    builder.add(file_id_message)
    builder.add(workout_message)
    builder.add_all(workout_steps)

    fit_file = builder.build()

    # 4. Write the file to the output directory
    ensure_output_directory_exists(OUTPUT_DIRECTORY)
    out_filename = f"{workout_name}_workout.fit"
    out_path = os.path.join(OUTPUT_DIRECTORY, out_filename)
    print(f"Generating: {out_path}")
    fit_file.to_file(out_path)
