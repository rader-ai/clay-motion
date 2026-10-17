# How the studio runs on Claude

Companion to STUDIO_BIBLE.md (who does what), ENGINEERING.md (the mechanics) and GOLD_SET.md (what the judges compare against). This file says which model each role runs on, which Claude Code feature does which studio job, and which skills and workflows exist. Checked against the Claude Code docs on Oct 17, 2026.

## The short version

- Chris is the Executive Producer. He greenlights, sets budgets, and signs every gate and lock.
- The main Claude Code session, on Opus 5.5, is the Producer. It plans, staffs, tracks and spends, and never makes a creative call.
- Every other role is a subagent with its own model, effort, tools and skills.
- Makers run on Sonnet 5.5; heads, leads, seniors and reviewers on Opus 5.5; clerical work on Haiku 5.5; anything measurable runs as code; final taste sits with Chris.
- The equipment is Blender 5.2 LTS driven from Python, ffmpeg, Rhubarb Lip Sync, and open-weight voice models for scratch voices. Generative video and image services are not part of the default pipeline. The only outside APIs are the Gemini and OpenAI models on the critic panel.
- Agents don't share memory, so everything they need to hand on goes into files in the production repo, and a decision only counts once it's recorded there.

## Five rules

1. **One owner per deliverable.** Many roles contribute; one is accountable. This stops agents from waiting on each other or overwriting each other.
2. **Nobody grades their own work.** Makers never approve their own output, and taste calls go to a cross-family critic panel, because judges favor output from their own model family (research/04).
3. **Code enforces what code can measure.** Motion QC, cadence, holds, palette, loudness and lock status are checked by scripts behind the tracker CLI and hooks, so no agent can argue past a failed check.
4. **Seniority is model plus effort plus authority plus review.** Senior roles get stronger models, more thinking time, the right to approve, and fewer reviews above them.
5. **Intent comes from the top and evidence from the checks.** The Director and Creative Director write intent; QC, critics and continuity report evidence; the Director decides; Chris breaks ties.

## Models and effort

| Role | Level | Model | Effort |
|---|---|---|---|
| Executive Producer | Studio head | Chris | n/a |
| Producer (main session) | Head | Opus 5.5 | high |
| Creative Director | Studio head | Opus 5.5 | high |
| Director | Head | Opus 5.5 | xhigh |
| Co-director / Sequence Director | Head | Opus 5.5 | high |
| Head of Story | Head | Opus 5.5 | high |
| Writer | Artist (exception) | Opus 5.5 | high |
| Storyboard Artist | Artist | Sonnet 5.5 | medium |
| Animatic Editor | Artist | Sonnet 5.5 | medium |
| Production Designer | Head | Opus 5.5 | high |
| Visual Development Artist | Artist | Sonnet 5.5 | medium |
| Character Designer | Artist | Sonnet 5.5 | high |
| Set and World Designer | Artist | Sonnet 5.5 | medium |
| Look Development Supervisor | Head | Opus 5.5 | high |
| Look Development Artist | Artist | Sonnet 5.5 | medium |
| Head of Fabrication | Head | Opus 5.5 | high |
| Fabricator / Rigger | Artist | Sonnet 5.5 | medium |
| Costume and Textile Artist | Artist | Sonnet 5.5 | high |
| Supervising Animator | Head | Opus 5.5 | high |
| Lead Animator | Lead | Opus 5.5 | high |
| Senior Animator | Senior | Opus 5.5 | high |
| Animator | Artist | Sonnet 5.5 | medium |
| Lip Sync Artist | Artist | Sonnet 5.5 | low |
| Animation Assistant | Assistant | Haiku 5.5 | low |
| Director of Photography | Head | Opus 5.5 | high |
| Camera and Lighting Operator | Artist | Sonnet 5.5 | medium |
| VFX Supervisor | Head | Opus 5.5 | high |
| Compositor | Artist | Sonnet 5.5 | medium |
| Effects Artist | Artist | Sonnet 5.5 | medium |
| Editor | Head | Opus 5.5 | high |
| Assistant Editor | Assistant | Haiku 5.5 | low |
| Sound Supervisor | Head | Opus 5.5 | high |
| Sound Designer and Dialogue Editor | Artist | Sonnet 5.5 | medium |
| Script Supervisor (Continuity) | Reviewer (exception) | Sonnet 5.5 | high |
| Production Coordinator | Assistant | Haiku 5.5 | low |
| Pipeline TD | Head | Opus 5.5 | xhigh |
| Animation TD | Senior | Opus 5.5 | high |
| Researcher | Artist | Sonnet 5.5 | medium |
| Studio Critic (panel member) | Reviewer | Opus 5.5 | high |
| Technical QC | Gate | Code | n/a |

**Exceptions and why**
- **Writer on Opus:** scripts are short and cheap to generate, and story is the one thing that can't be fixed later.
- **Script Supervisor on Sonnet:** dress manifests, puppet specs and camera data do most of the checking in code; the agent handles the visual comparison of neighbors.
- **Fable 5.1:** never a default. If Chris approves the spend, the Director or Pipeline TD can switch to `fable` for a hard problem; it may bill to usage credits and needs Claude Code 2.1.257 or later.
- Pin model versions in agent files once the studio is stable (`claude-opus-5-5`, etc.) and re-run judge calibration whenever a judge model changes.

## Which feature does which job

| Studio need | Claude Code feature | How it's used |
|---|---|---|
| A crew member | Subagent (`agents/<role>.md`) | Frontmatter: `model`, `effort`, `tools` (tool names only), `skills`, `memory`. Body: the role from the bible, written as instructions with reasons. |
| Studio rules for everyone | The `studio-charter` skill, preloaded into every agent | Plugins can't ship a CLAUDE.md, so the charter (lines of communication, notes format, file rules, who can approve what) is a skill, with copies of the studio docs in its `reference/` folder. The `make` skill also writes a short CLAUDE.md and `.claude/settings.json` into each production repo. |
| Craft know-how | Skills (`skills/<craft>/SKILL.md` plus scripts) | Preloaded into the roles that use them; bundled files via `${CLAUDE_SKILL_DIR}`. |
| The tracker and pipeline commands | `bin/studio` in the plugin | On the Bash PATH while the plugin is enabled. The only way to change state, and the way agents run renders, QC, post and judging (ENGINEERING.md section 4). |
| Big parallel jobs | Saved workflows (`workflows/*.js`, run as `/clay-studio:<name>`) | Fan-outs keep raw output out of the Producer's context and are resumable within a session. |
| A room that argues | Agent team (experimental, interactive only) or a workflow with adversarial review | Story room, design crit. |
| Gates | Hooks plus the tracker CLI | ENGINEERING.md section 5. |
| Keep tuning until the bar is met | `/goal` | Chris pastes the goal line Claude prints; the evaluator only reads the transcript, so every round prints its scorecard. |
| Taste that compounds | `memory: user` on Director and Creative Director | Persists across production repos (project scope would reset per repo). |
| Delegation depth | Subagents can spawn subagents up to 3 layers by default | We use 2: Producer to heads and crew; heads to a reviewer or assistant. Crew never spawn. |
| Overnight work | Scheduled tasks (optional) | Nightly renders and a morning dailies page. |

## Skills

| Skill | Used by | What it carries |
|---|---|---|
| `studio-charter` | Everyone | Org rules, lines of communication, notes format, file rules, approvals |
| `make` | Producer | The entry point: `/clay-studio:make <brief>` runs a production through every lock |
| `production-tracking` | Producer, Coordinator | Tracker CLI usage, statuses, packets, ledgers, reports |
| `story-development` | Head of Story, Writer | Loglines to script, table read, story rules for clay |
| `boards` | Storyboard Artist, Head of Story | SVG symbol library, beat board, Blender board renders, panel JSON, board checks |
| `animatic-and-edit` | Animatic Editor, Editor, Assistant Editor | ffmpeg and OTIO assembly, timing files, edit drafts, conform |
| `world-bible` | Production Designer, Set and World Designer | World and material bible template, palette rules, originality check |
| `character-build` | Character Designer, Head of Fabrication, Fabricator, Costume and Textile Artist | Silhouettes, maquette, model sheet, code build recipe, mouth sets, costumes |
| `set-build` | Set and World Designer, Fabricator | Greybox, kit modules, dressing tiers, handmade pass, dress manifests |
| `look-dev` | Look Dev Supervisor and Artist | Clay shader, fibers, other materials, boil, screen test, texture licensing |
| `camera-and-light` | DP, Operator | Lens and aperture rules, breathing, miniature lighting, flicker policy |
| `post-and-color` | VFX Supervisor, Compositor, Effects Artist | Post chain order, per-pose noise, show LUT, handmade effects |
| `animate-shot` | Animators, Lip Sync, Supervising and Lead Animators | Writing `shot.yaml`, the motion style guide, pop-through, reading motion QC |
| `animation-engine` | Animation TD | Rig, compiler, solver, secondary layers, lip-sync mapper, tests |
| `clay-qc` | Pipeline TD, Technical QC | Code checks and their validation |
| `critic-panel` | Studio Critic, Creative Director | Blind pairwise protocol, filmstrips, calibration |
| `continuity-check` | Script Supervisor | Manifest diffs and neighbor comparison |
| `dailies` | Director, Editor | Mini-cuts, review protocol, notes format |
| `sound` | Sound Supervisor, Sound Designer | Voices and consent, effects sourcing, mix targets, audio QA |

## Workflows
| Workflow | Does |
|---|---|
| `research-refresh` | Re-verifies versions, prices and licenses across the research files, with an adversarial second pass |
| `board-sequence` | Thumbnails, beat board, Blender boards and board checks for a sequence |
| `screen-test` | Renders a batch of new materials on the screen-test scene and scores them |
| `shoot-sequence` | For each ready shot: layout, pop-through, final, post, QC, in parallel up to the render budget |
| `run-dailies` | For each shot pending review: critics and continuity, then a dailies page and a Director review (named to avoid clashing with the `dailies` skill) |
| `tune` | One round of the R&D loop on the tuning shots (the prompt defines the full loop) |

## Production folder
```
<production repo>/
  CLAUDE.md            short pointer to the studio charter
  STATUS.md            the Producer's report
  brief.md  decisions.md  locks.json  ledger.csv  tracker.json   (state files, changed only by `studio`)
  bible/               world.md (with material bible), palette.yml, scale.yml, colorscript.json, show LUT
  story/               loglines, beat sheet, treatment, script drafts, table read audio
  characters/<name>/   puppet.json, model sheet renders, mouth set, character bible
  sets/<name>/         set brief, kit config, greybox, manifests
  boards/  animatic/   panels with JSON sidecars, timing.csv, OTIO
  shots/SQ010_SH020/   shot.json, kickoff.md, shot.yaml, exposures.json, dress_manifest.json,
                       versions/, qc.json, critics.json, continuity.json, notes.md
  sound/  edit/  deliver/
  renders/             gitignored; synced to a bucket if configured
```

## Handoff packets

Every spawn gets a packet from `studio packet <shot> <role>`: the folder and version to start from, the bible sections and model sheets that apply, the open notes for this role verbatim, the definition of done, and who reviews next. Anything the next person needs goes in a file, not only in the packet text. Every agent ends by writing a handoff note (what changed, which version, what's open); a SubagentStop hook checks it exists.

## What stays human
- Greenlight, budgets, and every gate and lock signature.
- The blind A/B taste checks: Chris alone at tune-loop checkpoints and a production's Look Lock; 3 to 5 outside raters at Studio Bar and at a production's Final (GOLD_SET.md).
- Final voices (human performers, or Chris), unless Chris approves licensed AI voices with disclosure.
- Commissioning music.
- The real clay gold shoot (strongly recommended, GOLD_SET.md). Optional: live-action reference for hero shots and a later material shoot.
