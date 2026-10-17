# Resolution of review 2 (v0.2 to v0.3)

Every finding in `kit-review-2.md`, and what changed.

## Coverage gaps
- Costume and textile role: added Costume and Textile Artist (bible 4.6, mapping, fabrication, crew sizes).
- Lead and Senior levels outside animation: bible section 3 now says other departments add them when a production needs them.
- Role claims through `--by`: replaced with packet-based role checks in the CLI (ENGINEERING section 4).
- Subsurface conflict with nothing real to match: GOLD_SET.md specifies the probes in Chris's clay shoot; LOOK_DEV 2.1 says plainly the values stay guesses without it.
- Voice Lock: added as production lock 4 (bible 5.2, SOUND, STORY, CLI refuses lip sync before it).
- Waiting on Chris: `studio wait` and a waiting-on-Chris list in STATUS.md; the prompt tells Claude to block only dependent work.
- No plateau or revert rule, no named optimizers: keep-best rule, revert, plateau stop, Optuna and GEPA-style reflection (prompt Phase 6).

## Review-1 items not resolved in v0.2
- Hooks and MCP writes: Protect-state hook now matches file-writing MCP tools too.
- Paid judge calls: go through `studio judge`, which does its own ledger checks.
- "Keep the best" undefined: defined in Phase 6.2.
- Real clay shoot optional: strongly recommended with a shoot spec (GOLD_SET.md); Chris decides in Phase 0.
- Film name in the Director example: removed; cites research/05.
- Counsel note on do-not-resemble frames and personal vs company use: added (DESIGN_AND_WORLD 7, prompt ground rules, GOLD_SET).
- Boil stated as fact: LOOK_DEV 2.4 now labels it an inference.
- "Studio Bar evidence (bible section 5)": bible 5.2 now defines Studio Bar evidence and Look Lock evidence separately.

## Contradictions
- `dailies` skill vs workflow: workflow renamed `run-dailies`.
- Generative-route leftovers: "route" replaced with "bucket and render budget"; `--type route` removed.
- Pop-through approval: only the Supervising Animator (Director on hero shots) can approve; the Lead reviews.
- Sound sign-off: Producer consulted on rights before Voice and Sound Lock; RACI updated.
- Dialogue Lock: replaced with Voice Lock everywhere.
- Motif rule: the fiber appears in every scene, not every frame; deliberate breaks belong to the palette accent (CREATIVE_DIRECTION, DESIGN_AND_WORLD).
- Who rates the A/B: GOLD_SET.md is the single source (Chris alone at checkpoints and Look Lock; outside raters at Studio Bar and Final); bible, mapping and prompt point to it.
- Judge dimensions: the six are named in the bible, ENGINEERING and the /goal; Gemini counts only on pose and performance.
- Mouth timing vs one exposure grid: MOTION rule 4 and 4.7 now state the dialogue exception and the snap-to-grid fallback.

## Unsupported claims
- Pinocchio cross-studio calls: supported by the original research report; the line had been dropped when condensing research/05 and is restored.
- "Laika drift" source tag: retagged as our default (D).
- Vengeance Most Fowl water and fog to VFX: supported by the original camera research report; restored in research/11.
- Missing Link buckets: reworded as an idea from Missing Link's previs with our own labels.
- Laika screen tests: now "every wardrobe item; we do it for every material."
- Key light size: corrected to 3 to 4 cm across (1.5 to 2 cm radius).
- $1 to $5 render estimate: qualified as a simple-scene figure; Phase 0 measures real costs.

## Claude Code accuracy
- `${CLAUDE_PLUGIN_ROOT}` in skills: pipeline scripts are now `studio` subcommands; skill helpers use `${CLAUDE_SKILL_DIR}`.
- Docs unavailable inside production repos: copies ship in `skills/studio-charter/reference/`.
- Venv path for `bin/studio`: SessionStart writes it to a known file.
- Plugins don't ship permissions: `make` writes `.claude/settings.json` per production.
- bpy install: moved to Phase 0; SessionStart only verifies.
- Unverified features: marked [verify] and tested in Phase 0.
- Producer starting workflows: tested in Phase 0 with an Agent-tool fallback; no workflows before Phase 1.
- /goal: rewritten as a done test with stop conditions, a 48-hour bound, a plateau stop and named dimensions.
- Frontmatter enforcement: `disallowedTools` on critics and the Script Supervisor; blind Studio Critic (`tools: Read`, `omitClaudeMd`); `maxTurns` on artists; `Agent` tool for heads that spawn. Director and Creative Director keep Edit and Write because `memory` needs them, with a hook limiting writes to their memory folder.
- Plugin not loaded during build: local marketplace install in Phase 0.

## Stalls
- Packets for non-shot work: `studio packet --task`.
- Benchmark worlds without an owner: two R&D worlds owned by the Creative Director (Phase 2 item 12, Phase 5).
- Gold shoot spec: GOLD_SET.md.
- Hidden judge and held-out briefs: in the private R&D repo, run by a separate agent.

## Feasibility and cost
- Render cost: Phase 0 measures a fiber and clay close-up; look tuned on stills, motion at pop-through quality, full renders at checkpoints; GPU required for Phase 6.
- Judge cost: priced in Phase 0.
- Gold set quality and blindness: outside raters at Studio Bar; Chris's votes on his own footage don't count toward it; reports name the gold set.

## Writing
- Rewrote every flagged line in the prompt, mapping, bible, motion doc and Director example.

## IP, licensing, safety
- Real names in making-driving text: stripped in Phase 4; skills cite research numbers.
- `rnd/` in the public repo: moved to a private R&D repo.
- Plugin license: Chris chooses in Phase 0, with a note on Blender's GPL position.
- Data use: provider terms checked before sending any gold item.
