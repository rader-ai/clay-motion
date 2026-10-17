# Clay Studio status

Updated: 2026-10-17. Producer: Claude (Opus 5.5).

## Phase

**Phase 0: setup, measurements, questions.** In progress.

## Decisions from Chris (Oct 17)

| Question | Answer |
|---|---|
| Render machine | This Mac only (M4 Pro, 16-core GPU, Metal) |
| First production | 10 to 20 second test film |
| Review pages | Local files (a local page that exports `feedback.json`) |
| Voices | Open-weight scratch voices only |
| Judges' API access | Vercel AI Gateway, project `clay-motion` (Chris linked it Oct 17) |

## Done

- Repo cloned; machine inventory in `studio/ENVIRONMENT.md`.
- `bpy` 5.2.2 installed in a pinned environment at `~/.local/share/clay-studio/bpy-5.2.2` (Python 3.13).
- Blender API smoke test (`lib/blender/smoke.py`) passes: version, node types, engines, 5.x APIs, one-frame EEVEE and Cycles Metal renders.
- Render benchmark (`lib/blender/bench.py`), warm, on Metal: pop-through 1.5 s a frame; dailies close-up with wool fiber 42 s; final 161 s. Details in ENVIRONMENT.md.
- Claude Code behaviors marked [verify] checked against the docs; ENGINEERING.md corrected (PreToolUse deny format, plugin agent hooks ignored, workflows not self-started).
- Plugin skeleton: manifest, local marketplace, stub `bin/studio` (`env`, `smoke`), SessionStart hook. Validates, and installed as `clay-studio@clay-motion`. Still to confirm in a fresh session: the hook message and `studio` on PATH.
- git LFS installed; `.blend` files tracked through LFS.
- Judge pricing from AI Gateway's public price list (estimate, see ENVIRONMENT.md).

## Next

- Phase 1, the research refresh (4 to 6 researchers in parallel).

## Spend

| Ledger | Cap | Spent |
|---|---|---|
| R&D | not set (waiting on Chris) | $0.00 |
| Pilot | not set (waiting on Chris) | $0.00 |

Compute is local, so it costs nothing in dollars. Paid spend is judge API calls only.

## Waiting on Chris

Each of these blocks only the work listed after it.

1. **Budget caps for R&D and the pilot.** Blocks: any paid judge call, calibration (Phase 5), the tune loop (Phase 6).
2. **Free disk space.** 13 GB free of 460 GB (97% full). Blender and stills fit; production renders, caches and EXRs won't. Suggest 100 GB free before Phase 5. Blocks: Phase 5 onward.
3. **Plugin license** (GPL-3.0 is the safe match for code that imports `bpy`) **and OK to create the private R&D repo** (suggested `rader-ai/clay-motion-rnd`). Blocks: R&D ledger, held-out briefs, open-sourcing.
4. **Studio signature fiber:** yes or no, and which fiber (suggested: undyed natural wool). Blocks: Style Bible v0 house rules (Phase 2).
5. **Gold references:** will you do the 20-minute phone probe session (stills of clay), and who are your 3 to 5 outside raters. Public clips in `gold/` are the default either way. Blocks: shader numbers settling (Phase 5), Studio Bar gate (Phase 6).
6. **Is the Vercel team on Pro?** Checked the terms: AI Gateway keeps nothing, and per-request zero data retention (free) covers Google and OpenAI, but only on Pro or Enterprise. `studio judge` will always request it. Blocks: first judge call on gold items.
