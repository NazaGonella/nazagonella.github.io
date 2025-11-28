%Decoding the UTFs

<header>
    <link rel="icon" href="/assets/favicon.svg" type="image/svg">
    <a class="author-name" href="/">Nazareno Gonella</a>
    <nav>
        <a class="title" href="/">Blog</a>
        <span class="separator"></span>
        <a class="title" href="/about/">About</a>
        <span class="separator"></span>
        <a class="title" href="/resume/es/">Resume</a>
    </nav>
</header>

---

<article>

## Decoding the UTFs

November 12, 2025

---

How do we represent characters in memory?

Some days ago I found out that JSON supports Unicode e

---

### Unicode is not just ASCII++

You probably know ASCII, characters represented by numbers from 0 to 127; you may also know Unicode, same thing as ASCII but expanded, right?
There is a slight difference. ASCII and Unicode are both *coded character sets*, they map abstract symbols to numeric values called *code points*. The way they differ is on how they store these code points in memory, what is called *encoding*. ASCII is both a coded character set and an encoding format. Unicode itself is NOT an encoding format, in fact, it has multiple encodings.

---

### How ASCII does it

ASCII is straightforward. These are small values; we can assign a byte for each code point, so the character with the code point `84` would be stored in a byte like `0101 0100`. We can extend this idea to Unicode with a naive approach, mapping the code point directly to bytes.


The problem arises from the number of characters in Unicode, over 150,000 characters that will need more than a single byte. This gets worse when you take into account the *codespace* of Unicode, the total set of possible codepoints Unicode defines for present and future use, which ranges from 0 to 1,114,111 code points[^1], or `U+0000` to `U+10FFFF` using Unicode notation with the `U+` prefix.

---

### UTF-32: The Naive Approach

The UTF-32 encoding solves this by assigning 4 bytes for each code point. Code point `84` would be stored as  `00 00 00 54` in hexadecimal. A string like `Dog` would be encoded this way:

- D: `0000 0000` `0000 0000` `0000 0000` `0100 0100`
- o: `0000 0000` `0000 0000` `0000 0000` `0110 1111`
- g: `0000 0000` `0000 0000` `0000 0000` `0110 0111`

You may notice the problem UTF-32 introduces. A lot of bytes go to waste when using the most common letters in the english alphabet. What in ASCII takes only 3 bytes to encode (dog), becomes 12 bytes with UTF-32. With this encoding, every character takes the same amount of bytes, so we call UTF-32 a *fixed-length* encoding.

---

### UTF-16 and Surrogate Pairs

UTF-16 introduces *variable-width* encoding. Every code point is encoded as one or two 16 bit sequences.

Code points less than or equal to `U+FFFF`, corresponding to characters in the *Basic Multilingual Plane* (BMP), are directly encoded in a 16 bit unit.

For code points outside the BMP (greater than `U+FFFF`), UTF+16 uses *surrogate pairs*, each pair consist of two 16 bit values, the first one being the *high surrogate* followed by the *low surrogate*.

Surrogate pairs follow a simple formula for encoding the code points.

- Subtract 0x10000 to the code point (**U**), the result (**U'**) being a 20 bit-value in the `0x00000` - `0xFFFFF` range.
- **high surrogate** --> `0x1101100000000000` *OR* top ten bits of **U'**
- **low surrogate**  --> `0x1101110000000000` *OR* bottom ten bits of **U'**

So high surrogates have the form `0x110110xxxxxxxxxx` and low surrogates `0x0x110111xxxxxxxxxx`. The `x` bits are then filled with the code point value minus `0x10000`. This substraction allows to insert values from 0 to 2^20 - 1, an additional 1,048,576 code points.


---

### UTF-8: This is the Way

Now let's look into UTF-8, which uses *variable-width* encoding.

In UTF-8, the number of bytes it takes to store a code point correspond to the range of the value. Code points from `U+0000` to `U+007F` are stored in 1 byte, ranges from `U+0080` to `U+07FF` are stored in 2 bytes, and so on.

- `U+00000` - `U+00007F`: 1 Byte
- `U+00080` - `U+0007FF`: 2 Bytes
- `U+00800` - `U+00FFFF`: 3 Bytes
- `U+01000` - `U+10FFFF`: 4 Bytes

The Smiling Face with Sunglasses emoji 😎 corresponds to the Unicode code point `U+1F60E` which in UTF-8 uses 4 bytes. How would you encode this?

If we took the same encoding as UTF-32 there would 4 bytes one next to the other, and nothing to indicate this is a whole one character. How do we know if this isn't 4 characters each one taking 1 byte? Or 2 characters of 2 bytes? Let's say we want to index the third character in a string. How would we do that?

We need to to define a more complex structure when working with variable-width encoding. An ideal encoding format will make it possible to identify where a character starts and where it ends in a string.

A document with UTF-8 encoding will have every byte either be a *leading byte*, which indicates the start of a character as well as how many bytes follow it; or a *continuation byte*, which is used to help indexing and to detect if the sequence is valid UTF-8.

`U+1F60E` encoded with UTF-8 looks like this:

- `(11110)000`
- `(10)011111`
- `(10)011000`
- `(10)001110`

Inside the parentheses are the header bits. Just by looking at the header bits we can determine if we are in a leading or continuation byte.

Continuation bytes start with `10`. We look at continuation bytes to validate UTF-8. If the number of continuation bytes do not correspond to those indicated by the leading byte, we know it's invalid UTF-8.

Leading bytes consist of a sequence of ones followed by a zero. The number of ones indicate the total number of bytes used by the code point, including the leading byte. In our emoji example we see the leading byte has header bits `11110`, so we can read the code point as one character of 4 bytes. This rule applies to all code points lengths except for those of 1 byte, the ASCII characters.

ASCII characters have a leading byte that starts with zero, followed by the code point value. The letter `A` will be encoded in UTF-8 the same way as one would encode it in ASCII.[^2]

The rest of the bits are the data bits. These contain the code point value in binary, padded with leading zeros.

---

### The UTF-8 Structure

We can visualize UTF-8 with this table

| First code point | Last code point | Byte 1 | Byte 2 | Byte 3 | Byte 4 |
|------------------+-----------------+--------+--------+--------+--------|
| U+0000   | U+007F   | 0xxxxxxx |-|-|-|
| U+0080   | U+07FF   | 110xxxxx | 10xxxxxx |-|-|
| U+0800   | U+FFFF   | 1110xxxx | 10xxxxxx | 10xxxxxx |-|
| U+010000 | U+10FFFF | 11110xxx | 10xxxxxx | 10xxxxxx | 10xxxxxx |

The table contains the bytes with the header bits set. The `x` bits correspond to data bits holding the code point values.

---

### Combining characters

Not all characters have a direct visual representation (for example, control characters like the null terminator or line breaks), and not all characters have a single representation when encoded in Unicode. Believe it or not, the letters `é` and `é` don't share the same code point

```
c = "é"
c_utf = c.encode("utf-8")
print("byte length", len(c_utf))    # output: byte length 2
print(c_utf)                        # output: b'\xc3\xa9'

c = "é"
c_utf = c.encode("utf-8")
print("byte length", len(c_utf))    # output: byte length 3
print(c_utf)                        # output: b'e\xcc\x81'
```

What is going on? The answer to this is *combining characters*. These are special characters that modify preceding characters in order to create new variations.

In the first example, we are using a *precomposed character*, a character with a dedicated code point. In this case `é` has the code point `U+00E9`. In the next example, we are creating a combination of two characters for `é`, `U+0065` + `U+0301`, that is the letter `e` and the acute diacritic.

Most letters and symbols accept combining characters, and there is no limit to how many you can apply. This allows you to create some monstrous-looking characters that this site's font won't allow me to render properly, so I'm attaching an image

![[Zalgo text!](https://en.wikipedia.org/wiki/Zalgo_text)](https://upload.wikimedia.org/wikipedia/commons/4/4a/Zalgo_text_filter.png)

Now comes a new problem: How do we know if two strings are the same? They may look the same when printed but have totally different encodings. Luckily, Unicode defines *Unicode equivalence* to solve this issue.

Code points sequences are defined as **canonically equivalent** if they represent the same abstract character while also looking the same when displayed. In the last case `é` and `é` would be an example of this type of equivalence. When code points sequences are **compatible**, they might look similar, but are used in different contexts, as they represent different abstract characters. It is the case of `A` and `𝔸`. You understand the meaning of the word `𝔸mbiguous`, but the character `𝔸` is primarily used in mathematical texts.

Based on these equivalences the standard also defines *Unicode normalization*, to make sure that text sequences have the same code point equivalence. You can read more on types of normalization (and also about UTF-16 and other characters encodings I haven't mentioned) in this [article](https://mcilloni.ovh/2023/07/23/unicode-is-hard/) by Marco Cilloni.

---

### UTF-8 in Code

This C function decodes Unicode code points to UTF-8

```
#include <stdio.h>

int CodepointToUTF8(unsigned int codepoint, unsigned char *output) {
    // codepoint: U+uvwxyz
    if (codepoint <= 0x7F) {
        output[0] = (unsigned char)codepoint;                            // (0)yyy zzzz
        output[1] = '\0';
        return 1;
    } else if (codepoint <= 0x7FF) {
        output[0] = (unsigned char)(0xC0 | ((codepoint >> 6) & 0x1F));   // (110)0 0000 | 000x xxyy = (110)x xxyy
        output[1] = (unsigned char)(0x80 | (codepoint & 0x3F));          // (10)00 0000 | 00yy zzzz = (10)yy zzzz
        output[2] = '\0';
        return 2;
    } else if (codepoint <= 0xFFFF) {
        output[0] = (unsigned char)(0xE0 | ((codepoint >> 12) & 0x0F));  // (1110) 0000 | 0000 wwww = (1110) wwww
        output[1] = (unsigned char)(0x80 | ((codepoint >> 6) & 0x3F));   // (10)00 0000 | 00xx xxyy = (10)xx xxyy
        output[2] = (unsigned char)(0x80 | (codepoint & 0x3F));          // (10)00 0000 | 00yy zzzz = (10)yy zzzz
        output[3] = '\0';
        return 3;
    } else if (codepoint <= 0x10FFFF) {
        output[0] = (unsigned char)(0xF0 | ((codepoint >> 18) & 0x07));  // (1111 0)000 | 0000 0uvv = (1111 0)uvv
        output[1] = (unsigned char)(0x80 | ((codepoint >> 12) & 0x3F));  // (10)00 0000 | 00vv wwww = (10)vv wwww
        output[2] = (unsigned char)(0x80 | ((codepoint >> 6) & 0x3F));   // (10)00 0000 | 00xx xxyy = (10)xx xxyy
        output[3] = (unsigned char)(0x80 | (codepoint & 0x3F));          // (10)00 0000 | 00yy zzzz = (10)yy zzzz
        output[4] = '\0';
        return 4;
    }

    // Invalid codepoint
    return 0;
}

int main(void) {
    unsigned char utf[5]; // The functions assigns 4 bytes max, including null terminator
    CodepointToUTF8(0x1F60E, utf);

    printf("%s\n", utf);    //  OUTPUT: 😎

    return 0;
}
```

If we encode two code points in a sequence, first a base character and then a combining character, the sequence renders as a single displayed character

```
int main(void) {
    unsigned char utf[10];
    unsigned char* p = utf;

    p += CodepointToUTF8(0x0065, utf);
    CodepointToUTF8(0x0301, p);

    printf("%s\n", utf);    // OUTPUT: é

    return 0;
}
```

Hopefully you’ll now be able to make sense of a UTF-8 byte sequence the next time you stumble upon one.

[^1]: This doesn't mean all code points are assigned, some space is reserved for future use.
[^2]: One of the major benefits of using UTF-8 is backwards compatibility with ASCII.

</article>
