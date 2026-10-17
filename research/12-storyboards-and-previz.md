# Storyboards, sketching and previz for a code-driven clay studio (research, Oct 17, 2026)

~40 searches and fetches. Blender 5.x manual/API pages returned navigation only; Blender details come from the 2.93 manual, 5.0 release notes and a 5.x API-drift article. [U] = unverified.

## 1. The real story process
- Beat boards are pitch-stage images: many fast thumbnails, emotional clarity over polish, most get replaced. Pixar loop: board, pitch, feedback, re-board, re-pitch until it works; editorial adds dialogue, music, timing.
- Selick boarded all of Coraline, cut timed story reels with temp voices and music, swapped in real voices after casting. Boards and reels decided how many sets and puppets to build, and were revised continuously.
- Park and Crossingham call boarding "editing done upfront."
- Laika's feasibility pass: Butler says a stop-motion film is made twice; the whole film is boarded, then department heads work out how to achieve each shot. Casting follows script lock. VFX supervisor Steve Emerson: previs informs puppets, sets, camera, VFX: set size, where extensions start, how far a puppet travels. After sequences lock, heads break the film down shot by shot against animatics. Production designer Nelson Lowry tiered hard boards by complexity (physical vs digital) and wants lens, set depth and extension needs known before building.
- Aardman: directors, art department and camera team set up each shot (move, dressing, animator access, lighting) before briefing the animator; Becher filmed rough camera moves on an iPad; VR previs on Early Man.
- Panel conventions: fix the aspect ratio first (project parameter). Arrows for camera and character moves; multiple panels for big moves. Keep relative sizes and positions consistent; keep screen direction across cuts; camera stays on one side of the action axis unless a neutral shot bridges. Cut only when the new shot adds information; move only when motivated. Vary framing between consecutive shots of the same subject (avoid jump cuts). OTS for two-person dialogue; avoid extreme angles. Readable silhouettes, light direction, clear action and camera notes. Stable IDs like `seq010_sh0030`.
- How boards fail: unclear staging, motion hiding weak staging, jump cuts, axis crossings, weak silhouettes, unbuildable moves, continuity errors that propagate into layout.

## 2. Character sketching and design
- Silhouette first: Laika's Kubo design lead calls silhouette the most important part of character design; Boxtrolls' Snatcher chosen from black-silhouette drawings.
- Approval chain: paper design to digital sculpt or maquette, which the director approves before other departments start; ~9 months to an animation-ready puppet.
- Maquettes fix head size and expression range (Corpse Bride); proportions drive armature engineering (Snatcher's belly needed a gear mechanism).
- Faces: replacement faces numbered and labeled; Coraline split upper and lower halves for combinatorial expression.
- Design sheets: turnarounds, 5-7 expressions, pose sheets, size-comparison sheet with silhouettes, colour key. Silhouettes double as a drift check.
- Scale: Laika hero puppets ~17 in; 6-10 in (15-25 cm) suits simple wire armatures. Vary finger lengths (equal reads as rakes). Magnet feet are big. No sourced head-to-body ratios; treat any target as a house rule to test [U].

## 3. Doing it in code
### a. LLM-drawn SVG thumbnails
- Frontier models are decent at single-subject drawings (Willison's pelican benchmark shows steady gains through 2026). Max effort can backfire (one Sonnet 5.5 max run burned 128k thinking tokens and returned no SVG; xhigh worked). OpenRouter's sketch benchmark is weak evidence [U].
- Limits: weak on textures, 3D spatial relations, occlusion order, counts (SGP-CompBench); VectorGym shows gaps on sketch-to-SVG; naive multi-turn self-refinement doesn't help.
- Technique: fixed `<symbol>` library of mannequins and props with named poses; model outputs JSON (floor positions, pose names, camera) and code draws it; primitives only; validate XML; rasterize; 2-3 look-and-fix rounds max; arrows drawn from data. Use SVG for thumbnails and beat boards only, never for staging or depth.

### b. Blender grey-box previz (5.x)
- 5.0 renamed EEVEE to `BLENDER_EEVEE`; `scene.node_tree` gone (`scene.compositing_node_group`); enums upper-case; 5.1 on Python 3.13. Grease Pencil is v3; annotations in `bpy.data.annotations`. LLMs emit 4.x-era calls: declare the version, introspect the running Blender, fail loudly on unknown enums.
- Workbench: Studio/MatCap/Flat lighting, outline, cavity, shadow, X-ray, camera DOF; fast enough for hundreds of panels.
- Line Art modifier: scene/collection/object source; contour, material borders, edge marks, intersections, crease; occlusion levels; chaining; bake. `GreasePencilLineartModifier` still in the 5.0 API; exact 5.x option names [U].
- Freestyle: high memory, no Z in output, misses face-intersection edges; SVG exporter add-on 5.x status [U].
- Proxy puppets from primitives at true scale; real `lens`, `sensor_width`, `sensor_fit`; floor grid with a ruler.
- Blender Studio's Charge previs: mannequins and simple geometry, each frame one storyboard drawing, shots 10-20 frames, exported into the edit for timing; previs did much of layout's groundwork.
- Export per shot: PNG plus JSON sidecar (shot ID, lens, sensor, camera matrix, subject positions in cm, light direction, frame range, dialogue, audio cue).
- Agent evidence: SimWorlds (a correct render doesn't prove a correct build; deterministic geometry verifiers plus reviewers); VIGA (write, run, render, compare, revise); SceneCraft (scene graph, vision critic, reusable function library).

### c. Grease Pencil via Python
- GPv3 model: layers, frames, drawing, strokes, points. 4.2-style `frame.strokes.new()` no longer applies. Reported 5.x pattern `drawing.add_strokes(sizes)` [U]; introspect and smoke-test first.
- Use for annotation overlays (camera arrows, floor marks, safe frames) and baked Line Art ink; don't freehand characters.

### d. Layout and animatic assembly
- Contact sheets and boards: Python plus HTML, print to PDF via headless Chromium or WeasyPrint [U].
- Animatic: ffmpeg concat with per-panel durations plus scratch audio [U on exact commands].
- OpenTimelineIO for cut order and durations (FCP XML, AAF, EDL adapters; Blender Studio used OTIO for Sprite Fright; FCP XML worked, AAF relink problems).
- Scratch audio recorded or TTS; durations via ffprobe.

### e. AI storyboarding and film-planning agents
| System | How it plans and checks | Relevance |
|---|---|---|
| FilmAgent | Director, screenwriter, actors, two cinematographers; Critique-Correct-Verify (3 rounds) and debate; 9 shot types; group 3.98 vs solo 3.04 | No 180-degree or axis logic |
| Mind-of-Director | Unity 3D previz, camera templates, two cinematographer agents plus a director; engine checks collisions and occlusion; ~25 min per idea | Closest to our approach |
| CamPilot (Sep 2026) | Per-shot camera brief trained on ~14.6k films | Modest gains |
| Script Is All You Need | JSON shot scripts, 10 s shot cap, last-frame conditioning | No axis handling |
| Anim-Director, StoryAgent, MovieAgent, DreamRunner, AnimeAgent, CANVAS | Consistency via reference images, character banks, LoRAs, persistent memory, embedding checks | Depend on generative models; method transfers, tools don't |
Takeaway: structured plans plus engine-checked constraints transfer; nobody ships a real axis check, so we write our own.

## 4. Previs to production
- Dragonframe 5+ imports FBX camera moves into its Arc motion-control workspace; Blender FBX to Dragonframe plausible but untested [U].
- Blender Studio's previs camera importer baked camera actions with constraints to props or characters.
- Make `shot.json` canonical: camera keyframes at 24 fps, lens, sensor, focus distance, f-stop, puppet marks in cm, light direction, duration, panel image, dialogue, audio cue.
- `build_shot(shot.json)` generates each shot's .blend with camera and proxy actors; layout refines that file; panel pose = first key pose.
- Layout outputs: floor-plan PDF with marks, lens and height sheet, X-sheet CSV with dialogue frame counts.

## 5. Reviewing boards
Directors check staging clarity, whether each shot adds information, motivated cuts and moves, screen direction and eyelines, pacing against dialogue, feasibility.
Automatic checks (thresholds proposed [U]):
1. Axis: define the axis from the two principal actors' floor positions at each establishing shot; flag camera side changes (cross-product sign) and flipped screen order or eyelines; reset on a declared new establishing shot. Warning, not failure (viewers caught only ~42% of violations in one study; deliberate breaks are legitimate).
2. Silhouette readability: per-actor flat masks; screen height fraction, overlap and occlusion, contrast against background, solidity.
3. Shot-size variety: classify by subject height fraction; flag runs of the same size and same-subject cuts with too little change.
4. Pacing: shot duration vs dialogue length plus reaction beat; flag cut-off lines and long holds with no new information; total runtime vs target.
5. Buildability: camera inside set bounds and lens kit, no collisions, puppet scale, floor contact.
6. Vision critic as a second opinion only ("where does the eye go?"). Deterministic checks first.

## 6. Recommended pipeline
| Stage | Format | Tools | Automatic checks | Sign-off |
|---|---|---|---|---|
| 0 Script and bible | Script, `characters.yaml`, scale and camera spec | Claude | Names, props, sets resolve | Director |
| 1 Thumbnails | SVG from symbol library + JSON | Claude, resvg/cairosvg | Valid SVG, beats covered, 2-3 refine rounds max | Director picks |
| 2 Beat board | 8-15 images, HTML contact sheet | Claude, Python | Arc and beat coverage | Director (pitch) |
| 3 Boards | PNG at project aspect + JSON; Line Art ink, GP arrows | Blender headless (Workbench) | Axis, silhouette, shot size, buildability | Director, plus DP/fabrication for feasibility |
| 4 Animatic | MP4 + OTIO, scratch audio | ffmpeg, OTIO, ffprobe | Pacing vs dialogue, runtime | Director locks sequence |
| 5 Layout | Per-shot .blend from `shot.json`, floor plan, X-sheet CSV | Blender | Buildability, lens, reach | Director, DP, lead animator |
Revision loop capped at a few rounds per sequence; everything versioned with stable shot IDs. Claude proposes; humans hold the gates.

## Sources
https://www.cartoonbrew.com/how-to/how-they-did-it-missing-link-production-designer-nelson-lowry-on-the-complexities-of-hybrid-production-184010.html
https://www.artofvfx.com/?p=16167
https://www.boxofficepro.com/in-search-of-laikas-missing-link-a-talk-with-writer-director-chris-butler/
https://www.focusfeatures.com/article/henry_selick_in_conversation
https://awn.com/animationworld/team-effort-bringing-aardmans-early-man-big-screen
https://behindthelensonline.net/site/interviews/interview-exclusives/nick-park-merlin-crossingham-talk-about-the-magic-of-making-wallace-gromit-vengeance-most-fowl-exclusive-interview/
https://www.cartoonbrew.com/feature-film/laika-crazy-enough-animate-16-foot-tall-skeleton-kubo-two-strings-142544.html
https://animationmagazine.net/2016/07/puppet-masters
https://awn.com/animationworld/scene-stealing-star-boxtrolls
https://www.awn.com/animationworld/advanced-art-stop-motion-animation-building-puppets-part-1
https://cmerritthoughton.substack.com/p/a-guide-to-character-design-sheets
https://gnomon.thegnomonworkshop.com/workshops/creating-beatboards-for-pre-production
https://studiobinder.com/blog/storyboard-rules
https://pure.hud.ac.uk/ws/files/16045791/Kachkovski_17_180Rule_OA.pdf
https://morphic.com/docs/3d-scene/continuity-checks
https://studio.blender.org/blog/charge-previsualization/
https://projects.blender.org/Andy_Goralczyk/previs_cam_importer
https://studio.blender.org/blog/opentimelineio-in-blender
https://github.com/AcademySoftwareFoundation/OpenTimelineIO
https://www.dragonframe.com/ufaqs/how-do-i-export-a-move-from-maya-and-import-it-into-dragonframe/
https://developer.blender.org/docs/release_notes/5.0/eevee/
https://developer.blender.org/docs/release_notes/5.0/grease_pencil/
https://developer.blender.org/docs/release_notes/4.3/grease_pencil_migration/
https://docs.blender.org/manual/en/2.93/grease_pencil/modifiers/generate/line_art.html
https://docs.blender.org/manual/en/2.93/render/workbench/options.html
https://simonwillison.net/tags/pelican-riding-a-bicycle/
https://arxiv.org/html/2509.05208v1
https://arxiv.org/html/2501.12909v1
https://arxiv.org/html/2408.09787v1
https://arxiv.org/html/2602.20664v1
https://arxiv.org/html/2403.01248v1
https://arxiv.org/html/2601.11109v2
