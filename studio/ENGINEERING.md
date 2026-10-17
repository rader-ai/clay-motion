# Engineering: repos, tools, gates and infrastructure

Owner: the **Pipeline TD**. Claude Code facts checked against the docs on Oct 17, 2026 (plugins, subagents, hooks, workflows, /goal). Re-verify anything marked [verify] at build time.

## 1. Repos and storage

- **Plugin repo:** `rader-ai/clay-motion` (this repo). Holds the plugin, the studio docs and the research. Public today; no secrets, no studio stills, no renders.
- **Production repos:** one private repo per production. Holds scripts, specs, manifests, notes, decisions, ledgers.
- **Large files:** `.blend` files through Git LFS. Renders, caches and EXRs never go in git: they live in a gitignored `renders/` folder and, if a bucket is configured (Cloudflare R2 or S3), sync there. Manifests in git point to them by content hash.
- **Secrets:** API keys in an untracked `.env`, never in `.mcp.json`, agent files or commits.

## 2. Plugin layout (verified mechanics)

```
clay-motion/
  .claude-plugin/plugin.json
  agents/              one file per role (STUDIO_BIBLE.md section 4)
  skills/
    studio-charter/    the rules every agent follows (plugins can't ship a CLAUDE.md, so this is a skill every agent preloads)
    make/              entry point, runs as /clay-studio:make (plugin name set in plugin.json)
    ...                craft skills (CLAUDE_MAPPING.md)
  workflows/           saved workflows, run as /clay-studio:<name>
  hooks/hooks.json     gates (section 5)
  bin/studio           the tracker CLI; plugin bin/ is on the Bash PATH while the plugin is enabled
  scripts/             qc, post, render, build helpers, referenced as ${CLAUDE_PLUGIN_ROOT}/scripts/...
  .mcp.json            optional equipment servers (no keys inside)
```
- `${CLAUDE_PLUGIN_ROOT}` changes with each plugin version; never write state there. `${CLAUDE_PLUGIN_DATA}` survives updates; the pinned Python environment with bpy lives there.
- Inside a skill, bundled files are referenced with `${CLAUDE_SKILL_DIR}`.
- A `bin/` folder blocks installation on claude.ai and Cowork; this plugin targets Claude Code only.

## 3. Blender

- Pin Blender 5.2 LTS through the `bpy` 5.2.2 package (Python 3.13, about 1.2 GB, GPL-3.0), installed in `${CLAUDE_PLUGIN_DATA}/venv` by a SessionStart hook on first use. On a machine with a full Blender 5.2 install, `blender -b -P script.py` works too.
- One scene per process; `bpy` is global state.
- All keying, node and compositor calls go through one adapter module, because 5.0 and 5.2 changed APIs that models often get wrong (slotted actions, `scene.compositing_node_group`, Grease Pencil v3, `modifier.properties.inputs`, `BLENDER_EEVEE`).
- An API smoke test runs at session start: version string, required node types, engine IDs, a one-frame render. Unknown names fail loudly.
- EEVEE in headless mode is uncertain on some machines. Test it on the target box; fall back to low-sample Cycles for previews.
- `fake-bpy-module-5.2` for type hints.

## 4. The tracker CLI (`studio`)

The only door into any state change. Plain Python, stdlib plus `jsonschema`. Every command validates against schemas and appends to an audit log.

| Command | Does | Refuses when |
|---|---|---|
| `studio init <production>` | Creates the production folder, schemas, empty tracker, ledger, decisions, locks | Folder exists |
| `studio shot add <id>` / `studio asset add <id>` | Registers work | ID exists or doesn't match naming |
| `studio kickoff <shot> --file kickoff.md` | Records the Director's kickoff | Not called by the Director's packet; animatic not locked |
| `studio version add <shot> <file>` | Registers a version and runs code QC (motion QC, cadence, holds, flicker, blur, palette); writes `qc.json` | File outside the shot folder; render settings missing |
| `studio pop approve <shot> --by <role>` | Approves a pop-through (status `pop` to `ip` for final) | Reviewer isn't Lead/Supervising Animator (Director on hero shots) |
| `studio note add/restate/reply/verify` | Notes with IDs, threads, status | Verify by anyone but the note's author or gate owner |
| `studio status <shot> <code>` | Moves status (`wtg rdy ip pop rev rtk apr fin hld omt`) | `apr` without: passing `qc.json`, `critics.json`, no open blocking continuity issues (or a Director waiver in decisions), and a Director approval note |
| `studio decide --type <lock/waiver/scope/route/budget>` | Writes a dated decision with owner, reason, impact, cost | Lock or budget decisions without a recorded EP approval |
| `studio lock <artifact>` / `studio unlock` | Locks or reopens; reopening needs an EP-approved change request | Missing approval |
| `studio packet <shot> <role>` | Builds the handoff packet for a spawn | Shot not `rdy` for that role |
| `studio ledger add` / `studio ledger check <cost>` | Records spend; checks a planned spend against the cap | Would exceed the cap |
| `studio report` | One-screen status for the EP (also written to `STATUS.md`) | n/a |

Creative retake rounds are counted per shot from notes of type `creative` or `scope`, not from version numbers, so QC-driven re-renders don't use up the retake ladder.

## 5. Hooks

| Hook | Event and matcher | What it does |
|---|---|---|
| Protect state | PreToolUse on `Edit|Write` | Denies direct edits to `tracker.json`, `locks.json`, `ledger.csv`, `decisions.md` and any locked artifact |
| Protect state from the shell | PreToolUse on `Bash` | Denies commands that write those files directly (redirection, `sed -i`, `mv`, `rm`, `git checkout` on them); `studio` commands pass |
| Paid calls | PreToolUse on any paid MCP tool or API wrapper script | Runs `studio ledger check`; denies over the cap. Only relevant if a paid service is ever enabled |
| Handoff note | SubagentStop, command hook | Checks that the agent wrote its handoff note file for the packet; if not, blocks the stop with a reason so it writes one |
| Session start | SessionStart | Ensures the pinned bpy environment; runs the API smoke test |
Notes: exit code 2 or `{"decision": "block"}` blocks; PostToolUse can't undo an action, so state protection lives in PreToolUse. Permission rules (`permissions.deny`) back up the Bash hook for the most dangerous patterns.

## 6. Agents and spawning

- Subagents can spawn subagents up to three layers deep by default (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`). This studio keeps it to two: the Producer spawns heads and crew; heads may spawn a reviewer or assistant for their own department; crew never spawn.
- Fan-outs (dailies across a batch, per-shot production across a sequence, research refreshes, critic panels) run as saved workflows so their raw output stays out of the Producer's context.
- The subagent `tools` field takes tool names only; command-level limits (for example "Bash, but only `studio`") come from permission rules and hooks, not frontmatter.
- `memory: user` for the Director and Creative Director, so taste journals persist across production repos (`project` scope would reset per repo).
- Agent teams (experimental, interactive only) are optional for the story room and design crits.

## 7. Compute

- **Render only unique poses** and duplicate holds in post: halves render time on twos.
- Rough cost: a 60-second film on twos is about 720 unique frames. At 20 seconds a frame on a 4090-class GPU that's about 4 GPU-hours, roughly $1 to $5 on a rented GPU including retries [U, research/03].
- Options, chosen in Phase 0: local GPU (NVIDIA or Apple Silicon with Metal), rented GPU (RunPod, Modal; Modal has a documented Blender fan-out example), or CPU only (previews only; finals will be slow).
- Fiber-heavy and close-up frames cost more (hair curves, subsurface, displacement). Budget from the tune loop's measured render times, not from this estimate.

## 8. Review site (dailies and A/B tests)

Chris reviews from his phone, so reviews are web pages:
- **Dailies page per batch:** each shot's mini-cut, filmstrip, QC and critic summaries, and approve / note buttons.
- **A/B page:** blinded pairs (random left and right), forced choice plus "can't tell" and a one-line reason.
- **Hosting (decide in Phase 0):** a password-protected Vercel deployment or Cloudflare Pages behind Cloudflare Access (Chris uses both). Responses are written to a small store (Vercel KV, a Cloudflare D1 table, or a JSON file committed to the private production repo by a serverless function). Fallback with no hosting: the page runs locally and exports a `feedback.json` that Chris sends back.
- **Never** put studio stills or the do-not-resemble reference set on a hosted page.

## 9. Testing

- **Unit tests** on every pure-Python component (timing compiler, contact solver, lip-sync mapper, tracker CLI) with golden JSON files.
- **QC validation:** every code check is tested on controlled degradations of approved clips (inserted interpolated frames, injected flicker, blur, cross-dissolve morphs, foot slide). A check that misses its own degradation is broken.
- **Look regression** (LOOK_DEV.md section 8) on every shader, light or post change.
- **Motion regression:** every approved test shot recompiles to identical `exposures.json`.
- **End-to-end smoke test:** one 2-second shot through the full shot cycle with every gate firing; critic results may be stubs until the panel is calibrated.

## 10. Judges and keys
- The critic panel uses Claude (a Studio Critic agent), Gemini and one OpenAI model through their APIs. Gemini samples video at about 1 frame per second, so its votes count only on performance and pacing, never on cadence or surface.
- The hidden judge is a separate configuration the tune loop never sees: a different model version and prompt per family, plus a held-out slice of the gold set.
- Never send studio stills or anything from the private reference set to a third-party API. Gold sets sent to judges are our own renders, public-domain or openly licensed clips, and, later, our own photographs.
