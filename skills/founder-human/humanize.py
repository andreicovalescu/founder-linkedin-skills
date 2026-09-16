#!/usr/bin/env python3
"""
founder-human / humanize.py

Cleans a draft of common AI-writing fingerprints: invisible characters,
em/en dash and curly-quote typography, and a stock-phrase lexicon.
No dependencies. Runs entirely on your machine; nothing is uploaded.

Usage:
    python3 humanize.py draft.txt                # clean, write draft.clean.txt
    python3 humanize.py draft.txt --report        # clean, and print every change
    python3 humanize.py draft.txt -o out.txt       # choose output path
"""

import argparse
import json
import os
import re
import sys
import unicodedata

INVISIBLE_CHARS = {
    "​": "zero-width space",
    "‌": "zero-width non-joiner",
    "‍": "zero-width joiner",
    "⁠": "word joiner",
    "­": "soft hyphen",
    "﻿": "byte-order mark",
    " ": "non-breaking space",
    " ": "narrow no-break space",
}

TAG_CHAR_RANGE = (0xE0000, 0xE007F)


def load_lexicon():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slop.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def strip_invisibles(text, changes):
    out = []
    for ch in text:
        cp = ord(ch)
        if ch in INVISIBLE_CHARS:
            changes.append(f"removed {INVISIBLE_CHARS[ch]}")
            continue
        if TAG_CHAR_RANGE[0] <= cp <= TAG_CHAR_RANGE[1]:
            changes.append("removed Unicode tag character")
            continue
        out.append(ch)
    return "".join(out)


def fix_typography(text, changes):
    replacements = [
        ("—", ", ", "em dash to comma"),
        ("–", "-", "en dash to hyphen"),
        ("‘", "'", "curly single quote to straight"),
        ("’", "'", "curly single quote to straight"),
        ("“", '"', "curly double quote to straight"),
        ("”", '"', "curly double quote to straight"),
        ("…", "...", "ellipsis to three dots"),
    ]
    for old, new, label in replacements:
        count = text.count(old)
        if count:
            changes.append(f"{label} x{count}")
            text = text.replace(old, new)
    return text


def apply_lexicon(text, lexicon, changes):
    for phrase, replacement in lexicon.get("phrases", {}).items():
        if not phrase or "(" in phrase:
            continue
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)

        def _sub(match, replacement=replacement):
            original = match.group(0)
            if original.isupper():
                return replacement.upper()
            if original[:1].isupper():
                return replacement[:1].upper() + replacement[1:]
            return replacement

        new_text, count = pattern.subn(_sub, text)
        if count:
            changes.append(f'"{phrase}" -> "{replacement}" x{count}')
            text = new_text
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def flag_structural(text, lexicon):
    flags = []
    for tell in lexicon.get("structural_tells", []):
        if tell.startswith("it's not just"):
            if re.search(r"\bit'?s not (just|only)\b.{0,40}\bit'?s\b", text, re.IGNORECASE):
                flags.append(tell)
        elif tell.startswith("hashtag walls"):
            if len(re.findall(r"#\w+", text)) > 3:
                flags.append(tell)
        elif tell.startswith("reflex engagement"):
            if re.search(r"\b(agree\?|thoughts\?)\s*$", text.strip(), re.IGNORECASE):
                flags.append(tell)
    return flags


def main():
    parser = argparse.ArgumentParser(description="Clean AI-writing fingerprints from a draft.")
    parser.add_argument("file", help="path to the draft text file")
    parser.add_argument("-o", "--output", help="output path (default: <file>.clean.txt)")
    parser.add_argument("--report", action="store_true", help="print every change made")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    lexicon = load_lexicon()
    changes = []

    text = strip_invisibles(text, changes)
    text = fix_typography(text, changes)
    text = apply_lexicon(text, lexicon, changes)
    text = unicodedata.normalize("NFC", text)

    out_path = args.output or (os.path.splitext(args.file)[0] + ".clean.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    flags = flag_structural(text, lexicon)

    print(f"Cleaned draft written to {out_path}")
    if args.report:
        print(f"\n{len(changes)} change(s) made:")
        for c in changes:
            print(f"  - {c}")
    if flags:
        print(f"\n{len(flags)} structural issue(s) flagged for manual rewrite (not auto-fixed):")
        for fl in flags:
            print(f"  - {fl}")


if __name__ == "__main__":
    sys.exit(main())
