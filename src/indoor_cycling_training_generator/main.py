import os
import yaml
import copy
import datetime
import argparse
import sys
from typing import List, Dict, Any, Optional
from importlib import resources

from .fit_encoder import create_workout, create_workout_step

# --- Constants ---
FIT_POWER_OFFSET = 1000  # Offset required for custom Watts in .fit files


# --- File Operations ---

def parse_yaml(file_path: str) -> Optional[Dict[str, Any]]:
    """Parses a YAML file and returns its content as a dictionary."""
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {file_path}: {e}")
        return None


# --- Data Conversion Utilities ---

def time_to_milliseconds(time_str: str) -> Optional[int]:
    """Converts time in 'MM:SS' format to milliseconds."""
    try:
        minutes, seconds = map(int, time_str.split(":"))
        return (minutes * 60 + seconds) * 1000
    except (ValueError, AttributeError):
        print(f"Invalid time format '{time_str}'. Expected 'MM:SS'.")
        return None

def ftp_percent_to_watts(ftp_percentage: str, ftp: int) -> Optional[int]:
    """Converts a percentage of FTP to an absolute power value in watts."""
    if not isinstance(ftp_percentage, str) or not ftp_percentage.endswith("%"):
        raise ValueError("Invalid input: FTP percentage must be a string ending with '%'")
    try:
        percentage = float(ftp_percentage.strip("%")) / 100
        return round(percentage * ftp)
    except ValueError:
        print(f"Invalid FTP percentage format: '{ftp_percentage}'")
        return None


# --- Core Workout Processing Logic ---

def prepare_workout_steps_for_fit(workout: Dict[str, Any], ftp: int) -> List[Dict[str, Any]]:
    """Prepares the steps of a single workout for FIT encoding."""
    prepared_steps = []
    for step in workout["steps"]:
        time_ms = time_to_milliseconds(step["time"])
        watts = ftp_percent_to_watts(step["ftp_percentage"], ftp)

        if time_ms is None or watts is None:
            print(f"Skipping invalid step in workout '{workout['name']}'")
            continue

        prepared_steps.append({
            "time_ms": time_ms,
            "watts_offset": watts + FIT_POWER_OFFSET
        })
    return prepared_steps

def encode_workouts_to_fit_files(workouts: List[Dict[str, Any]], ftp: int, output_dir: str):
    """Converts a list of workouts to .fit files, ensuring unique timestamps."""
    print(f"Generating workouts for FTP: {ftp}")
    start_time = datetime.datetime.now()
    for i, workout in enumerate(workouts):
        fit_steps = []
        prepared_steps = prepare_workout_steps_for_fit(workout, ftp)
        for step_data in prepared_steps:
            fit_steps.append(
                create_workout_step(
                    step_duration_ms=step_data["time_ms"],
                    watts_offset=step_data["watts_offset"]
                )
            )
        
        creation_time = start_time + datetime.timedelta(seconds=i)
        create_workout(
            workout_name=workout["name"], 
            workout_steps=fit_steps, 
            creation_time=creation_time,
            output_dir=output_dir
        )


# --- Training Plan Logic ---

def load_workouts_by_name(path: str) -> Dict[str, Any]:
    """Loads workouts from a YAML file and maps them by name for quick lookup."""
    workout_data = parse_yaml(path)
    if not workout_data or "workouts" not in workout_data:
        return {}
    return {workout["name"]: workout for workout in workout_data["workouts"]}

def build_workouts_from_plan(
    training_plan: Dict[str, Any], 
    available_workouts: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Builds a list of workout objects based on the training plan, handling duplicates."""
    plan_workouts = []
    for workout_name in training_plan.get("workouts", []):
        if workout_name in available_workouts:
            plan_workouts.append(copy.deepcopy(available_workouts[workout_name]))
        else:
            print(f"Warning: Workout '{workout_name}' from training plan not found in available workouts.")
    return plan_workouts

def rename_plan_workouts(
    plan_workouts: List[Dict[str, Any]], 
    training_plan: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Renames workouts according to the training plan's configuration."""
    prefix = training_plan.get("workout_file_prefix", "w")
    use_rename = training_plan.get("workout_rename_enabled", False)
    use_indexing = training_plan.get("workout_indexing_enabled", True)

    renamed_workouts = []
    for i, workout in enumerate(plan_workouts):
        original_name = workout["name"]
        if use_rename:
            new_name = f"{prefix}_{i+1}" if use_indexing else prefix
        else:
            safe_original_name = original_name.replace(" ", "_").lower()
            new_name = f"{prefix}_{i+1}_{safe_original_name}" if use_indexing else f"{prefix}_{safe_original_name}"
        
        workout["name"] = new_name
        renamed_workouts.append(workout)
    return renamed_workouts

# --- Main Execution ---

def main():
    """Main function to generate workouts from a training plan."""
    parser = argparse.ArgumentParser(description="Indoor Cycling Training Generator")
    parser.add_argument("--list-plans", action="store_true", help="List all available training plans.")
    parser.add_argument("--list-workouts", action="store_true", help="List all available workouts.")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate workout files from a plan.")
    gen_parser.add_argument("-p", "--plan", required=True, help="Path to the training plan YAML file.")
    gen_parser.add_argument("--ftp", type=int, help="Override the FTP value in the training plan.")
    gen_parser.add_argument("-o", "--output-dir", default="output", help="Directory to save the generated .fit files.")

    # List command
    list_parser = subparsers.add_parser("list", help="Display information about a specific training plan.")
    list_parser.add_argument("plan_file", help="The training plan file to inspect (e.g., ftp_increase_1month/week1.yaml)")

    # Default to 'generate' if no command is given, but a plan is specified
    args = parser.parse_args()
    if args.command is None and any(arg in sys.argv for arg in ['--plan', '-p']):
        # Manually re-parse with 'generate' as the command
        args = parser.parse_args(['generate'] + sys.argv[1:])

    base_path = resources.files("indoor_cycling_training_generator")
    workouts_path = base_path / "workouts" / "workouts.yaml"
    plans_path = base_path / "training_plans"

    # --- Handle Utility Arguments ---
    if args.list_plans:
        print("Available training plans:")
        for root, _, files in os.walk(plans_path):
            for file in files:
                if file.endswith(".yaml"):
                    print(f"  - {os.path.relpath(os.path.join(root, file), plans_path)}")
        return

    if args.list_workouts:
        available_workouts = load_workouts_by_name(str(workouts_path))
        if not available_workouts:
            print("No available workouts found.")
            return
        print("Available workouts:")
        for name in sorted(available_workouts.keys()):
            print(f"  - {name}")
        return

    # --- Handle Subcommands ---
    if args.command == "list":
        plan_path = plans_path / args.plan_file
        if not plan_path.exists():
            print(f"Error: Training plan not found at '{args.plan_file}'")
            return
        
        plan_data = parse_yaml(str(plan_path))
        if not plan_data:
            return

        print(f"Details for training plan: {args.plan_file}")
        print(f"  Path: {plan_path}")
        print(f"  Configured FTP: {plan_data.get('ftp', 'Not set')}")
        print("  Workouts:")
        for workout in plan_data.get("workouts", []):
            print(f"    - {workout}")

    elif args.command == "generate":
        training_plan_path = args.plan
        if not os.path.exists(training_plan_path):
            maybe_path = plans_path / training_plan_path
            if maybe_path.exists():
                training_plan_path = str(maybe_path)
            else:
                print(f"Error: Training plan not found at '{args.plan}'")
                return

        available_workouts = load_workouts_by_name(str(workouts_path))
        if not available_workouts:
            print("No available workouts found. Exiting.")
            return

        training_plan = parse_yaml(training_plan_path)
        if not training_plan:
            print("Could not parse training plan. Exiting.")
            return

        plan_workouts = build_workouts_from_plan(training_plan, available_workouts)
        renamed_workouts = rename_plan_workouts(plan_workouts, training_plan)

        plan_ftp = args.ftp if args.ftp is not None else training_plan.get("ftp")
        if not plan_ftp:
            print("FTP not specified in the training plan or with --ftp flag. Exiting.")
            return

        encode_workouts_to_fit_files(renamed_workouts, plan_ftp, args.output_dir)
        print(f"Workouts generated in the '{args.output_dir}' directory.")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()