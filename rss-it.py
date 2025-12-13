import subprocess
from pathlib import Path

markdown_files = [md for md in Path("./posts").rglob("*.md")]

print("\n### Converting to RSS ###")

md_string : list[str] = []

for md in markdown_files:
    md_string.append(str(md))
    print(md)

print("")

with open("rss.xml", "w", encoding="utf-8") as f:
    subprocess.run([
        "pandoc-rss", "-s",
        "-t", "Naza Gonella",
        "-d", "Hello and welcome to the feed!!",
        "-l", "https://ngonella.com/",
        *md_string
    ],
    stdout=f, check=True)
