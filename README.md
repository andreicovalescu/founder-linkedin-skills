# founder-linkedin-skills

Eleven Claude skills for running LinkedIn as a startup founder or early
operator, SF-founder style. Free, no signup, no API key, nothing to
connect.

One turns one real idea into a post, off a set of hook formulas. One
drafts comments on other people's posts. One handles the replies under
your own. One scores your profile out of 100 and rewrites what's costing
points. One plans the week: what to post, when, and who to engage with.
One turns a video, newsletter, or transcript into a week of standalone
posts. One builds document/carousel posts slide by slide. One drafts
connection notes and DM sequences. One triages the inbox. One audits
what's already published, ranked by what actually worked.

And one is the humanizer, which is why the rest are usable. It strips
invisible characters, dash/quote typography, and stock AI-writing
vocabulary out of a draft, then scores what's left against a five-check
panel before it's posted.

**Nothing gets posted automatically.** Every skill hands back a
copy-ready draft. You paste it in yourself.

## Install

**In Claude Code, project-local:**

```bash
git clone https://github.com/andreicovalescu/founder-linkedin-skills.git
cp -r founder-linkedin-skills/skills/* .claude/skills/
```

**Global (all projects):**

```bash
cp -r founder-linkedin-skills/skills/* ~/.claude/skills/
```

**No Claude Code:** paste any single `SKILL.md` at the top of a chat and it
runs as a mode for that conversation. You lose the two Python scripts in
`founder-human`, which is most of the point of that one, but the rest
works.

Then spend ten minutes on `templates/voice.md`. Copy it to
`~/.claude/linkedin/voice.md` and fill it in, or paste three of your own
posts into Claude and say "write my voice.md from these." Every skill
reads that file. Skip it and everything comes out sounding like everyone
else.

## The eleven

| skill | what it does |
| --- | --- |
| `founder-post` | One idea into a full post draft, hook-driven, checked for AI tells. |
| `founder-comment` | Comments on other people's posts: real links where findable, agree-first, backed by a researched fact instead of invented experience. |
| `founder-reply` | Sorts the thread under your own post by who deserves a reply first, and drafts each. |
| `founder-plan` | Plans the week: what to post, when, and a 10-person engagement list split into reach / peers / buyers. |
| `founder-profile` | Scores your profile out of 100 against a fixed rubric, rewrites in fix-first order. |
| `founder-carousel` | Document posts: slide-by-slide copy, the cover that earns the swipe. |
| `founder-repurpose` | One video, newsletter, or transcript into a week of posts that each stand alone. |
| `founder-dm` | The connection note, first message, and follow-ups, sent only after real engagement. |
| `founder-inbox` | Triages the inbox into lead / recruiter / peer / ask / spam. |
| `founder-audit` | Post-mortem on what's already published, ranked by engagement rate, not impressions. |
| `founder-human` | The humanizer. Two scripts that actually run locally. See below. |

## The humanizer

`founder-human` ships two dependency-free Python scripts:

```bash
python3 skills/founder-human/humanize.py draft.txt --report   # clean it, show every change
python3 skills/founder-human/detect.py draft.txt               # score it, five checks
python3 skills/founder-human/detect.py before.txt after.txt    # prove the delta
```

What comes out automatically: invisible characters (zero-width spaces and
joiners, soft hyphens, byte-order marks, non-breaking spaces), dash and
quote typography (em dash to comma, curly quotes to straight), and a stock
AI-writing lexicon swapped for plain English, editable in `slop.json`.

What gets flagged instead of fixed: "it's not just X, it's Y," hashtag
walls, reflex engagement bait ("Agree?"), since changing sentence
structure needs judgment a script shouldn't make on its own.

Five checks, scored 0-100, higher is more human: **burstiness**
(sentence-length variation), **specificity** (numbers and named details
per 100 words), **slop density** (lexicon hits per 100 words),
**fingerprint** (invisible characters, em dashes, curly quotes per 1,000
characters), **voice** (contractions, first person, structural tells).
The overall score weights the mean at 60% and the weakest single check at
40%.

These are local heuristics modeled on the signals public detectors are
believed to use, not a call to GPTZero, Originality, Copyleaks, or
Turnitin, and not a promise of what those tools would say. Nothing here
claims "undetectable."

## The rules baked in everywhere

- Never expose internal or dashboard data in a public draft. If a number
  isn't public, it comes back as `{{number}}` with a flag, never invented
  and never pulled from a connected tool.
- Never fabricate personal experience in a comment or reply.
- Never claim founder-pitch authority someone hasn't earned yet: an
  employee with ownership writes from real ownership, not fundraising or
  build-in-public content, unless it's their own venture.
- No em dashes, ever.
- Nothing here ever auto-posts, auto-comments, or auto-sends anything to
  LinkedIn, under any framing.

## The fine print, which is the honest part

These skills do not post to LinkedIn, and they should not. There's no
official API for posting to a personal profile without an approved
partner app, and automating the site with a browser or a third-party tool
risks the account getting restricted. So every skill here ends the same
way: a copy-ready block, and you paste it. That's not a limitation bolted
on afterward, it's the design, and it's why the approval gate is real
instead of a setting.

The five checks in `founder-human` are local heuristics, not a detector
API. They're modeled on the signals public detectors are believed to key
on, and they run entirely on your machine. They are not GPTZero,
Originality, Copyleaks, or Turnitin, they don't call those services, and
they can't promise those verdicts. Fixing what they measure tends to move
those numbers too, because they're measuring related things. That's the
whole claim.

The invisible-character pass is real and narrow: it removes the
zero-width and format characters that end up in generated text and
survive a copy-paste. That's a genuine, checkable fingerprint. It's not a
claim about defeating a cryptographic watermark, and this repo doesn't
make one.

Nothing here fabricates. No invented metrics, clients, or outcomes go
under your name. If a draft needs a number you haven't given, it comes
back with `{{your number}}` and a flag, every time.

## Files
