import subprocess
import sys

PIPELINE_STEPS = [
    ("Install requirements", "setup_requirements.py"),
    ("Extract data", "01_extract.py"),
    ("Count comments", "02_count.py"),
    ("Create database", "03_database.py"),
    ("Ping LLM", "05_ping_llm.py"),
    ("Predict four factors", "06_prediction.py"),
    ("Create responses", "07_create_responses.py"),
    ("Extract categories", "08_categories.py"),
    ("Create visualization", "09_visualization.py"),
    ("Export dataset", "11_export.py"),
]

def run_step(name, script):
    print(f"\n{'='*60}")
    print(f"Step: {name} ({script})")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            [sys.executable, script],
            check=True,
            capture_output=False,
        )
        print(f"[SUCCESS] {name}")
    except subprocess.CalledProcessError as e:
        print(f"[FAILED] {name} - Exit code: {e.returncode}")
        raise

def main():
    print("Starting data pipeline...")

    for name, script in PIPELINE_STEPS:
        run_step(name, script)

    print(f"\n{'='*60}")
    print("Pipeline completed successfully!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
