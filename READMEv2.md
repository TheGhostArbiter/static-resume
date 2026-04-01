# static-resume

Audience-routed static resume site for **Brandon S. Clark**.

This repo is not a single resume page. It is a small, purpose-built resume system with multiple entry points for different readers:

- **Atlas** for recruiters, ATS uploads, and print/PDF review
- **Signal** for hiring managers and tailored technical reads
- **Proof Hub** for case studies, hard evidence, and bullet-bank depth
- **Switchboard** for low-motion, privacy-first routing
- **Home** for a more branded, cinematic landing experience

## Live site

- Home: <https://theghostarbiter.github.io/static-resume/>
- Atlas: <https://theghostarbiter.github.io/static-resume/resume-atlas.html>
- Signal: <https://theghostarbiter.github.io/static-resume/resume-signal.html>
- Proof Hub: <https://theghostarbiter.github.io/static-resume/proof-hub.html>
- Switchboard: <https://theghostarbiter.github.io/static-resume/resume-switchboard.html>

## What this repo is optimizing for

Most resume sites force every reader through the same path. This one does the opposite.

The goal is to let each reviewer land on the version that fits how they actually evaluate candidates:

- **Recruiters** get a fast, classic, ATS-friendly scan
- **Hiring managers** get a focused, role-tailored view
- **Technical interviewers** get evidence, case studies, and deeper execution detail
- **Low-motion / conservative-browser readers** get a simpler fallback hub

## Resume modes

### 1) Home (`index.html`)
The presentation-heavy landing page.

Use this when you want a stronger first impression, a cinematic intro, and fast routing into the right resume mode.

Highlights:
- mode-based routing to Atlas, Signal, Proof Hub, and Switchboard
- plain-mode fallback for safer/reduced-motion sharing
- theme toggle and atmosphere palette
- one-click Signal presets and a tailored link builder

### 2) Atlas (`resume-atlas.html`)
The recruiter-safe, document-style resume.

Use this when you need:
- a traditional resume layout
- quick screening
- print / save-as-PDF behavior
- the safest all-purpose version for uploads and attachments

### 3) Signal (`resume-signal.html`)
The interactive, hiring-manager-first resume.

Use this when you want to tailor emphasis without rewriting the whole resume.

Highlights:
- focus filters for areas like cloud, APIs, IoT, data, ops, leadership, enablement, and GenAI
- shareable filtered URLs
- copy-ready ATS text
- print / save-as-PDF support
- fast role-specific presets

Example:

```text
resume-signal.html?focus=cloud,api
```

### 4) Proof Hub (`proof-hub.html`)
The evidence layer under the resume.

Use this when someone wants proof behind the headline bullets.

Highlights:
- recruiter pack and 60-second pitch helpers
- job-description matching
- bullet selection + ATS/Markdown export
- case studies and accomplishment inventory
- public-safe sharing mode for external audiences

### 5) Switchboard (`resume-switchboard.html`)
The low-motion, routing-first fallback hub.

Use this when you want a simple share-safe entry point that explains where each reader should go next.

Best for:
- reduced-motion readers
- conservative browsers
- “send one link and let them choose” scenarios

## Repo structure

```text
.
├── README.md
├── index.html
├── proof-hub.html
├── resume-atlas.html
├── resume-signal.html
└── resume-switchboard.html
```

This repo is intentionally flat. Each page is a standalone HTML document with its own markup, styling, and behavior.

## Tech approach

- **Static HTML/CSS/JavaScript**
- **No app framework required**
- **No build step required for day-to-day edits**
- **GitHub Pages-friendly deployment model**
- **Three.js + Vanta Fog** used on the cinematic home page only
- **Local browser storage** used for theme and last-used mode preferences

## Run locally

Because this repo is fully static, you can preview it with any simple local server.

### Option 1: Python

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

### Option 2: VS Code Live Server
Open the repo folder and launch `index.html` with Live Server.

> Tip: use a local server instead of `file://` so features like query-string testing, copy actions, and print flows behave more like the live site.

## Editing guide

Because this project is **reader-first**, some content is intentionally repeated across multiple pages. That makes the experience better for each audience, but it also means content updates usually touch more than one file.

### Update these together

When making content changes, check all of the following:

- **Header/contact details** across every page
- **Core summary language** in Atlas, Signal, and Proof Hub
- **Key metrics** so the same numbers stay consistent everywhere
- **Case studies / accomplishment inventory** in Proof Hub
- **Routing copy** in Home and Switchboard
- **Preset links** that point into Signal

### After editing, test these flows

- Home page loads and routes correctly
- `?plain=1` works on the home page
- Signal presets open with the right focus areas selected
- Atlas prints cleanly to PDF
- Proof Hub filters, JD matching, and copy actions still work
- Switchboard still routes readers to the right mode
- Theme toggles still behave consistently across pages

## Content maintenance philosophy

This repo favors **clarity for the reader** over strict DRY reuse.

That is a deliberate tradeoff.

Duplicating selected content across modes makes each page stronger in context:
- Atlas stays linear and recruiter-friendly
- Signal stays tailored and interactive
- Proof Hub stays evidence-heavy
- Switchboard stays fast and directive

If this repo ever grows much larger, the next evolution would be moving shared content into a lightweight data source or generation step. For the current size, hand-authored static pages keep the site easy to reason about and easy to ship.

## Privacy / UX notes

This site is designed to stay simple and respectful:

- no login
- no backend
- local, browser-side state for theme and routing preferences
- reduced-motion and fallback paths available
- explicit print/PDF-friendly routes

## Deployment

This project is intended to be published as a static site.

Current live URL:

```text
https://theghostarbiter.github.io/static-resume/
```

If you are publishing changes through GitHub Pages:

1. commit your edits
2. push to the repo’s published branch
3. verify the live routes listed above
4. test Home, Atlas, Signal, Proof Hub, and Switchboard after deploy

## Notes for future improvements

Potential next steps if this repo keeps growing:

- move repeated resume content into shared JSON/YAML data
- add a lightweight build step for synchronization across modes
- add screenshots/previews to this README
- add a license if the repo is meant to be reused as a template
- add automated link checks for the cross-page routes

---

If you are reviewing this repo as a hiring manager or technical interviewer, start with **Signal** or **Proof Hub**.
If you are reviewing it as a recruiter, start with **Atlas**.
