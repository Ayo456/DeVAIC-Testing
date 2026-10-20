# DeVAIC-Testing
A GitHub Repository made to organize files that will be used for my Student Research Project. Various files will be kept and organized for testing, analysis, and review as I strive to learn more about AI-Generated code and understanding its safeties and vulnerablities.

## Models

| Model | Type | How it was run |
|---|---|---|
| ChatGPT (`gpt-4.1-2025-04-14`) | Closed | OpenAI API (`generate_api.py`) |
| Gemini (`gemini-2.5-flash`) | Closed | Gemini API (`generate_api.py`) |
| Qwen2.5-Coder 32B (`qwen2.5-coder:32b`, Q4_K_M) | Open-weight | Locally via Ollama (`generate_local.py`) |
| Gemma 2 9B (`gemma2:9b`, Q4_0) | Open-weight | Locally via Ollama (`generate_local.py`) |

All four models use the same prompts and settings: temperature 0.2, top_p 0.9, at most
2048 output tokens, seeds 43/44/45 for runs 1/2/3, and one independent request per prompt.
Earlier ChatGPT and Gemini outputs in `bottle_repo_regen/` were made in the web
interfaces, where model version and temperature are unknown; they are kept for reference only.

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
├── raw_outputs/                   # Unaltered model outputs (may include Markdown & comments)
│   ├── qwen2.5-coder_32b/run_1..3/
│   ├── gemma2_9b/run_1..3/
│   ├── gpt-4.1-2025-04-14/run_1..3/
│   └── gemini-2.5-flash/run_1..3/ # Each model folder also holds generation_config_*.json
│
├── clean_outputs/                 # Same layout as raw_outputs, cleaned to plain Python
│
├── generate_local.py              # Stateless Ollama batch generator (records its configuration)
├── generate_api.py                # Stateless OpenAI / Gemini API generator (records its configuration)
├── strip_comments.py              # Markdown, comment, and docstring stripper
├── get_metrics.py                 # Radon & AST software metrics calculator
│
└── software_metrics.csv           # Software metrics dataset
```

## Pipeline

1. `python generate_local.py` – sends each prompt to each local model in a fresh chat
   (temperature 0.2, max 2048 output tokens, seed 42 + run number, 3 runs). Use
   `--models <tag>` to run a subset and `--overwrite` to replace existing outputs.
   The log `raw_outputs/<model>/generation_config_<timestamp>.json` records the model tag, digest,
   quantization, every sampling setting and seed, the GPU and CPU, the Ollama version, and how much
   of the model was on the GPU.
2. `python generate_api.py` – the same for ChatGPT and Gemini through their APIs. Needs
   `OPENAI_API_KEY` and `GEMINI_API_KEY`. The log records the model version that answered each
   prompt (and OpenAI's `system_fingerprint`), the settings, finish reason and token counts.
   `--providers openai` or `--providers gemini` runs one; `--dry-run` shows the plan without calling.
3. `python strip_comments.py` – extracts the Python code from `raw_outputs/` and writes it to `clean_outputs/`.
4. `python get_metrics.py` – writes `software_metrics.csv` with, per file: SLOC, average/maximum
   cyclomatic complexity, maintainability index, maximum nesting depth,
   and the Halstead measures. Each row also carries the model version, quantization,
   temperature, seed and token limit it was generated with, read from the generation logs.

Requirements: `pip install ollama radon openai google-genai`, plus a running Ollama server with the models pulled.
