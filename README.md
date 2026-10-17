# Clay Studio

A starter kit for building an AI clay stop-motion studio as a Claude Code plugin: Claude agents as the crew, Blender driven from code as the stage, tuned toward the standard of the best clay studios.

**Status: v0.4 (design plus first measurements).** No studio code yet. This repo holds the operating model, the design docs, the research, a measured gold set of public clay footage, and the prompt that has Claude Code build the rest. Two independent reviews have been applied (see `reviews/`).

## Start here

1. Read `KICKOFF_PROMPT.md` (setup steps for Chris at the top).
2. Open Claude Code on Opus 5.5 in this repo and paste the prompt.

## What's here

| Path | What it is |
|---|---|
| `KICKOFF_PROMPT.md` | The prompt that runs research, spec, spec review, build, calibration, the tune loop, a pilot production, and packaging |
| `studio/STUDIO_BIBLE.md` | The org: every role, seniority, gates and locks, shot cycle, notes, communication, accountability |
| `studio/CREATIVE_DIRECTION.md` | Creative direction: real textures, fibers, earthy materials, tied by four layers |
| `studio/CLAUDE_MAPPING.md` | Model per role, Claude Code features, skills, workflows, production folder |
| `studio/STORY.md` | Story drafts, thumbnails, boards from Blender, animatic, layout, edit drafts |
| `studio/DESIGN_AND_WORLD.md` | World and material bible, characters, sets, effects, originality checks |
| `studio/FABRICATION.md` | Building characters, sets and props in code |
| `studio/LOOK_DEV.md` | Clay shader, fibers, boil, camera, light, color, post, screen test |
| `studio/MOTION.md` | Motion style guide, the animation engine, motion QC |
| `studio/SOUND.md` | Voice, effects, music, mix, audio QA |
| `studio/ENGINEERING.md` | Repos, Blender pinning, tracker CLI, hooks, compute, review site, tests |
| `studio/GOLD_SET.md` | What the judges compare against (public clips first, a short probe session), who rates |
| `gold/` | 199 openly licensed clay clips cataloged, a curated shortlist, and per-clip measurements |
| `research/01-15` | Fifteen research reports from Oct 17, 2026, with sources |
| `research/16` | What real public clay footage measures: timing, holds, contrast, sharpness |
| `research/17` and `research/studios/` | How Laika, Aardman and other masters work, and CG films that faked stop motion; what that changed in the kit |
| `reviews/` | Independent reviews of the kit |
| `templates/` | Agent file template and a worked Director example |
| `tools/` | R&D scripts from the first pass: clip measurement, look stats, the Blender clay test scene |

Research was gathered by Sonnet research agents on Oct 17, 2026. Versions, prices and licenses move monthly; the prompt re-verifies them first.
