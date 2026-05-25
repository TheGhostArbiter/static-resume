# Brandon S. Clark — Audience-Routed Resume Site

> Not one resume. A system. Built for the way people actually hire.

Most resume sites force every reader through the same generic page. This one routes them to the version that fits how they actually evaluate candidates — and it does it in plain static HTML with no framework and no build step.

**Senior Software Engineer — AWS Backend / Cloud Platform.** Five years at Milwaukee Tool building serverless APIs, platform tooling, and data foundations. Prior: $85M payment portal, 1,200-hour automation, and full-stack product work across fintech and public sector.

**Live site:** [static-resume-9qq.pages.dev](https://static-resume-9qq.pages.dev/)

---

## The five entry points

| Page | Audience | What it does |
| ---- | -------- | ------------ |
| [Home](https://static-resume-9qq.pages.dev/) | First impression | Cinematic landing with mode routing, FX panel, swipe-to-switch atmospheres, command palette, theme toggle, and tailored link builder |
| [Atlas](https://static-resume-9qq.pages.dev/resume-atlas.html) | Recruiters / ATS | Classic document layout — clean, fast, print-to-PDF safe |
| [Signal](https://static-resume-9qq.pages.dev/resume-signal.html) | Hiring managers | Focus-filtered view with shareable URLs and copy-ready ATS text |
| [Proof Hub](https://static-resume-9qq.pages.dev/proof-hub.html) | Technical interviewers | Case studies, accomplishment inventory, JD matching, and bullet export |
| [Switchboard](https://static-resume-9qq.pages.dev/resume-switchboard.html) | Reduced-motion / conservative browsers | Low-motion, privacy-first routing hub |

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
- **11 atmospheres** (blue, crimson, emerald, violet, ghost, void, amethyst, neon-rose, chrome, prism, castle) across **5 visual effects** (fog, ocean, depth, lava, aurora) — Three.js + Vanta for the first three, custom canvas renderers for lava and aurora
- **FX panel** — glass-HUD toggle bank for cursor spotlight, 3D card tilt, click sparks, swipe-to-switch, and confetti, persisted to `localStorage` and synced across tabs
- **Swipe gestures** on the home page — full horizontal flick cycles atmospheres; swipe up opens the command palette; swipe down fires confetti
- **Command palette** (`⌘K` / `Ctrl+K`) for keyboard-first navigation
- Hero typing animation, availability badge, scroll-reveal stagger, click sparks, cursor spotlight
- Local browser storage for theme, atmosphere, effect, and FX preferences
- Structured data (JSON-LD), OG tags, favicons, sitemap, and robots.txt for SEO
- Cloudflare Pages deployment via GitHub Actions — every PR gets a sticky preview URL
- Headless-Chrome UI test suite (CDP over websockets) gating every deploy

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
├── index.html                 # Home — cinematic landing + routing
├── resume-atlas.html          # Atlas — recruiter-safe document resume
├── resume-signal.html         # Signal — hiring manager + focus filters
├── proof-hub.html             # Proof Hub — evidence layer + case studies
├── resume-switchboard.html    # Switchboard — low-motion fallback hub
├── shared-enhancements.js     # Cursor spotlight, 3D tilt, sparks (gated by BSC_FX)
├── resume-ats.txt             # Plain-text ATS-friendly resume
├── favicon.ico / favicon.svg / apple-touch-icon.png / og-image.png
├── robots.txt / sitemap.xml / _headers
├── tests/
│   ├── harness.py             # CDP-over-websocket Chrome driver
│   └── test_home.py           # 18 functional UI tests
└── .github/workflows/
    └── deploy.yml             # test → deploy → sticky PR preview comment
```

Intentionally flat. Each page owns its own markup, styling, and behavior; `shared-enhancements.js` is the one shared module and only adds optional desktop effects.

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

- [ ] `python3 tests/test_home.py` from the repo root — all 18 functional tests pass
- [ ] Home loads and routes correctly; `?plain=1` fallback works
- [ ] FX panel toggles each persist + visibly turn the corresponding effect on/off
- [ ] Horizontal swipe (or click-and-drag on desktop) cycles atmospheres in both directions
- [ ] Signal presets open with the right focus areas active
- [ ] Atlas prints cleanly to PDF
- [ ] Proof Hub filters, JD matching, and copy actions work
- [ ] Switchboard routes readers to the right mode
- [ ] Theme toggles behave consistently across all pages

CI runs the test suite on every push and PR automatically; a regression blocks deploy.

---

## Deployment

Pushes to `main` deploy to Cloudflare Pages via the `.github/workflows/deploy.yml` workflow. The workflow first runs the headless-Chrome test suite — if any test fails, the deploy step is skipped. Pull requests get an isolated preview deploy at a branch-aliased URL, with the link posted as a sticky comment that updates on every push.

```text
Production:  https://static-resume-9qq.pages.dev/
PR preview:  https://<branch-name>.static-resume-9qq.pages.dev/
```

Verify all five routes after deploy.

---

## If you're reviewing this repo as a hiring manager or interviewer

Start with **[Signal](https://static-resume-9qq.pages.dev/resume-signal.html)** or **[Proof Hub](https://static-resume-9qq.pages.dev/proof-hub.html)**.

If you're a recruiter, start with **[Atlas](https://static-resume-9qq.pages.dev/resume-atlas.html)**.
