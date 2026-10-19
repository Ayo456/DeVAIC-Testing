# DeVAIC-Testing
A GitHub Repository made to organize files that will be used for my Student Research Project. Various files will be kept and organized for testing, analysis, and review as I strive to learn more about AI-Generated code and understanding its safeties and vulnerablities.

## Models

| Model | Type | How it was run |
|---|---|---|
| ChatGPT | Closed | Vendor service (not run locally) |
| Gemini | Closed | Vendor service (not run locally) |
| Qwen2.5-Coder 32B | Open-weight | Locally via Ollama (`generate_local.py`) |
| Gemma 2 9B | Open-weight | Locally via Ollama (`generate_local.py`) |

## Repository layout

```
DeVAIC-Testing/
├── bottle_repo/                   # Functions taken from the Bottle web framework
│   ├── prompts/                   # 20 implementation-neutral prompt .txt files (FRG-3 instruction + task)
│   ├── human_code/                # Original human-written Bottle functions
│   ├── closed_source/
│   │   ├── chatgpt_code/          # ChatGPT outputs (*_gpt.py)
│   │   └── gemini_code/           # Gemini outputs (*_gemini.py)
│   └── open_weight/
│       └── qwen2.5-coder-32b/     # Qwen html_escape regenerations
│
├── bottle_repo_regen/             # Closed-model regenerations (3 per function)
│   ├── chatgpt/<function>/regen_1..3.py
│   └── gemini/<function>/regen_1..3.py
│
├── encode_repo/                   # Functions taken from the encode (httpx) project
│   ├── human_code/
│   ├── chatgpt_code/
│   └── gemini_code/
│
├── raw_outputs/                   # Unaltered local-model outputs (may include Markdown & comments)
│   ├── qwen2.5-coder_32b/run_1..3/
│   └── gemma2_9b/run_1..3/        # Each model folder also holds generation_config_*.json
│
├── clean_outputs/                 # Same layout as raw_outputs, cleaned to plain Python
│
├── generate_local.py              # Stateless Ollama batch generator (records its configuration)
├── strip_comments.py              # Markdown, comment, and docstring stripper
├── get_metrics.py                 # Radon & AST software metrics calculator
│
└── software_metrics.csv           # Software metrics dataset
```

## Pipeline

1. `python generate_local.py` – sends each prompt to each local model in a fresh chat
   (temperature 0.2, max 2048 output tokens, seed 42 + run number, 3 runs). Use
   `--models <tag>` to run a subset and `--overwrite` to replace existing outputs.
   The exact settings and model digest are written to `raw_outputs/<model>/generation_config_<timestamp>.json`.
2. `python strip_comments.py` – extracts the Python code from `raw_outputs/` and writes it to `clean_outputs/`.
3. `python get_metrics.py` – writes `software_metrics.csv` with, per file: SLOC, average/maximum
   cyclomatic complexity, maintainability index, maximum nesting depth,
   and the Halstead measures.

Requirements: `pip install ollama radon`, plus a running Ollama server with the models pulled.
