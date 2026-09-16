#!/usr/bin/env python3
"""
founder-human / detect.py

Scores a draft against five local heuristics modeled on the signals public
AI-detectors key on. Not a detector API, not affiliated with or a
substitute for GPTZero/Originality/Copyleaks/Turnitin/etc. Runs entirely on
your machine; nothing is uploaded.

Usage:
    python3 detect.py draft.txt                  # score one file
    python3 detect.py before.txt after.txt        # score both, show the delta
"""

import json
import os
import re
import sys

INVISIBLE_CHARS = "​‌‍⁠­﻿  "


def load_lexicon():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slop.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def words(text):
    return re.findall(r"[A-Za-z0-9']+", text)


def burstiness(text):
    sents = sentences(text)
    if len(sents) < 2:
        return 50.0
    lengths = [len(words(s)) for s in sents]
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return 0.0
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    stdev = variance ** 0.5
    coeff_var = stdev / mean
    return min(100.0, coeff_var * 130)


def specificity(text):
    w = words(text)
    if not w:
        return 0.0
    numbers = len(re.findall(r"\b\d[\d,.]*\b", text))
    caps = len(re.findall(r"\b[A-Z][a-z]{2,}\b", text))
    per_100 = (numbers + caps) / (len(w) / 100)
    return min(100.0, per_100 * 8)


def slop_density(text, lexicon):
    w = words(text)
    if not w:
        return 100.0, 0, 0.0
    hits = 0
    text_lower = text.lower()
    for phrase in lexicon.get("phrases", {}):
        if "(" in phrase:
            continue
        hits += text_lower.count(phrase.lower())
    per_100 = hits / (len(w) / 100)
    score = max(0.0, 100.0 - per_100 * 8)
    return score, hits, per_100


def fingerprint(text):
    invisible = sum(text.count(c) for c in INVISIBLE_CHARS)
    em_dash = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    per_1000 = (invisible + em_dash + curly) / max(1, len(text) / 1000)
    score = max(0.0, 100.0 - per_1000 * 20)
    return score, invisible, em_dash, curly


def voice(text, lexicon):
    tells = 0
    for tell in lexicon.get("structural_tells", []):
        if tell.startswith("it's not just") and re.search(
            r"\bit'?s not (just|only)\b.{0,40}\bit'?s\b", text, re.IGNORECASE
        ):
            tells += 1
        elif tell.startswith("hashtag walls") and len(re.findall(r"#\w+", text)) > 3:
            tells += 1
        elif tell.startswith("reflex engagement") and re.search(
            r"\b(agree\?|thoughts\?)\s*$", text.strip(), re.IGNORECASE
        ):
            tells += 1
    contractions = len(re.findall(r"\b\w+'(t|re|ve|ll|d|s|m)\b", text, re.IGNORECASE))
    has_first_person = bool(re.search(r"\b(I|we|my|our)\b", text))
    score = 50.0
    score += min(30.0, contractions * 5)
    score += 20.0 if has_first_person else 0.0
    score -= tells * 16.7
    return max(0.0, min(100.0, score)), tells


def bar(value, width=24):
    filled = int(round(value / 100 * width))
    return "#" * filled + "." * (width - filled)


def score_file(path, lexicon):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    b = burstiness(text)
    s = specificity(text)
    sd, slop_hits, slop_per_100 = slop_density(text, lexicon)
    fp, invis, em, curly = fingerprint(text)
    v, tells = voice(text, lexicon)

    checks = {"BURSTINESS": b, "SPECIFICITY": s, "SLOP DENSITY": sd, "FINGERPRINT": fp, "VOICE": v}
    mean = sum(checks.values()) / len(checks)
    weakest = min(checks.values())
    human_score = mean * 0.6 + weakest * 0.4
    verdict = "PASS" if human_score >= 75 else "REVIEW" if human_score >= 50 else "FLAGGED"

    details = {
        "SLOP DENSITY": f"{slop_hits} stock terms, {slop_per_100:.1f} per 100 words",
        "FINGERPRINT": f"{invis} invisible, {em} em dash, {curly} curly quote",
        "VOICE": f"{tells} structural tell(s)",
    }

    print(f"\n{path}")
    for name, value in checks.items():
        detail = details.get(name, "")
        print(f"  {name:<13} {bar(value)}  {value:5.1f}   {detail}")
    print("  " + "-" * 62)
    print(f"  HUMAN SCORE   {bar(human_score)}  {human_score:5.1f}   {verdict}")
    return human_score


def main():
    if len(sys.argv) < 2:
        print("Usage: detect.py <file> [file2]")
        return 1
    lexicon = load_lexicon()
    scores = [score_file(p, lexicon) for p in sys.argv[1:3]]
    if len(scores) == 2:
        print(f"\nDelta: {scores[1] - scores[0]:+.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
