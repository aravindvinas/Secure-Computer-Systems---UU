#!/usr/bin/env python3
"""
xkcd_password.py - Generate an "XKCD-style" password (see https://xkcd.com/936)
and report its entropy.

An XKCD-style password is made of several words chosen uniformly at random
from a word list, e.g. "correct horse battery staple". The program:

  1. reads a word list and removes duplicates / unusable entries,
  2. picks N words at random using a cryptographically secure generator,
  3. computes the entropy of the password:   H = N * log2(W)
     where W is the number of distinct words in the list,
  4. computes how many random characters from [a-zA-Z0-9] (62 symbols)
     give the same entropy:                   L = H / log2(62)

Usage:
    python xkcd_password.py <number_of_words> [--wordlist FILE]

Example:
    python xkcd_password.py 4
    python xkcd_password.py 6 --wordlist eff_large_wordlist.txt
"""

import argparse
import math
import os
import secrets   # cryptographically secure randomness (NOT the 'random' module)
import sys

# Size of the alphabet [a-zA-Z0-9]: 26 lowercase + 26 uppercase + 10 digits
ALPHANUMERIC_SIZE = 26 + 26 + 10   # = 62

# Default word list: the EFF large word list placed next to this script
DEFAULT_WORDLIST = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "eff_large_wordlist.txt")


def load_words(path):
    """Read a word list file and return a sorted list of distinct words.

    Works with two common formats:
      - one word per line            (e.g. /usr/share/dict/words)
      - "<dice number> <word>"       (e.g. the EFF list: "11111  abacus")
    We take the LAST field on each line, keep only purely alphabetic words,
    and convert them to lower case. Duplicates are removed with a set, which
    matters: entropy is only correct if every word in the list is distinct.
    """
    words = set()
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            fields = line.split()
            if not fields:
                continue                      # skip empty lines
            word = fields[-1].lower()
            if word.isalpha():                # drop "o'clock", "t-shirt", numbers ...
                words.add(word)
    return sorted(words)


def entropy_bits(num_words, list_size):
    """Entropy of N words chosen independently and uniformly from W words.

    There are W^N equally likely passwords, so H = log2(W^N) = N * log2(W).
    """
    return num_words * math.log2(list_size)


def equivalent_random_chars(bits, alphabet_size=ALPHANUMERIC_SIZE):
    """Number of random characters from an alphabet giving the same entropy.

    One random character gives log2(alphabet_size) bits, so we need
    L = H / log2(alphabet_size) characters.
    """
    return bits / math.log2(alphabet_size)


def main():
    # --- 1. Read the command-line arguments ---------------------------------
    parser = argparse.ArgumentParser(
        description="Generate an XKCD-style password and report its entropy.")
    parser.add_argument("num_words", type=int,
                        help="how many words the password should contain")
    parser.add_argument("--wordlist", default=DEFAULT_WORDLIST,
                        help="path to the word list (default: %(default)s)")
    args = parser.parse_args()

    if args.num_words < 1:
        sys.exit("Error: the number of words must be at least 1.")

    # --- 2. Load the word list ----------------------------------------------
    try:
        words = load_words(args.wordlist)
    except OSError as e:
        sys.exit(f"Error: cannot read word list '{args.wordlist}': {e}")

    if len(words) < 2:
        sys.exit("Error: the word list must contain at least 2 distinct words.")

    # --- 3. Pick the words at random ----------------------------------------
    # secrets.choice uses the operating system's secure random generator,
    # so every word is equally likely and the choice cannot be predicted.
    password_words = [secrets.choice(words) for _ in range(args.num_words)]
    password = " ".join(password_words)

    # --- 4. Compute entropy and the equivalent number of characters ---------
    bits = entropy_bits(args.num_words, len(words))
    chars = equivalent_random_chars(bits)

    # --- 5. Report ----------------------------------------------------------
    print(password)
    print(f"{args.num_words} RANDOM words from word list of {len(words)} words")
    print(f"Entropy: {bits:.2f} bits")
    print(f"You need {chars:.2f} RANDOM characters in [a-zA-Z0-9] "
          f"to get the same entropy.")


if __name__ == "__main__":
    main()
