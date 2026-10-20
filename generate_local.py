import argparse
import datetime
import glob
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
import urllib.request

import ollama

# The progress messages use ✓, which the default Windows console encoding cannot print.
sys.stdout.reconfigure(encoding="utf-8")

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

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
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


def get_model_info(model):
    info: dict = {"digest": "unknown"}

    try:
        for entry in ollama.list().models:
            if entry.model == model:
                info["digest"] = entry.digest or "unknown"
    except Exception:
        pass

    try:
        details = ollama.show(model).details
        if details is not None:
            info["quantization"] = details.quantization_level
            info["parameter_size"] = details.parameter_size
            info["family"] = details.family
            info["format"] = details.format
    except Exception as e:
        info["details_error"] = str(e)

    return info


def get_ollama_server_version():
    try:
        with urllib.request.urlopen(f"{OLLAMA_HOST}/api/version", timeout=5) as r:
            return json.load(r).get("version", "unknown")
    except Exception:
        return "unknown"


def get_gpus():
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
             "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout
        return [
            dict(zip(("name", "memory", "driver"), (p.strip() for p in line.split(","))))
            for line in out.splitlines() if line.strip()
        ]
    except Exception:
        pass

    if platform.system() != "Windows":
        return []

    # Win32_VideoController caps AdapterRAM at 4 GB, so VRAM is read from
    # the display adapter's registry entry instead.
    script = (
        "Get-ChildItem 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Class\\"
        "{4d36e968-e325-11ce-bfc1-08002be10318}' -ErrorAction SilentlyContinue |"
        " ForEach-Object { try { $p = Get-ItemProperty $_.PSPath -ErrorAction Stop;"
        " if ($p.DriverDesc) { [pscustomobject]@{ name = $p.DriverDesc;"
        " memory_gb = [math]::Round($p.'HardwareInformation.qwMemorySize' / 1GB, 1);"
        " driver = $p.DriverVersion } } } catch {} } | ConvertTo-Json"
    )
    # Some adapter keys are admin-only, which makes PowerShell exit 1 even
    # though the readable entries were printed, so the exit code is ignored.
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            capture_output=True, text=True, timeout=20,
        ).stdout
        gpus = json.loads(out)
        return gpus if isinstance(gpus, list) else [gpus]
    except Exception:
        return []


def get_cpu_name():
    if platform.system() == "Windows":
        try:
            return subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-CimInstance Win32_Processor).Name"],
                capture_output=True, text=True, timeout=20, check=True,
            ).stdout.strip()
        except Exception:
            pass
    return platform.processor() or "unknown"


def get_environment():
    return {
        "os": platform.platform(),
        "cpu": get_cpu_name(),
        "gpus": get_gpus(),
        "ollama_server_version": get_ollama_server_version(),
        "ollama_python_version": importlib.metadata.version("ollama"),
        "python_version": platform.python_version(),
    }


def get_gpu_offload(model):
    """How much of the loaded model sits in GPU memory (the rest runs on CPU)."""
    try:
        for entry in ollama.ps().models:
            if entry.model == model and entry.size and entry.size_vram is not None:
                return {
                    "model_size_bytes": entry.size,
                    "vram_bytes": entry.size_vram,
                    "percent_on_gpu": round(100 * entry.size_vram / entry.size, 1),
                }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "model not loaded"}


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

    environment = get_environment()

    for model in args.models:
        clean_model_name = model.replace(":", "_").replace("/", "_")
        model_dir = os.path.join(OUTPUT_BASE_DIR, clean_model_name)
        os.makedirs(model_dir, exist_ok=True)

        manifest = {
            "model": model,
            "model_info": get_model_info(model),
            "environment": environment,
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

            # Measured while the model is still loaded after the run.
            run_record["gpu_offload"] = get_gpu_offload(model)

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
