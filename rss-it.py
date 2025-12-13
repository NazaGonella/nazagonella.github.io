import subprocess
from pathlib import Path

markdown_files = [md for md in Path("./posts").rglob("*.md")]

print("\n### Converting to RSS ###")

md_string : list[str] = []

for md in markdown_files:
    md_string.append(str(md))
    print(md)

print("")

with open("feed.xml", "w", encoding="utf-8") as f:
    subprocess.run([
        "pandoc-rss", "-s",
        "-t", "Naza Gonella Blog",
        "-d", "Hello and welcome to my feed!!",
        "-l", "https://ngonella.com/",
        "-w", "nazagonella2@gmail.com (Nazareno Gonella)",
        *md_string
    ],
    stdout=f, check=True)
