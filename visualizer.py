import os
import glob
import plotly.graph_objects as go
from flask import Flask, render_template
from main import parse_yaml, time_to_milliseconds, ftp_percent_to_watts

app = Flask(__name__)

WORKOUTS_DIR = "workouts"

def create_workout_graph(workout, ftp):
    x_values = []
    y_values = []
    current_time_ms = 0

    for step in workout["steps"]:
        duration_ms = time_to_milliseconds(step["time"])
        # Handle cases where ftp_percentage might be missing or invalid
        ftp_percentage = step.get("ftp_percentage", "0%")
        try:
            power = ftp_percent_to_watts(ftp_percentage, ftp)
        except (ValueError, AttributeError):
            power = 0 # Default to 0 if conversion fails

        x_values.append(current_time_ms / 1000 / 60)  # Convert to minutes
        y_values.append(power)
        current_time_ms += duration_ms
        x_values.append(current_time_ms / 1000 / 60)  # Convert to minutes
        y_values.append(power)

    fig = go.Figure(
        data=go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            line=dict(shape="hv"),
            name=workout["name"],
        )
    )

    fig.update_layout(
        title=workout["name"],
        xaxis_title="Duration (minutes)",
        yaxis_title="Power (watts)",
    )
    return fig.to_html(full_html=False)

@app.route("/")
def index():
    workout_files = glob.glob(os.path.join(WORKOUTS_DIR, "*.yaml"))
    workout_groups = []

    for file_path in workout_files:
        workout_data = parse_yaml(file_path)
        if not workout_data or "workouts" not in workout_data:
            continue

        source_file = os.path.basename(file_path)
        ftp = workout_data.get("ftp", 200)  # Default FTP
        graphs = []

        for workout in workout_data["workouts"]:
            try:
                graph_html = create_workout_graph(workout, ftp)
                graphs.append(graph_html)
            except Exception as e:
                print(f"Could not generate graph for {workout.get('name', 'Unnamed')} in {source_file}: {e}")
        
        if graphs:
            workout_groups.append({"source": source_file, "graphs": graphs})

    return render_template("index.html", workout_groups=workout_groups)

if __name__ == "__main__":
    app.run(debug=True, port=5001)