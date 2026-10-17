# Engineering: repos, tools, gates and infrastructure

Owner: the **Pipeline TD**. Claude Code facts checked against the docs on Oct 17, 2026 (plugins, subagents, hooks, workflows, /goal). Items marked [verify] weren't confirmed in the docs; test them in Phase 0.

## 1. Repos, storage and licenses

- **Plugin repo:** `rader-ai/clay-motion` (this repo, public). Holds the plugin, studio docs and research. No secrets, no renders, no gold footage, no A/B results.
- **R&D repo:** a private repo (for example `rader-ai/clay-motion-rnd`) for the R&D ledger, tune log, A/B results, gold-set provenance, and, in a folder the tune loop never reads, the held-out benchmark briefs, the held-out gold slice and the hidden judge configuration.
- **Production repos:** one private repo per production: specs, manifests, notes, decisions, ledger.
- **Large files:** `.blend` files through Git LFS. Renders, caches and EXRs never go in git; they live in a gitignored `renders/` folder and, if a bucket is configured (Cloudflare R2 or S3), sync there. Manifests point to them by content hash.
- **Secrets:** API keys in an untracked `.env`, never in `.mcp.json`, agent files or commits.
- **Plugin license:** Chris picks one before anything is open-sourced. Blender's license guidance treats add-ons that use its Python API as covered by the GPL [verify]; check how that applies to scripts that import `bpy` before choosing.

## 2. Plugin layout

```
clay-motion/
  .claude-plugin/plugin.json   name: clay-studio
  agents/                      one file per role (STUDIO_BIBLE.md section 4)
  skills/
    studio-charter/            rules every agent follows, with reference/ copies of the studio docs
    make/                      entry point: /clay-studio:make
    ...                        craft skills (CLAUDE_MAPPING.md)
  workflows/                   saved workflows: /clay-studio:<name>
  hooks/hooks.json             gates (section 5)
  bin/studio                   tracker CLI and every pipeline command; on the Bash PATH while the plugin is enabled
  lib/                         Python modules bin/studio imports (found relative to bin/studio's own path)
  .mcp.json                    optional, no keys
```
Mechanics that matter:
- Plugins can't ship a CLAUDE.md that loads as context, so the charter is a skill every agent preloads. Production repos don't contain the studio docs, so `studio-charter` carries copies in `reference/` and skills cite those paths.
- `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}` are available to hooks and MCP config, not reliably to Bash. So pipeline scripts are `studio` subcommands (`studio render`, `studio qc`, `studio post`, `studio build-shot`, `studio judge`), and `bin/studio` finds `lib/` relative to its own location. Skill-specific helpers live in the skill and are referenced with `${CLAUDE_SKILL_DIR}`.
- Plugins don't ship permission rules, so `make` writes `.claude/settings.json` into each production repo with the deny rules in section 5.
- A plugin with `bin/` installs only in Claude Code, not on claude.ai or Cowork.
- While building, install the plugin from a local marketplace (a `marketplace.json` in this repo, added with `/plugin marketplace add`) so agents, skills and hooks actually load.

## 3. Blender

- Install Blender 5.2 LTS through `bpy` 5.2.2 (Python 3.13, about 1.2 GB, GPL-3.0) in Phase 0, into a pinned virtual environment under the plugin data folder. A SessionStart hook verifies it and writes the environment's path to `~/.config/clay-studio/env`, which `bin/studio` reads. A full Blender install with `blender -b -P` also works.
- One scene per process; `bpy` is global state.
- All keying, node and compositor calls go through one adapter module, because 5.0 and 5.2 changed APIs that models often get wrong (slotted actions, `scene.compositing_node_group`, Grease Pencil v3, `modifier.properties.inputs`, `BLENDER_EEVEE`).
- An API smoke test runs at session start: version string, required node types, engine IDs, a one-frame render. Unknown names fail loudly.
- Test headless EEVEE on the render machine; fall back to low-sample Cycles for previews.

## 4. The tracker CLI (`studio`)

The only door into any state change. Every command validates against schemas and appends to an audit log.

**Who's calling.** Each spawn gets a packet with a random ID, recorded in the tracker with the role it was issued to. Commands that need authority take `--packet <id>` and the CLI checks the role from the tracker, so an agent can't claim another role by typing it. The Producer's own commands use the session packet.

| Command | Does | Refuses when |
|---|---|---|
| `studio init <production>` | Creates the production folder, schemas, tracker, ledger, decisions, locks, `.claude/settings.json` | Folder exists |
| `studio shot add` / `studio asset add` / `studio task add` | Registers work | ID exists or breaks naming |
| `studio packet --shot <id> --role <r>` or `--task <id> --role <r>` | Builds a handoff packet and its ID; sets the handoff-note path `handoff/<packet>.md` | Work not ready for that role |
| `studio kickoff <shot> --file <f>` | Records the Director's kickoff | Caller isn't the Director; Look Lock not signed (except the Look Lock test shot); animatic not locked |
| `studio version add <shot> <file>` | Registers a version and runs code QC; writes `qc.json` | File outside the shot folder; render settings missing |
| `studio pop approve <shot>` | Approves a pop-through | Caller isn't the Supervising Animator (or the Director on hero shots) |
| `studio lipsync <shot>` | Runs Rhubarb and maps mouths | Voice Lock not signed |
| `studio note add / restate / reply / verify` | Notes with IDs, threads, status | Verify by anyone but the note's author or the gate owner |
| `studio status <shot> <code>` | Moves status (`wtg rdy ip pop rev rtk apr fin hld omt`) | `apr` without a passing `qc.json`, a `critics.json`, no open blocking continuity issues (or a Director waiver), and a Director approval note |
| `studio decide --type <lock, waiver, scope, budget>` | Writes a dated decision with owner, reason, impact, cost | Lock or budget decisions without a recorded EP approval |
| `studio lock` / `studio unlock` | Locks or reopens an artifact | Missing approvals |
| `studio wait --on chris --for "<what>" --blocks <task ids>` | Adds an item to `STATUS.md`'s waiting-on-Chris list and blocks dependent tasks | n/a |
| `studio ledger check <cost>` / `studio ledger add` | Checks a planned spend against the cap; records spend | Would exceed the cap |
| `studio judge` | Runs the critic panel on pairs; calls `ledger check` before each batch and `ledger add` after | Over budget; gold items with unchecked data-use terms |
| `studio report` | One-screen status, written to `STATUS.md` and the review site | n/a |

Creative retake rounds are counted from notes of type `creative` or `scope`, not from version numbers, so QC-driven re-renders don't use up the retake ladder.

## 5. Hooks and permission rules

| Hook | Event and matcher | What it does |
|---|---|---|
| Protect state | PreToolUse on `Edit|Write|NotebookEdit` and on file-writing MCP tools (`mcp__.*`) | Denies writes to `tracker.json`, `locks.json`, `ledger.csv`, `decisions.md`, `handoff/` (except the caller's own note) and any locked artifact |
| Protect state from the shell | PreToolUse on `Bash` | Denies commands that write those files directly (redirection, `sed -i`, `mv`, `rm`, `cp`, `git checkout` on them). `studio` commands pass |
| Handoff note | SubagentStop, command hook | Checks `handoff/<packet>.md` exists; if not, blocks the stop with a reason |
| Session start | SessionStart | Verifies the pinned Blender environment, writes its path, runs the API smoke test |

- Exit code 2 or `{"decision": "block"}` blocks. PostToolUse can't undo an action, so protection lives in PreToolUse.
- Paid calls (the Gemini and OpenAI judges) go through `studio judge`, which does its own ledger checks, because a Bash hook can't tell a judge call from any other command.
- `make` writes `permissions.deny` rules into each production's `.claude/settings.json` as a second layer behind the Bash hook.

## 6. Agents and spawning

- Subagents can spawn subagents up to three layers deep by default. This studio uses two: the Producer spawns heads and crew; heads that need a reviewer or assistant get the `Agent` tool; crew don't.
- The `tools` field takes tool names only. Use frontmatter to enforce the bible:
  - Critic Panel and Script Supervisor: `disallowedTools: Edit, Write` (they write only through `studio`).
  - Director and Creative Director keep Edit and Write because `memory` needs them; a per-agent PreToolUse hook in their frontmatter limits those writes to their memory folder, and everything else goes through `studio`.
  - Studio Critic: `tools: Read`, `omitClaudeMd: true`, and it receives only anonymized pairs and the rubric, so it stays blind.
  - Artists: `maxTurns` set so a stuck agent hands back instead of looping.
- `memory: user` for the Director and Creative Director (persists across production repos).
- Workflows are started by a typed `/clay-studio:<name>` or a request in a typed prompt. Whether the Producer can start one mid-loop on its own needs testing in Phase 0 [verify]; the fallback is spawning the same agents with the Agent tool. The kickoff prompt tells Claude not to start any workflow before Phase 1.
- Also [verify] in Phase 0: auto mode naming and behavior, workflow resume, agent teams, scheduled tasks, and the Fable minimum version.

## 7. Compute

- Render only unique poses and duplicate holds in post (halves render time on twos).
- research/03's figure (a 60-second film is about 720 unique frames, about 4 GPU-hours at 20 seconds a frame) is for a simple tabletop scene at 64 to 128 samples. Subsurface clay, fibers and displacement at final quality can cost 2 to 5 GPU-minutes a frame [U, reviewer's estimate]. Measure in Phase 0: render a fiber-and-clay close-up at final settings and record seconds per frame.
- Tuning plan that keeps cost sane: tune the look on stills (screen test and turntables), tune motion at pop-through quality, and render full-quality motion only at checkpoints. A GPU is required for Phase 6; CPU-only machines can do previews and stills.
- Options: local NVIDIA GPU, Apple Silicon with Metal, or a rented GPU (RunPod; Modal has a documented Blender fan-out example).

## 8. Review site

Chris reviews from his phone:
- **Dailies page per batch:** each shot's mini-cut, filmstrip, QC and critic summaries, approve and note buttons.
- **A/B page:** blinded pairs (random left and right), forced choice plus "can't tell" and a one-line reason. Raters per GOLD_SET.md.
- **Hosting (Phase 0 choice):** a password-protected Vercel deployment or Cloudflare Pages behind Cloudflare Access. Responses go to a small store (Vercel KV, a Cloudflare D1 table, or a JSON file committed to the private repo by a serverless function). Fallback: a local page that exports `feedback.json`.
- Never put studio stills, the do-not-resemble set, or footage Chris hasn't cleared on a hosted page.

## 9. Testing
- Unit tests with golden JSON on every pure-Python component (timing compiler, contact solver, lip-sync mapper, tracker CLI).
- QC validation on controlled degradations of approved clips (interpolated frames, injected flicker, blur, cross-dissolve morphs, foot slide). A check that misses its own degradation is broken.
- Look regression (LOOK_DEV.md section 8) on every shader, light or post change.
- Motion regression: every approved test shot recompiles to identical `exposures.json`.
- End-to-end smoke test: one 2-second shot through the full shot cycle, every gate firing; critic results may be stubs until calibration.

## 10. Judges
- Panel: a Studio Critic agent (Claude), Gemini and one OpenAI model, through `studio judge`. Six dimensions: clay surface, sculpt and character craft, lighting and miniature depth, set and prop scale, pose and performance, handmade cues. Gemini counts only on pose and performance.
- Inputs: 6 to 12 labeled full-resolution frames and crops per item plus the filmstrip, never a single downscaled mosaic (it erases clay grain).
- Hidden judge: a different model version and prompt per family plus the held-out gold slice, stored in the private R&D repo and run only at checkpoints by a separate workflow agent; the tuning crew never gets its path.
- Data use: check each provider's API terms before sending any gold item (GOLD_SET.md).
- Price it in Phase 0: calls per round, images per call, cost per call.
