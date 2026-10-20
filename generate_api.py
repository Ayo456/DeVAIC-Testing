import argparse
import datetime
import glob
import importlib.metadata
import json
import os
import platform
import sys
import time

# The progress messages use ✓, which the default Windows console encoding cannot print.
sys.stdout.reconfigure(encoding="utf-8")

# ==================== CONFIGURATION ====================
# Pin exact model versions so every call is answered by the same model.
# Each provider's API reports the version that actually answered, and that
# version is logged for every output.
OPENAI_MODEL = "gpt-4.1-2025-04-14"
GEMINI_MODEL = "gemini-2.5-flash"

PROMPTS_DIR = os.path.join("bottle_repo", "prompts")
OUTPUT_BASE_DIR = "raw_outputs"
NUM_REPETITIONS = 3

# Same sampling settings as generate_local.py, so all four models are
# generated under one configuration. OpenAI has no top_k parameter.
TEMPERATURE = 0.2
TOP_P = 0.9
TOP_K = 40
MAX_TOKENS = 2048
BASE_SEED = 42

# Gemini 2.5 Flash "thinks" before answering unless this is 0. The local
# models do not, and thinking tokens would count against MAX_TOKENS.
GEMINI_THINKING_BUDGET = 0

MAX_ATTEMPTS = 3
# =======================================================


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate function implementations with the OpenAI and Gemini APIs."
    )
    parser.add_argument(
        "--providers",
        nargs="+",
        choices=["openai", "gemini"],
        default=["openai", "gemini"],
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing outputs instead of skipping them.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the configuration and planned outputs without calling any API.",
    )
    return parser.parse_args()


def package_version(name):
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "not installed"


class OpenAIProvider:
    name = "openai"
    model = OPENAI_MODEL
    package = "openai"
    key_variable = "OPENAI_API_KEY"

    def __init__(self):
        from openai import OpenAI

        self.client = OpenAI()

    @staticmethod
    def settings(seed):
        return {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "max_completion_tokens": MAX_TOKENS,
            "seed": seed,
        }

    def generate(self, prompt_text, seed):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt_text}],
            **self.settings(seed),
        )
        choice = response.choices[0]
        return choice.message.content or "", {
            "model_version": response.model,
            "system_fingerprint": response.system_fingerprint,
            "response_id": response.id,
            "finish_reason": choice.finish_reason,
            "truncated": choice.finish_reason == "length",
            "input_tokens": response.usage.prompt_tokens if response.usage else None,
            "output_tokens": response.usage.completion_tokens if response.usage else None,
        }


class GeminiProvider:
    name = "gemini"
    model = GEMINI_MODEL
    package = "google-genai"
    key_variable = "GEMINI_API_KEY"

    def __init__(self):
        from google import genai
        from google.genai import types

        self.client = genai.Client()
        self.types = types

    @staticmethod
    def settings(seed):
        settings = {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "top_k": TOP_K,
            "max_output_tokens": MAX_TOKENS,
            "seed": seed,
        }
        if GEMINI_THINKING_BUDGET is not None:
            settings["thinking_budget"] = GEMINI_THINKING_BUDGET
        return settings

    def generate(self, prompt_text, seed):
        settings = self.settings(seed)
        thinking_budget = settings.pop("thinking_budget", None)
        config = self.types.GenerateContentConfig(
            **settings,
            thinking_config=(
                self.types.ThinkingConfig(thinking_budget=thinking_budget)
                if thinking_budget is not None
                else None
            ),
        )
        response = self.client.models.generate_content(
            model=self.model, contents=prompt_text, config=config
        )
        candidate = response.candidates[0] if response.candidates else None
        finish_reason = (
            candidate.finish_reason.name
            if candidate is not None and candidate.finish_reason is not None
            else None
        )
        usage = response.usage_metadata
        return response.text or "", {
            "model_version": response.model_version,
            "response_id": response.response_id,
            "finish_reason": finish_reason,
            "truncated": finish_reason == "MAX_TOKENS",
            "input_tokens": usage.prompt_token_count if usage else None,
            "output_tokens": usage.candidates_token_count if usage else None,
            "thinking_tokens": usage.thoughts_token_count if usage else None,
        }


PROVIDERS = {"openai": OpenAIProvider, "gemini": GeminiProvider}


class FatalAPIError(Exception):
    """An error that retrying cannot fix, so the provider's run stops."""


def is_fatal(error):
    status = getattr(error, "status_code", None)
    if status is None and isinstance(getattr(error, "code", None), int):
        status = error.code

    # Bad request, bad key, no access, unknown model, invalid parameter.
    if status in (400, 401, 403, 404, 422):
        return True

    # OpenAI reports an empty balance as a 429, like a rate limit, but
    # waiting does not refill it.
    return status == 429 and "insufficient_quota" in str(error)


def call_with_retries(provider, prompt_text, seed):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            code, metadata = provider.generate(prompt_text, seed)
            metadata["attempts"] = attempt
            return code, metadata
        except Exception as e:
            if is_fatal(e):
                raise FatalAPIError(f"{type(e).__name__}: {e}") from e
            if attempt == MAX_ATTEMPTS:
                raise
            wait = 20 * attempt
            print(f"     attempt {attempt} failed ({type(e).__name__}); retrying in {wait}s")
            time.sleep(wait)


def generate_one(provider, prompt_path, run_dir, seed, overwrite):
    task_name = os.path.splitext(os.path.basename(prompt_path))[0]
    output_filepath = os.path.join(run_dir, f"{task_name}.py")

    if os.path.exists(output_filepath) and not overwrite:
        print(f" [-] Skipped {task_name}.py (exists; use --overwrite)")
        return {"status": "skipped_existing"}

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_text = f.read().strip()

    try:
        # Each prompt is a separate request with no shared conversation.
        code, metadata = call_with_retries(provider, prompt_text, seed)
    except FatalAPIError:
        raise
    except Exception as e:
        print(f" [X] Failed {task_name}: {e}")
        return {"status": "error", "error": str(e)}

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(code)

    if metadata["truncated"]:
        print(
            f" [!] Generated {task_name}.py but it hit the"
            f" {MAX_TOKENS}-token limit (may be truncated)"
        )
    else:
        print(f" [✓] Generated {task_name}.py ({metadata['model_version']})")

    return {"status": "ok", **metadata}


def run_provider(provider_cls, prompt_files, args):
    model_dir = os.path.join(
        OUTPUT_BASE_DIR, provider_cls.model.replace(":", "_").replace("/", "_")
    )

    if args.dry_run:
        print(f"\n[{provider_cls.name}] model {provider_cls.model} -> {model_dir}")
        for run_num in range(1, NUM_REPETITIONS + 1):
            print(f"  run_{run_num}: {provider_cls.settings(BASE_SEED + run_num)}")
        return

    if not os.environ.get(provider_cls.key_variable):
        print(f"Error: set {provider_cls.key_variable} before running {provider_cls.name}.")
        sys.exit(1)

    provider = provider_cls()
    os.makedirs(model_dir, exist_ok=True)

    manifest = {
        "provider": provider_cls.name,
        "requested_model": provider_cls.model,
        "environment": {
            "os": platform.platform(),
            "python_version": platform.python_version(),
            "sdk": provider_cls.package,
            "sdk_version": package_version(provider_cls.package),
        },
        "started_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "prompts_dir": PROMPTS_DIR,
        "num_repetitions": NUM_REPETITIONS,
        "runs": {},
    }

    try:
        run_all(provider, model_dir, prompt_files, manifest, args.overwrite)
    except FatalAPIError as e:
        manifest["stopped_early"] = str(e)
        print(f"\n [X] Stopped {provider_cls.name}: {e}")
        print("     Fix the problem above, then rerun; existing outputs are kept.")
    except KeyboardInterrupt:
        manifest["stopped_early"] = "interrupted by user"
        write_manifest(manifest, model_dir)
        raise

    write_manifest(manifest, model_dir)


def run_all(provider, model_dir, prompt_files, manifest, overwrite):
    for run_num in range(1, NUM_REPETITIONS + 1):
        run_name = f"run_{run_num}"
        run_dir = os.path.join(model_dir, run_name)
        os.makedirs(run_dir, exist_ok=True)

        seed = BASE_SEED + run_num
        run_record = {"settings": provider.settings(seed), "outputs": {}}
        manifest["runs"][run_name] = run_record

        print(
            f"\n--- [{provider.name}: {provider.model}]"
            f" | [Run {run_num}/{NUM_REPETITIONS}] | [Seed {seed}] ---"
        )

        for prompt_path in prompt_files:
            task_name = os.path.splitext(os.path.basename(prompt_path))[0]
            run_record["outputs"][task_name] = generate_one(
                provider, prompt_path, run_dir, seed, overwrite
            )


def write_manifest(manifest, model_dir):
    versions = {
        output.get("model_version")
        for run in manifest["runs"].values()
        for output in run["outputs"].values()
        if output.get("model_version")
    }
    manifest["answered_by_model_versions"] = sorted(versions)
    manifest["finished_at"] = datetime.datetime.now().isoformat(timespec="seconds")

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_path = os.path.join(model_dir, f"generation_config_{stamp}.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    if len(versions) > 1:
        print(f" [!] Answers came from more than one model version: {sorted(versions)}")
    print(f"\nConfiguration recorded in {manifest_path}")


def main():
    args = parse_args()

    prompt_files = sorted(glob.glob(os.path.join(PROMPTS_DIR, "*.txt")))
    if not prompt_files:
        print(f"Error: No .txt files found in '{PROMPTS_DIR}'.")
        sys.exit(1)

    print(f"Found {len(prompt_files)} prompts.")

    for name in args.providers:
        run_provider(PROVIDERS[name], prompt_files, args)

    print("\n✓ API generation pipeline complete!")


if __name__ == "__main__":
    main()
