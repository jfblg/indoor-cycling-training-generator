import click

"""
This module provides a command-line interface (CLI) for generating workouts for an indoor trainer.

Functions:
    cli: The main entry point for the CLI application.
    
    
Commands:

from_training_plan:
    Generate workouts from a training plan.
    
    Usage:
        from_training_plan [OPTIONS] TRAINING_PLAN WORKOUT_DATA
        
    Arguments:
        FTP: The FTP to generate workouts for.  Overwrites the FTP from the workout data.
        TRAINING_PLAN: The training plan to generate workouts from.
        WORKOUT_DATA: The workout data to use for generating workouts.
        OUTPUT_DIR: The output directory to write the generated workouts to.
        
    Options:
        --ftp INTEGER: The FTP to generate workouts for. Overwrites the FTP from the workout data.
        --training-plan-file TEXT: The name of the training plan to generate workouts from.
        --output-dir TEXT: The output directory to write the generated workouts to. Default: local directory.
        --help: Show this message and exit.
        
from_workout_data:
    Generate workouts from workout data.
    
    Usage:
        from_workout_data [OPTIONS] WORKOUT_DATA
        
    Arguments:
        FTP: The FTP to generate workouts for. Overwrites the FTP from the workout data.
        WORKOUT_DATA: The workout data to use for generating workouts.
        OUTPUT_DIR: The output directory to write the generated workouts to.
        
    Options:
        --ftp INTEGER: The FTP to generate workouts for. Overwrites the FTP from the workout data.
        --workout-name TEXT: The name of the workout to generate. Mutually exclusive with --all-workouts.
        --all-workouts: Generate all workouts from the workout data. Mutually exclusive with --workout-name.
        --output-dir TEXT: The output directory to write the generated workouts to. Default: local directory.
        --help: Show this message and exit.
    
"""


@click.group()
def cli():
    """Workout generator for indoor trainer."""
    pass
