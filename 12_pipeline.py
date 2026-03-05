import os
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

REQUIRED_FILES = [
    ("sample_data.json", "Sample data"),
    ("prompt.txt", "Classification prompt"),
]

def run_step(name, script):
    print(f"\n{'='*60}")
    print(f"Step: {name} ({script})")
    print(f"{'='*60}")
    try:
        subprocess.run(
            [sys.executable, script],
            check=True,
            capture_output=False,
        )
        print(f"[SUCCESS] {name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAILED] {name} - Exit code: {e.returncode}")
        return False

def check_required_files():
    print(f"\n{'='*60}")
    print("Step: Verify sample data (sample_data.json, prompt.txt)")
    print(f"{'='*60}")
    all_ok = True
    for filepath, desc in REQUIRED_FILES:
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print(f"  [OK] {filepath} exists")
        else:
            print(f"  [MISSING] {filepath}")
            all_ok = False
    if all_ok:
        print("[SUCCESS] Verify sample data")
    else:
        print("[FAILED] Verify sample data")
    return all_ok

def main():
    print("Starting data pipeline...")

    failed_steps = []
    for name, script in PIPELINE_STEPS[:4]:
        success = run_step(name, script)
        if not success:
            failed_steps.append(name)

    if not check_required_files():
        failed_steps.append("Verify sample data")

    for name, script in PIPELINE_STEPS[4:]:
        success = run_step(name, script)
        if not success:
            failed_steps.append(name)

    print(f"\n{'='*60}")
    if failed_steps:
        print(f"Pipeline completed with {len(failed_steps)} error(s):")
        for step in failed_steps:
            print(f"  - {step}")
    else:
        print("Pipeline completed successfully!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
