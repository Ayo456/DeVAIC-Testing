import argparse
import csv
import glob
import json
import os
import re
import subprocess
import sys

# The progress messages use ✓, which the default Windows console encoding cannot print.
sys.stdout.reconfigure(encoding="utf-8")


# ==================== CONFIGURATION ====================
# Redlyne (https://github.com/redlyne-ai/redlyne) cloned next to this repo.
DEFAULT_ENGINE = os.path.join(
    "..", "redlyne", "launch_tool", "redlyne_engine.py"
)
CLEAN_DIR = "./clean_outputs"
FINDINGS_CSV = "redlyne_findings.csv"
SUMMARY_CSV = "redlyne_summary.csv"
# =======================================================

MODEL_TYPES = {
    "qwen": "Open-weight",
    "gemma": "Open-weight",
    "chatgpt": "Closed",
    "gpt": "Closed",
    "gemini": "Closed",
    "human": "Human",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Scan the cleaned outputs with the Redlyne security engine."
    )
    parser.add_argument(
        "--models",
        nargs="+",
        help="Only scan folders whose name contains one of these (e.g. gpt human).",
    )
    parser.add_argument(
        "--engine",
        default=DEFAULT_ENGINE,
        help=f"Path to redlyne_engine.py (default: {DEFAULT_ENGINE})",
    )
    return parser.parse_args()


def get_model_type(model_folder):
    name = model_folder.lower()
    for keyword, model_type in MODEL_TYPES.items():
        if keyword in name:
            return model_type
    return "Unknown"


def get_engine_version(engine):
    """Commit of the Redlyne checkout, so results can be tied to a rule set."""
    try:
        return subprocess.run(
            ["git", "-C", os.path.dirname(os.path.abspath(engine)),
             "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout.strip()
    except Exception:
        return "unknown"


def scan_file(engine, filepath):
    # -I keeps the engine isolated from this repo's modules and environment.
    result = subprocess.run(
        [sys.executable, "-I", engine, filepath],
        capture_output=True, text=True, encoding="utf-8", timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"exit code {result.returncode}")
    return json.loads(result.stdout)


def main():
    args = parse_args()

    if not os.path.isfile(args.engine):
        print(
            f"Error: Redlyne engine not found at '{args.engine}'.\n"
            "Clone it next to this repo with:\n"
            "  git clone https://github.com/redlyne-ai/redlyne.git ../redlyne"
        )
        sys.exit(1)

    engine_version = get_engine_version(args.engine)

    files = []
    for filepath in sorted(glob.glob(f"{CLEAN_DIR}/**/*.py", recursive=True)):
        model_run = os.path.dirname(os.path.relpath(filepath, CLEAN_DIR))
        model_folder = re.split(r"[\\/]", model_run)[0]
        if args.models and not any(
            m.lower() in model_folder.lower() for m in args.models
        ):
            continue
        files.append((filepath, model_run, model_folder))

    if not files:
        print(f"No matching files found in '{CLEAN_DIR}'.")
        sys.exit(1)

    print(
        f"Scanning {len(files)} files with Redlyne ({engine_version})..."
    )

    findings = []
    summary = []

    for filepath, model_run, model_folder in files:
        filename = os.path.basename(filepath)
        base = {
            "File": filename,
            "Model_Run": model_run,
            "Model_Type": get_model_type(model_folder),
        }

        try:
            output = scan_file(args.engine, filepath)
        except Exception as e:
            summary.append({
                **base, "Status": "Scan Error", "Vulnerabilities": "",
                "Flagged_Lines": "", "Vulnerable_Lines": "",
                "Unique_Rules": "", "Rule_IDs": "",
                "OWASP_Categories": "",
                "Error_Details": str(e), "Redlyne_Version": engine_version,
                "Path": filepath,
            })
            print(f" [X] {filename} ({model_run}) -> Scan Error: {e}")
            continue

        matches = output.get("matches", [])
        rule_ids = sorted({m["rule_id"] for m in matches})
        categories = sorted({c for m in matches for c in m.get("owasp", [])})

        for m in matches:
            findings.append({
                **base,
                "Line": m.get("line"),
                "Rule_ID": m.get("rule_id"),
                "OWASP_Categories": "; ".join(m.get("owasp", [])),
                "Code": (m.get("code") or "").strip(),
                "Comment": m.get("comment", ""),
                "Path": filepath,
            })

        summary.append({
            **base,
            "Status": "Vulnerable" if matches else "Safe",
            # Counted like the Redlyne VS Code extension: each OWASP
            # category once per file, however many lines it flags.
            "Vulnerabilities": len(categories),
            "Flagged_Lines": len(matches),
            # Line numbers in the cleaned file (clean_outputs/), where the
            # vulnerable code sits.
            "Vulnerable_Lines": "; ".join(
                str(line) for line in sorted({m.get("line") for m in matches})
            ),
            "Unique_Rules": len(rule_ids),
            "Rule_IDs": "; ".join(rule_ids),
            "OWASP_Categories": "; ".join(categories),
            "Error_Details": "",
            "Redlyne_Version": engine_version,
            "Path": filepath,
        })

        flag = "!" if matches else "✓"
        print(
            f" [{flag}] {filename} ({model_run}) -> {len(categories)}"
            f" vulnerability(ies) on {len(matches)} line(s)"
        )

    with open(SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    findings_fields = [
        "File", "Model_Run", "Model_Type", "Line", "Rule_ID",
        "OWASP_Categories", "Code", "Comment", "Path",
    ]
    with open(FINDINGS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=findings_fields)
        writer.writeheader()
        writer.writerows(findings)

    vulnerable = sum(1 for row in summary if row["Status"] == "Vulnerable")
    print(
        f"\n✓ Done! {vulnerable}/{len(summary)} files had vulnerabilities"
        f" ({len(findings)} flagged lines). Results in '{SUMMARY_CSV}' and"
        f" '{FINDINGS_CSV}'."
    )


if __name__ == "__main__":
    main()
