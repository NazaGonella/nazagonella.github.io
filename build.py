#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path

css_path : Path = Path("style.css").resolve()

template_path : Path = Path("template.html").resolve()

ignored_mds = [Path("./README.md")]         # will not apply to ALL Markdown files

markdown_files = [md for md in Path(".").rglob("*.md") if md not in ignored_mds]

paired_files = [(md, md.parent / "index.html") for md in markdown_files if md not in ignored_mds]   # target: index.html file in the same directory

print("### BUILD ###")

for md, html in paired_files:
    mod_time_md = md.stat().st_mtime
    if html.exists():
        mod_time_html = html.stat().st_mtime
        if mod_time_html >  mod_time_md:
            continue

    relative_path_css : str = os.path.relpath(css_path, start=html.parent)  # relative to html and md path

    """
    subprocess.run([
        "pandoc",
        "-s", str(md),
        "-o", str(html),
        "--css", relative_path_css,
        "-V", "title=",
        "-f", "markdown+pipe_tables"
    ])
    """

    subprocess.run([
        "pandoc", "-s", str(md),
        "-o", str(html),
        "--css", relative_path_css,
        "--template", "template.html",
        "-f", "markdown+pipe_tables"
    ])

    #pandoc home.md -o index.html --template=template.html

    print(md, "->", html)
