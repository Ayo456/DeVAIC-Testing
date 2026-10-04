import csv
import glob
import os
import subprocess
import sys

from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze as raw_analyze


CLEAN_DIR = "clean_outputs\gemma2_9b"
OUTPUT_CSV = "software_metrics.csv"

rows = []

python_files = sorted(
    glob.glob(f"{CLEAN_DIR}/**/*.py", recursive=True)
)

if not python_files:
    print(f"No files found in '{CLEAN_DIR}'. Please check the directory path.")
    sys.exit(1)

print(
    f"Processing software metrics for {len(python_files)} files (including"
    " error tracking)..."
)

for filepath in python_files:
    filename = os.path.basename(filepath)
    model_run_folder = os.path.dirname(
        os.path.relpath(filepath, CLEAN_DIR)
    )

    # Default status and metric values
    status = "Valid"
    sloc = "Error"
    avg_cc = "N/A"
    max_cc = "N/A"
    mi = "N/A"
    pylint_score = "N/A"
    error_msg = ""

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        # 1. Raw SLOC (Attempts Radon first; falls back to raw line count if parse fails)
        try:
            raw = raw_analyze(code)
            sloc = raw.sloc

        except Exception:
            sloc = len(
                [
                    line
                    for line in code.splitlines()
                    if line.strip()
                    and not line.strip().startswith("#")
                ]
            )

        # 2. Cyclomatic Complexity
        try:
            cc_blocks = cc_visit(code)

            if cc_blocks:
                avg_cc = round(
                    sum(b.complexity for b in cc_blocks) / len(cc_blocks),
                    2,
                )
                max_cc = max(b.complexity for b in cc_blocks)

            else:
                avg_cc = 0
                max_cc = 0

        except Exception as e:
            status = "Syntax Error"
            avg_cc = "Parse Error"
            max_cc = "Parse Error"
            error_msg = f"Radon CC: {type(e).__name__}"

        # 3. Maintainability Index
        try:
            mi = round(mi_visit(code, multi=True), 2)

        except Exception as e:
            status = "Syntax Error"
            mi = "Parse Error"

            if not error_msg:
                error_msg = f"Radon MI: {type(e).__name__}"

        # 4. Pylint Score
        try:
            res = subprocess.run(
                [sys.executable, "-m", "pylint", filepath],
                capture_output=True,
                text=True,
                timeout=15,
            )

            for line in res.stdout.splitlines():
                if "rated at" in line:
                    pylint_score = (
                        line.split("rated at")[1]
                        .split("/10")[0]
                        .strip()
                    )
                    break

            if pylint_score == "N/A":
                pylint_score = "Parse Error"

        except Exception:
            pylint_score = "Exec Error"

    except Exception as main_err:
        status = "File Error"
        error_msg = str(main_err)

    # Always append the row to ensure 100% file coverage in the CSV
    rows.append(
        {
            "File": filename,
            "Model_Run": model_run_folder,
            "Status": status,
            "SLOC": sloc,
            "Avg_Cyclomatic_Complexity": avg_cc,
            "Max_Cyclomatic_Complexity": max_cc,
            "Maintainability_Index": mi,
            "Pylint_Score": pylint_score,
            "Error_Details": error_msg,
            "Path": filepath,
        }
    )

    status_flag = "✓" if status == "Valid" else "X"

    print(
        f" [{status_flag}] {filename} ({model_run_folder}) -> Status: {status}"
    )

# Write all results (including syntax errors) to the CSV
if rows:
    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        fieldnames = [
            "File",
            "Model_Run",
            "Status",
            "SLOC",
            "Avg_Cyclomatic_Complexity",
            "Max_Cyclomatic_Complexity",
            "Maintainability_Index",
            "Pylint_Score",
            "Error_Details",
            "Path",
        ]

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

print(
    f"\n✓ Done! Metrics and error logs recorded for all {len(rows)} files in"
    f" '{OUTPUT_CSV}'."
)