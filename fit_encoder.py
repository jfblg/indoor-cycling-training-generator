import datetime

from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.workout_message import WorkoutMessage
from fit_tool.profile.messages.workout_step_message import WorkoutStepMessage
from fit_tool.profile.profile_type import Sport, SubSport, Intensity, WorkoutStepDuration, WorkoutStepTarget, Manufacturer, FileType

NAME = "dev16"

def main():
    file_id_message = FileIdMessage()
    file_id_message.type = FileType.WORKOUT
    file_id_message.manufacturer = Manufacturer.GARMIN.value
    file_id_message.product = 0
    file_id_message.time_created = round(datetime.datetime.now().timestamp() * 1000)
    file_id_message.serial_number = 0x12345678

    workout_steps = []

    step = WorkoutStepMessage()
    step.workout_step_name = 'Step 1'
    step.intensity = Intensity.OTHER
    step.duration_type = WorkoutStepDuration.TIME
    step.duration_time = 700000.0 # 10 mminutes
    step.target_type = WorkoutStepTarget.POWER_3S
    step.target_value = 0
    step.custom_target_value_low = 0
    step.custom_target_value_high = 0
    step.custom_target_power_low = 1100 # must be offset by 1000 (1200 = 200 Watts)
    step.custom_target_power_high = 1100
    workout_steps.append(step)

    step = WorkoutStepMessage()
    step.workout_step_name = 'Step 2'
    step.intensity = Intensity.OTHER
    step.duration_type = WorkoutStepDuration.TIME
    step.duration_time = 700000.0 # 10 mminutes
    step.target_type = WorkoutStepTarget.POWER_3S
    step.target_value = 0 # must be set to 0
    step.custom_target_value_low = 0 # must be set to 0
    step.custom_target_value_high = 0 # must be set to 0
    step.custom_target_power_low = 1200 # must be offset by 1000 (1200 = 200 Watts)
    step.custom_target_power_high = 1200
    workout_steps.append(step)

    step = WorkoutStepMessage()
    step.workout_step_name = 'Step 3'
    step.intensity = Intensity.OTHER
    step.duration_type = WorkoutStepDuration.TIME
    step.duration_time = 700000.0 # 10 mminutes
    step.target_type = WorkoutStepTarget.POWER_3S
    step.target_value = 0
    step.custom_target_value_low = 0
    step.custom_target_value_high = 0
    step.custom_target_power_low = 1400 # must be offset by 1000 (1200 = 200 Watts)
    step.custom_target_power_high = 1400
    workout_steps.append(step)

    workout_message = WorkoutMessage()
    workout_message.workout_name= NAME
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

    out_path = f'{NAME}_workout.fit'
    fit_file.to_file(out_path)


if __name__ == "__main__":
    main()
