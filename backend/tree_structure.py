import os

IGNORE = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    ".mypy_cache",
    ".pytest_cache",
    ".idea",
    ".vscode",
    ".DS_Store",
    ".coverage",
    ".env",
    ".blackignore",
    ".gitignore",
    ".ruff_cache",
}
IGNORE_EXTENSIONS = {".pyc", ".pyo", ".log"}

MAX_DEPTH = 4


def print_tree(root, prefix="", depth=0):
    if depth > MAX_DEPTH:
        return

    entries = sorted(os.listdir(root))
    for i, entry in enumerate(entries):
        path = os.path.join(root, entry)

        # Пропускаем ненужные файлы и папки
        if entry in IGNORE or any(entry.endswith(ext) for ext in IGNORE_EXTENSIONS):
            continue

        connector = "└── " if i == len(entries) - 1 else "├── "
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if i == len(entries) - 1 else "│   "
            print_tree(path, prefix + extension, depth + 1)


if __name__ == "__main__":
    print("Project structure:\n")
    print("Scanning path:", os.path.abspath("."))
    print_tree(".")
