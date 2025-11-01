%Setting Up This Simple Blog - Tools I Used

<header>
    <a class="name" href="../../index.html">Nazareno Gonella</a><nav><a class="title" href="">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a> &nbsp;&nbsp; <a class="title" href="">CV</a></nav>
</header>

<hr />

## Setting Up This Simple Blog - Tools I Used

October 31st, 2025

---

The idea to start writing a blog has been in my mind for quite some time now, until today that I decided to get on with it. And what better way to start than writing about this same process?

---

### What Am I Looking For?

From the start I knew I wanted something simple, easy to maintain and fast to iterate with. One of the major reasons I'm doing this is to structure my thinking when working on personal projects or studying for university, and for that I need not to lose the focus on anything other than the writing.

Still, I would like to have some formatting, as there were times I would take notes in a plain text file for then to never come back to them. So I'm using the next closest thing, Markdown.

Now what I need is to convert this Markdown file into a HTML file, and after looking around for some converter recommendations on Reddit, I found pandoc, which is exactly what I needed, easy to use and fast. For any .md file I had I just had to run `pandoc input.md -o index.html`.

And there it was, all of just what I wanted, almost.

---

### The Looks

A plain HTML file with formatted text is a lot better than a plain text file, but unfortunately it doesn't look well on my portfolio. I need something simple, but still good looking. Luckily you can link a .css file to the output of pandoc using the `--css` argument. The problem is I'm not used at all to using css, so it is time to look for references.

I really like [Fabien Sanglard's](https://fabiensanglard.net/) and [Steve Losh's](https://stevelosh.com/) websites. They are minimalistic, nice to look at, and easy to read. I appreciate how you can immediately see all the stuff the authors have been working or pondering on the last couple of years as soon as you enter. The structure of these websites I will also be focusing on, not just the looks. So with the help of inspect element and a couple of queries to ChatGPT, I ended up with a style I was happy with.

There was now a need for a nice header: css and Markdown alone wouln't suffice. Fortunately pandoc allows for HTML to be written to the Markdown file, which then it passes to the final output unchanged. I can now define a simple header to include on all the pages to ensure a concise style, but to achieve that I would have to copy and paste the same header everytime I create a new page. It would be nice to have some sort of page template.

---

### Page Template

I went on and created `create-article.py`, a Python script that takes `<file-name>` and `<article-title>` as arguments. This script creates `<file-name>.md` and writes to it the pandoc markdown title `% <article-title>`, the page header, and the article header with the date when the article was created.

```
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
```
