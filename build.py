import os
import subprocess
from pathlib import Path

css_path: Path = Path("style.css").resolve()
ignored_mds = [Path("./README.md")]

markdown_files = [md for md in Path(".").rglob("*.md") if md not in ignored_mds]
paired_files = [(md, md.parent / "index.html") for md in markdown_files]

print("### BUILD ###")

for md, html in paired_files:
    if html.exists() and html.stat().st_mtime > md.stat().st_mtime:
        continue

    relative_path_css = os.path.relpath(css_path, start=html.parent)

    # extract front matter manually
    template_to_use = "template.html"  # default
    with md.open("r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines[0].strip() == "---":
            for line in lines[1:]:
                line = line.strip()
                if line == "---":
                    break
                if line.startswith("template:"):
                    template_to_use = line.split(":", 1)[1].strip()

    subprocess.run([
        "pandoc", "-s", str(md),
        "-o", str(html),
        "--css", relative_path_css,
        "--template", template_to_use,
        "-f", "markdown+pipe_tables"
    ])

    print(md, "->", html)
