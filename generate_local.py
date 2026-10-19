import argparse
import datetime
import glob
import json
import os
import platform
import sys

import ollama

# ==================== CONFIGURATION ====================
MODELS = ["qwen2.5-coder:32b", "gemma2:9b"]
PROMPTS_DIR = os.path.join("bottle_repo", "prompts")
OUTPUT_BASE_DIR = "raw_outputs"
NUM_REPETITIONS = 3

# Sampling settings fixed by the study plan. top_p / top_k are Ollama's
# defaults, set explicitly so the full configuration is recorded.
TEMPERATURE = 0.2
TOP_P = 0.9
TOP_K = 40
MAX_TOKENS = 2048
CONTEXT_WINDOW = 4096

# Run N uses seed BASE_SEED + N: each run is reproducible, but the three
# repetitions still differ from one another.
BASE_SEED = 42
# =======================================================


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate function implementations with local Ollama models."
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=MODELS,
        help=f"Ollama model tags to run (default: {' '.join(MODELS)})",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing outputs instead of skipping them.",
    )
    return parser.parse_args()


def get_model_digest(model):
    try:
        for entry in ollama.list().models:
            if entry.model == model:
                return entry.digest
    except Exception:
        pass
    return "unknown"


def build_options(seed):
    return {
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "top_k": TOP_K,
        "num_predict": MAX_TOKENS,
        "num_ctx": CONTEXT_WINDOW,
        "seed": seed,
    }


def generate_one(model, prompt_path, run_dir, options, overwrite):
    task_name = os.path.splitext(os.path.basename(prompt_path))[0]
    output_filepath = os.path.join(run_dir, f"{task_name}.py")

    if os.path.exists(output_filepath) and not overwrite:
        print(f" [-] Skipped {task_name}.py (exists; use --overwrite)")
        return {"status": "skipped_existing"}

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_text = f.read().strip()

    try:
        # Stateless call: every prompt starts from a fresh chat.
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt_text}],
            options=options,
        )
    except Exception as e:
        print(f" [X] Failed {task_name}: {e}")
        return {"status": "error", "error": str(e)}

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(response["message"]["content"])

    done_reason = response.get("done_reason")
    if done_reason == "length":
        print(
            f" [!] Generated {task_name}.py but it hit the"
            f" {MAX_TOKENS}-token limit (may be truncated)"
        )
    else:
        print(f" [✓] Generated {task_name}.py")

    return {
        "status": "ok",
        "done_reason": done_reason,
        "output_tokens": response.get("eval_count"),
    }


def main():
    args = parse_args()

    prompt_files = sorted(glob.glob(os.path.join(PROMPTS_DIR, "*.txt")))

    if not prompt_files:
        print(f"Error: No .txt files found in '{PROMPTS_DIR}'.")
        sys.exit(1)

    print(
        f"Found {len(prompt_files)} prompts. Starting batch generation across"
        f" {len(args.models)} models..."
    )

    for model in args.models:
        clean_model_name = model.replace(":", "_").replace("/", "_")
        model_dir = os.path.join(OUTPUT_BASE_DIR, clean_model_name)
        os.makedirs(model_dir, exist_ok=True)

        manifest = {
            "model": model,
            "model_digest": get_model_digest(model),
            "ollama_python_version": getattr(ollama, "__version__", "unknown"),
            "python_version": platform.python_version(),
            "started_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "prompts_dir": PROMPTS_DIR,
            "num_repetitions": NUM_REPETITIONS,
            "runs": {},
        }

        for run_num in range(1, NUM_REPETITIONS + 1):
            run_name = f"run_{run_num}"
            run_dir = os.path.join(model_dir, run_name)
            os.makedirs(run_dir, exist_ok=True)

            options = build_options(BASE_SEED + run_num)
            run_record = {"options": options, "outputs": {}}
            manifest["runs"][run_name] = run_record

            print(
                f"\n--- [Model: {model}] | [Run {run_num}/{NUM_REPETITIONS}]"
                f" | [Seed {options['seed']}] ---"
            )

            for prompt_path in prompt_files:
                task_name = os.path.splitext(os.path.basename(prompt_path))[0]
                run_record["outputs"][task_name] = generate_one(
                    model, prompt_path, run_dir, options, args.overwrite
                )

        manifest["finished_at"] = datetime.datetime.now().isoformat(
            timespec="seconds"
        )
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        manifest_path = os.path.join(model_dir, f"generation_config_{stamp}.json")

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        print(f"\nConfiguration recorded in {manifest_path}")

    print("\n✓ Local generation pipeline complete!")


if __name__ == "__main__":
    main()
