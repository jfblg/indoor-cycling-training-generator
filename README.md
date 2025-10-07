# Indoor Cycling Training Generator

> [!WARNING]
> **Project Status: Under Development**
> This project is currently under active development. The code should be considered unstable, and breaking changes may be introduced.

This project allows you to generate indoor cycling training plans from YAML files and visualize the workouts.

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