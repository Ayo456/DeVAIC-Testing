import argparse
import ast
import csv
import glob
import json
import os
import re
import sys

from radon.complexity import cc_visit
from radon.metrics import h_visit, mi_visit
from radon.raw import analyze as raw_analyze

# The progress messages use ✓, which the default Windows console encoding cannot print.
sys.stdout.reconfigure(encoding="utf-8")


# Closed models are only reachable through a vendor API; open-weight models
# publish their weights and run locally through Ollama.
MODEL_TYPES = {
    "qwen": "Open-weight",
    "gemma": "Open-weight",
    "chatgpt": "Closed",
    "gpt": "Closed",
    "gemini": "Closed",
    "human": "Human",
}

# Folder in clean_outputs/ that holds the cleaned original Bottle functions.
HUMAN_FOLDER = "human_code"

SYNTAX_ERROR = "Syntax Error"
PARSE_ERROR = "Parse Error"

HALSTEAD_FIELDS = {
    "Halstead_Distinct_Operators": "h1",
    "Halstead_Distinct_Operands": "h2",
    "Halstead_Total_Operators": "N1",
    "Halstead_Total_Operands": "N2",
    "Halstead_Vocabulary": "vocabulary",
    "Halstead_Length": "length",
    "Halstead_Volume": "volume",
    "Halstead_Difficulty": "difficulty",
    "Halstead_Effort": "effort",
    "Halstead_Time": "time",
    "Halstead_Bugs": "bugs",
}

NESTING_NODES = (
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.Try,
    ast.With,
    ast.AsyncWith,
    ast.Match,
) + ((ast.TryStar,) if hasattr(ast, "TryStar") else ())


def get_model_type(model_folder):
    name = model_folder.lower()
    for keyword, model_type in MODEL_TYPES.items():
        if keyword in name:
            return model_type
    return "Unknown"


def max_nesting_depth(node, depth=0):
    """Deepest level of nested control-flow blocks; an elif does not add a level."""
    deepest = depth

    for field, value in ast.iter_fields(node):
        children = value if isinstance(value, list) else [value]

        for child in children:
            if not isinstance(child, ast.AST):
                continue

            is_elif = (
                isinstance(node, ast.If)
                and field == "orelse"
                and len(node.orelse) == 1
                and isinstance(child, ast.If)
            )

            if isinstance(child, NESTING_NODES) and not is_elif:
                child_depth = max_nesting_depth(child, depth + 1)
            else:
                child_depth = max_nesting_depth(child, depth)

            deepest = max(deepest, child_depth)

    return deepest


GENERATION_FIELDS = [
    "Model_Version",
    "Quantization",
    "Temperature",
    "Seed",
    "Max_Tokens",
]

_manifest_cache = {}


def load_manifests(model_folder):
    """All generation logs for a model, newest first."""
    if model_folder not in _manifest_cache:
        paths = sorted(
            glob.glob(os.path.join(RAW_DIR, model_folder, "generation_config_*.json")),
            reverse=True,
        )
        manifests = []
        for path in paths:
            with open(path, "r", encoding="utf-8") as f:
                manifests.append(json.load(f))
        _manifest_cache[model_folder] = manifests
    return _manifest_cache[model_folder]


def get_generation_settings(model_folder, run_name, task_name):
    """Settings from the newest log in which this exact output was generated."""
    # Human code has no generation settings; web-interface outputs (e.g.
    # gemini-web) have no generation log, so their settings are unknown.
    if model_folder == HUMAN_FOLDER or not load_manifests(model_folder):
        return dict.fromkeys(GENERATION_FIELDS, "N/A")

    for manifest in load_manifests(model_folder):
        run = manifest.get("runs", {}).get(run_name, {})
        output = run.get("outputs", {}).get(task_name, {})

        if output.get("status") != "ok":
            continue

        settings = run.get("options") or run.get("settings") or {}
        model_info = manifest.get("model_info", {})
        return {
            "Model_Version": output.get("model_version") or manifest.get("model"),
            "Quantization": model_info.get("quantization", "N/A"),
            "Temperature": settings.get("temperature"),
            "Seed": settings.get("seed"),
            "Max_Tokens": (
                settings.get("num_predict")
                or settings.get("max_completion_tokens")
                or settings.get("max_output_tokens")
            ),
        }

    return dict.fromkeys(GENERATION_FIELDS, "Not logged")


# ==================== TARGET CONFIGURATION ====================
# Set to True to calculate metrics ONLY for the target files
TARGET_ONLY = False

# Matches any model folder containing 'qwen' (e.g. 'qwen2.5-coder_32b')
TARGET_MODEL_KEYWORD = "qwen"

# The EXACT 7 (filename, run_folder) pairs to process for Qwen:
TARGET_PAIRS = [
    ("redirect.py", "run_1"),
    ("redirect.py", "run_2"),
    ("static_file.py", "run_1"),
    ("static_file.py", "run_2"),
    ("template.py", "run_1"),
    ("template.py", "run_2"),
    ("template.py", "run_3"),
]
# =============================================================


CLEAN_DIR = "./clean_outputs"
RAW_DIR = "./raw_outputs"
OUTPUT_CSV = "software_metrics.csv"

parser = argparse.ArgumentParser(
    description="Calculate software metrics for the cleaned model outputs."
)
parser.add_argument(
    "--models",
    nargs="+",
    help=(
        "Only measure model folders whose name contains one of these (e.g. gpt)."
        " Rows already in the CSV for other models are kept."
    ),
)
args = parser.parse_args()


def is_selected(model_folder):
    return not args.models or any(
        m.lower() in model_folder.lower() for m in args.models
    )


all_files = sorted(
    glob.glob(f"{CLEAN_DIR}/**/*.py", recursive=True)
)

python_files = []

for filepath in all_files:
    rel_path = os.path.relpath(filepath, CLEAN_DIR)
    parts = rel_path.split(os.sep)

    if len(parts) >= 3:
        model_folder, parent_run, filename = parts[0], parts[1], parts[2]

    elif len(parts) == 2:
        # Folders without runs, such as the human baseline (human_code/<file>.py).
        model_folder, parent_run, filename = parts[0], "", parts[1]

    else:
        filename = os.path.basename(filepath)
        parent_run = os.path.basename(os.path.dirname(filepath))
        model_folder = os.path.basename(
            os.path.dirname(
                os.path.dirname(filepath)
            )
        )

    if not is_selected(model_folder):
        continue

    if TARGET_ONLY:
        is_qwen = TARGET_MODEL_KEYWORD in model_folder.lower()
        is_target_pair = (filename, parent_run) in TARGET_PAIRS

        if is_qwen and is_target_pair:
            python_files.append(filepath)

    else:
        python_files.append(filepath)

if not python_files:
    print(
        f"No matching files found in '{CLEAN_DIR}' for model keyword"
        f" '{TARGET_MODEL_KEYWORD}'."
    )
    sys.exit(1)

print(
    f"Processing software metrics for {len(python_files)} files..."
)

rows = []

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
    nesting = "N/A"
    halstead = dict.fromkeys(HALSTEAD_FIELDS, "N/A")
    error_msg = ""

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        # 1. Raw SLOC
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
            status = SYNTAX_ERROR
            avg_cc = PARSE_ERROR
            max_cc = PARSE_ERROR
            error_msg = f"Radon CC: {type(e).__name__}"

        # 3. Maintainability Index
        try:
            mi = round(
                mi_visit(code, multi=True),
                2,
            )

        except Exception as e:
            status = SYNTAX_ERROR
            mi = PARSE_ERROR

            if not error_msg:
                error_msg = f"Radon MI: {type(e).__name__}"

        # 4. Maximum Nesting Depth
        try:
            nesting = max_nesting_depth(ast.parse(code))

        except Exception as e:
            status = SYNTAX_ERROR
            nesting = PARSE_ERROR

            if not error_msg:
                error_msg = f"Nesting: {type(e).__name__}"

        # 5. Halstead Measures (whole file)
        try:
            h_total = h_visit(code).total

            for column, attr in HALSTEAD_FIELDS.items():
                halstead[column] = round(getattr(h_total, attr), 2)

        except Exception as e:
            status = SYNTAX_ERROR
            halstead = dict.fromkeys(HALSTEAD_FIELDS, PARSE_ERROR)

            if not error_msg:
                error_msg = f"Radon Halstead: {type(e).__name__}"

    except Exception as main_err:
        status = "File Error"
        error_msg = str(main_err)

    rows.append(
        {
            "File": filename,
            "Model_Run": model_run_folder,
            "Model_Type": get_model_type(model_run_folder),
            **get_generation_settings(
                model_run_folder.split(os.sep)[0],
                os.path.basename(model_run_folder),
                os.path.splitext(filename)[0],
            ),
            "Status": status,
            "SLOC": sloc,
            "Avg_Cyclomatic_Complexity": avg_cc,
            "Max_Cyclomatic_Complexity": max_cc,
            "Maintainability_Index": mi,
            "Max_Nesting_Depth": nesting,
            **halstead,
            "Error_Details": error_msg,
            "Path": filepath,
        }
    )

    status_flag = "✓" if status == "Valid" else "X"

    print(
        f" [{status_flag}] {filename} ({model_run_folder}) -> Status: {status}"
    )

# With --models, keep the existing rows of every model that was not re-measured.
kept_rows = []

if args.models and os.path.exists(OUTPUT_CSV):
    with open(OUTPUT_CSV, "r", newline="", encoding="utf-8") as f:
        kept_rows = [
            row
            for row in csv.DictReader(f)
            if not is_selected(re.split(r"[\\/]", row["Model_Run"])[0])
        ]

# Write to CSV
if rows:
    measured_count = len(rows)
    rows = sorted(kept_rows + rows, key=lambda row: row["Path"])

    # Values that do not apply (e.g. quantization for API models, generation
    # settings for human code) are left blank so spreadsheets read the
    # numeric columns as numbers.
    rows = [
        {key: "" if value == "N/A" else value for key, value in row.items()}
        for row in rows
    ]

    with open(
        OUTPUT_CSV,
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        fieldnames = [
            "File",
            "Model_Run",
            "Model_Type",
            *GENERATION_FIELDS,
            "Status",
            "SLOC",
            "Avg_Cyclomatic_Complexity",
            "Max_Cyclomatic_Complexity",
            "Maintainability_Index",
            "Max_Nesting_Depth",
            *HALSTEAD_FIELDS,
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
        f"\n✓ Done! Metrics recorded for {measured_count} files in"
        f" '{OUTPUT_CSV}' ({len(kept_rows)} existing rows kept)."
    )