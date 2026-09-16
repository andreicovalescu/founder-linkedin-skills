---
name: founder-human
description: >-
  Use to clean a LinkedIn draft of AI-writing tells before it's posted:
  invisible characters, dash/quote typography, stock vocabulary, and a
  five-check human-ness score. Runs locally via two Python scripts.
---

# Founder Human

The reason the other skills in this pack are usable. Every draft that
comes out of founder-post, founder-comment, founder-carousel, or
founder-repurpose should pass through this before it goes anywhere.

Two scripts, no dependencies, nothing uploaded:

```bash
python3 skills/founder-human/humanize.py draft.txt --report
python3 skills/founder-human/detect.py draft.txt
python3 skills/founder-human/detect.py before.txt after.txt   # show the delta
```

## What `humanize.py` fixes automatically

- **Invisible characters**: zero-width spaces and joiners, word joiners,
  soft hyphens, byte-order marks, non-breaking spaces, Unicode tag
  characters. These don't come from a keyboard; they survive copy-paste
  and are invisible in any editor.
- **Typography**: em dash to comma, en dash to hyphen, curly quotes to
  straight, ellipsis to three dots.
- **Vocabulary**: a lexicon of common AI-writing stock phrases (delve,
  leverage, robust, "in today's fast-paced world," and so on) swapped for
  plain English, in `slop.json`, which is meant to be edited as the user's
  own ear for this improves.

## What gets flagged, not auto-fixed

"It's not just X, it's Y," hashtag walls, and reflex engagement bait
("Agree?", "Thoughts?") get flagged rather than rewritten, since fixing
sentence-level structure needs judgment a regex shouldn't make.

## The five checks (`detect.py`), scored 0-100, higher is more human

| check | what it measures |
| --- | --- |
| BURSTINESS | sentence-length variation; even-length sentences are a model tell |
| SPECIFICITY | numbers and named specifics per 100 words |
| SLOP DENSITY | lexicon hits per 100 words |
| FINGERPRINT | invisible characters, em dashes, curly quotes per 1,000 chars |
| VOICE | contractions, first person, structural tells |

The overall score weights the mean of the five at 60% and the single
weakest check at 40%, since a detector usually only needs one signal to
fire.

## The honest limits

These are local heuristics modeled on the signals public detectors are
believed to key on. They are not GPTZero, Originality, Copyleaks, or
Turnitin, don't call those services, and can't promise their verdicts.
Fixing what they measure tends to move real detector scores because
they're measuring related things, that's the whole claim, nothing
stronger.

## Output

Run `humanize.py --report` first and hand back the cleaned draft plus the
list of changes made and anything flagged for manual rewrite. Then run
`detect.py` and report the five scores, the overall verdict, and one line
on which check to address next if it isn't at PASS.
