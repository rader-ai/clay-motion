# Environment (Phase 0, Oct 17, 2026)

Owner: the Pipeline TD. Measured on this machine; re-measure if the machine or Blender version changes.

## Machine

| Item | Value |
|---|---|
| Machine | Apple M4 Pro, 12 CPU cores, 16-core GPU (Metal 4), 24 GB unified memory |
| OS | macOS 27.0.1 (arm64) |
| Disk | 460 GB, **13 GB free (97% full)**. Not enough for production renders; see STATUS.md |
| Render machine | This Mac only (Chris, Oct 17) |
| ffmpeg / ffprobe | 8.1.1 |
| Python | 3.13.16 for Blender; also 3.11, 3.15 on the system |
| Node / npm | 22.23.1 / 10.9.8 |
| git / gh | 2.54.0 / 2.83.1, logged in as `rader-ai` |
| git LFS | **missing** (needed for `.blend` files; `brew install git-lfs`) |
| uv | missing (not needed; plain venv works) |
| Claude Code | 2.1.292 |
| Vercel CLI | 54.21.0 (64.x is current), project `clay-motion` linked |

## Blender

- `bpy` 5.2.2 (Blender 5.2 LTS) from PyPI, in a pinned venv: `~/.local/share/clay-studio/bpy-5.2.2`.
- Smoke test: `~/.local/share/clay-studio/bpy-5.2.2/bin/python lib/blender/smoke.py [out_dir]`. Passes all checks.
- Gotchas found:
  - The render engine list is dynamic: Cycles only appears after `addon_utils.enable("cycles")`. Checking `bl_rna` enum items before that reports only EEVEE.
  - New Python properties (like `Action.slots`) must be checked through `bl_rna.properties`, not `hasattr` on the type.
  - **Metal compiles Cycles kernels on first use**, per feature set: 122 s the first time, then cached. New shader features (hair, subsurface) trigger another compile (about 50 s). Benchmarks must be warm.
- Headless EEVEE works on this Mac.

## Render speed (warm, Metal, one frame)

Scene: `tools/clay_test_scene.py` with round-9 params, plus a 20,000-strand undyed wool yarn collar (`lib/blender/bench.py`).

| Tier | Settings | Seconds per frame |
|---|---|---|
| Pop-through, EEVEE | medium shot, 854x480 | 1.5 |
| Pop-through, Cycles | medium shot, 854x480, 24 spp | 1.4 |
| Dailies | clay and fiber close-up, 1920x1080, 256 spp, adaptive 0.01 | 42 (28 without visible fiber) |
| Final | clay and fiber close-up, 1920x1080, 1024 spp, adaptive 0.005, OIDN Accurate | 161 (108 without visible fiber) |

Visible wool fiber adds about 50% to close-up render time.

What it means for budgets (on twos, 12 unique poses a second, holds duplicated in post):
- The 10 to 20 second test film is 120 to 240 unique frames: about 3 to 11 hours at final quality if every shot were a fiber close-up (wider shots are cheaper), 1.4 to 2.8 hours at dailies quality, a few minutes at pop-through.
- Tune loop: look changes on stills cost seconds to a few minutes each; motion at pop-through is about 1.5 s a frame. A held-out checkpoint (10 shots of about 2 s, about 240 unique frames) at dailies quality is about 3 hours.
- All local, so the cost is time, not dollars. Overnight runs fit the tune loop.
- Each 1080p 16-bit PNG is about 6 to 8 MB, so a 240-frame final pass is about 2 GB before EXRs and caches. With 13 GB free, disk is the real limit.

Look note for the Look Dev Supervisor: at dailies settings the denoiser leaves blotchy, posterized patches on the clay and backdrop (watercolor look). Logged as a first look-dev issue, not a setup blocker.

## Judges and API cost

- Access: Vercel AI Gateway (one endpoint for Gemini, OpenAI and Claude models). The linked project gives a `VERCEL_OIDC_TOKEN` in `.env.local` (gitignored) that the gateway accepts; it expires in about 12 hours (`vercel env pull` refreshes it). A gateway API key in `.env` is the longer-lived option.
- No Gemini or OpenAI keys exist on this machine, and none are needed if we use the gateway.
- Prices (gateway list, Oct 17, per million tokens in / out): Gemini 3.1 Pro preview $2 / $12; GPT-6 Sol $2 / $10; Claude Sonnet 5.5 $2 / $10; Claude Opus 5.5 $4 / $20. Batch variants are half price.
- Estimate per judge call (one pair, 12 full-resolution frames per item, about 2k tokens per image, about 1.5k output): **about $0.12** for Gemini or GPT-6 Sol. [U] until a real call measures token counts.
- Per pair, two paid families, both orders: about $0.50. Per tune round (about 72 pairs): about $35; with batch pricing and 6 frames per item, about $9.
- The Studio Critic (Claude) runs as a Claude Code agent, so it isn't on the API bill.
- Data use (checked Oct 17, vercel.com/docs/ai-gateway/security-and-compliance/zdr, updated 2026-09-22): the gateway itself retains nothing. Per-request zero data retention (`providerOptions.gateway.zeroDataRetention: true`) costs nothing extra but needs a Vercel Pro or Enterprise team; it routes only to providers with ZDR agreements and fails rather than falling back. Google Vertex AI and OpenAI are both listed as ZDR and no-training (OpenAI: "ZDR with safety retention"). `studio judge` will always set the flag. Not yet confirmed: whether the `clay-motion` team is on Pro.
