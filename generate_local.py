import glob
import os
import sys
import ollama

# ==================== CONFIGURATION ====================
MODELS = ["gemma2:9b"] # qwen2.5-coder:32b for later
PROMPTS_DIR = "bottle_repo\\prompts" 
OUTPUT_BASE_DIR = "./raw_outputs"
NUM_REPETITIONS = 3
TEMPERATURE = 0.7
# =======================================================

prompt_files = sorted(glob.glob(os.path.join(PROMPTS_DIR, "*.txt")))

if not prompt_files:
    print(f"Error: No .txt files found in '{PROMPTS_DIR}'.")
    sys.exit(1)

print(
    f"Found {len(prompt_files)} prompts. Starting batch generation across"
    f" {len(MODELS)} models..."
)

for model in MODELS:
    clean_model_name = model.replace(":", "_").replace("/", "_")

    for run_num in range(1, NUM_REPETITIONS + 1):
        run_dir = os.path.join(
            OUTPUT_BASE_DIR,
            clean_model_name,
            f"run_{run_num}"
        )
        os.makedirs(run_dir, exist_ok=True)

        print(
            f"\n--- [Model: {model}] | [Run {run_num}/{NUM_REPETITIONS}] ---"
        )

        for prompt_path in prompt_files:
            task_name = os.path.splitext(os.path.basename(prompt_path))[0]
            output_filepath = os.path.join(run_dir, f"{task_name}.py")

            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_text = f.read().strip()

            try:
                # Completely stateless API call (fresh chat context)
                response = ollama.chat(
                    model=model,
                    messages=[{"role": "user", "content": prompt_text}],
                    options={"temperature": TEMPERATURE},
                )

                generated_code = response["message"]["content"]

                with open(output_filepath, "w", encoding="utf-8") as f:
                    f.write(generated_code)

                print(f" [✓] Generated {task_name}.py")

            except Exception as e:
                print(f" [X] Failed {task_name}: {e}")

print("\n✓ Local generation pipeline complete!")