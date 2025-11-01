%Setting Up a Simple Blog - Tools I Used

<header>
    <a class="name" href="../../index.html">Nazareno Gonella</a><nav><a class="title" href="../../index.html">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a> &nbsp;&nbsp; <a class="title" href="">CV</a></nav>
</header>

<hr />

## Setting Up a Simple Blog - Tools I Used

October 31st, 2025

---

The idea to start writing a blog has been in my mind for quite some time now, until today that I decided to get on with it. And what better way to start than writing about this same process?

---

### What Am I Looking For?

From the start I knew I wanted something simple, easy to maintain and quick to iterate. One of the major reasons I'm doing this is to structure my thinking when working on any type of project, and for that I need not be distracted by implementation details.

---

### Barebones

Still, I would like to have some formatting, as there were times I would take notes in plain text files for then to never come back to them. So I'm using the next closest thing, Markdown.

Now what I need is to convert this Markdown file into a HTML file, and after looking around through some posts on reddit, I found the [pandoc](https://pandoc.org/) document converter, which is exactly what I needed. For any `.md` file I just had to run `pandoc input.md -o index.html`. 

Pandoc utilizes an extended version of Markdown which comes in handy, as it includes support for tables, definition lists, footnotes, citations and even math.

It also supports *Metadata Blocks*, which allows including information such as `% title`, `% author` and `% date`. I will only be using `% title` since the tool requires it.

And there it was, just what I wanted, almost.

---

### The Looks

A plain HTML file with formatted text is a lot better than a plain text file, but unfortunately it doesn't look good on the portfolio. 

I need something simple, but still good looking. Luckily you can link a `.css` file to the output of pandoc using the `--css` argument. The problem is I don't have much experience using css, so it is time to look for references.

I really like [Fabien Sanglard's](https://fabiensanglard.net/) and [Steve Losh's](https://stevelosh.com/) websites. They are minimalistic, nice to look at, and easy to read. I appreciate how you can immediately see all the stuff the authors have been working on or pondering over the last couple of years as soon as you enter. With the help of inspect element and a couple of queries to ChatGPT, I ended up with a style I was happy with.

There was now a need for a nice header: css and Markdown alone wouldn't suffice. Fortunately, pandoc allows for HTML to be written into the Markdown file, which it then passes to the final output unchanged. I can now define a simple header to include on all the pages and ensure a concise style, but to achieve that I would have to copy and paste the same header everytime I create a new page. It would be nice to have some sort of page template.

---

### The Page Template

I went on and created `create-article.py`, a Python script that takes `<file-name>` and `<article-title>` as arguments. This script creates `<file-name>.md` and writes to it the metadata block `% <article-title>`, the page header and the article header with the date of when the article was created.[^1]

```
header_date : datetime = datetime.now().strftime("%B {S}, %Y").replace('{S}', str(datetime.now().day))

header : str = f"""%{article_title}

<header>
    <a class="name" href="../../index.html">Nazareno Gonella</a><nav><a class="title" href="">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a> &nbsp;&nbsp; <a class="title" href="">CV</a></nav>
</header>

<hr />

## {article_title}

{header_date}

---
"""

with open(f"{articles_path}/{file_name}/{file_name}.md", "w", encoding="utf-8") as f:
    f.write(header)
```

I also included in the script some code to add the article entry along with the date to the home page

```
home_path : str = "./home.md"
date_entry = datetime.now().strftime("%d/%m/%Y")
article_entry : str = f"{date_entry}: [**{article_title}**](./articles/{file_name}/index.html)  \n"

with open(home_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

lines.insert(7, article_entry)

with open(home_path, "w", encoding="utf-8") as f:
    f.writelines(lines)
```

And to convert both `home.md` and the article entry `.md` file to html
```
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

```

Notice I'm adding additional arguments to **pandoc**: `-s` introduces the headers and footers to make the output a standalone HTML document. `-V` sets the `title` variable to nothing, preventing it of adding the Metadata Block `% title` as a header in the document.

With this, I now have an easy way of creating new entries. How about working with them?

---

### Workflow

I will be using **vim** as my text editor. Markdown is not too complicated so 


[^1]: Actually,
