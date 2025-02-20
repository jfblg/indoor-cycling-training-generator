import datetime
import os

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

OUTPUT_DIRECTORY = "output"


def ensure_output_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_workout_step(step_duration_ms, watts_offset):
    step = WorkoutStepMessage()
    step.workout_step_name = "Step 1"
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


def create_workout(workout_name, workout_steps):
    file_id_message = FileIdMessage()
    file_id_message.type = FileType.WORKOUT
    file_id_message.manufacturer = Manufacturer.GARMIN.value
    file_id_message.product = 0
    file_id_message.time_created = round(datetime.datetime.now().timestamp() * 1000)
    file_id_message.serial_number = 0x12345678

    workout_message = WorkoutMessage()
    workout_message.workout_name = workout_name
    workout_message.sport = Sport.CYCLING
    workout_message.sub_sport = SubSport.INDOOR_CYCLING
    workout_message.num_valid_steps = len(workout_steps)

    # We set autoDefine to true, so that the builder creates the required
    # Definition Messages for us.
    builder = FitFileBuilder(auto_define=True, min_string_size=50)
    builder.add(file_id_message)
    builder.add(workout_message)
    builder.add_all(workout_steps)

    fit_file = builder.build()
    out_filename = f"{workout_name}_workout.fit"
    ensure_output_directory_exists(OUTPUT_DIRECTORY)
    out_path = os.path.join(OUTPUT_DIRECTORY, out_filename)
    print(f"generating: {out_path}")
    fit_file.to_file(out_path)
