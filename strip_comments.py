import ast
import glob
import os
import re


def extract_python_code(text: str) -> str:
    """Extracts pure Python code from LLM Markdown responses."""
    pattern = r"```(?:python)?\s*\n(.*?)\n```"
    matches = re.findall(pattern, text, re.DOTALL)

    if matches:
        for match in matches:
            if "def " in match or "import " in match or "class " in match:
                return match.strip()

        return matches[0].strip()

    return text.strip()


class DocstringRemover(ast.NodeTransformer):
    """AST Transformer to remove docstrings from functions, classes, and modules."""

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        return node

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)

        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        return node

    def visit_ClassDef(self, node):
        self.generic_visit(node)

        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        return node

    def visit_Module(self, node):
        self.generic_visit(node)

        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

        return node


def clean_python_code(raw_text: str) -> str:
    # 1. Extract pure code block from Markdown
    code_only = extract_python_code(raw_text)

    # 2. Parse into AST to strip comments and docstrings
    try:
        tree = ast.parse(code_only)
        remover = DocstringRemover()
        clean_tree = remover.visit(tree)
        ast.fix_missing_locations(clean_tree)

        return ast.unparse(clean_tree)

    except Exception:
        # Fallback if syntax error occurs: strip '#' lines manually
        lines = [
            line
            for line in code_only.splitlines()
            if not line.strip().startswith("#")
        ]

        return "\n".join(lines)


RAW_DIR = "./raw_outputs"
CLEAN_DIR = "./clean_outputs"

python_files = glob.glob(f"{RAW_DIR}/**/*.py", recursive=True)

print(f"Cleaning {len(python_files)} Python files...")

for raw_path in python_files:
    rel_path = os.path.relpath(raw_path, RAW_DIR)
    clean_path = os.path.join(CLEAN_DIR, rel_path)

    os.makedirs(os.path.dirname(clean_path), exist_ok=True)

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned_code = clean_python_code(raw_text)

    with open(clean_path, "w", encoding="utf-8") as f:
        f.write(cleaned_code)

    print(f" [✓] Cleaned: {rel_path}")

print(
    "\n✓ Cleaning complete! All markdown text, comments, and docstrings"
    " removed."
)