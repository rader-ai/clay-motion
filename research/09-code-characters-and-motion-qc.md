# Code-built clay characters and motion QC from 3D data (research, Oct 17, 2026)

About 45 searches and 60 fetches. Blender manual/API pages didn't load for the researcher, so Blender node and API details come from release notes and prior knowledge, marked [U]. All numeric thresholds are the researcher's starting points, not published values, unless a source is named.

## PART A: Building characters, sets, props in code

### A1. Sculptor workflow in code
- Aardman puppets are kits of parts in wool, clay, silicone and textiles over hidden engineered armatures. Chicken Run bodies skinned in sculpted silicone; clay wings pressed from two-part molds. No primary source on bulking with lumps and coils [U]; assumed order: armature, masses, smoothing, marks.
- Blender 5.0 added a grid socket and ~27 volume nodes: Mesh to SDF Grid, Points to SDF Grid, SDF Grid Boolean, SDF Offset, Fillet, Mean, Median, Laplacian, Grid to Mesh. Smooth-blend option on SDF Grid Boolean is [U].
- Proven workaround (80.lv claymation fire): min/max on density fields with Smooth Maximum; cuts read as pressed clay.
- fogleman/sdf (MIT): out-of-Blender SDF modeling with k-smooth union/difference/intersection, numpy-batched marching cubes, STL output (OBJ/PLY via meshio).
- Scripted sculpt strokes (`bpy.ops.sculpt.brush_stroke`) exist but are likely fragile headless [U]; avoid.
- Commercial references only: Kin Klei "klei krush" GN noise distortion; Clay 4.Doh (paid, ~$30, finger dents, 13 presets). Licenses unchecked [U].

### A2. Hand-sculpted, not CG
- Nick Park wants the clay visible; animators discouraged from smoothing; fingerprints kept on purpose.
- Aardman's creative director: the most expressive facial moments are shaped by hand, so thumbprints show there.
- Aardman color-matches clay to silicone and plastic parts; supports per-part hue variation (range is a design choice [U]).
- Blender "wonky modifier" pattern (BlenderNation) for un-perfecting geometry with loopable noise.
- ambientCG Fingerprints001-009: CC0, grease smudges with Color/Normal/Roughness/Opacity maps. Use for roughness only, not dents.
- ambientCG added ClaySubstance002 and Clay005-009 on 2026-10-15: CC0, SBSAR source, ~20 cm tile, Color/Displacement/Normal/Roughness. Tagged Clean/Flat/Smooth; appearance unseen [U].
- No "plasticine" results on ambientCG; "felt" only Fabric034. Poly Haven is CC0 (API needs a unique User-Agent); clay availability [U].
- No scanned plasticine library found. Procedural dents (real geometry depth) plus roughness smudges likely beat scans in close-ups, since scans carry baked lighting [U].

### A3. Cycles clay shading
- No public measured values. Aardman and University of Bath (Howell, Hall, Child) measured plasticine reflectance and fitted a model claimed ~20% more accurate than standard shaders; parameters not accessible.
- Plasticine is oil, wax and clay mineral, non-drying. Inferred: waxy, semi-matte, low translucency [U].
- Cycles 5.0 improved random-walk SSS (fewer dark artifacts, higher cost).
- Starting values [U], tune against a reference photo: roughness 0.45-0.6 with fingerprint modulation ~+/-0.1; sheen weight 0.1-0.25, sheen roughness 0.5, tinted to base color; subsurface weight 0.05-0.15, random walk, radius a few mm in scene units; coat 0.
- Small hard area lights (a few cm). Check that the denoiser doesn't erase fingerprints [U].

### A4. Mouth sets
- Rhubarb shapes: A closed (P/B/M); B slightly open, clenched (K/S/T/EE); C open (EH/AE); D wide (AA); E rounded (AO/ER); F pucker (UW/OW/W); G teeth on lip (F/V); H tongue up (long L); X rest. Output TSV, JSON or XML. `--extendedShapes` defaults to GHX. Recognizer: PocketSphinx (English) or phonetic.
- Laika prints replacement faces on a Stratasys Connex3; Missing Link 106,000 faces (Guinness). Kubo counts conflict between sources. Coraline faces hand-painted, seams cleaned in post.
- Gromit has no mouth; the brow carries emotion. Nothing found on Aardman mouth-set size [U].

### A5. Boil
- Kin Klei changes a global seed every Frame Step frames; material and displacement steps must match.
- Stop Motion Style Animator (GPL-3.0+, Blender 5.0+, v0.3.2, Feb 2026): twos and threes via stepped F-curves, phase offsets, noise jitter, 3D onion skin.
- Real boil comes from hands touching the puppet each pose, so held duplicate frames are identical. No published amplitude [U].

### A6. Sets and props
- Aardman uses felt puppets (Robin Robin), tiny-table sets, ~200 miniature chickens for wide shots. No source found on miniature-set materials [U].

### A7. Image-to-3D (only with an input image: a hand drawing or a Blender render)
- TRELLIS.2: MIT, ~4B, 24 GB+ VRAM, GLB with PBR; H100 ~3/17/60 s at 512/1024/1536.
- Hunyuan3D 2.1: license excludes EU, UK, South Korea; >1M MAU needs a license; outputs can't improve other models; ~10 GB shape, 21 GB texture, 29 GB both.
- Pixal3D: TencentARC, MIT, built on TRELLIS.2, single image to GLB; meshes face the opposite way from TRELLIS.2.
- Verdict [U, untested]: procedural wins for final characters (part separation for rigging, deterministic seeds, registered mouth sets, no baked lighting). Image-to-3D for blockouts and odd props only.

## PART B: Motion quality from 3D scene data

### B1. Foot, ground, interpenetration
- MDM/OmniControl skating ratio: fraction of frames where a foot under 5 cm high slides more than 2.5 cm.
- Kimodo (NVIDIA): toe under 0.05 m = contact; skate = toe speed above 0.2 m/s.
- PhysDiff: Penetrate and Float (mm, 5 mm tolerance), Skate, Phys-Err as their sum.
- UnderPressure / Kovar footskate cleanup: mean horizontal foot velocity during contact; IK planting.
- Our advantage: the agent authors the plants, so contact labels are ground truth.
- Blender's Sept 2025 GN workshop: SDFs less precise than BVH trees for collision; use BVH for interpenetration.

### B2-B3. Arcs, spacing, holds
- SPARC (spectral arc length of the speed profile) preferred over jerk metrics (LDLJ noise-sensitive); score per move segment; compare only across similar tasks.
- Cartoon Animation Filter (Wang et al. 2006): anticipation and follow-through from an inverted, smoothed, time-shifted second derivative; reverse it to detect them.
- Even spacing = equal steps; eased = growing then shrinking. Twos = one pose per two frames. Mixing ones and twos is legitimate for fast action.
- HumanScore aggregation worth copying: D = 0.5r + 0.3s + 0.2p (r flagged fraction, s mean severity, p longest run).

### B4. Readability and twinning
- Twinning = mirrored limbs or weight; fix with a few frames of offset and deliberate asymmetry. Symmetry fine for intended slams.
- No published silhouette-clarity metric; mask-based measures below are the researcher's design [U].

### B5. Research and fit
- 3D human animation quality (arXiv 2505.23301): linear regressor ~90% correlation with human realism ratings.
- PP-Motion (2508.08179): learned metric combining physical and perceptual fidelity.
- MotionCritic (ICLR 2025): FID-style metrics align poorly with perception; code public.
- HumanScore (2604.20157): extra limbs, bone length (tau 0.15), joint range (15 deg), self-collision (0.01 mild, 0.03 severe), kinematic extremes, smoothness.
- AnimationBench (2604.15299): VLM (Qwen3-VL-Max) scores principles at 84.4% on diagnostic cases; anticipation and follow-through by VLM yes/no; slow-in/out from tracked speed curve; drops timing and staging as too style-dependent.
- MMU principle-based evaluation of generative animation (5 samples): squash/stretch, anticipation, exaggeration absent.
- Fit: learned and FID-style metrics are trained on realistic human mocap; puppets with stepped timing are out of distribution [U]. Advisory only, never a gate.

### B6. Combining with a VLM
- NextMotionQA (2606.04773): VLM-expert agreement kappa 0.70 on coarse criteria, 0.10 on part-level criteria.
- Design: metrics measure spacing, skate, pops; the VLM judges coarse things (pose read, staging, appeal, acting intent) through structured yes/no questions.
- Feed contact sheets with metric flags overlaid, trajectory arcs and onion skins drawn, flagged poses marked. Route metric/VLM disagreements to a human or a higher-res re-render.

## (a) Build a character in code: recipe
1. Parametric character spec: bone chain, per-part size, seed per part.
2. Lumps as capsules and ellipsoids along bones; per-part scale +/-3-8%, rotation +/-2-4 deg; never mirror left and right [U].
3. Smooth-union at joints with small k (the sculptor's pinch); leave a seam crease where parts meet by skipping the blend on one joint edge [U].
4. SDF Mean/Median smoothing, Offset for bulk, Fillet; low-amplitude field noise at two scales (part-size lumps, thumb-scale softness).
5. Grid to Mesh, then remesh.
6. Stamp thumbprints and tool marks as real SDF or displacement dents, 1-3 per touched part, at pinch points, neck, waist, head sides and top, shoulders, backs of limbs; faces cleaner [U].
7. ambientCG Fingerprints (CC0) for roughness smudge only; finer bump/displacement noise.
8. A3 starting shader; per-part hue variation (dH ~+/-1-2%, dV ~+/-3%) [U].
9. Nine mouth shapes from one parametric lip model with a shared socket; freeze each with its own seed; add brow and eyelid sets.
10. Rig, then stepped twos with phase offsets.
11. Key boil seeds by (part, pose index); re-seed only parts that changed pose; amplitude ~0.2-0.5% of part size [U]; held frames identical.
12. Render at miniature scale (puppet 0.15-0.3 m), real-sensor camera, small hard lights; oversized set textures; wonky modifier on straight set edges; visible tape or pins on backdrops [U].

## (b) Motion QC suite
Setup: per frame, `obj.evaluated_get(depsgraph)`, `pose.bones[n].matrix` times `matrix_world`, `mathutils.bvhtree` [U on API specifics]. Scale thresholds by character height H. All thresholds [U] starting points.

| Metric | Compute | Starting threshold | Catches |
|---|---|---|---|
| Foot skate | Horizontal drift of foot anchor in each authored plant | Fail above 0.5% of H per plant | Sliding feet |
| Ground penetration/float | Lowest vertex z minus ground during plants | 5 mm at human scale, scaled to puppet | Sinking, hovering |
| Part interpenetration | BVH overlap between non-adjacent parts | Fail above 1% of a part's triangles | Limbs through body |
| Spacing evenness | Coefficient of variation of step lengths on moves of 5+ poses | CV below 0.1 = robotic | Linear moves |
| Ease profile | First and last step vs middle; rise-then-fall | Warn if no slow-in or slow-out | Missing eases |
| Arc quality | Sagitta / chord for head, hands, feet | Warn below 2% on moves over 0.5 H | Straight-line paths |
| Smoothness | SPARC per move | Flag worst decile vs character median | Jerky moves |
| Pops | Second difference above 4x windowed median | 4x | Pose snaps |
| Anticipation | Opposite-direction displacement 2-6 poses before a big move | Warn under 5% of amplitude for moves over 0.3 H | Missing windup |
| Overshoot and settle | Peak beyond target / amplitude, settle within N poses | Warn if none above 3% on big stops | Dead stops |
| Cadence | Distinct-pose detection, hold-length histogram | Mode 2; flag unplanned 1 or 3 runs | Inconsistent cadence |
| Pose change per step | Max joint rotation delta between poses | Warn above ~30 deg unless tagged fast | Strobing |
| Silhouette clarity | Flat mask render: hand/foot overlap with torso mask, negative-space holes | Warn if a hand overlaps torso above 60% on a key pose | Unreadable poses |
| Line of action | Spine-head curve projected to camera; curvature | Warn if near-straight on key poses | Stiff posing |
| Twinning | Mirror-compare L/R limb angles; speed cross-correlation lag | RMS below 5 deg and lag 0 for 3+ poses, unless tagged | Mirrored limbs |
| Boil | Per-part vertex RMS between distinct poses; silhouette crawl | Crawl under ~1 px at 1080p; zero change on held frames | Shimmer, held-frame flicker |

Aggregate per metric with D = 0.5r + 0.3s + 0.2p. Hard fails: skate, penetration, interpenetration, held-frame flicker. Everything else is a scored warning for the VLM critic and a human.

## Sources
https://developer.blender.org/docs/release_notes/5.0/geometry_nodes/
https://developer.blender.org/docs/release_notes/5.0/cycles/
https://developer.blender.org/docs/release_notes/5.3/geometry_nodes/
https://code.blender.org/2025/10/geometry-nodes-workshop-september-2025/
https://80.lv/articles/nodevember-2025-simulating-a-claymation-fire-in-blender
https://80.lv/articles/clay-d-oh-a-clay-shader-for-blender
https://superhivemarket.com/products/kin-klei/docs
https://superhivemarket.com/products/iconprints-procedural-fingerprint-imperfections/docs
https://www.blendernation.com/2025/03/06/make-things-look-wonky-in-blender/
https://extensions.blender.org/add-ons/stop-motion-style-animator/
https://github.com/fogleman/sdf
https://github.com/microsoft/TRELLIS.2
https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
https://github.com/TencentARC/Pixal3D
https://github.com/DanielSWolf/rhubarb-lip-sync
https://ambientcg.com/view?id=ClaySubstance002
https://ambientcg.com/view?id=Clay005
https://ambientcg.com/view?id=Fingerprints001
https://polyhaven.com/our-api
https://researchportal.bath.ac.uk/en/publications/plasticine-shading/
https://digital-entertainment.org/2022/11/24/investigating-how-computational-tools-can-improve-the-production-process-of-stop-motion-animation/
https://www.netflix.com/tudum/features/wallace-and-gromit-vengeance-most-fowl
https://www.awn.com/animationworld/aardman-50-inside-clay-felt-and-fingerprints
https://www.shortlist.com/entertainment/aardmans-sir-peter-lord-on-his-journey-from-a-kitchen-table-to-hollywood-rocket-packs-and-how-the-studio-favours-thumbiness-over-ai
https://animateclay.com/how-aardman-makes-puppets
https://www.fxguide.com/?p=186839
https://www.guinnessworldrecords.com/world-records/693110-most-3d-printed-faces-made-for-a-stop-motion-film
https://arxiv.org/pdf/2310.08580
https://research.nvidia.com/labs/sil/projects/kimodo/docs/benchmark/metrics.html
https://arxiv.org/pdf/2212.02500
https://research.cs.wisc.edu/graphics/Gallery/kovar.vol/Cleanup
https://www.microsoft.com/en-us/research/?p=157386
https://www.animatorisland.com/defining-the-art-twinning/
https://arxiv.org/abs/2505.23301
https://arxiv.org/abs/2508.08179
https://arxiv.org/abs/2407.02272
https://arxiv.org/pdf/2604.20157
https://arxiv.org/pdf/2604.15299
https://arxiv.org/abs/2606.04773
