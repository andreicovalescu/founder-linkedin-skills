# founder-linkedin-skills

Personal Claude skills for running LinkedIn as a startup founder or early
operator, SF-founder style. A tailored rebuild of
[linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill),
with rules learned the hard way baked in: never expose internal or
dashboard data in a public draft, never fabricate personal experience in a
comment, never claim founder-pitch authority you don't have yet, no em
dashes, and nothing here ever auto-posts to LinkedIn. Every skill hands
back a copy-ready draft; you paste it in yourself.

## What's here

| skill | what it does |
| --- | --- |
| `founder-post` | Turns one real idea, number, or moment into a full post draft, hook-driven, checked for AI tells. |
| `founder-comment` | Drafts comments on other people's posts: real posts, real links where findable, agree-first, backed by a researched fact instead of invented experience. |
| `founder-plan` | Plans the week: what to post, when, and a 10-person engagement list split into reach / peers / buyers. |

## Install

**In Claude Code, project-local:**

```bash
git clone <your-repo-url>
cp -r founder-linkedin-skills/skills/* .claude/skills/
```

**Global (all projects):**

```bash
cp -r founder-linkedin-skills/skills/* ~/.claude/skills/
```

**No Claude Code:** paste any single `SKILL.md` at the top of a chat and it
runs as a mode for that conversation.

## Adding more

The original pack also has profile scoring, DMs, inbox triage, carousels,
repurposing, a humanizer, and reply-thread sorting. Same shape (a folder
under `skills/` with its own `SKILL.md`) if you want to add tailored
versions of those later.
