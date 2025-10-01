# Indoor Cycling Training Generator

This project allows you to generate indoor cycling training plans from YAML files and visualize the workouts.

## Setup

This project uses `uv` for environment and package management.

1.  **Install `uv`:**
    If you don't have `uv` installed, you can install it with pip:
    ```bash
    pip install uv
    ```

2.  **Create a virtual environment and install dependencies:**
    Run the following commands in your terminal:
    ```bash
    # Create a virtual environment
    uv venv

    # Activate the environment
    source .venv/bin/activate

    # Install the required packages
    uv pip install -r requirements.txt
    ```

## Usage

### Generating `.fit` Workout Files

To generate the `.fit` files for your cycling computer, run the `main.py` script:

```bash
python main.py
```

The generated workout files will be saved in the `output/` directory.

### Visualizing Workouts

To see a visual representation of the workouts, you can run the web-based visualizer:

```bash
python visualizer.py
```

This will start a local web server. Open your web browser and go to the following URL to see the graphs:

[http://127.0.0.1:5001](http://127.0.0.1:5001)
