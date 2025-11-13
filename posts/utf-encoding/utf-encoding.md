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
There is a slight difference. ASCII and Unicode are both *coded character sets*, they map abstract symbols to numeric values called *code points*. The way they differ is on how they store these code points in memory, this is what we call *encoding*. ASCII is both a coded character set and a encoding format.

---

### Easy ways to encode

ASCII is straightforward. These are not big numbers, we can assign a byte for each code point, so the character with the code point `84`, would be stored in a byte like `0101 0100`. The next plausible step for Unicode would be to do the same, we map the code point directly to bytes.

The problem arises from the number of characters in Unicode, 159,801 characters that will need more than a single byte. This gets worse when you take into account the *codespace* of Unicode, being the range of code points, from 0 to 1,114,111.[^1]

**UTF-32** solves this by assigning 4 bytes for each code point. Code point `84` would be stored as `0000 0000 0000 0000 0000 0000 0101 0100` in binary, or `00 00 00 54` in hexadecimal. A string like `Dog` would be encoded this way:

- D: `0000 0000 0000 0000 0000 0000 0100 0100`
- o: `0000 0000 0000 0000 0000 0000 0110 1111`
- g: `0000 0000 0000 0000 0000 0000 0110 0111`

You may notice the problem UTF-32 introduces. A lot of bytes go to waste when using the most common letters in the english alphabet. What in ASCII would take only 3 bytes to encode dog, we are using 12 bytes when encoding with UTF-32. With this encoding, every character takes the same amount of bytes, so we call UTF-32 a *fixed-length encoding*.

---

### Complex ways to encode

**UTF-8** fixes the fixed-length problem by using a *variable-width encoding*. 

Let's analyze the Smiling Face with Sunglasses emoji 😎. Unicode characters are usually represented in hexadecimal, in this case `U+1F60E`.

[^1]: Not all code points are assigned.

</article>
