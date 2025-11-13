%Decoding UTF-8

<header>
    <link rel="icon" href="/assets/favicon.svg" type="image/svg">
    <a class="author-name" href="/">Nazareno Gonella</a><nav><a class="title" href="/">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a> &nbsp;&nbsp; <a class="title" href="/resume/">RESUME</a></nav>
</header>

<hr />

<article>

## Decoding UTF-8

November 12, 2025

---

How do we represent characters in memory?

---

You probably may know ASCI, characters represented by numbers from 0 to 127; you may also know Unicode, same thing as ASCII but expanded, right?
There is a slight difference. ASCII and Unicode are both *coded character sets*, they map abstract symbols to numeric values called *code points*. The way they differ is on how they store these code points in memory.

ASCII is straightforward. These are not big numbers, we can assign a byte for each code point, so the character with the code point `84`, would be stored in a byte like `0101 0100`. The next plausible step for Unicode would be to do the same, just store every code point to whatever amount of bytes we need.

Let's analyze the % Unicode character, Smiling Face with Sunglasses emoji 😎. Unicode characters are usually represented in hexadecimal, in this case 1F60E. We 

</article>
