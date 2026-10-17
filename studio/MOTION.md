# Motion: style guide and animation engine

Owners: the **Supervising Animator** owns the style guide and performance quality. The **Animation TD** owns the engine. Sources: research/07 (craft), research/08 (engine), research/09 (motion QC). Tags: (S) studio-sourced, (T) teaching-site number, (D) our default to tune, [U] unverified.

## 1. The core idea

Nobody has shown a language model writing good character keyframes directly. What works (ArtiMo, Kubrick, Animation2Code in research/08) is a split: the model makes the discrete acting choices, deterministic code does the numbers, and checks run on measured data plus pictures. So here:

- **Claude decides:** which poses, held how long, in what order, with what intent, where contacts land, what the eyes do.
- **Code decides:** spacing, easing, anticipation and settle shapes, sampling on twos, contact solving, secondary layers, lip-sync timing.
- **Checks read numbers first:** bone positions per exposure, contact drift, cadence, spacing. A vision critic gives a second opinion on poses and staging from filmstrips. Vision models are weak at judging timing (research/08: temporal score at most 0.31), so they never gate timing.

Claude edits `shot.yaml`, never raw keyframes.

## 2. Acting principles

1. Act it out first. For hero shots Chris records a live-action reference on his phone; the Animator interprets it rather than copying it (Nick Park acted every Early Man shot).
2. Every shot has one story point. Protect it.
3. Eyes and brows lead, the head follows, the body follows the head.
4. Pauses are performance. Contrast fast and slow. Hold back on expressive puppets.
5. Each character has a movement vocabulary: pose size, speed, blink rate, arm carriage (Memoir of a Snail did this per character). It lives in the character bible.
6. Repeat a gesture to land a repeated line.
7. Small business (a glance, a finger tap) holds attention.
8. Play it straight. The comedy comes from seriousness.
9. Feel the weight. Plant before you move.

## 3. Motion style guide v1 (24 fps)

Frame strategy
1. Bodies on twos: 12 poses a second. (S: Aardman, Isle of Dogs, Selick)
2. Ones for camera-move shots, actions shorter than 6 frames, eye and lid work, and fast moves, because twos strobe at speed. (S)
3. The camera always moves on ones. A character on twos under a camera move gets its poses offset half a step, or goes to ones for that shot, so it doesn't stutter against the camera (Aardman's "one-and-a-half" correction). (S)
4. One exposure grid per puppet: every part of a puppet changes pose on the same frame, because a real puppet can't update parts independently. The one exception: during dialogue the face (mouth, lids, brows) may run on ones while the body stays on twos, which Laika's face counts suggest [U]. When the face stays on twos, mouth changes snap to the body's grid. The spec decides per character.

Eyes and face
5. Blink: 6 frames (2 closing, 1 closed, 3 opening). Fast 5, long 9. At least 2 frames of half-lid. (T)
6. Blinks are irregular, 60 to 180 frames apart, placed at thought changes or mid-to-late in head turns. A tense character doesn't blink. (T, D)
7. Eye dart: 2 to 3 frames, about 80% of the move in the first frame. Eyes arrive 2 to 4 frames before the head. (T, [U] on the lead)
8. Change expression through brows and eyes first, then hold at least 12 frames so it registers. (T)
9. Thinking beat: eyes settle, then hold 12 to 24 frames before acting. (D)

Timing
10. Anticipation 4 frames (6 if punchy), action, settle 7. A take: anticipation 4, take 7, settle 7; a punchy take uses a 1-frame pop. (T)
11. Small overshoot, then return over 6 to 8 frames with shrinking steps. (D)
12. Never hold for 3 to 5 frames; it reads as a mistake. Minimum hold 6 frames, and only with a moving hold. 12 frames for an expression, 16 to 18 comfortable, 24+ for comedy. (T)
13. Moving hold: the body drifts along the momentum of the last move, with a breath, eye dart or weight settle every 6 to 12 frames. Never stop everything on the same frame. (D)
14. Starting durations: gesture 6 to 8, head turn 8 to 12, weight shift 12 to 18, sit or stand 18 to 30. (D)

Spacing
15. Moves travel on arcs with 3 ease-in steps, even middle steps, 3 ease-out steps (roughly 1 : 3 : 4 : 3 : 1 of the main step). Extremities settle last. (S: surface-gauge practice)
16. No unmotivated spacing jumps ("pops"). A deliberate pop (snap-look, flinch) gets 4 to 6 frames of anticipation and a hold of 6 or more. (S: Priebe's publisher site names pops as serious distractions)
17. Overlap: head lags torso 2 to 3 frames, hands lag forearm 1 to 2, ears or cloth lag 2 to 4 with shrinking amplitude. (D)

Lip sync
18. Mouth shapes land 1 frame before the sound. Closed shapes (B, M, P) land on the sound frame or 1 before. Every shape holds at least 2 frames. (T)
19. 8 to 15 shapes per character. Accent the stressed syllables; skip or merge the rest. Keep the jaw small. (S: Shaun used 15, Isle of Dogs 12 to 14)
20. A gesture or head move starts 4 to 6 frames before a line. Brow accent on the stressed word. Blink at phrase ends. (T, D)

Locomotion
21. Avoid walks where the story allows: crop below the knee, slide on a hidden rig with a small bounce, cut away, or exit frame. (S: Memoir of a Snail)
22. When a walk is needed: 16 to 18 frames per step for chunky puppets, 12 for light ones, and the planted foot is locked from contact to passing. Sliding feet are the most obvious amateur tell. (T, D)
23. Jump: anticipation 4 to 6 frames, wide spacing at take-off and landing, tight at the top, contact, 2 to 3 frames of squash, settle 6 to 8. (D)

Clay and handmade
24. Squash and stretch lives in faces, hands and gags: 1 to 2 frames of extreme, volume preserved. Full-body squash breaks the puppet illusion. (D)
25. Imperfection goes into surface texture (boil, see LOOK_DEV.md) and into step sizes (about plus or minus 10 to 15% on channels the animator "touched"). Never on contacts, eyelines or holds, where noise reads as wobble. (D)

## 4. The animation engine

All of it is plain Python except the Blender adapter, pinned to Blender 5.2 LTS (bpy 5.2.2, Python 3.13). Every component has golden-file tests.

### 4.1 Standard puppet rig (`puppet.json` + builder)
- One shared bone set of about 25 bones: root, pelvis, two spine, neck, head, arms (FK), legs (IK), optional hand and foot controls. Every character uses it; only proportions and meshes change, the way a studio reuses an armature design.
- Rigid parts: each body part is its own mesh, parented to its bone. No skin weights. This matches how clay puppets are built (kits of parts over an armature) and makes code-built characters easy (see FABRICATION.md).
- Squash and stretch: a per-bone `stretch` property drives scale along the bone and `1/sqrt(stretch)` on the other two axes.
- Replacement slots: `mouth`, `brow_l`, `brow_r`, `lids`, `eyes`. Each slot is a set of objects on one anchor bone plus one integer property keyed CONSTANT. Applied with a Geometry Nodes Index Switch (Blender 5.2 reads modifier inputs from `modifier.properties.inputs`).
- Mouth set: Rhubarb shapes A to H plus X, built from one parametric lip model per character, each frozen with its own seed.

### 4.2 Pose library (`poses/*.json`)
- Named poses stored as bone rotations plus replacement states, with a one-line description and a thumbnail. JSON diffs and validates better than Blender pose assets; export to pose assets only when a human wants to edit.
- Operators: mirror, blend, mask by body part, offset.
- Every character starts with 12 base poses (neutral, lean in, lean back, look left, look right, reach, point, shrug, slump, surprise, think, laugh) and grows a library per production.

### 4.3 Beat sheet (`shot.yaml`)
The animator's exposure sheet in data form. Example:

```yaml
shot: SQ010_SH020
fps: 24
exposure: twos            # default; segments can override
camera: {move: push_in, from: 0, to: 48, ease: s_curve, on: ones}
beats:
  - at: 0     pose: neutral          hold: 18   note: listening
  - at: 18    look: {target: kettle, eyes_lead: 3}
  - at: 24    pose: lean_in          ease: settle   anticipation: auto
  - at: 40    pose: think            hold: 16   blink: true
  - at: 56    pose: surprise         ease: snap     exposure: ones
contacts:
  - plant: left_foot   frames: 0-72
  - plant: right_foot  frames: 0-72
dialogue:
  - line: "It's boiling over!"   audio: vo/sh020_v3.wav   start: 58
secondary: {breath: on, idle_shift: off, mask: [56, 66]}
seed: 4112
```

### 4.4 Timing compiler (`exposures.json`)
1. Expand beats into dense curves with the named ease (linear, ease, snap, overshoot-settle).
2. Insert anticipation (a small counter-move 2 to 4 frames before a move), overshoot of 5 to 15%, and settle over 3 to 6 frames. Tag these keys `auto` so a reviewer can see what the compiler added.
3. Sample the curves at the exposure rate (twos by default, per-segment overrides) and write CONSTANT keys. Bake the steps rather than leaving a stepped modifier, so irregularity and reproducibility are exact.
4. Apply seeded irregularity only to channels a beat touched (about 0.2 to 0.5% of limb length, under 1 degree). Everything else holds exactly.
5. Add moving-hold drift (about 1 to 2% of the previous move).
6. Output `exposures.json`: the single source of truth for every bone, slot and camera value at every exposure.

### 4.5 Contact solver
- Contacts come from the beat sheet, so they are ground truth.
- During a plant, the IK target holds its world transform. Between plants, feet swing on a lifted arc. Feet raycast to the floor.
- Props hand off with keyed Child Of influence. Simulated props are baked by stepping frames, then sampled on twos like everything else.

### 4.6 Secondary layers
Seeded additive layers summed before sampling: blinks and eye darts per the style guide, breathing (3 to 4 second cycle, low amplitude), idle weight shifts, settles after moves. Masked out during emphatic acting. Seed from shot, channel and take.

### 4.7 Lip sync
Rhubarb 1.14.0 CLI with the dialogue text supplied, JSON output, run only after Voice Lock. `frame = round(t * fps) - 1` (a 1-frame lead), minimum hold 2 frames, cues shorter than an exposure merged, snapped to the body's grid when the face runs on twos, keyed CONSTANT on the mouth slot. Brow accents and blinks come from transcript tags Claude adds (emotion and beat labels), converted by rules.

### 4.8 Camera
A motion-control style rig (dolly, pan, tilt, boom) with S-curve eases, sampled on ones. Optional seeded low-frequency shake, off by default; miniature moco is clean.

### 4.9 Review outputs
For every pop-through and final, the engine writes:
- `exposures.json` (above), plus per-exposure world positions of every bone and contact state.
- A filmstrip: one image per key pose, cropped to the subject, with onion-skin ghosts and drawn arcs for head and hands, with motion-QC flags marked.
- `motion_qc.json` (section 6).
Claude Code reads images, not video, so filmstrips are the visual review format.

### 4.10 Performance from reference video (optional)
1. Chris records the shot on his phone.
2. MoCapAnything V2 (MIT) turns it into 3D joints fitted to our rig (it supports custom rigs through a Blender script).
3. Key-pose extraction (Roberts et al. dynamic programming over piecewise-linear fits; keep about 10% of frames; we reimplement it) reduces dense motion to a few strong poses.
4. Each key snaps to the nearest library pose or keeps a small residual, then gets re-timed onto twos in `shot.yaml`.
5. Mocap is reference, not the animation. Retarget by matching root path, head, hands and foot contacts scaled by proportion, never by copying rotations onto short limbs.
- Licensing: GVHMR, SMPL, WHAM and 4D-Humans need SMPL or are non-commercial. Don't use them. HY-Motion and SAM 3D Body licenses are unverified; check before any use.

## 5. Pop-through first

The pop-through is the cheap preview approved before any final render (research/06): key poses only, rendered fast (Workbench or low-sample Cycles), shown as a filmstrip plus a stepped playblast. The Lead Animator reviews it and gives notes, the Supervising Animator approves it (the Director on hero shots), and the tracker CLI refuses a final render until it's approved.

## 6. Motion QC

Computed from Blender data, never pixels. Thresholds scale with character height H and are starting points (research/09) to calibrate against our own approved shots.

| Check | Hard fail or warning | Starting threshold | Catches |
|---|---|---|---|
| Foot skate during plants | Fail | Drift above 0.5% of H | Sliding feet |
| Ground penetration or float | Fail | 5 mm at human scale, scaled to puppet | Sinking, hovering |
| Part interpenetration (BVH) | Fail | Above 1% of a part's triangles | Limbs through body |
| Held-frame change | Fail | Any change on a held exposure | Flicker on holds |
| Cadence | Fail if unplanned | Hold-length mode 2; unplanned 1s or 3s flagged | Inconsistent stepping |
| Spacing evenness | Warning | Step-length variation below 0.1 on moves of 5+ poses | Robotic moves |
| Ease profile | Warning | No slow-in or slow-out | Mechanical starts and stops |
| Arc quality | Warning | Sagitta/chord below 2% on big moves | Straight-line paths |
| Pops | Warning | Acceleration above 4x local median | Unmotivated snaps |
| Anticipation | Warning | Below 5% of amplitude before a big move | Missing windup |
| Overshoot and settle | Warning | None above 3% on big stops | Dead stops |
| Pose change per step | Warning | Above about 30 degrees unless tagged fast | Strobing |
| Twinning | Warning | Mirrored limbs for 3+ poses unless tagged | Symmetric, lifeless posing |
| Silhouette clarity | Warning | Hand overlapping torso mask above 60% on a key pose | Unreadable poses |
| Line of action | Warning | Near-straight spine on key poses | Stiff posing |
| Mouth timing | Fail | Shape after its sound, or held under 2 frames | Late or flapping mouths |

Warnings go to the Lead Animator and the vision critic with the filmstrip. The vision critic answers fixed yes or no questions per key pose (does the pose read, where does the eye go, is the intent clear) and never scores timing.

Learned motion-quality metrics from the research (MotionCritic, PP-Motion, HumanScore) are trained on realistic human motion. Stepped puppets are outside what they've seen, so they're advisory only, never gates.

## 7. Build order (Animation TD)
1. Pinned bpy environment and a filmstrip renderer.
2. Puppet builder and 12 base poses for one test character.
3. Timing compiler on twos, golden tests, then a first acting shot with no dialogue.
4. Replacement slots, Rhubarb mapper, blinks and eyes; a dialogue shot.
5. Contact solver and motion QC; a walk and a prop pick-up.
6. Camera rig; a push-in shot with the half-step offset.
7. Tune irregularity and moving holds against the Supervising Animator's notes.
8. Reference-video pipeline.
9. Regression suite: every approved test shot becomes a golden test that must still compile identically.

## 8. Risks
- The real quality ceiling is the clay look and the mouth and eye sets, not the timing code.
- Irregularity can read as jitter. Tune it on approved shots, never by eye on one shot.
- Blender API churn (5.0 slotted actions, 5.2 modifier inputs): all keying goes through one adapter module.
- Vision critics miss motion faults, so the numeric checks are the gates, the filmstrip critic only advises, and Chris spot-checks.
