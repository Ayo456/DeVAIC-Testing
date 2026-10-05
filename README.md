# DeVAIC-Testing
A GitHub Repository made to organize files that will be used for my Student Research Project. Various files will be kept and organized for testing, analysis, and review as I strive to learn more about AI-Generated code and understanding its safeties and vulnerablities.


DeVAIC-Testing/
├── prompts/                     # 20 implementation-neutral prompt .txt files
│
├── raw_outputs/                 # Unaltered AI outputs (includes Markdown & comments)
│   ├── qwen2.5-coder_32b/       # Runs 1, 2, and 3
│   ├── gemma2_9b/               # Runs 1, 2, and 3
│   ├── chatgpt/                 # Runs 1, 2, and 3
│   └── gemini/                  # Runs 1, 2, and 3
│
├── clean_outputs/               # AST-cleaned executable Python code
│
├── 01_generate_local.py         # Stateless Ollama batch generator
├── 02_strip_comments.py         # Markdown, comment, and docstring stripper
├── 03_get_metrics.py            # Radon & Pylint software metrics calculator
│
└── software_metrics.csv         # Master software metrics dataset