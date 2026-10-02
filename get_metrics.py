import csv
import glob
import os
import subprocess
import sys
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze as raw_analyze

# Path to the directory containing your 120 generated Python files
FUNCTIONS_DIR = "./bottle_repo_regen"  # <--- Change this to your folder path
OUTPUT_CSV = "software_metrics.csv"

rows = []

# Search for all .py files in the directory recursively
python_files = glob.glob(f"{FUNCTIONS_DIR}/**/*.py", recursive=True)

if not python_files:
    print(f"No Python files found in '{FUNCTIONS_DIR}'. Please check the path.")
else:
    print(f"Found {len(python_files)} Python files. Calculating metrics...\n")

    for filepath in python_files:
        filename = os.path.basename(filepath)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()

            # 1. Cyclomatic Complexity & SLOC using Radon
            cc_blocks = cc_visit(code)

            avg_cc = (
                sum(b.complexity for b in cc_blocks) / len(cc_blocks)
                if cc_blocks
                else 0
            )

            max_cc = max((b.complexity for b in cc_blocks), default=0)

            # Raw SLOC analysis
            raw = raw_analyze(code)
            sloc = raw.sloc

            # 2. Maintainability Index using Radon
            mi = mi_visit(code, multi=True)

            # 3. Extract Pylint Score
            pylint_score = "N/A"

            try:
                res = subprocess.run(
                    [sys.executable, "-m", "pylint", filepath],
                    capture_output=True,
                    text=True,
                    timeout=15,
                )

                for line in res.stdout.splitlines():
                    if "rated at" in line:
                        # Parses score out of string: "Your code has been rated at 8.50/10..."
                        pylint_score = (
                            line.split("rated at")[1].split("/10")[0].strip()
                        )
                        break

            except Exception:
                pylint_score = "Error"

            rows.append({
                "File": filename,
                "Path": filepath,
                "SLOC": sloc,
                "Avg_Cyclomatic_Complexity": round(avg_cc, 2),
                "Max_Cyclomatic_Complexity": max_cc,
                "Maintainability_Index": round(mi, 2),
                "Pylint_Score": pylint_score,
            })

            print(f"Processed: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Save all results to a single CSV file
if rows:
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "File",
            "Path",
            "SLOC",
            "Avg_Cyclomatic_Complexity",
            "Max_Cyclomatic_Complexity",
            "Maintainability_Index",
            "Pylint_Score",
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"\nSuccess! Software metrics for {len(rows)} files saved to"
        f" '{OUTPUT_CSV}'."
    )