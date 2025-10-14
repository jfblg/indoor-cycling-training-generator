# Indoor Cycling Training Generator

> [!WARNING]
> **Project Status: Under Development**
> This project is currently under active development. The code should be considered unstable, and breaking changes may be introduced.

This project allows you to generate indoor cycling training plans from YAML files and visualize the workouts.

## Origin story

This project is driven by my personal passion for cycling and my background in development. It began two years ago when I invested in a smart bike trainer to elevate my indoor training.

Initially, my training lacked structure. I soon realized the benefits of a planned approach and subscribed to a service like TrainerRoad. This platform is excellent; it generates detailed training plans tailored to specific goals, and crucially, it adapts based on user feedback. For instance, if you report sickness or fatigue, the service intelligently skips sessions or adjusts the intensity of future workouts.

While the targeted training was highly valuable, adherence to the rigid schedule proved challenging due to external circumstances. As a result, I cancelled my subscription.

However, the desire for structured training remained. I realized that I was comfortable managing the plan's difficulty myself, without the need for AI assistance. Given my technical background and coding ability, I quickly concluded that creating my own structured workouts shouldn’t be overly complex.

My key piece of hardware is a Garmin Edge 830. This device is capable of pairing with a smart trainer and operating in what's known as Ergo Mode. In this mode, the Garmin Edge device dictates the exact resistance (or wattage) the smart trainer must maintain, providing a highly controlled training environment.

This project is therefore a Python-based application designed to generate the specific .fit files that the Garmin Edge device requires to execute these structured indoor training sessions, effectively allowing me to create and run my own custom training plans.

## Setup

This project uses `uv` for environment and package management.

1.  **Install `uv`:**
    If you don't have `uv` installed, you can install it with pip:
    ```bash
    pip install uv
    ```

2.  **Create a virtual environment and install dependencies:**
    Run the following commands in your terminal to create a virtual environment and install the project in "editable" mode with all development dependencies.
    ```bash
    # Create a virtual environment
    uv venv

    # Activate the environment (you must do this in every new terminal session)
    source .venv/bin/activate

    # Install the project and its dependencies
    uv pip install -e ".[dev]"
    ```

## Usage

Once the project is installed and your virtual environment is activated, you can use the following commands from any directory.

### Generating `.fit` Workout Files

To generate the `.fit` files for your cycling computer, run the `indoor-cycling-generator` command:

```bash
indoor-cycling-generator
```

The generated workout files will be saved in an `output/` directory in your current location.

### Visualizing Workouts

To see a visual representation of the workouts, run the web-based visualizer:

```bash
indoor-cycling-visualizer
```

This will start a local web server. Open your web browser and go to the following URL to see the graphs:

[http://127.0.0.1:5001](http://127.0.0.1:5001)
