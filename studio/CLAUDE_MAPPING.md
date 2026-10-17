# How the studio runs on Claude

Companion to STUDIO_BIBLE.md. The bible says who does what and what good looks like. This file says how each piece runs inside Claude Code: which model, which feature, which files, and which rules are enforced by code instead of by trust.

Checked against the Claude Code docs on Oct 17, 2026 (subagents, skills, workflows, agent teams, hooks, /goal, plugins, model aliases). Re-check anything marked [verify] before building on it.

## The short version

- Chris is the Executive Producer. He greenlights, sets the budget, and signs every lock.
- The main Claude Code session, running Opus 5.5, is the Producer. It holds the plan, spawns the crew, keeps the tracker, and enforces the budget. It never makes a creative call.
- Every other role is a subagent with its own model, tools, skills and authority.
- Makers run on Sonnet 5.5. Department heads and reviewers run on Opus 5.5. Clerical work runs on Haiku 5.5. Anything measurable runs as code. Final taste sits with Chris.
- Generation models and tools (Veo, Kling, Nano Banana, Blender, ComfyUI) are the studio's equipment, the way cameras and 3D printers are. Crew members operate the equipment. Equipment is never crew.
- Agents do not share memory. They share files. The production folder is the studio floor: if a decision is not written in the right file, it did not happen.

## Five rules the whole design rests on

1. **One owner per deliverable.** Many roles contribute; exactly one is accountable and signs. Real studios work this way (the Director approves shots, the Producer owns schedule), and it stops agents from waiting on each other or overwriting each other.
2. **Nobody grades their own work.** The maker never approves its own output. Taste calls go to a different agent, and the critic panel mixes model families, because research shows judges favor output from their own family (research/04-eval-harness.md).
3. **Code enforces what code can measure.** Cadence, flicker, blur, identity drift and lock status are checked by scripts and hooks. A model cannot talk its way past a failed cadence check.
4. **Seniority is model plus effort plus authority plus review.** A senior role gets a stronger model, more thinking time, the right to approve, and fewer reviews above it. A junior role gets a cheaper model and every output reviewed.
5. **Taste flows down, evidence flows up.** The Director and Creative Director set intent in writing. QC, critics and continuity report evidence. The Director decides with the evidence in hand. Chris breaks ties.

## Model and effort per role

Effort levels: low, medium, high, xhigh, max. Opus 5.5, Sonnet 5.5 and Haiku 5.5 default to medium.

| Role | Level | Model | Effort | Why this model |
|---|---|---|---|---|
| Executive Producer | Studio head | Chris (human) | n/a | Taste, budget and lock sign-off stay human |
| Producer (main session) | Head | Opus 5.5 | high | Holds the plan, routes work, judges scope and risk |
| Creative Director | Studio head | Opus 5.5 | high | Few calls, all high stakes: the house bar across every production |
| Director | Head | Opus 5.5, or Fable 5.1 if available | xhigh | Owns every creative call; consistency across many shots needs the strongest judgment |
| Head of Story | Supervisor | Opus 5.5 | high | Story problems are the most expensive to find late |
| Writer | Senior artist | Opus 5.5 | high | Scripts are short and cheap to generate; audiences forgive rough animation but not a weak story (Adam Elliot, BFI interview) |
| Storyboard Artist | Artist | Sonnet 5.5 + image model | medium | Volume work with clear specs |
| Animatic Editor | Artist | Sonnet 5.5 + ffmpeg scripts | medium | Mostly assembly and timing |
| Production Designer | Head | Opus 5.5 | high | Owns the look; every design passes through |
| Character Designer | Senior artist | Sonnet 5.5 + image model | high | Model sheets need care but follow a clear spec |
| Set and Props Designer | Artist | Sonnet 5.5 + image model | medium | Volume work against the style bible |
| Head of Fabrication | Supervisor | Opus 5.5 | high | Asset consistency is where AI work usually breaks |
| Fabricator / Rigger | Artist | Sonnet 5.5 | medium to high | Builds reference packs, meshes, rigs, mouth sets |
| Supervising Animator | Head | Opus 5.5 | high | Performance quality and consistency across shots |
| Lead Animator | Lead | Sonnet 5.5 | high | First review on a sequence, breaks shots into tasks |
| Senior Animator (retakes) | Senior | Opus 5.5 | high | Takes shots that failed twice |
| Animator | Artist | Sonnet 5.5 | medium | Volume: X-sheets, poses, generation runs |
| Lip Sync Artist | Artist | Sonnet 5.5 + Rhubarb | low | Mostly mechanical once the mouth set exists |
| Animation Assistant | Assistant | Haiku 5.5 | low | Prep, contact sheets, renaming, file checks |
| Director of Photography | Head | Opus 5.5 | high | Lens, scale and light logic decide whether it reads as miniature |
| Camera and Lighting Operator | Artist | Sonnet 5.5 | medium | Executes the DP's setups per shot |
| VFX Supervisor | Head | Opus 5.5 | high | Owns the post look and frame-level technical quality |
| Compositor | Artist | Sonnet 5.5 + scripts | medium | Runs the post stack per shot |
| Editor | Head | Opus 5.5 | high | Pacing and picture lock with the Director |
| Assistant Editor | Assistant | Haiku 5.5 | low | Conform, versions, edit lists |
| Sound Supervisor | Head | Sonnet 5.5 | high | Voice, effects, music and mix; most of the craft is in the tools |
| Script Supervisor (Continuity) | Specialist | Sonnet 5.5 | high | Careful visual comparison across shots |
| Production Coordinator | Assistant | Haiku 5.5 | low | Tracker updates, note routing, reminders |
| Pipeline TD | Head | Opus 5.5, or Fable 5.1 for root-cause hunts | xhigh | Builds and fixes the tools; "why does this look fake" is a root-cause problem |
| Researcher | Artist | Sonnet 5.5 | medium | Fan-out web research |
| Technical QC | Gate | Scripts, no model | n/a | Pass/fail on measurable signals |
| Critic Panel | Reviewers | Opus 5.5 + Gemini + one GPT model | n/a | Blind, pairwise, cross-family, advisory |

Notes on models:
- `fable` resolves to Fable 5.1. It is never the default, may bill to usage credits, and needs Claude Code v2.1.257 or later. Use it only where the table says so, and only if Chris has approved the spend.
- Pin versions in subagent files once the studio is stable (`claude-opus-5-5`, etc.) so a model update does not silently move the bar. Re-run judge calibration whenever a judge model changes.
- Cost reality: generation API spend and GPU time will usually dwarf Claude token spend. The Producer tracks both in one ledger.

## Which Claude Code feature does which studio job

| Studio need | Claude Code feature | How it is used here |
|---|---|---|
| A crew member with a job and authority | Subagent (`agents/<role>.md`) | Frontmatter sets `model`, `effort`, `tools`, `skills`, `memory`. Body holds the role definition from the bible. |
| Craft know-how several roles share | Skill (`skills/<craft>/SKILL.md` + `scripts/`) | Preloaded into roles via the subagent `skills:` field. Scripts referenced with `${CLAUDE_SKILL_DIR}`. |
| Studio rules every agent follows | `CLAUDE.md` (the studio charter) | Every subagent and teammate loads it: roles, folders, notes format, who can approve what. |
| Big parallel jobs | Saved workflows (`workflows/*.js`, run as `/dailies`, `/shoot`, `/bakeoff`, `/research-refresh`) | Scripts call `agent()`, `pipeline()`, `parallel()`. Intermediate results stay in script variables instead of flooding the Producer's context. Resumable. |
| A room that argues (story room, design crit) | Agent team (experimental, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) or a workflow with adversarial review | Writer, Head of Story and Director debate and challenge each other. Use teams only in interactive sessions; they do not spawn under `claude -p`. |
| Hard gates nobody can skip | Hooks + the tracker CLI | See "Gates enforced by code" below. |
| Keep improving until the bar is met | `/goal` with a printed scorecard | The evaluator only reads the transcript, so the loop must print its scores every round. |
| Equipment | MCP servers and APIs | Higgsfield MCP (Veo, Kling, Seedance, Wan, FLUX Video, Topaz, Deflicker, generate_3d), fal MCP, ComfyUI MCP, Blender Lab MCP for look-dev, Gemini API for Veo direct. Plain `blender -b -P` for production renders. |
| Taste that compounds across sessions | Subagent `memory: project` on Director and Creative Director | Each keeps a taste journal: notes that worked, notes that didn't, what Chris approved and rejected. |
| Packaging and reuse | Plugin `clay-studio` in a rader-ai GitHub marketplace | One install brings every agent, skill, workflow, hook and MCP config to any project. |
| Overnight work | Scheduled tasks (optional) | Nightly render queue and morning dailies report. |

## Plugin layout

```
clay-studio/                         (plugin root, its own repo on rader-ai)
  .claude-plugin/plugin.json         name, version, description
  .mcp.json                          equipment: higgsfield, fal, comfyui, blender-lab
  agents/                            one file per role in the bible
    producer.md  director.md  creative-director.md
    head-of-story.md  writer.md  storyboard-artist.md  animatic-editor.md
    production-designer.md  character-designer.md  set-props-designer.md
    head-of-fabrication.md  fabricator.md
    supervising-animator.md  lead-animator.md  senior-animator.md  animator.md
    lip-sync-artist.md  animation-assistant.md
    director-of-photography.md  camera-lighting-operator.md
    vfx-supervisor.md  compositor.md  editor.md  assistant-editor.md
    sound-supervisor.md  script-supervisor.md  production-coordinator.md
    pipeline-td.md  researcher.md  studio-critic.md
  skills/
    clay-studio/        umbrella skill: "/clay-studio:make <brief>" runs the whole pipeline
    clay-style-bible/   look rules, material vocabulary, ban list
    stop-motion-timing/ twos, holds, ones on camera moves, X-sheet format
    xsheet/             exposure sheet spec + phoneme breakdown
    model-sheet/        turnarounds, expressions, mouth chart, scale lineup
    storyboard/         panel spec, shot naming, camera notation
    animatic/           boards + timing + scratch audio
    keyframe-gen/       clay keyframes with reference packs
    shot-gen-video/     image-to-video routes, first/last frame, references
    blender-clay-shot/  bpy scene template, clay shader, stepped animation, mouths, miniature camera
    clay-post/          on-twos decimation, per-pose boil, grain, flicker, deflicker, upscale
    lip-sync/           Rhubarb to replacement mouths, held on twos
    clay-qc/            code metrics and gates
    critic-panel/       blind pairwise judging protocol
    continuity-check/   cross-shot consistency
    dailies/            review protocol and notes format
    sound/              voice, effects, music, mix
    edit-conform/       assembly, OTIO, deliverables
    production-tracking/ tracker CLI, statuses, packets, ledger
  workflows/
    dailies.js  shoot-sequence.js  bakeoff.js  research-refresh.js  tune.js
  hooks/hooks.json
  scripts/
    studio            tracker CLI (status, notes, packets, locks, ledger)
    qc/               cadence, holds, flicker, blur, boil band, identity drift, ghost frames
    post/             ffmpeg recipes
    render/           blender headless + cloud GPU fan-out
```

Production work happens in a separate project repo per film that installs the plugin. The plugin is the studio; each project repo is one production.

## Production folder (the studio floor)

```
<production>/
  CLAUDE.md                 production charter (points to the studio charter in the plugin)
  brief.md                  EP's brief: purpose, audience, length, budget, deadline
  decisions.md              every decision and waiver, dated, with owner
  locks.json                which artifacts are locked, who locked them, when
  ledger.csv                every paid call: date, role, tool, model, units, cost
  tracker.json              shots and assets, status, owner, version (written only by the tracker CLI)
  story/                    logline.md, treatment.md, script.md, beat-sheet.md
  bible/                    production style guide, colour script, scale rules
  characters/<name>/        model-sheet.png, turnaround, expressions, mouth-chart, refs/, mesh/, rig/
  sets/<name>/  props/<name>/
  boards/                   panels per shot
  animatic/                 versions, timing.csv
  shots/SQ010_SH020/
    shot.json               spec: duration, frames, lens, camera move, characters, props, dialogue
    kickoff.md              Director's brief: intent, acting beats, references, constraints
    xsheet.csv              frame-by-frame timing, holds, phonemes, camera notes
    versions/v001.mp4 ...   every version kept
    qc.json                 code gate results per version
    critics.json            panel verdicts per version
    continuity.json         continuity report per version
    notes.md                all notes, threaded, with status
  edit/  sound/  deliver/
```

## Gates enforced by code

Think of the tracker CLI as the only door into an approved state, and the hooks as locks on every other door.

1. **The tracker CLI is the only way to change status.** `studio status set <shot> approved` refuses unless: the latest version has a passing `qc.json`, `critics.json` exists, `continuity.json` has no open blocking issues (or a written Director waiver in `decisions.md`), and the Director's approval note is in `notes.md`.
2. **PreToolUse hook on Edit|Write** denies direct edits to `tracker.json`, `locks.json`, and any file listed as locked in `locks.json`. Reopening a lock is a Producer action that requires a recorded EP approval.
3. **PostToolUse hook** on writes into `shots/*/versions/` runs the QC scripts and writes `qc.json`, so no version escapes measurement.
4. **SubagentStop prompt hook** on maker roles checks that the agent left a handoff note (what changed, which version, open questions). If not, it sends the agent back to write one.
5. **Budget guard.** Generation scripts append to `ledger.csv` and refuse to run when the production budget would be exceeded. Only the EP can raise it.

## Handoff packets

Subagents start with no memory of the Producer's conversation. Every spawn therefore gets a packet, generated by `studio packet <shot> <role>`:
- The role's agent file (automatic)
- The exact folder path to work in and the version to start from
- The bible sections and model sheets that apply
- The open notes addressed to this role, verbatim
- The definition of done for this task and who reviews it next

If a fact matters to the next person, it goes in a file, not in the packet text alone.

## Retake ladder (seniority in action)

Real studios give the hardest shots to their most senior animators. Here:
1. v001 and v002: Animator (Sonnet 5.5).
2. v003: Senior Animator (Opus 5.5, high effort) takes over with all prior notes.
3. Still failing: the Supervising Animator and DP simplify the shot (restage, crop, change the move, switch route from video generation to Blender or back).
4. Still failing: the Director and Producer choose redesign, cut, or accept with a written waiver. The decision is logged.

## The tune loop (R&D)

Between productions, the Pipeline TD and Creative Director run R&D on the skill itself, using the eval harness from research/04. The loop runs under `/goal` with a condition that the scorecard itself must prove (see the kickoff prompt for the exact text). Rules:
- Gates are constraints, not weights. A version that fails a code gate never counts, however well it judges.
- Tune on 5 to 8 benchmark shots; validate on 10 or more held-out shots the loop never sees.
- A hidden judge and a hidden slice of the gold set stay out of the loop to catch reward hacking.
- Chris does a blind A/B check every 5 rounds and at every threshold crossing.

## What stays human

- Greenlight, budget, and every lock signature (Script, Design, Animatic, Look, Picture, Final).
- The blind A/B taste panel at Look Lock and Final, with 3 to 5 other people.
- Optional and recommended: a real clay reference shoot (macro stills and a few seconds of real stop motion), which gives the studio gold references it owns outright.
- Optional: scratch voices recorded by Chris for the animatic.
