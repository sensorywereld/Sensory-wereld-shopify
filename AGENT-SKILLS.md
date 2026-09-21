# Agent-skills — inventaris en overdracht

Stand: 21 september 2026. Dit document staat in **elk** van de vier repo's van
`sensorywereld` en is overal identiek.

Het bestaat om één misverstand te voorkomen bij de overdracht naar Codex of naar
een nieuwe machine:

> ⚠ **Er zit geen enkele skill in deze repo's.** Alles wat hieronder staat is
> geïnstalleerd op **gebruikersniveau** in `~/.claude/` op één laptop. Wie deze
> repo kloont krijgt de code, en geen van de werkwijzen. Ze reizen niet mee.

Er is in geen van de projecten een `.claude/skills/`-map. Wat er is, zijn twee
Claude Code-**plugins**, allebei `scope: user`, dus actief in álle projecten
tegelijk — Bouw365, Sensory Wereld en de rest.

---

## 1. De twee geïnstalleerde plugins

| plugin | versie | bron | commit | geïnstalleerd |
|---|---|---|---|---|
| `superpowers` | 6.3.0 | GitHub `obra/superpowers` | `b36e082` | 18-08-2026 |
| `claude-video-vision` | 1.2.0 | `https://github.com/jordanrendric/claude-video-vision.git` | `5c8bc7b` | 21-05-2026 |

Marktplaatsen heten lokaal `superpowers-dev` en `claude-video-vision`.
Installatiepad: `~/.claude/plugins/cache/<marktplaats>/<plugin>/<versie>/`.
De boekhouding staat in `~/.claude/plugins/installed_plugins.json` en
`known_marketplaces.json`.

**Opnieuw installeren in Claude Code** (controleer de exacte vorm met `/plugin`):

```
/plugin marketplace add obra/superpowers
/plugin install superpowers@superpowers-dev

/plugin marketplace add https://github.com/jordanrendric/claude-video-vision.git
/plugin install claude-video-vision@claude-video-vision
```

## 2. De vijftien skills

Veertien komen uit `superpowers`, één uit `claude-video-vision`. De
omschrijvingen zijn letterlijk overgenomen uit de `SKILL.md`-frontmatter.

### Procesketen — de volgorde waarin ze elkaar oproepen

| skill | wanneer |
|---|---|
| `using-superpowers` | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions |
| `brainstorming` | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task, before touching code |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session |
| `executing-plans` | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| `finishing-a-development-branch` | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work |

### Kwaliteit en controle

| skill | wanneer |
|---|---|
| `test-driven-development` | Use when implementing any feature or bugfix, before writing implementation code |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation |

### Gereedschap

| skill | wanneer |
|---|---|
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans |
| `dispatching-parallel-agents` | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `writing-skills` | Use when creating new skills, editing existing skills, or verifying skills work before deployment |
| `video-perception` | Use when the user mentions a video file (.mp4, .mov, .avi, .mkv, .webm), a YouTube URL, asks to watch/analyze/review a video, or references video content in conversation |

## 3. Wat hier NIET in staat

Claude Code levert daarnaast **ingebouwde** skills mee (onder meer
`artifact-design` en `run`). Die zijn niet geïnstalleerd, staan nergens in een
map die je kunt kopiëren, en horen bij de Claude Code-versie zelf. Ze zijn dus
niet over te dragen — noch naar Codex, noch naar een nieuwe machine.

## 4. Overdragen aan Codex

Codex kent het plugin-systeem van Claude Code niet. Wat je wél kunt doen:

1. **De inhoud is gewone markdown.** Elke skill is één `SKILL.md` onder
   `~/.claude/plugins/cache/superpowers-dev/superpowers/6.3.0/skills/<naam>/`.
   Wil je dat Codex volgens dezelfde werkwijze werkt, kopieer dan de `SKILL.md`
   van de skills die er voor jou toe doen de repo in en verwijs ernaar vanuit
   `AGENTS.md`.
2. **Begin klein.** De drie die hier in de praktijk het meeste verschil maakten:
   `systematic-debugging` (geen fix voordat de oorzaak vaststaat),
   `verification-before-completion` (bewijs vóór de bewering) en
   `brainstorming` (ontwerp en akkoord vóór implementatie).
3. **Codex leest `AGENTS.md`, Claude leest `CLAUDE.md`.** Zie hieronder.

## 5. Welke repo welk instructiebestand heeft

Codex leest `AGENTS.md`, Claude leest `CLAUDE.md`. Alle vier de repo's gebruiken
nu hetzelfde patroon: een `CLAUDE.md` van één regel (`@AGENTS.md`) met de echte
inhoud in `AGENTS.md`, zodat beide agents dezelfde instructies zien en er niets
op twee plekken uit elkaar kan lopen.

| repo | `CLAUDE.md` | `AGENTS.md` |
|---|---|---|
| `bouw365` | 1 regel: `@AGENTS.md` | de niet-onderhandelbare regels + stack + bouwvolgorde |
| `bouw365-admin` | 1 regel: `@AGENTS.md` | het Next.js-blok |
| `collectief-schoonmaak` | 1 regel: `@AGENTS.md` | het Next.js-blok |
| `Sensory-wereld-shopify` | ⛔ ontbreekt | 360 regels: merk, oprichter, tone of voice, non-negotiables |

Tot 21-09-2026 had `bouw365` alleen een `CLAUDE.md`. Codex liep die repo dus
binnen zonder de regels te zien die erin staan: tenant-isolatie op elke tabel,
geld altijd als `Decimal`, immutable snapshots voor verzonden offertes en
facturen, en nooit queryen via `DATABASE_URL` (die rol heeft op Neon
`BYPASSRLS` en negeert RLS). Dat is verholpen door `CLAUDE.md` te hernoemen naar
`AGENTS.md` en er een verwijzing voor in de plaats te zetten.

`Sensory-wereld-shopify` heeft het omgekeerde en is bewust zo gelaten: daar is
`AGENTS.md` een inhoudelijk merkdocument, geen technische instructieset, en er
draait geen Claude Code-werk op dat een `CLAUDE.md` mist.
