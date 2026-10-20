import ast
import glob
import os
import re
import sys

# The progress messages use ✓, which the default Windows console encoding cannot print.
sys.stdout.reconfigure(encoding="utf-8")


# ==================== TARGET CONFIGURATION ====================
# Set to True to clean ONLY the target files
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


def extract_python_code_blocks(text: str) -> str:
    """
    Extracts pure Python code from LLM Markdown responses.
    Filters out non-Python blocks (e.g. ```sh, ```bash) and joins valid Python code.
    """
    python_specific_pattern = r"```(?:python|py)\s*\n(.*?)\n```"
    specific_matches = re.findall(
        python_specific_pattern,
        text,
        re.DOTALL,
    )

    if specific_matches:
        blocks_to_check = specific_matches

    else:
        tagged_pattern = r"```([a-zA-Z0-9_-]*)\s*\n(.*?)\n```"
        tagged_matches = re.findall(
            tagged_pattern,
            text,
            re.DOTALL,
        )

        blocks_to_check = []

        for tag, content in tagged_matches:
            tag = tag.lower().strip()

            if tag in [
                "sh",
                "bash",
                "shell",
                "cmd",
                "powershell",
                "json",
                "yaml",
                "txt",
                "html",
                "css",
            ]:
                continue

            blocks_to_check.append(content)

    valid_blocks = []

    for block in blocks_to_check:
        clean_block = block.strip()

        try:
            ast.parse(clean_block)
            valid_blocks.append(clean_block)

        except SyntaxError:
            if any(
                k in clean_block
                for k in [
                    "def ",
                    "import ",
                    "class ",
                    "return ",
                    "if ",
                    "=",
                ]
            ):
                valid_blocks.append(clean_block)

    if valid_blocks:
        return "\n\n".join(valid_blocks)

    return text.strip()


class DocstringRemover(ast.NodeTransformer):
    """AST Transformer to remove docstrings from functions, classes, and modules."""

    def _remove_docstring(self, node):
        self.generic_visit(node)

        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

            if not node.body:
                node.body.append(ast.Pass())

        return node

    def visit_FunctionDef(self, node):
        return self._remove_docstring(node)

    def visit_AsyncFunctionDef(self, node):
        return self._remove_docstring(node)

    def visit_ClassDef(self, node):
        return self._remove_docstring(node)

    def visit_Module(self, node):
        return self._remove_docstring(node)


def clean_python_code(raw_text: str) -> str:
    code_only = extract_python_code_blocks(raw_text)

    try:
        tree = ast.parse(code_only)
        remover = DocstringRemover()
        clean_tree = remover.visit(tree)
        ast.fix_missing_locations(clean_tree)

        return ast.unparse(clean_tree)

    except Exception:
        lines = [
            line
            for line in code_only.splitlines()
            if not line.strip().startswith("#")
        ]

        return "\n".join(lines)


RAW_DIR = "./raw_outputs"
CLEAN_DIR = "./clean_outputs"

all_files = sorted(
    glob.glob(f"{RAW_DIR}/**/*.py", recursive=True)
)

python_files = []

for filepath in all_files:
    rel_path = os.path.relpath(filepath, RAW_DIR)
    parts = rel_path.split(os.sep)

    if len(parts) >= 3:
        model_folder, parent_run, filename = parts[0], parts[1], parts[2]

    else:
        filename = os.path.basename(filepath)
        parent_run = os.path.basename(os.path.dirname(filepath))
        model_folder = os.path.basename(
            os.path.dirname(
                os.path.dirname(filepath)
            )
        )

    if TARGET_ONLY:
        is_qwen = TARGET_MODEL_KEYWORD in model_folder.lower()
        is_target_pair = (filename, parent_run) in TARGET_PAIRS

        if is_qwen and is_target_pair:
            python_files.append(filepath)

    else:
        python_files.append(filepath)

print(
    f"Cleaning {len(python_files)} model output files"
    "..."
)

for raw_path in python_files:
    rel_path = os.path.relpath(raw_path, RAW_DIR)
    clean_path = os.path.join(CLEAN_DIR, rel_path)

    os.makedirs(
        os.path.dirname(clean_path),
        exist_ok=True,
    )

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned_code = clean_python_code(raw_text)

    with open(clean_path, "w", encoding="utf-8") as f:
        f.write(cleaned_code)

    print(f" [✓] Cleaned: {rel_path}")

print("\n✓ Cleaning complete!")