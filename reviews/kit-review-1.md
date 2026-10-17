# Independent review of the kit, round 1 (Opus reviewer, Oct 17, 2026)

Reviewer did not write the kit. Findings to resolve in the revision pass.

## Top 5 changes, priority order
1. Make the gates real: the tracker CLI does every state write and runs QC on `version add`; hooks cover Bash and MCP writes, not just Edit|Write; the budget hook covers MCP generation calls.
2. Rewrite the tune loop and /goal: pick winners on tuning shots only; score held-out and hidden every 5 rounds (printing them every round leaks them to the optimizer); print spend and round number (the evaluator can't read ledger.csv); define judge agreement and "keep the best"; add a "waiting on Chris" exit; have Claude print the /goal line for Chris to paste.
3. One lock table with a matching RACI. Settle Spec Lock, Studio Ready, where Look Lock sits (once per studio version vs per production), Sound Lock, and who signs Picture/Sound/Delivery.
4. Fix plugin mechanics: charter as a preloaded skill (plugins don't ship a CLAUDE.md); entry skill folder `skills/make/` so the command is `/clay-studio:make`; script paths (`${CLAUDE_SKILL_DIR}` can't reach plugin-root scripts; `studio` not on PATH); only the Producer or workflow `agent()` spawns agents; add missing roles (Visual Development, Effects, Co-director) to the mapping; drop `agents/producer.md`; give the Director CLI commands to write kickoffs and decisions.
5. Make the gold set real: commit to the real clay shoot; minimum 30+ gold and 30+ known-bad; 60+ labeled pairs for judge-human agreement; decide how the A/B page is hosted and how results come back; keep studio stills off third-party APIs.

## Other findings
- Lock counts differ across files ("seven locks" vs eight signatures; Spec Lock only in prompt; Sound Lock missing from mapping).
- Status naming: CLI uses "approved", bible uses `apr`; pop-through approval has no recorded field.
- RACI vs section 5 disagree on Picture/Sound/Delivery signers, CD role at Look Lock, Animatic Editor vs Editor.
- Seniority rule broken: Sonnet Lead reviews Opus Senior; Sound Supervisor head on Sonnet.
- `/shoot` vs `shoot-sequence.js`; `tune.js` missing from run list; productions/ area vs repo per film; ledger and decisions location.
- Retake ladder counts versions; QC fails create versions too. Count creative rounds.
- Prompt says "Look Lock evidence in section 6" (wrong section).
- Unsupported claims: ShadowMachine puppet heads; handmade effects claim and "effects are where AI snaps into CG" unsourced (research says studios use CG for water and fire); "around 1%" phrasing; boil, faces on ones and two-round cap stated as fact though marked inferred/unverified; Blender MCP no-auth applies to ahujasid's server, not Blender Lab's; aperture conflict (T11-T16 vs f/2.8-5.6) unresolved; "within 0.05" unsourced; 30-60 A/B pairs below the 60+ needed; "every controlled degradation caught" overstates research (90% code / 80% panel); missing "press-kit terms unverified, ask counsel".
- Claude Code: frontmatter needs single values (no "Opus or Fable", no "medium to high"); `memory: project` resets per production repo, consider `user`; some features to verify (workflow resume, AskUserQuestion limits, auto mode naming, permission patterns inside `tools:`).
- Gaps: Director can't write kickoffs with read-only tools; hidden judge has no model; STYLE_BIBLE.md never created by any phase; smoke test needs critic stubs; gold/known-bad minimum sizes missing.
- Cost: tune loop on the generation route at ~50 clips/round could run $1.4k-$4.8k over 30 rounds. Gemini at 1 fps should only count on performance and pacing. Generation route may never pass the blur gate; test first. Public-domain gold (1926 black and white) won't match; real clay shoot effectively required. A/B raters every 5 rounds unrealistic: Chris alone every 5 rounds, full panel at gates. Open-weight tools need 16-29 GB VRAM. Clay Doh and Rhubarb NG missing from "have ready".
- Writing: no dashes found. AI-sounding lines flagged in mapping ("Equipment is never crew", "They share files") and Director example ("That separation is deliberate"); tangled line in Brave bet 1.
- IP: studio stills must not go to third-party judge APIs or a public A/B page; keep studio and character names out of agent files that feed generation prompts; add a lookalike check at Design Lock; avoid LoRAs with no card; Gemini judging Google-generated clips is same-family, require the other two to agree; don't bundle paid add-ons in open source; clarify personal vs company use for license terms; keep API keys out of `.mcp.json`.
