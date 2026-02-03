+++
title = "All You Need to Know to Use yogen"
author = "Nazareno Gonella"
date = "2026-01-30"
template = "template-post"
section = "tutorials"
+++

---

Here is all you need to know to effectively use yogen.

The way you create a yogen site is by running *yogen create* followed by the name of your site.

The command will create the site folder, which contains the *content*, *static* and *templates* folder.

Most of your work, and the structure of the site, will be inside the content folder, where you'll spent most of your time.

Inside the content folder, we have some predefined files, that you are free to erase or modify as you please.

By default, we have the home page, an about page, and posts page, which contains an example post (show how the folders would look as urls).

Now we go inside the site folder, and we can build it by running *yogen build*.

As you can see, we've now created a build folder.

Inside, we can find the same folder structure as the content folder, but replacing Markdown files with HTML files.

Inside, we can find the same folder structure as the content folder, except that every Markdown file has been converted to HTML.

Also, we'll find some additional files, in this case: an icon, a css file, and a generated RSS file of your posts.

In this case, the icon and css files come from... the static folder!

When building the site, everything inside the static folder will be copied as is / verbatim.

Now, let's finally take a look at the site we've created.

To do that, we can start hosting the site by running *yogen serve* by default, it hosts at port 8000, but you can change that by giving an argument.