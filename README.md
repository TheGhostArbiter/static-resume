# Brandon S. Clark — Audience-Routed Resume Site

> Not one resume. A system. Built for the way people actually hire.

Most resume sites force every reader through the same generic page. This one routes them to the version that fits how they actually evaluate candidates — and it does it in plain static HTML with no framework and no build step.

**Live site:** [theghostarbiter.github.io/static-resume](https://theghostarbiter.github.io/static-resume/)

---

## The five entry points

| Page | Audience | What it does |
|------|----------|--------------|
| [Home](https://theghostarbiter.github.io/static-resume/) | First impression | Cinematic landing with mode routing, theme toggle, and tailored link builder |
| [Atlas](https://theghostarbiter.github.io/static-resume/resume-atlas.html) | Recruiters / ATS | Classic document layout — clean, fast, print-to-PDF safe |
| [Signal](https://theghostarbiter.github.io/static-resume/resume-signal.html) | Hiring managers | Focus-filtered view with shareable URLs and copy-ready ATS text |
| [Proof Hub](https://theghostarbiter.github.io/static-resume/proof-hub.html) | Technical interviewers | Case studies, accomplishment inventory, JD matching, and bullet export |
| [Switchboard](https://theghostarbiter.github.io/static-resume/resume-switchboard.html) | Reduced-motion / conservative browsers | Low-motion, privacy-first routing hub |

---

## Why this exists

Hiring reviewers don't all want the same thing. A recruiter skimming in 20 seconds needs something different than a hiring manager prepping for a loop, which is different again from a technical interviewer who wants proof behind the bullets.

This repo solves that without making the candidate rewrite five separate resumes by hand.

The design principles:

- **Reader-first, not author-first.** Each mode is optimized for one specific audience, not for the convenience of maintaining a single file.
- **No framework tax.** Every page is standalone HTML, CSS, and vanilla JS — readable, forkable, and deployable to GitHub Pages in one push.
- **Depth on demand.** The Home and Switchboard pages explain where to go. Atlas gives a fast signal. Signal and Proof Hub reward closer reads.

---

## Signal — the interactive mode

Signal is the most powerful entry point for hiring managers and role-specific tailoring.

Focus filters let you surface the work most relevant to a given role without rewriting anything:

```text
resume-signal.html?focus=cloud,api
resume-signal.html?focus=iot,data
resume-signal.html?focus=leadership,enablement
resume-signal.html?focus=genai,ops
```

Each filtered URL is shareable and produces copy-ready ATS-formatted output for fast submissions.

---

## Tech

- Static HTML / CSS / Vanilla JavaScript — no framework, no build step
- Three.js + Vanta Fog on the cinematic home page
- Local browser storage for theme and routing preferences
- Structured data (JSON-LD), OG tags, sitemap, and robots.txt for SEO
- GitHub Pages deployment — commit and push to ship

---

## Run locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000/
```

Or use VS Code Live Server. Avoid opening via `file://` — query-string features, copy actions, and print flows all behave correctly on a local server.

---

## Repo structure

```text
.
├── index.html            # Home — cinematic landing + routing
├── resume-atlas.html     # Atlas — recruiter-safe document resume
├── resume-signal.html    # Signal — hiring manager + focus filters
├── proof-hub.html        # Proof Hub — evidence layer + case studies
└── resume-switchboard.html  # Switchboard — low-motion fallback hub
```

Intentionally flat. Each page owns its own markup, styling, and behavior.

---

## Editing guide

Content is intentionally repeated across pages so each mode stays optimized for its audience. When making content updates, touch all of the following:

- Header / contact details on every page
- Core summary language in Atlas, Signal, and Proof Hub
- Key metrics (keep numbers consistent across modes)
- Case studies and accomplishment inventory in Proof Hub
- Routing copy in Home and Switchboard
- Preset links that point into Signal

After editing, verify:

- [ ] Home loads and routes correctly; `?plain=1` fallback works
- [ ] Signal presets open with the right focus areas active
- [ ] Atlas prints cleanly to PDF
- [ ] Proof Hub filters, JD matching, and copy actions work
- [ ] Switchboard routes readers to the right mode
- [ ] Theme toggles behave consistently across all pages

---

## Deployment

Push to the repo's published branch. GitHub Pages handles the rest.

```text
https://theghostarbiter.github.io/static-resume/
```

Verify all five routes after deploy.

---

## If you're reviewing this repo as a hiring manager or interviewer

Start with **[Signal](https://theghostarbiter.github.io/static-resume/resume-signal.html)** or **[Proof Hub](https://theghostarbiter.github.io/static-resume/proof-hub.html)**.

If you're a recruiter, start with **[Atlas](https://theghostarbiter.github.io/static-resume/resume-atlas.html)**.
