<!-- Independent review of v0.2 by a fresh Opus agent, Oct 17, 2026. Findings resolved in v0.3; see reviews/RESOLUTION-2.md. -->
# Review of Clay Studio kit v0.2 (independent, Oct 17, 2026)

I read every file and changed nothing. No .md file has an em or en dash.

## Coverage of Chris's ten asks
1. **Research, spec, review, build, tune loop:** covered (Phases 0 to 8). Thin: no revert rule, no plateau stop (research/04 §5), no named optimizers (Optuna, GEPA).
2. **Roles, stages, good work, communication, accountability:** strong (bible §2 to 9). Thin: no costume or textile role even though fiber is a house layer; the Lead and Senior layers exist only in animation; `--by <role>` is self-declared.
3. **Claude mechanics:** covered (CLAUDE_MAPPING). Thin: see D.
4 and 5. **No generative video:** met. **Motion:** strong (thin spot: B9).
6. **Shading:** strong. Thin: the subsurface conflict gets "settled with the screen test," but there's nothing real to match against unless Chris's shoot includes the research/10 (c) probes, and Phase 0 doesn't ask for them.
7 and 8. **Boards, sets and world:** covered.
9. **Sound:** covered. Thin: there's no Voice Lock, and nothing pauses for Chris's recordings or a music commission.
10. **Art direction:** covered. Thin: motif conflict (B6); "the maker's hand" has no measurable check.

## A. Review-1 findings not resolved
- Hooks still skip MCP writes (only `Edit|Write` and `Bash`).
- The budget hook says "Only relevant if a paid service is ever enabled." The Gemini and OpenAI judges are paid and on by default, and they run through Bash, which a hook matcher can't tell apart from other commands. Fix: the judge client calls `studio ledger check` before each batch and `studio ledger add` after it.
- "Keep the best" is still undefined (Phase 6.1).
- The real clay shoot is still optional ("or both").
- `templates/example-director.md` says "On Vengeance Most Fowl the directors reviewed...", which breaks the Kickoff's own no-names rule.
- No counsel note on the do-not-resemble film frames (DESIGN_AND_WORLD §7). Personal vs company use is still not addressed.
- Boil is still stated as fact: LOOK_DEV 2.4 says "The surface changes when the puppet is touched, and only then." research/01 marks this as inference and research/09 marks it [U].
- "Studio Bar evidence (bible section 5)": §5 only defines Look Lock evidence.

## B. Contradictions
1. A skill and a workflow are both named `dailies`, so both would run as `/clay-studio:dailies`. Rename the workflow `run-dailies`.
2. Leftovers from the generation route: example-director "the route, and the generation budget"; ENGINEERING `--type <lock/waiver/scope/route/budget>`; bible "bucket or route." Change these to "bucket and render budget."
3. Bible §6.4 says the Supervising Animator approves pop-throughs, but the CLI only refuses when the "Reviewer isn't Lead/Supervising Animator," so a Lead can approve. Fix the CLI.
4. SOUND §8 has the Producer signing off on rights, but the lock table leaves the Producer out and the RACI marks the Producer I on Sound Lock. Make the Producer C and add a rights check.
5. SOUND §3 says "After Dialogue Lock," but that lock isn't in §5.2 and has no owner and no CLI check. Add a Voice Lock after Animatic Lock.
6. CREATIVE_DIRECTION says the fiber "runs through every scene." DESIGN_AND_WORLD §2 says to "cap the motif at roughly a third of frames" and "schedule one deliberate break per act." Pick one rule.
7. Who rates the A/B? Studio Bar: bible says "Chris's blind A/B," Kickoff 6.6 says "my blind A/B with 3 to 5 others." Look Lock: bible says Chris, CLAUDE_MAPPING says Chris plus 3 to 5 others "at... Look Lock and Final," and the Final lock doesn't mention an A/B.
8. The /goal says "every dimension" and counts Gemini only "on performance and pacing," but no kit file lists the dimensions, and none of research/04's six is pacing. Name the six in the prompt.
9. MOTION rule 4 says every part of a puppet changes pose on the same frame. Rule 4.7's `round(t*fps) - 1` puts mouth changes on odd frames. Decide in the spec whether mouths run on ones.

## C. Claims the research doesn't support
- Bible 4.6: "Pinocchio's puppet supervisor ran daily cross-studio calls." research/05 only lists three build cities. Remove it.
- MOTION rule 13 cites "S: Laika 'drift'," but research/07 has no such source. Tag it (D).
- DESIGN §6: "Vengeance Most Fowl left water and fog to VFX." research/01 §4 names no film and no fog.
- DESIGN §5 buckets A, B and C are attributed "as Missing Link did," but research/13 describes Missing Link's buckets differently. Call them ours.
- LOOK_DEV §7: "Laika screen-tests every material." research/15 says wardrobe items.
- LOOK_DEV §4: "key spot about 1.5 to 2 cm across." The research value, `shadow_soft_size` 0.015 to 0.02 m, is a radius, so the spot is 3 to 4 cm across.
- ENGINEERING §7's "$1 to $5" comes from research/03's simple tabletop at 64 to 128 samples, not from finals with subsurface and fibers.

## D. Claude Code accuracy
- ENGINEERING §2 has skills reference "${CLAUDE_PLUGIN_ROOT}/scripts/," but that variable is only available to hooks and MCP config. Ship the scripts as `studio` subcommands (bin/ is on the PATH) or bundle them in each skill with ${CLAUDE_SKILL_DIR}.
- Inside a production repo, agents can't read `studio/*.md` or "bible section 5." Ship those docs as reference files inside `skills/studio-charter/`.
- `bin/studio` needs the bpy venv in ${CLAUDE_PLUGIN_DATA}, and Bash isn't documented to see that variable. Have SessionStart write the path to a known file.
- Plugins don't ship `permissions.deny`; have `make` write `.claude/settings.json` per production.
- Install bpy (1.2 GB) in Phase 0, not inside the SessionStart hook.
- Not in the verified list, so mark [verify]: auto mode, workflow resume, agent teams, scheduled tasks, Fable "needs Claude Code 2.1.257."
- Workflows start from `/plugin:name` or a typed prompt. The kit assumes the Producer can start `tune` or `dailies` on its own in the middle of a loop. Test that in Phase 0, with the Agent tool as the fallback. Also, the pasted prompt says "Use workflows," which may start one right away. Add "don't start a workflow until Phase 1."
- /goal: "after 30 rounds" isn't a turn or time bound, so add "or 300 turns or 48 hours." It also mixes instructions ("Every round prints...") into the done test. Rewrite it as "Done when the latest output shows X, or shows stop reason Y."
- Unused frontmatter that would enforce the bible: `disallowedTools: Edit, Write` on the Director and critics; `omitClaudeMd` and minimal tools on critics, so they stay blind; `maxTurns` on artists; per-agent `hooks` that refuse `--by X` from the wrong role. Spawning heads need the Agent tool listed.
- `agents/` and `skills/` don't load until the plugin is installed. Add a local-marketplace install in Phase 0.

## E. Gaps that will stall or mislead
- Steps that need Chris have no pause: the gold shoot, final voices, the music commission, 60 labeled pairs, outside raters, voice releases. Only the gates say to stop. Add a `waiting_on_chris` list in STATUS.md and a `studio wait` command that blocks dependent tasks.
- `studio packet` is per shot only, so writers, designers and R&D get none. Add `--task <id>` and a fixed handoff-note path for the SubagentStop hook.
- The benchmark shots need characters, sets and voices before Studio Ready. That's a mini-production with no owner and no locks. Define an R&D world, plus a second world for the held-out shots.
- There's no spec for the gold shoot. It should say: 24 fps on twos, tripod, locked exposure and white balance, plus the research/10 (c) probes.
- Keep the hidden judge and held-out briefs outside the repo.

## F. Feasibility and cost
- **Render** (my estimate, not measured): a round is 6 to 8 shots times 3 seeds, about 650 to 860 unique poses. At 2 to 5 GPU-minutes per fiber and subsurface frame, that's 20 to 70 GPU-hours a round ($200 to $1,650 over 30 rounds at research/03 rates). On CPU only, a round takes days. Fix: Phase 0 benchmarks a fiber and subsurface close-up; tune the look on stills; run motion rounds at pop-through tier; require a GPU for Phase 6.
- **Judges:** about 144 image-heavy calls a round, plus critics on every production version. Price it in Phase 0.
- **Gold set:** 10 to 20 seconds of phone clay won't yield 30+ varied items. Chris will recognize his own footage, so his A/B isn't blind. A 0.40 win rate against it means "close to Chris's clay," not studio standard. Fix: outside raters, plus local, human-only studio stills after a counsel check.
- **A/B logistics:** limit the 3 to 5 outside raters to Studio Bar and the pilot.

## G. Writing
Lines that sound AI-written:
- Kickoff: "Plan, staff, track, spend." / "Report what you measured. Mark guesses." / "This tests the org, not just the look."
- CLAUDE_MAPPING: "Taste flows down, evidence flows up." / "The production folder is the studio floor."
- Bible: "Files decide; messages coordinate." / "The Director judges; makers make."
- MOTION §8: "Numbers gate; pictures advise; Chris spot-checks."
- example-director (tangled): "a judge who also builds starts defending choices instead of seeing them"; "mixing the two makes both worse."

Fix: one plain sentence each.

## H. IP, licensing, safety
- Skills built from the studio docs will carry studio, film and character names into agents. Add a scrub step in Phase 4 so skills cite research file numbers instead.
- `rnd/` (ledger, A/B results, gold provenance) sits in the public repo. Move it to a private R&D repo.
- The plugin has no license. Pick one before Brave bet 4; check whether bpy's GPL applies to scripts that import it.
- Check Gemini and OpenAI data-use terms before sending Chris's footage.

## Seven changes, in priority order
1. **Fix the gold set and the bar:** a required shoot spec, outside raters, local studio references, and a bar that claims only what it measures.
2. **Make the plugin work at runtime:** docs shipped as charter references, scripts as `studio` subcommands, a venv path file, settings written by `make`, and a local install while building.
3. **Add a waiting-on-Chris mechanism and a Voice Lock.** The CLI refuses production kickoffs before Look Lock and dialogue shots before Voice Lock.
4. **Rewrite the /goal:** a done test only, a turn or time bound, a plateau stop, the six dimensions named, and a keep-best rule.
5. **Enforce roles:** `--by` hooks, `disallowedTools`, blind critics, and a hidden judge kept out of reach.
6. **Measure compute and judge cost in Phase 0** on a fiber close-up, require a GPU for tuning, and have the judge client handle the ledger checks.
7. **Clean up contradictions and IP:** the dailies name, route leftovers, pop-through approval, sound sign-off, the motif rule, real names, unsupported attributions, a private R&D repo, and a plugin license.
