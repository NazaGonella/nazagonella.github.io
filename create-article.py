import subprocess
import sys
import os
from datetime import datetime


if len(sys.argv) != 3:
    print("Usage: python create-article.py <file_name> <article_title>")
    sys.exit(1)

file_name = sys.argv[1]
article_title = sys.argv[2]

home_path : str = "./home.md"
articles_path : str = "./articles"


# creates the articles and article entry folder

os.makedirs(f"{articles_path}/{file_name}", exist_ok=True)


# def suffix(d):
#     return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

# date_header = datetime.now().strftime("%B {S}, %Y").replace('{S}', str(datetime.now().day) + suffix(datetime.now().day))
# creates the article md file, and inserts the header

date_header : datetime = datetime.now().strftime("%B {S}, %Y").replace('{S}', str(datetime.now().day))

header : str = f"""%{article_title}

<header>
    <a class="name" href="../../index.html">Nazareno Gonella</a><nav><a class="title" href="">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a> &nbsp;&nbsp; <a class="title" href="">CV</a></nav>
</header>

<hr />

## {article_title}

{date_header}

---
"""

with open(f"{articles_path}/{file_name}/{file_name}.md", "w", encoding="utf-8") as f:
    f.write(header)


# adds the article entry to home.md

date_entry = datetime.now().strftime("%d/%m/%Y")
article_entry : str = f"{date_entry}: [**{article_title}**](./articles/{file_name}/index.html)  \n"

with open(home_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines.insert(7, article_entry)

with open(home_path, "w", encoding="utf-8") as f:
    f.writelines(lines)


# converts home.md and article md file to html

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


subprocess.run([
    "vim",
    f"{articles_path}/{file_name}/{file_name}.md"
])
