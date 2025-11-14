%Decoding UTF-8

<header>
    <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
    <link rel="shortcut icon" href="/assets/favicon.svg" type="image/svg+xml">
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

UTF-32 solves this by assigning 4 bytes for each code point. Code point `84` would be stored as `0000 0000 0000 0000 0000 0000 0101 0100` in binary, or `00 00 00 54` in hexadecimal. A string like `Dog` would be encoded this way:

- D: `0000 0000 0000 0000 0000 0000 0100 0100`
- o: `0000 0000 0000 0000 0000 0000 0110 1111`
- g: `0000 0000 0000 0000 0000 0000 0110 0111`

You may notice the problem UTF-32 introduces. A lot of bytes go to waste when using the most common letters in the english alphabet. What in ASCII takes only 3 bytes to encode (dog), becomes 12 bytes with UTF-32. With this encoding, every character takes the same amount of bytes, so we call UTF-32 a *fixed-length encoding*.

---

### UTF-8 Format

Now let's look into UTF-8, which uses *variable-width encoding*.

In UTF-8, the amount of bytes it takes to store a code point correspond to the range of the value. Code points from `U+0000` to `U+007F` are stored in 1 byte, ranges from `U+0080` to `U+207F` are stored in 2 bytes, and so on.

- U+00000 - U+00007F: 1 Bytes
- U+00080 - U+0007FF: 2 Bytes
- U+00800 - U+00FFFF: 3 Bytes
- U+01000 - U+10FFFF: 4 Bytes

The Smiling Face with Sunglasses emoji 😎 corresponds to the Unicode code point `U+1F60E` which, according to UTF-8, takes 4 bytes to store:

- 00: `0000 0000`
- 01: `0000 0001`
- F6: `1111 0110`
- 0E: `0000 1110`

In here, we store the number `1F60E` as presented in memory; this is NOT the way UTF-8 encodes. There are 4 bytes one next to the other, and nothing to indicate this is a whole one character. How do we know if this isn't 4 characters each one taking 1 byte? Or 2 characters of 2 bytes? Let's say we want to index the third character in a string. How would we do that?

It becomes necessary to define a more complex structure when working with variable-width encoding. An ideal encoding format will make it possible to index characters, as well as to identify where a character starts and where it ends in a byte stream.

A document with UTF-8 encoding will have every byte either be a *leading byte*, which indicates the start of a character as well as how many bytes follow it; and a *continuation byte*, which is used to facilitate indexing and to detect if the sequence is valid UTF-8.

`U+1F60E` encoded with UTF-8 will look like this:

- `(11110)000`
- `(10)011111`
- `(10)011000`
- `(10)001110`

Inside the parentheses are the header bits. Just by looking at the header bits of a byte we can determine if we are in a leading or continuation byte.

Continuation bytes start with `10`. We look at continuation bytes to validate UTF-8. If the number of continuation bytes do not correspond to those indicated by the leading byte, we know the sequence of bytes is invalid UTF-8.

Leading bytes consist of a sequence of ones followed by a zero. The number of ones indicate the total number of bytes used by the code point. In our emoji example we see the leading byte has header bits `11110`, so we can read the code point as one character of 4 bytes. This rule applies to all code points lengths except for those of 1 byte, the ASCII characters.

ASCII characters have a leading byte that start with zero, followed by the code point digits in binary. The letter `A` will be encoded in UTF-8 the same way as one would encode it in ASCII:

- U+0041: `(0)100 0001`

| First code point | Last code point | Byte 1 | Byte 2 | Byte 3 | Byte 4 |
|-+-+-+-+-+-|
|U+0000|U+007F|0yyyzzzz|-|-|-|
|U+0080|U+07FF|110xxxyy|10yyzzzz|-|-|
|U+0800|U+FFFF|1110wwww|10xxxxyy|10yyzzzz|-|
|U+010000|U+10FFFF|11110uvv|10vvwwww|10xxxxyy|10yyzzzz|


[^1]: Not all code points are assigned.

</article>
