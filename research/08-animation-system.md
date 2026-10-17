# Code-driven clay animation in Blender 5.x: research and architecture (Oct 17, 2026)

~37 searches and 50+ fetches. Blender manual and API pages returned navigation only, so unconfirmed API names are marked [U]. Numeric acting heuristics in section 5 had no source [U] (see research/07 for sourced timing).

## Bottom line
- Nobody has shown LLMs writing good character keyframes directly. What works: the LLM emits discrete, structured plans; a deterministic executor does the numbers.
- No Blender add-on does anticipation, overshoot and settle for you. Existing stop-motion add-ons are UI tools with no documented Python API. Build the timing compiler.
- Licensing is a hard constraint: SMPL and GVHMR are non-commercial, which matters for any company use.

## 1. Rigs and replacement parts
- Standard rig: a puppet spec (JSON) and a builder script that creates armature, parts and replacement sets. ~25 bones: root, pelvis, 2 spine, neck, head, arm and leg chains (leg IK, FK arms), optional hand and foot controls. Every character shares the topology; only proportions and meshes change.
- Rigid-part characters: one mesh per part, parented to its bone at weight 1.0. No skinning; skip auto-rigging.
- Auto-rigging, skip for the standard puppet: Rigify generates large rigs [U]; Auto-Rig Pro (paid, no documented scripting API; its Remap feature for BVH/FBX retargeting is useful); UniRig (MIT, 8 GB+ GPU, degrades on odd skeletons); SkinTokens/TokenRig (MIT, 14 GB GPU, no stylized evidence). Use only for one-off creatures or props.
- Squash and stretch: per-bone custom property, scale 1/sqrt(stretch) on the other two axes. Alternatives: Stretch To, bendy bones, lattice or Simple Deform, shape keys. Blender Studio Tools (GPL v2+) ships Lattice Magic, Pose Shape Keys, Geonode Shapekeys.
- Replacement parts: each slot (mouth, eyes, brows) is a set of objects sharing an anchor bone, plus one integer property keyed CONSTANT. Apply via Geometry Nodes Switch / Index Switch on that integer, or drivers on `hide_render`/`hide_viewport` [U]. Blender 5.2 moved GN modifier inputs to `modifier.properties.inputs`; older scripts break.
- Existing replacement add-ons: Swap Animator (Blender 4.x; warns collection-visibility keying is unreliable); Keymesh (v2.3.2, updated for 5.0, no documented API).
- Real productions: Aardman premakes clay mouths, keeps clay on the face. The Shopkeeper's Tail (indie game) used low-poly meshes, Remesh for a gloopy look, simple FK armatures.

## 2. Performance as data
- Pose storage: Blender pose assets work (5.2 fixes cross-rotation-mode application). For an agent, plain JSON poses (bone to quaternion, plus named replacement states) diff and validate better; export to pose assets only for human editing.
- Pose language: named poses with descriptions and thumbnails, plus mirror, blend and body-part mask operators.
- Beat sheet: an exposure sheet of beats, e.g. `t=1.25s pose=lean_in ease=settle hold=0.5s`, plus look_at, contact and dialogue rows.
- Animation DSLs: no mature "animation as code" project for Blender.
  - MotionScript: structured text for poses and motions; still needed a trained model; LLM output hallucinated extra motion.
  - ArtiMo (arXiv 2608.20699, Aug 2026) is the best template: a VLM perceives, an LLM writes a time-stamped joint plan in JSON with phases (actuate, latency, effect, settle), a deterministic executor runs it, and a VLM critic views keyframes with trajectory overlays for up to 3 rounds. Structured planning raised the main score 0.703 to 0.962. The critic caught 93.5% of injected faults, weaker on excess motion. No code linked.
- Blender LLM agents (mostly static): SceneCraft (scene graph + VLM critique, static); LL3M (six agents, five-view critic renders, API-doc RAG cut errors 26%; VLMs missed spatial faults; object-in-hand took 3-4 follow-ups); BlenderLLM (CAD only); Kubrick (Mixamo rigs, VLM reviewer with screenshots plus measured armature coordinates, up to 15 iterations, misjudged subtle orientation); StoryBlender (Apr 2026) and Cutscene Agent (Unreal, 2026) retrieve prebuilt motion instead of writing keys.
- Why verification must be numeric too: Animation2Code (Jun 2026): VLMs reproduce appearance but not timing (temporal score at most 0.31); tracking metrics beat a VLM judge. Code2Video: timing between beats and missing easing are typical failures.
- Takeaway: Claude picks poses, holds and beats; code does spacing; check with bone-data numbers plus filmstrips.
- MCP: Blender Lab official server (projects.blender.org/lab/blender_mcp, Blender 5.1+, runs code unguarded); ahujasid's renamed "MCP for Blender" (Sept 2026). Look-dev only.

## 3. Timing and spacing compiler
1. Expand beats into dense curves; each beat has a named ease: linear, ease, snap, overshoot-settle.
2. Auto-insert anticipation (small counter-pose 2-4 frames before a move), overshoot ~5-15%, settle over 3-6 frames [U]. Tag these keys "auto" so they stay reviewable.
3. Sample the evaluated pose at exposure times (twos by default, ones for fast action, per-segment rate) and write CONSTANT keys. Bake, don't leave stepping as a modifier: baking gives per-exposure irregularity and exact reproducibility.
4. Irregularity: seeded offsets ~0.2-0.5% of limb length and a degree or less of rotation, only on channels the animator "touched". Everything else holds exactly. Moving holds as tiny drift (~1-2% of the preceding move [U]).
5. Pure Python compiler. Output `exposures.json` is the single source of truth.
- Existing tools: Stop Motion Style Animator (v0.3.2, Feb 2026, GPL, Blender 5.0+; Step Frames, Phase Offset, Noise Jitter 0.05-0.3; no API). Stop-Mo (step amount only). Blender Stepped F-curve modifier (`fcurve.modifiers.new('STEPPED')`, frame_step and frame_offset [U]).
- API churn: every action is slotted in 5.0. Third-party guides report `action.fcurves` removed; replacement is `bpy_extras.anim_utils.action_ensure_channelbag_for_slot()` and channelbag `fcurves.find/new/ensure`. Wrap keying in one adapter and pin the Blender version.

## 4. Contact and physics
- Contact intervals in the beat sheet, e.g. `plant(left_foot, frames 10-22)`.
- Solver: during a plant, hold the IK target's world transform (Blender 5.0 Copy Global Transform helps); swing feet on a lifted arc between plants; raycast to the floor with `scene.ray_cast` plus surface offset [U]. Spider Walker (Blender 5.2+) shows the plant-and-swing pattern baked to an Action.
- Lint: foot world velocity during plants below epsilon; minimum foot height at or above floor; `mathutils.bvhtree` overlap tests [U].
- Props: keyed Child Of influence for handoffs. Simulated props: bake rigid bodies by stepping frames, then sample on twos [U].

## 5. Secondary motion (all numbers [U]; prefer research/07 values)
- Seeded additive layers summed before sampling: blinks, eye darts, breathing (3-4 s cycle, low amplitude), idle weight shifts (every 4-8 s), settles after each move. Mask out during emphatic acting. Seed with `random.Random(hash(shot, channel, take))`.

## 6. Reference video and text-to-motion
- GVHMR (zju3dv): world-grounded; `-s` skips visual odometry for static cameras; NON-COMMERCIAL license, commercial use needs permission.
- SMPL body model: commercial use needs a separate license (Meshcapade or MPI). WHAM and 4D-Humans: MIT code but require SMPL.
- FlowHMR (Oct 2, 2026; github.com/flowhmr/flowhmr): physics-trained; 82% PHC+ simulation success vs 63% for GVHMR, lower penetration and floating; GVHMR still lower skating. License unchecked [U].
- SAM 3D Body (Meta, Nov 2025): single image, MHR mesh, gated checkpoints, license unchecked.
- MoCapAnything (CVPR 2026): predicts 3D joints from video, fits rotations by IK onto any skeleton. V2 repo (animotionlab26/MocapAnything, MIT) is a clean reimplementation; outputs BVH; supports custom FBX rigs via a Blender script; no contact reasoning. Best commercial-safe starting point.
- Retargeting to short-limbed rigs: don't copy rotations. Match root path, head, hand targets and foot contacts scaled by proportion, then IK. Mocap is a performance reference, not the final animation.
- Key-pose extraction: Roberts et al. (CVM 2019) dynamic programming over piecewise-linear fits; ~10% of frames keeps most detail; a human picks the count at error cliffs; roughly cubic cost, so split long clips. Reimplement (no repo found [U]). Snap each key to the nearest library pose or keep a residual; re-time to even frames.
- Text-to-motion: HY-Motion 1.0 (1.0B, SMPL-H 22 joints, no hands, 30 fps, 26 GB VRAM; Lite 24 GB; license unverified); MoScale (Apr 2026, fast, inpainting); MoMask, MotionGPT-2 older. Draft references only; no published stop-motion stylization.

## 7. Facial performance
- Rhubarb Lip Sync 1.14.0: WAV or OGG in; TSV (default), XML, JSON or DAT out. Shapes A-F, optional G, H, X. English via pocketSphinx; `-d` transcript improves accuracy.
- Pipeline: CLI to JSON, `frame = round(start*fps)`, merge cues shorter than the exposure step, key CONSTANT on the mouth-set integer, lead audio 1-2 frames.
- Skip Rhubarb Lipsync NG (UI-only) and caption-based mouth add-ons.
- Brows and blinks: LLM tags the transcript with discrete emotion and beat labels; rules convert to brow states, blinks at phrase boundaries, nods.
- Audio-to-expression (NVIDIA Audio2Face-3D, LAM_Audio2Expression) output ARKit blendshapes that don't fit discrete clay sets. Skip for v1.

## 8. Camera
- Moco on ones even when puppets are on twos. Rig with dolly, pan, tilt, boom parameters, S-curve eases, frame-by-frame sampling.
- Shake: Camera Shakify (v0.5.1, Feb 2026, GPL) or seeded low-frequency noise; optional, since miniature moco is usually clean.
- Framing templates computed from bone positions (Cutscene Agent pattern).

## 9. Agent engineering
- Runtime: `blender -b scene.blend -P run.py -- args`, or `pip install bpy` 5.2.2 (Sept 15, 2026): CPython 3.13 only, Linux x86-64 glibc 2.28+, macOS ARM, Windows; ~1.2 GB; GPL-3.0. Blender 5.1 moved to Python 3.13. `bpy` is global state: one scene per process. Pin 5.2 LTS; fake-bpy-module-5.2 for typing.
- Preview: EEVEE engine id is `BLENDER_EEVEE` in 5.0; headless GL via EGL exists; 5.2 added `gpu.init()` for background mode; EEVEE headless unverified, test on the target box. Fallback: Cycles CPU at 16-32 samples with denoise at 480p, or `xvfb-run`. Render only unique exposures; repeat holds in ffmpeg (halves cost on twos).
- What Claude reads: per-exposure JSON (bone world positions, replacement indices, contact states, camera); contact-sheet filmstrips cropped to the subject with ghosting or trails; a lint report (foot slide, penetration, odd-frame changes, peak angular velocity, hold lengths, minimum mouth cue length). Claude Code reads images, not video.
- Tests: pytest on the pure-Python compiler with golden JSON; Blender integration tests exiting nonzero on error (`--python-exit-code` [U]).
- Determinism: seed everything, pin versions, bake physics.
- Farm: Flamenco (Blender Studio, GPL-3.0) if one machine isn't enough.

## Recommended architecture
Claude edits `shot.yaml`, not Python.
1. Puppet spec and builder (build)
2. Pose language and library (build)
3. Beat sheet (build)
4. Timing compiler: easing, anticipation, overshoot, settle, sampling, irregularity, `exposures.json` (build, pure Python)
5. Contact solver and lint (build)
6. Secondary-motion layers (build)
7. Lip sync: Rhubarb CLI plus a cue-to-exposure mapper
8. Camera rig (build; Camera Shakify optional)
9. Review loop: headless render, filmstrip, JSON, lint (build)
10. Reference mocap: MoCapAnything V2 plus a key-pose extractor
11. Farm: Flamenco or a single box
Skip: Rigify, Auto-Rig Pro, UniRig for the standard puppet; Swap Animator, Keymesh, Stop Motion Style Animator in the pipeline; MCP in production; ARKit audio-to-face.

Risks: licensing (SMPL, GVHMR, HY-Motion, SAM) needs a legal check; Blender API churn (pin and adapt); weak VLM motion judgment (numeric lint plus human spot checks); the look of the clay and the mouth/eye sets is the real quality ceiling; irregularity can read as jitter (tune against reference clips); headless EEVEE uncertain; mocap onto chunky proportions causes intersections.

Build order: (1) pinned bpy environment and a sheet renderer; (2) puppet builder with 12 poses; (3) compiler on twos, then a first acting shot; (4) replacement system with Rhubarb, blinks, eyes; (5) contact solver and lint, then a walk and a prop pickup; (6) camera moco; (7) irregularity and moving-hold tuning; (8) mocap and key-pose pipeline, then text-to-motion drafts; (9) farm and golden regression tests.

## Sources
https://pypi.org/project/bpy/
https://developer.blender.org/docs/release_notes/5.0/animation_rigging/
https://developer.blender.org/docs/release_notes/5.1/python_api/
https://developer.blender.org/docs/release_notes/5.2/python_api/
https://developer.blender.org/docs/release_notes/5.2/animation_rigging/
https://pypi.org/project/fake-bpy-module-5.2/
https://studio.blender.org/tools/overview/introduction
https://flamenco.blender.org/
https://github.com/Premik/blender_rhubarb_lipsync_ng
https://github.com/DanielSWolf/rhubarb-lip-sync
https://extensions.blender.org/add-ons/keymesh/
https://extensions.blender.org/add-ons/stop-motion-style-animator/
https://extensions.blender.org/add-ons/camera-shakify/
https://dawsonturska.itch.io/shopkeepers-tail/devlog/913535/devlog-2-how-we-used-blender-to-simulate-claymation
https://digitalproduction.com/2026/08/28/spider-walker-automates-multi-leg-animation/
https://github.com/VAST-AI-Research/UniRig
https://github.com/VAST-AI-Research/SkinTokens
https://arxiv.org/html/2608.20699
https://arxiv.org/html/2312.12634v5
https://arxiv.org/html/2403.01248v1
https://arxiv.org/html/2508.08228v1
https://arxiv.org/html/2412.14203v1
https://arxiv.org/html/2408.10453v1
https://arxiv.org/html/2604.03315v1
https://arxiv.org/html/2604.25318
https://arxiv.org/pdf/2606.28593
https://www.blender.org/lab/mcp-server/
https://github.com/zju3dv/GVHMR
https://smpl.is.tue.mpg.de/modellicense.html
https://arxiv.org/html/2610.03691v1
https://github.com/facebookresearch/sam-3d-body
https://arxiv.org/html/2512.10881v1
https://github.com/animotionlab26/MocapAnything
https://scribblethink.org/Work/Pdfs/roberts_OptimalAndInteractiveKeyframeSelectionForMotionCaptureJournalversion.pdf
https://github.com/Tencent-Hunyuan/HY-Motion-1.0
https://arxiv.org/html/2604.03799v2
https://github.com/aigc3d/LAM_Audio2Expression
