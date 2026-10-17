# Clay Studio starter kit

Everything Claude Code needs to build an AI clay stop-motion studio as a plugin, tuned toward the standard of the best clay studios.

**Status: draft v0.1.** Research on motion, shading and storyboarding is in progress, and an independent review's fixes (in `reviews/`) haven't been applied yet. The next version makes code-driven Blender the primary route, with generative video optional.

## What's here

| File | What it is |
|---|---|
| `KICKOFF_PROMPT.md` | The prompt to paste into Claude Code (Opus 5.5). Setup steps for you at the top. |
| `studio/STUDIO_BIBLE.md` | The org: every role, seniority, stages and locks, shot cycle, notes format, communication, accountability. |
| `studio/CLAUDE_MAPPING.md` | How the org runs in Claude Code: model per role, features, plugin layout, gates enforced by code. |
| `research/01-studio-craft-standards.md` | What top clay studios actually do: timing, surface, faces, light, failure modes, a draft rubric. |
| `research/02-generative-video.md` | Video and image models, LoRAs, post tricks, lip sync, agent-drivable tools (Oct 2026). |
| `research/03-blender-3d-pipeline.md` | The code-driven Blender route: clay shaders, stepped animation, rigs, mouths, miniature camera. |
| `research/04-eval-harness.md` | How to grade clay automatically without being fooled: code gates, judge panel, human A/B. |
| `research/05-studio-roles.md` | How real studios staff a production, with seniority and sign-off. |
| `research/06-production-pipeline.md` | Stages, locks, artifacts, notes culture, statuses, throughput. |
| `templates/` | Agent file template and a worked Director example. |
| `reviews/` | Independent reviews of the kit and what they found. |

## How to start

1. Put this kit in a private repo (`rader-ai/clay-studio`).
2. Open Claude Code there on Opus 5.5.
3. Paste the prompt from `KICKOFF_PROMPT.md` (everything below the line).

All research was gathered Oct 17, 2026 by Sonnet research agents. Model versions, prices and licenses move monthly; the prompt tells Claude Code to re-verify them first.
