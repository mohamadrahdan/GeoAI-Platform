import os

EXCLUDE_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".vscode", "docs"}
INCLUDE_EXTENSIONS = {
    ".py",
    ".yml",
    ".yaml",
    ".txt",
    ".md",
    ".env",
    ".example",
    ".json",
    ".sh",
    ".toml",
    ".ini",
}
EXACT_MATCH_FILES = {"Dockerfile", "Makefile", ".dockerignore", ".gitignore"}

output_filename = "all_code.txt"
with open(output_filename, "w", encoding="utf-8") as outfile:
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file in (output_filename, "bundle.py", "tree.text"):
                continue
            if (
                any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS)
                or file in EXACT_MATCH_FILES
            ):
                file_path = os.path.join(root, file)
                outfile.write(f"\n\n{'='*50}\n")
                outfile.write(f"FILE PATH: {file_path}\n")
                outfile.write(f"{'='*50}\n\n")
                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"// Error reading file {file_path}: {e}\n")
print(f"Done! All updated source code combined into {output_filename}")
