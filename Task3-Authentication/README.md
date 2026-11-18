# Secure Computer Systems – Task 3: Authentication

## XKCD-style password generator

`xkcd_password.py` generates a password of N random words (see [XKCD 936](https://xkcd.com/936)),
reports its entropy, and the number of random `[a-zA-Z0-9]` characters giving the same entropy.

### Requirements
- Python 3 (standard library only, no packages to install)
- Word list: `eff_large_wordlist.txt` from the EFF
  (https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt), placed in this folder

### Usage
```
python xkcd_password.py 4
python xkcd_password.py 6 --wordlist path/to/other_wordlist.txt
```

### Example output
```
<four random words>
4 RANDOM words from word list of 7776 words
Entropy: 51.70 bits
You need 8.68 RANDOM characters in [a-zA-Z0-9] to get the same entropy.
```

### How it works
- **Randomness:** words are picked with `secrets.choice`, which uses the operating system's
  cryptographically secure random generator (the `random` module is predictable).
- **Entropy:** N words chosen uniformly from W distinct words give W^N equally likely
  passwords, so `H = N · log2(W)` bits. The list is de-duplicated first, because duplicates
  would make the real entropy lower than the formula says.
- **Equivalent characters:** one random character from 62 symbols gives `log2(62) ≈ 5.954` bits,
  so `L = H / log2(62)` characters give the same entropy.
