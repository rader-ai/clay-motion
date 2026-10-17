# Story, boards, animatic and edit

Owners: the **Head of Story** (story through boards), the **Editor** (animatic and cut), the **DP** (layout). Sources: research/12 (boards and previz), research/06 (pipeline), research/14 (voice first).

## 1. Story development

Stop motion is "made twice" (Chris Butler, Laika): the whole film is boarded and timed before anything is built, because a shot can't be fixed after it's shot. Boards are "editing done upfront" (Park and Crossingham). Drafts are cheap here, so we use them.

| Step | Output | Who | Check |
|---|---|---|---|
| Brief | `brief.md` (purpose, audience, length, aspect, budget, must-haves, never-dos) | EP | n/a |
| Loglines | 3 to 5 options, one sentence each | Writer | Head of Story picks with the Director |
| Beat sheet | Want, obstacle, turn per scene; runtime estimate | Writer | Each scene has one story point |
| Treatment | One page | Writer | Feasibility pre-check (Producer, Supervising Animator, DP) |
| Script drafts | `script.md` v1, v2, v3 | Writer | Head of Story notes per draft |
| Table read | Scratch voices for every line (SOUND.md), assembled to an audio-only read | Sound Supervisor, Animatic Editor | Director and Head of Story listen: clarity, pace, laughs |
| Script Lock | Locked script | Head of Story (owner), Director (approves), EP (signs) | Feasibility check passed |

Story rules for clay: one clear action per shot; fewer, stronger poses; avoid long walks; physical comedy, small worlds, props and reactions over talk; jokes that don't depend on perfect lip sync; keep shots inside the length the pipeline can hold. Adam Elliot's standard applies: audiences forgive rough animation, never a weak story.

Story QA beyond the table read: at the animatic stage, Chris and a few other viewers watch it cold and answer three questions: what happened, what did the character want, where did you laugh or feel something. Their answers are logged with the cut.

## 2. Thumbnails and beat board

- **Thumbnails:** Claude writes a JSON description (floor positions, named poses, camera) and code draws an SVG from a fixed library of mannequin and prop symbols. Many options per moment, judged on staging and silhouette only. At most 2 to 3 look-and-fix rounds; models are weak at depth and occlusion in SVG, so SVG is never used to judge staging in depth.
- **Beat board:** 8 to 15 images covering the whole story, laid out as an HTML contact sheet. The Head of Story pitches it to the Director, who gives notes; re-board and re-pitch, capped at a few rounds per sequence.

## 3. Boards from Blender

Boards are rendered from the 3D greybox, not drawn:
- Proxy puppets built from primitives at true scale, on the real set greybox, with real lenses and sensor sizes, a floor grid and ruler.
- Rendered in Workbench with outlines, inked with the Line Art modifier for a pencil look, with arrows for camera and character moves drawn from data (Grease Pencil v3 overlays).
- Each panel saves a PNG plus a JSON sidecar: shot ID, lens, sensor, camera matrix, subject positions in centimetres, light direction, frame range, dialogue, audio cue.
- The board's camera becomes the shot's starting camera, so nothing is redrawn later.
- Shot IDs: `SQ010_SH020`, numbered in tens so inserts fit.
- Blender 5.x warning: language models often emit 4.x-era calls (Grease Pencil v3, `scene.compositing_node_group`, EEVEE's engine ID). Declare the version, introspect the running Blender, and fail loudly on unknown names.

Panel conventions: fix the aspect ratio first; arrows for moves; keep relative sizes and screen positions consistent across cuts; stay on one side of the action line unless a neutral shot bridges it; cut only when the new shot adds information; move the camera only when motivated; vary framing between shots of the same subject.

## 4. Board checks

Deterministic checks run first; the vision critic is a second opinion only (research/12, section 5; thresholds [U]):
1. **Action line:** from the two main characters' floor positions at each establishing shot; flag camera side changes and flipped screen order or eyelines. A warning, not a failure: deliberate breaks are legitimate.
2. **Silhouette readability:** per-character flat masks; screen height, overlap, contrast against background, open negative space.
3. **Shot-size variety:** flag runs of the same size and same-subject cuts with too little change (jump cuts).
4. **Pacing:** shot duration against dialogue length plus a reaction beat; flag cut-off lines and long holds with nothing new; total runtime against the brief.
5. **Buildability:** camera inside the set and lens kit, no collisions, puppet scale, floor contact.
6. **Vision critic:** "where does the eye go?" and "what is this shot about?" answered from the panel.

## 5. Animatic

- Panels timed to scratch voice (SOUND.md), assembled with ffmpeg; the cut held as an OpenTimelineIO timeline.
- `timing.csv` records frames per shot; at Animatic Lock those become the shot durations in `shot.json`.
- **Animatic Lock:** the Editor owns it (the Animatic Editor builds it), the Director approves, the EP signs.

## 6. Layout

`build_shot(shot.json)` generates each shot's Blender file with the camera, set and proxy actors from the board. The DP refines camera and light; the first key pose of the pop-through starts from the board pose. Layout outputs: the shot file, a floor plan with marks, a lens and height sheet, and the X-sheet with dialogue frame counts.

## 7. Edit drafts

The Editor drops each shot into the cut as it lands, so the edit always mixes boards, pop-throughs and finals (Pinocchio's editor recut every shot on arrival).
| Draft | What it is | Who approves |
|---|---|---|
| Assembly | Every approved shot in order, nothing trimmed | Editor |
| Rough cut | Pacing pass, first trims | Director notes |
| Fine cut | Frame-level trims, sound ideas in | Director notes |
| Picture Lock | Final cut | Editor (owner), Director (approves), EP (signs) |
Dailies review uses 3 to 5 shot mini-cuts so the Director never judges a shot outside its neighbors.
