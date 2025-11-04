%Setting Up a Simple Blog - Tools I Used

<header>
    <a class="name" href="../../index.html">Nazareno Gonella</a><nav><a class="title" href="../../index.html">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a> &nbsp;&nbsp; <a class="title" href="">CV</a></nav>
</header>

<hr />

## Setting Up a Simple Blog - My Handmade Static Site Generator

October 31, 2025

---

You can check the repository [here](https://github.com/NazaGonella/yors-generator).

The idea to start writing a blog has been in my mind for quite some time now, until today that I decided to get on with it. And what better way to begin than writing about this same process?

---

### What Am I Looking For?

From the start I knew I wanted something simple, easy to maintain and quick to iterate. One of the major reasons I'm doing this is to structure my thinking when working on any type of project, and for that I need not be distracted by implementation details.

---

### Barebones

Still, I would like to have some formatting, as there were times I would take notes in plain text files for then to never come back to them. So I'm using the next closest thing, Markdown.

Now what I need is to convert this Markdown file into a HTML file. After looking around through some posts on reddit, I found the [pandoc](https://pandoc.org/) document converter, exactly what I needed. For any `.md` file I just had to run `pandoc input.md -o index.html`. 

Pandoc uses an extended version of Markdown which comes in handy, as it includes support for tables, definition lists, footnotes, citations and even math.  It also supports *Metadata Blocks*, which allows including information such as `% title`, `% author` and `% date`. I will only be using `% title` since the tool requires it.

And there it was, just what I wanted, almost.

---

### Not Stylish, Just Yet

A plain HTML file with formatted text is a lot better than a plain text file, but unfortunately it doesn't look good on the portfolio. 

I need something simple, but still good looking. Luckily you can link a `.css` file to the output of pandoc using the `--css` argument. The problem is I don't have much experience using css, so it is time to look for references.

I really like [Fabien Sanglard's](https://fabiensanglard.net/) and [Steve Losh's](https://stevelosh.com/) websites. They are minimalistic, nice to look at, and easy to read. I appreciate how you can immediately see all the stuff the authors have been working on or pondering over the last couple of years as soon as you enter. With the help of inspect element and a couple of queries to ChatGPT, I ended up with a style I was happy with.[^1]

There was now a need for a nice header: css and Markdown alone wouldn't suffice. Fortunately, pandoc allows for HTML to be written into the Markdown file, which it then passes to the final output unchanged. I can now define a simple header to include on all the pages and ensure a concise style, but to achieve that I would have to copy and paste the same header everytime I create a new page. It would be nice to have some sort of page template.

---

### The Page Template

I went on and created `create-post.py`, a Python script that takes `<file-name>` and `<post-title>` as arguments. This script creates `<file-name>.md` and writes to it the metadata block `% <post-title>`, the page header and the post header with the date of when the post was created.[^2]

```
header_date : datetime = datetime.now().strftime("%B {S}, %Y").replace('{S}', str(datetime.now().day))

header : str = f"""%{post_title}

<header>
    <a class="name" href="../../index.html">Nazareno Gonella</a><nav><a class="title" href="">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a> &nbsp;&nbsp; <a class="title" href="">CV</a></nav>
</header>

<hr />

## {post_title}

{header_date}

---
"""

with open(f"{posts_path}/{file_name}/{file_name}.md", "w", encoding="utf-8") as f:
    f.write(header)
```

I also included some code to add the post entry along with the date to the home page

```
home_path : str = "./home.md"
date_entry = datetime.now().strftime("%d/%m/%Y")
post_entry : str = f"{date_entry}: [**{post_title}**]({posts_path**}/{file_name}/index.html)  \n"

with open(home_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# hardcoded position
lines.insert(7, post_entry)

with open(home_path, "w", encoding="utf-8") as f:
    f.writelines(lines)
```

With this, I now have an easy way of creating new entries.

---

### Generating the Site

Calling pandoc for every `.md` file is not ideal. That's why I implemented `build.py`, a minimal build system for transforming recently modified Markdown files into HTML files.

```
import os
import subprocess
from pathlib import Path

css_path = Path("style.css").resolve()      # absolute path to CSS

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

    relative_path_css = os.path.relpath(css_path, start=html.parent)  # relative to html and md path

    subprocess.run([
        "pandoc",
        "-s", str(md),
        "-o", str(html),
        "--css", relative_path_css,
        "-V", "title="
    ])

    print(md, "->", html)
```

---

### Workflow

I will be using vim as my text editor, primarily for three reasons.

1. Fast and comfortable to write in.
2. Very customizable.
3. Looks cool.

Probably one of the most important aspects of using vim in this case is having the option to execute a command when saving the file. Thanks to this, I can now avoid having to call pandoc with the same arguments everytime I want to see the results on the browser. I just save the file and the HTML file is automatically generated.

I added the following to the `.vimrc`

```
autocmd BufWritePost *.md !pandoc -s % -o %:p:h/index.html --css style.css -V title=""
```

This will apply only when saving any file that ends with `.md`.

How about deployment? I just need to push my local files to the remote Github repository. The thing is, I don't want to deploy everytime I correct a minor mistake, it would make version control really uncomfortable.

To fix this I created a new `working` branch. Every change I make gets pushed to that branch, once I feel it's time to deploy, I overwrite the `master` branch.

I could also just merge both branches, but there is no need. For the time being I'm the only one pushing to the `master` branch, so the results of merging and overwriting are ultimately the same.

For easy deployment I made a simple shell script `deploy.sh`.

```
working_branch="working"

git checkout master
git reset --hard "$working_branch"
git push --force origin master

echo "Master branch updated"

git checkout "$working_branch"
```

---


And there it is, a simple framework for my use case. Every time I want to write about a new topic, I run `create-post.py` and start writing right away. Once I'm done, I simply save and check the browser. If I'm happy with the result, I commit, push to origin and then run `deploy.sh`. And just like that a new entry is added to the blog.

Initially, I wasn't familiar with the concept of static site generators. I've seen recommendations of tools like [Jekyll](https://jekyllrb.com/) or [Hugo](https://gohugo.io/) for easily creating personal websites, but I felt they were more than what I needed at the moment[^3]. I also liked the idea of creating a basic blog framework. What I ended up with was a custom static site generator. 

Now it's a matter of time to see how well this framework holds up for me.


[^1]: This stage took some time, tinkering with this kind of stuff can become dangerously addictive.
[^2]: It would make more sense for the date to be the day it's published.
[^3]: Reading Fabien Sanglard's post [All you may need is HTML](https://fabiensanglard.net/html/index.html) may have had an effect on this decision.

