import argparse
import subprocess
import sys

# The progress messages use ✓, which the default Windows console encoding cannot print.
sys.stdout.reconfigure(encoding="utf-8")


# ==================== CONFIGURATION ====================
# Every code origin in the study. Each keyword matches a folder name in
# raw_outputs/ and clean_outputs/ ("human" is the original Bottle code).
ORIGINS = ["human", "qwen", "gemma", "gpt", "gemini"]
# =======================================================


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run the full study pipeline: (optional) generation, cleaning,"
            " software metrics, Redlyne security scan, and the results report."
        )
    )
    parser.add_argument(
        "--generate-local",
        action="store_true",
        help="Regenerate Qwen and Gemma outputs with Ollama first (slow).",
    )
    parser.add_argument(
        "--generate-api",
        nargs="+",
        choices=["openai", "gemini"],
        help="Generate outputs with these APIs first (needs their API keys).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Let the generation steps replace existing outputs.",
    )
    parser.add_argument(
        "--origins",
        nargs="+",
        default=ORIGINS,
        help=f"Origins to clean, measure and scan (default: {' '.join(ORIGINS)}).",
    )
    parser.add_argument(
        "--skip-redlyne",
        action="store_true",
        help="Skip the Redlyne security scan (the report then shows metrics only).",
    )
    return parser.parse_args()


def run_step(name, command):
    print(f"\n==================== {name} ====================")
    print(" ".join(command))
    result = subprocess.run([sys.executable, *command])
    if result.returncode != 0:
        print(f"\n[X] '{name}' failed (exit code {result.returncode}); stopping.")
        sys.exit(result.returncode)


def main():
    args = parse_args()
    overwrite = ["--overwrite"] if args.overwrite else []

    if args.generate_local:
        run_step("Local generation", ["generate_local.py", *overwrite])

    if args.generate_api:
        run_step(
            "API generation",
            ["generate_api.py", "--providers", *args.generate_api, *overwrite],
        )

    run_step("Strip comments", ["strip_comments.py", "--models", *args.origins])
    run_step("Software metrics", ["get_metrics.py", "--models", *args.origins])

    if not args.skip_redlyne:
        run_step("Redlyne scan", ["run_redlyne.py", "--models", *args.origins])

    run_step("Results report", ["build_report.py"])

    print("\n✓ Pipeline complete! Open results/report.html to see the results.")


if __name__ == "__main__":
    main()
