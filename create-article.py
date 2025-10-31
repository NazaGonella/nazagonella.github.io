import subprocess
import sys
import os
from datetime import datetime

home_path : str = "./home.md"
articles_path : str = "./articles"

file_name : str = ""
article_title : str = ""

if len(sys.argv) != 3:
    print("Usage: python create-article.py <file_name> <article_title>")
    sys.exit(1)

file_name = sys.argv[1]
article_title = sys.argv[2]
header : str = f"""%{article_title}

<header>
    <a class="name" href="../../index.html">Nazareno Gonella</a><nav><a class="title" href="">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a> &nbsp;&nbsp; <a class="title" href="">CV</a></nav>
</header>

<hr />

## {article_title}

---
"""

today = datetime.now().strftime("%d/%m/%Y")
article_entry : str = f"{today}: [**{article_title}**](./articles/{file_name}/index.html) \n"

with open(home_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines.insert(-2, article_entry)

with open(home_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

os.makedirs(f"{articles_path}/{file_name}", exist_ok=True)

with open(f"{articles_path}/{file_name}/{file_name}.md", "w", encoding="utf-8") as f:
    f.write(header)


css_file = "../../style.css"

subprocess.run([
    "pandoc",
    "-s",
    home_path,
    "-o", "index.html",
    "--css", "./style.css",
    "-V", "title="
])

subprocess.run([
    "pandoc",
    "-s",
    f"{articles_path}/{file_name}/{file_name}.md",
    "-o", f"{articles_path}/{file_name}/index.html",
    "--css", "../../style.css",
    "-V", "title="
])
# pandoc -s <afile> -o index.html --css $HOME/css-styles/blog-style.css -V title=""

subprocess.run([
    "vim",
    f"{articles_path}/{file_name}/{file_name}.md"
])
