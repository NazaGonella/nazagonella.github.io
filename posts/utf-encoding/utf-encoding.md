%Decoding UTF-8

<header>
    <link rel="icon" href="/assets/favicon.svg" type="image/svg">
    <a class="author-name" href="/">Nazareno Gonella</a><nav><a class="title" href="/">BLOG</a> &nbsp;&nbsp; <a class="title" href="mailto:nazagonella2@gmail.com">CONTACT</a>
</header>

<hr />

<article>

## Decoding UTF-8

November 12, 2025

---

How do we represent characters in memory?

---

### Unicode is not just ASCII++

You probably know ASCII, characters represented by numbers from 0 to 127; you may also know Unicode, same thing as ASCII but expanded, right?
There is a slight difference. ASCII and Unicode are both *coded character sets*, they map abstract symbols to numeric values called *code points*. The way they differ is on how they store these code points in memory, what is called *encoding*. ASCII is both a coded character set and an encoding format. Unicode is NOT an encoding format.

---

### Simple Ways to Encode

ASCII is straightforward. These are small values; we can assign a byte for each code point, so the character with the code point `84` would be stored in a byte like `0101 0100`. The next plausible step for Unicode would be to do the same, we map the code point directly to bytes.

The problem arises from the number of characters in Unicode, over 150,000 characters that will need more than a single byte. This gets worse when you take into account the *codespace* of Unicode, which ranges from 0 to 1,114,111 code points[^1], or `U+0000` to `U+10FFFF` using Unicode notation.

UTF-32 solves this by assigning 4 bytes for each code point. Code point `84` would be stored as  `00 00 00 54` in hexadecimal. A string like `Dog` would be encoded this way:

- D: `0000 0000` `0000 0000` `0000 0000` `0100 0100`
- o: `0000 0000` `0000 0000` `0000 0000` `0110 1111`
- g: `0000 0000` `0000 0000` `0000 0000` `0110 0111`

You may notice the problem UTF-32 introduces. A lot of bytes go to waste when using the most common letters in the english alphabet. What in ASCII takes only 3 bytes to encode (dog), becomes 12 bytes with UTF-32. With this encoding, every character takes the same amount of bytes, so we call UTF-32 a *fixed-length* encoding.

---

### Complex Ways to Encode

Now let's look into UTF-8, which uses *variable-width* encoding.

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

In here, we store the number `1F60E` as presented in memory. This is NOT the way UTF-8 encodes. There are 4 bytes one next to the other, and nothing to indicate this is a whole one character. How do we know if this isn't 4 characters each one taking 1 byte? Or 2 characters of 2 bytes? Let's say we want to index the third character in a string. How would we do that?

It becomes necessary to define a more complex structure when working with variable-width encoding. An ideal encoding format will make it possible to identify where a character starts and where it ends in a string.

A document with UTF-8 encoding will have every byte either be a *leading byte*, which indicates the start of a character as well as how many bytes follow it; and a *continuation byte*, which is used to facilitate indexing and to detect if the sequence is valid UTF-8.

`U+1F60E` encoded with UTF-8 looks like this:

- `(11110)000`
- `(10)011111`
- `(10)011000`
- `(10)001110`

Inside the parentheses are the header bits. Just by looking at the header bits we can determine if we are in a leading or continuation byte.

Continuation bytes start with `10`. We look at continuation bytes to validate UTF-8. If the number of continuation bytes do not correspond to those indicated by the leading byte, we know it's invalid UTF-8.

Leading bytes consist of a sequence of ones followed by a zero. The number of ones indicate the total number of bytes used by the code point. In our emoji example we see the leading byte has header bits `11110`, so we can read the code point as one character of 4 bytes. This rule applies to all code points lengths except for those of 1 byte, the ASCII characters.

ASCII characters have a leading byte that start with zero, followed by the code point digits in binary. The letter `A` will be encoded in UTF-8 the same way as one would encode it in ASCII.[^2]

---

### The UTF-8 Structure

We can visualize UTF-8 with this table

| First code point | Last code point | Byte 1 | Byte 2 | Byte 3 | Byte 4 |
|------------------+-----------------+--------+--------+--------+--------|
| U+0000   | U+007F   | 0xxxxxxx |-|-|-|
| U+0080   | U+07FF   | 110xxxxx | 10xxxxxx |-|-|
| U+0800   | U+FFFF   | 1110xxxx | 10xxxxxx | 10xxxxxx |-|
| U+010000 | U+10FFFF | 11110xxx | 10xxxxxx | 10xxxxxx | 10xxxxxx |

The table contains the bytes with the header bits set. The `x` bits correspond to the code point value in binary, with leading zeroes for the remaining `x` bits.

---

### Combining characters

Unicode also supports special characters called *combining characters*, these are used 

Until now I've described that each character starts with a leading byte and cannot be larger than 4 bytes. So you might be confused when you encounter situations like this

---

### UTF-8 in Code

I wrote a function to decode Unicode code points to UTF-8

```
#include <stdio.h>

int CodepointToUTF8(unsigned int codepoint, unsigned char *output) {
    // codepoint: U+uvwxyz
    if (codepoint <= 0x7F) {
        output[0] = (char)codepoint;                            // (0)yyy zzzz
        output[1] = '\0';
        return 1;
    } else if (codepoint <= 0x7FF) {
        output[0] = (char)(0xC0 | ((codepoint >> 6) & 0x1F));   // (110)0 0000 | 000x xxyy = (110)x xxyy
        output[1] = (char)(0x80 | (codepoint & 0x3F));          // (10)00 0000 | 00yy zzzz = (10)yy zzzz
        output[2] = '\0';
        return 2;
    } else if (codepoint <= 0xFFFF) {
        output[0] = (char)(0xE0 | ((codepoint >> 12) & 0x0F));  // (1110) 0000 | 0000 wwww = (1110) wwww
        output[1] = (char)(0x80 | ((codepoint >> 6) & 0x3F));   // (10)00 0000 | 00xx xxyy = (10)xx xxyy
        output[2] = (char)(0x80 | (codepoint & 0x3F));          // (10)00 0000 | 00yy zzzz = (10)yy zzzz
        output[3] = '\0';
        return 3;
    } else if (codepoint <= 0x10FFFF) {
        output[0] = (char)(0xF0 | ((codepoint >> 18) & 0x07));  // (1111 0)000 | 0000 0uvv = (1111 0)uvv
        output[1] = (char)(0x80 | ((codepoint >> 12) & 0x3F));  // (10)00 0000 | 00vv wwww = (10)vv wwww
        output[2] = (char)(0x80 | ((codepoint >> 6) & 0x3F));   // (10)00 0000 | 00xx xxyy = (10)xx xxyy
        output[3] = (char)(0x80 | (codepoint & 0x3F));          // (10)00 0000 | 00yy zzzz = (10)yy zzzz
        output[4] = '\0';
        return 4;
    }

    // Invalid codepoint
    return 0;
}

int main(void) {
    unsigned char utf[5]; // The functions assigns 5 bytes max, including null terminator
    CodepointToUTF8(0x1F60E, utf);

    printf("%s\n", utf);    //  OUTPUT: 😎

    return 0;
}
```

[^1]: This doesn't mean all code points are assigned, some space is reserved for future use.
[^2]: One of the major benefits of using UTF-8 is backwards compatibility with ASCII.

</article>
