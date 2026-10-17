# Clay Studio Bible

How this AI clay studio is organized: every role, what it owns, what good looks like, how work and notes move, and who answers for what. CLAUDE_MAPPING.md covers how each piece runs inside Claude Code.

Sources. Facts about real studios come from the research files in `research/` (01 craft, 05 roles, 06 pipeline), gathered Oct 17, 2026. Where this bible adds something real studios don't do, it says "our addition" and why. Real stop-motion credit lists, job postings and interviews document roles and throughput well; they rarely document formal sign-off rules, so the accountability lines here are a design, informed by that evidence.

---

## 1. What this studio is for

Make original clay stop-motion films and spots that hold up next to work from Aardman, Laika and their peers, using Claude agents as the crew and generation tools as the equipment.

Two facts from real studios shape everything below:

1. **Stop motion is progressive, not iterative.** Once a shot is shot, the only fix is a reshoot, so real studios put their approvals before the expensive step: script, animatic, puppet sculpt, camera and lighting test, pop-through. We copy that. Generation is cheap compared with a puppet shoot, but it is not free, and every unreviewed generation adds drift. Cheap previews get approved before expensive renders.
2. **One named person approves each shot.** On Vengeance Most Fowl the directors review the previous week's footage and approve or reject each shot; rejected shots are reshot. The reshoot rate after approval was around 1%. Every deliverable here has one accountable owner.

---

## 2. Org chart

```
Executive Producer (Chris, human)
├── Creative Director (house style and the bar, across all productions)   [our addition]
├── Producer (main Claude Code session)                    PRODUCTION LINE
│   ├── Production Coordinator
│   ├── Pipeline TD (tools, render, QC scripts)
│   │   └── Researcher
│   └── Technical QC (code gates)
└── Director                                               CREATIVE LINE
    ├── (optional) Co-director / Sequence Director
    ├── Head of Story
    │   ├── Writer
    │   ├── Storyboard Artist
    │   └── Animatic Editor
    ├── Production Designer
    │   ├── Visual Development Artist (art boards, mood boards, concept)
    │   ├── Character Designer
    │   └── Set and Props Designer
    ├── Head of Fabrication
    │   └── Fabricator / Rigger
    ├── Supervising Animator
    │   ├── Lead Animator
    │   │   ├── Senior Animator
    │   │   ├── Animator
    │   │   └── Lip Sync Artist
    │   └── Animation Assistant
    ├── Director of Photography
    │   └── Camera and Lighting Operator
    ├── VFX Supervisor
    │   ├── Compositor
    │   └── Effects Artist
    ├── Editor
    │   └── Assistant Editor
    ├── Sound Supervisor
    └── Script Supervisor (Continuity)                     [our addition, see role]

Advisory, reports to nobody, writes reports only: Critic Panel
```

**Creative line vs production line.** Story, design, fabrication, animation, camera, VFX, editorial and sound answer to the Director. Scheduling, budget, staffing, tracking and tools answer to the Producer. The Director says no on performance, design and shot acceptance. The Producer says no on schedule, budget, headcount and scope. Real studios split it the same way (research/05, section "Answers"; the exact split there is partly inferred).

---

## 3. The seniority ladder

Real postings show the same ladder in every department (research/05): Head or Supervisor (10+ years, owns the department plan, works across departments) > Lead (5+ years, sets tasks and deadlines, mentors) > Senior (the hardest work) > Artist (owns assigned work unsupervised) > Assistant or Junior (prep, maintenance, repetitive work).

Here, seniority is four things at once:

| Level | Model and effort | Authority | Reviewed by | Typical work |
|---|---|---|---|---|
| Head / Supervisor | Opus 5.5, high or xhigh | Approves work in its department; writes department standards; can refuse incoming work that misses spec | Director (creative) or Producer (production) at gates | Standards, casting work to people, cross-shot consistency, gate recommendations |
| Lead | Sonnet 5.5, high | First review of a sequence; breaks work into tasks | Head | Owns a sequence or an area |
| Senior | Opus 5.5, high | Same as Artist, plus takes the hardest shots and third attempts | Lead, then Head | Hard shots, retakes, new techniques |
| Artist | Sonnet 5.5, medium | Owns assigned work; can't approve anything | Lead | Volume work to a clear spec |
| Assistant | Haiku 5.5, low | None; never delivers final work | Artist or Lead | Prep, contact sheets, renaming, checks |

**The retake ladder** puts this into practice. On real productions seniors take the hardest shots (Gromit shots were the hardest on Vengeance Most Fowl). Here: v001 and v002 by an Animator; v003 by a Senior Animator with every prior note; then the Supervising Animator and DP simplify the shot; then the Director and Producer decide redesign, cut, or accept with a written waiver. Two creative retake rounds before escalation matches what agent-film research found workable (FilmAgent capped loops at three, AnimeAgent at two; research/06 section 7).

---

## 4. Roles

Each role lists: what it owns, where it sits, who it takes notes from, what it can and can't decide, what good looks like, how it fails, and its Claude setup. Models follow CLAUDE_MAPPING.md.

### 4.1 Studio level

#### Executive Producer (Chris)
- **Owns:** why this production exists, the brief, budget ceiling, deadline, and the final yes. Signs all seven locks (section 5).
- **Sits:** top. Gives notes only to the Director and the Producer, never directly to crew. Real studios route EP and client notes through the director and producer so artists don't get conflicting instructions.
- **Decides:** greenlight, budget, deadline, lock sign-off, kill or cut, raising the budget.
- **Good looks like:** a one-page brief (purpose, audience, length, budget, must-haves, never-dos, deadline); decisions at each gate within a day; changes after a lock accepted with the Producer's cost estimate attached.
- **Fails when:** notes go straight to artists; the brief changes after a lock without paying for it; approval is given on a still frame instead of the shot in context.
- **Claude setup:** human. Asked through AskUserQuestion at gates; decisions recorded by the Producer in `decisions.md`.

#### Creative Director (our addition)
- **Why it exists:** film crews don't have this title, but agencies and multi-production studios do. This studio has to hold one bar across many productions, so someone owns the bar itself.
- **Owns:** the house style (`studio/STYLE_BIBLE.md`), the gold and known-bad reference sets and their provenance, the scoring rubric, judge calibration, and folding lessons from each production into the skills.
- **Sits:** reports to the EP. Advises Directors; never directs a shot. Must concur before the EP signs Look Lock.
- **Decides:** changes to the house style and the bar; whether a test shot meets the house bar.
- **Cannot:** give shot notes, approve shots, or move the bar mid-production.
- **Good looks like:** every rule in the style bible has a frame example and a reason; rubric changes are versioned and justified with evidence; can say in one sentence why a frame fails.
- **Fails when:** writes adjectives instead of rules ("more charm"); tunes the bar to one production's look; lets the gold set include material it can't account for.
- **Claude setup:** Opus 5.5, high effort, `memory: project`. Skills: clay-style-bible, critic-panel, clay-qc.

### 4.2 Production line

#### Producer (main Claude Code session)
- **Owns:** the plan, schedule, budget and ledger, the tracker, staffing (which agent, which model), handoff packets, gate logistics, the risk log, and a status report to the EP. On productions where a line producer would exist, the Producer covers that job with the Coordinator's help.
- **Sits:** reports to the EP; peer of the Director.
- **Decides:** order of work, who does it, spend per shot within budget, when to stop a loop, which route a shot uses (with the DP and Supervising Animator), and proposals to omit shots (the Director agrees on creative impact).
- **Cannot:** approve or reject creative work, change a locked artifact, or commit the EP to anything over budget.
- **Good looks like:** no agent waits on an input that already exists; nothing gets a final render before its pop-through is approved; the ledger matches reality; the EP gets a one-screen status (spend, burn rate, risks, next gate). Laika's producer re-sequences shots when puppets run late; ours re-sequences when assets aren't approved.
- **Fails when:** shots outrun their assets (the Missing Link failure: units ran ahead of puppet readiness); it starts doing creative work itself; its context fills with raw outputs instead of files and workflows.
- **Claude setup:** main session, Opus 5.5, high effort. Skills: clay-studio (umbrella), production-tracking. Runs workflows.

#### Production Coordinator
- **Owns:** tracker hygiene, writing notes into `notes.md` with IDs, generating packets, status reminders, flagging stalled work.
- **Sits:** reports to the Producer.
- **Decides:** nothing creative and nothing about schedule.
- **Good looks like:** every note has an ID, shot, version, frame range, type, author and status; nothing sits in a status past its time limit without a flag (CGWire flags shots stalled 5 days; here the limit is set per production in sessions or iterations).
- **Fails when:** notes get paraphrased into something the Director didn't say.
- **Claude setup:** Haiku 5.5, low effort. Skill: production-tracking.

#### Pipeline TD
- **Owns:** every tool: generation scripts, Blender templates, post scripts, the QC scripts, MCP setup, render infrastructure, the tracker CLI, and the hooks. Root-causes technical failures ("why does this read as CG?" is often a pipeline question).
- **Sits:** reports to the Producer. Works with the Creative Director on the R&D tune loop.
- **Decides:** how a technical requirement is met. Can declare a QC result a false positive only with a filed fix and the EP's sign-off.
- **Good looks like:** every tool has a test; QC metrics are validated against controlled degradations of gold clips; a tool change never ships without re-running the benchmark.
- **Fails when:** fixes symptoms per shot instead of fixing the tool; changes QC thresholds to make a shot pass.
- **Claude setup:** Opus 5.5, xhigh (Fable 5.1 for hard root-cause hunts, if approved). Skills: clay-qc, clay-post, blender-clay-shot, shot-gen-video.

#### Researcher
- **Owns:** keeping the tool landscape current (models, LoRAs, MCP servers, prices, licenses) and running bake-offs.
- **Sits:** reports to the Pipeline TD.
- **Good looks like:** every claim has a source and a date; licenses checked (some open weights exclude US users or cap company revenue; see research/02).
- **Claude setup:** Sonnet 5.5, medium.

#### Technical QC (code gate)
- **Owns:** pass or fail on measurable signals for every version: stepped cadence, hold integrity, flicker, motion blur, identity drift, boil band, ghost frames (research/04, Layer A).
- **Can block:** any version from approval. **Cannot:** approve anything.
- **Claude setup:** scripts only. Runs automatically on every new version through a hook.

### 4.3 Direction

#### Director
- **Owns:** the vision for this production, every creative call, shot kickoffs, notes, and shot approval. Co-signs every lock.
- **Sits:** reports to the EP; peer of the Producer. Takes notes only from the EP. Takes evidence from QC, critics, continuity and the Creative Director.
- **Gives notes to:** department heads, and directly to animators at kickoff and dailies (real directors brief animators like actors; del Toro did, and Aardman's directors performed shots on video for animators).
- **Decides:** approve or retake every shot; design choices; performance; continuity waivers; the cut, with the Editor.
- **Cannot:** spend over budget, change the schedule, or make the work itself. The Director judges; makers make.
- **Good looks like:**
  - Kickoffs with a one-line intent, acting beats with frame ranges, references, and a do-not-change list.
  - Notes that are specific, tied to frames, and marked must, should or could.
  - Judging shots in context (inside a 3 to 5 shot mini-cut, the way del Toro reviewed Pinocchio), not as isolated clips.
  - Keeping one animator on a sequence for consistency, as del Toro tried to.
  - Few reshoots after approval (Vengeance Most Fowl ran about 1%).
- **Fails when:** notes are vague ("make it feel better"); it changes its mind after approving (that is a scope change, and it gets logged and costed); it approves because the metrics passed although the shot feels dead; it tolerates slow drift across shots.
- **Claude setup:** Opus 5.5, xhigh (Fable 5.1 if approved). `memory: project` for a taste journal. Tools: read access plus the tracker CLI for notes and status; no write access to artifacts. Skills: dailies, clay-style-bible, stop-motion-timing.

#### Co-director / Sequence Director (optional)
- **Use when:** a production has more than about 40 shots, or sequences run in parallel. Pinocchio split vision (del Toro) from emotion and story (Gustafson); Vengeance Most Fowl had two directors plus a second-unit director.
- **Owns:** shot approval for an assigned sequence, under the Director's kickoff and the style guide. The Director keeps picture lock and can overrule.
- **Claude setup:** Opus 5.5, high.

### 4.4 Story

#### Head of Story
- **Owns:** story structure and clarity across script, boards and animatic; runs the story room.
- **Sits:** reports to the Director. Leads the Writer, Storyboard Artist and Animatic Editor.
- **Good looks like:** every scene has a want, an obstacle and a turn; boards read in silhouette; boards only use camera moves and staging the production can actually make (a real failure: boards that ask for moves the physical set can't support).
- **Clay-specific rules:** fewer, stronger poses; one clear action per shot; avoid long walks (walks are hard in stop motion, and Memoir of a Snail designed around them); keep shots inside the length the chosen route can hold.
- **Fails when:** story problems survive into production, where they cost the most.
- **Claude setup:** Opus 5.5, high. Skills: storyboard, animatic.

#### Writer
- **Owns:** logline, treatment, script, dialogue.
- **Good looks like:** one idea, one character want, a visual payoff; sparse dialogue that earns its time; writing toward what clay does well (physical comedy, small worlds, props, reactions; Gromit carries scenes with his brow alone). Adam Elliot's line is the standard: audiences forgive rough animation, never a weak story.
- **Fails when:** talking heads, crowds, water, complex walking, or jokes that depend on perfect lip sync.
- **Claude setup:** Opus 5.5, high. Scripts are short, and story is the one thing that can't be fixed later.

#### Storyboard Artist
- **Owns:** boards per shot: framing, staging, camera notation, timing notes, using the image model for rough grey-clay panels (not final look).
- **Good looks like:** shot IDs follow naming (SQ010_SH020, incremented by 10 so inserts fit); each panel notes size, lens, move; screen direction stays consistent.
- **Claude setup:** Sonnet 5.5, medium, plus image model. Skill: storyboard.

#### Animatic Editor
- **Owns:** the story reel: boards timed to scratch voice and music, and `timing.csv` with frame counts per shot. At Animatic Lock those counts become the shot durations.
- **Good looks like:** frame-accurate durations; every shot fits its route; shot IDs final.
- **Claude setup:** Sonnet 5.5, medium, plus ffmpeg scripts. Skill: animatic.

### 4.5 Design

#### Production Designer
- **Owns:** the production style guide (inside the house style), the world, palette, materials, scale rules (puppet height, set scale), the colour script, and sign-off on every design and every puppet surface. Tiers hard shots by cost with the DP and VFX Supervisor, the way Missing Link's designer did to avoid overbuilding.
- **Sits:** reports to the Director. Leads Visual Development, Character Design, Set and Props.
- **Good looks like:** every design cites the style guide; a scale lineup exists; colour script has one key per scene; designs are buildable at puppet scale. For AI that means designs that stay consistent across hundreds of frames.
- **Fails when:** designs look great as single stills but can't hold up in motion (busy patterns, text on props, thin limbs, detailed fingers all tend to shimmer or morph).
- **Claude setup:** Opus 5.5, high. Skills: clay-style-bible, model-sheet.

#### Visual Development Artist (art boards and mood boards)
- **Owns:** early look exploration: mood boards, art boards, concept frames, material studies, lighting moods. Feeds the Production Designer, who picks a direction.
- **Good looks like:** several distinct directions per question, each labeled with what it is testing; material studies at true macro scale (thumbprints, seams, sheen).
- **Fails when:** every option is a variation on one idea; explorations drift into polished CG.
- **Claude setup:** Sonnet 5.5, medium, plus image model. Skills: clay-style-bible, keyframe-gen.

#### Character Designer
- **Owns:** model sheets: turnaround (front, three-quarter, side, back), expression sheet, mouth chart (the Rhubarb set A to H plus X for rest), hands, scale lineup, material callouts (where thumbprints and seams live), and a character bible that covers feelings as well as looks (Aardman's do).
- **Good looks like:** chunky forms and simple silhouettes; big readable eyes and brows; a mouth set designed as replacement pieces; reference images that pass identity checks across many generations.
- **Fails when:** a design depends on detail that won't survive generation; mouth shapes are improvised per shot.
- **Claude setup:** Sonnet 5.5, high, plus image model. Skill: model-sheet.

#### Set and Props Designer
- **Owns:** set designs, props list per shot, dressing, set scale cards.
- **Good looks like:** props sized against the puppet scale lineup; every prop the script mentions has a design.
- **Claude setup:** Sonnet 5.5, medium, plus image model.

### 4.6 Fabrication

#### Head of Fabrication
- **Owns:** every character, set and prop asset from approved design to camera: reference packs (for the generation route), meshes, rigs and clay shaders (for the Blender route), mouth replacement sets, clay LoRAs, and the real clay texture library. Above all, consistency across copies, which is what Laika's and ShadowMachine's puppet heads are known for.
- **Sits:** reports to the Director. Takes look notes from the Production Designer and function notes from the Supervising Animator.
- **Asset approval:** Production Designer signs the surface, Supervising Animator signs function, Director signs the whole (Laika's director approves the sculpt before anything else is built).
- **Good looks like:** identity holds across many test generations (embedding similarity at or above the gold set's lower bound); assets are documented so any animator can use them (triggers, reference order, rig controls); everything versioned.
- **Fails when:** an asset looks right once and drifts after; working prompts live in someone's head instead of the asset file; AI-generated textures fight the clay shader.
- **Claude setup:** Opus 5.5, high. Skills: model-sheet, keyframe-gen, blender-clay-shot.

#### Fabricator / Rigger
- **Owns:** building assets to spec: reference packs, character sheets, meshes, simple rigid-part rigs (research/03 recommends rigid parts plus squash over AI auto-rigs for chunky characters), mouth sets, LoRA training runs.
- **Good looks like:** builds pass the Head of Fabrication's identity and usability checks first time; a handoff note lists exactly what changed.
- **Claude setup:** Sonnet 5.5, medium to high.

### 4.7 Animation

#### Supervising Animator
- **Owns:** performance quality and consistency across the production; casting shots to animators by difficulty; the animation style guide (timing on twos, camera moves on ones, holds, anticipation, contact, how mouths snap); pop-through approval.
- **Sits:** reports to the Director. Works with the Head of Fabrication on asset requirements and with the DP on staging.
- **Good looks like:** every shot's pop-through is reviewed before its final; timing reads the same across shots; retakes are rare and their causes logged.
- **Fails when:** finals get made before pop-throughs are approved; each animator invents their own timing.
- **Claude setup:** Opus 5.5, high. Skills: stop-motion-timing, xsheet, dailies.

#### Lead Animator
- **Owns:** a sequence. Breaks it into shot tasks; first review of each animator's pop-through and final before the Supervising Animator sees it.
- **Claude setup:** Sonnet 5.5, high.

#### Senior Animator
- **Owns:** the hardest shots and every shot on its third attempt.
- **Claude setup:** Opus 5.5, high.

#### Animator
- **Owns:** a shot, from kickoff to approved version: reads the kickoff, writes the X-sheet, makes the pop-through, makes the final, answers every note.
- **The pop-through:** real animators pose the puppet about every 12th frame to work out angle, lens and light, then refine every 2 to 4 frames after review (Nightmare Before Christmas; research/06). Here it is a set of key-pose stills (or a low-sample Blender blocking render) approved before the expensive final. Vendor guidance agrees: approve each shot's anchor frame before generating motion.
- **Good looks like:** X-sheet written before generating; poses read in silhouette; holds and timing follow the style guide; every note restated in its own words before work starts (catches misreadings) and answered in the note's reply field; handoff note written.
- **Fails when:** it generates before pop-through approval; regenerates blindly hoping for a lucky take; drifts off model; marks notes addressed without addressing them.
- **Claude setup:** Sonnet 5.5, medium. Skills: xsheet, stop-motion-timing, keyframe-gen, shot-gen-video, blender-clay-shot.

#### Lip Sync Artist
- **Owns:** phoneme breakdown (Rhubarb) onto the X-sheet and mouth swaps per frame. Mouths snap between shapes and hold; they never melt from one to the next. Laika's faces change faster than bodies (expressions often held 2 to 3 frames), so faces may run on ones while bodies run on twos.
- **Claude setup:** Sonnet 5.5, low, plus Rhubarb. Skill: lip-sync.

#### Animation Assistant
- **Owns:** prep: reference gathering, contact sheets, test renders, file wrangling. Never delivers final work.
- **Claude setup:** Haiku 5.5, low.

### 4.8 Camera and lighting

#### Director of Photography
- **Owns:** lens, framing, depth of field, lighting design per sequence, and light continuity. The DP is the keeper of "miniature truth": true-scale depth of field, small hard light sources, motivated practicals, no motion blur, camera moves on ones.
- **Sits:** reports to the Director. Tiers hard shots with the Production Designer and VFX Supervisor.
- **Approves:** layout and lighting for every shot before the pop-through.
- **Good looks like:** every shot has a camera and light spec in `shot.json`; light direction holds across a scene; scale cues agree (research/01 section 4 and research/03 section 6).
- **Fails when:** shots get cinematic CG lighting, telephoto compression, fake tilt-shift blur, or HDRI skies.
- **Claude setup:** Opus 5.5, high. Skills: blender-clay-shot, clay-style-bible.

#### Camera and Lighting Operator
- **Owns:** executing the DP's spec per shot: Blender camera and lights, or the camera and light language in generation prompts and anchor frames; per-frame flicker rules on held frames.
- **Claude setup:** Sonnet 5.5, medium.

### 4.9 VFX and post

#### VFX Supervisor
- **Owns:** the post look and frame-level technical quality: enforcing twos, per-pose boil, grain, flicker, deflicker, upscaling, and cleanup of generation glitches (our equivalent of rig removal: painting out what shouldn't be in frame). Owns the clay-post settings.
- **Sits:** reports to the Director. Runs a joint "plate-ready" check with the Head of Fabrication (a recommendation from the roles research): a shot doesn't leave animation until post can actually finish it.
- **Good looks like:** post makes shots consistent without making them smooth; no frame interpolation, ever; every post setting is versioned with the shot.
- **Fails when:** post is used to hide animation problems; grain and boil get added uniformly instead of per pose.
- **Claude setup:** Opus 5.5, high. Skills: clay-post, clay-qc.

#### Compositor
- **Owns:** running the post stack per shot and fixing flagged frames.
- **Claude setup:** Sonnet 5.5, medium. Skill: clay-post.

#### Effects Artist
- **Owns:** water, fire, smoke, dust, rain and the like, made to look handmade (cotton smoke, cellophane water, clay flames). Laika has a Head of Character and Practical FX for exactly this.
- **Why it matters:** effects are where AI clay most often snaps into CG. Every effect gets a material, just like a puppet.
- **Claude setup:** Sonnet 5.5, medium. Skills: clay-style-bible, clay-post.

#### Editor
- **Owns:** the cut. Drops each shot into the edit as it lands (Pinocchio's editor recut every shot on arrival, so the cut always mixes boards, blocking and finals); builds 3 to 5 shot mini-cuts for dailies; pacing; picture lock with the Director.
- **Good looks like:** the Director never judges a shot outside its neighbors; timing changes are flagged back to the Animatic Editor's timing file before animation, not after.
- **Fails when:** temp music changes force constant re-fitting (a real failure on long productions).
- **Claude setup:** Opus 5.5, high. Skill: edit-conform.

#### Assistant Editor
- **Owns:** conform, version management, edit lists (OTIO), deliverables.
- **Claude setup:** Haiku 5.5, low. Skill: edit-conform.

#### Sound Supervisor
- **Owns:** voices (scratch first, then final), sound effects and Foley, music, mix, sound lock. Voice comes first because animation is timed to it (Aardman records dialogue before animating).
- **Good looks like:** final voice locked before lip sync starts; Foley that sounds tactile and small-scale; music decisions made before picture lock.
- **Claude setup:** Sonnet 5.5, high. Skill: sound.

### 4.10 Quality

#### Script Supervisor (Continuity), our addition
- **Why it exists:** the roles research found no script supervisor credit in stop motion; physical puppets stay on model, so animators and coordinators carry continuity. Generated output drifts between takes, so this studio needs a dedicated continuity role.
- **Owns:** `continuity.json` for every version: character proportions against the model sheet, costume, prop state and position, screen direction, eyelines, light direction, time of day, between this shot and its neighbors. Keeps a continuity log per scene, the way the UK standard asks for photos of prop positions and a log of every change.
- **Can block:** approval of a shot with open continuity issues, unless the Director waives in writing.
- **Cannot:** fix anything; it reports.
- **Claude setup:** Sonnet 5.5, high. Skill: continuity-check.

#### Critic Panel
- **Owns:** blind, pairwise judgments of each version against gold references: Claude (a Studio Critic agent on Opus 5.5), Gemini (sees the video, though only at about 1 frame per second by default, so it judges performance and pacing), and one GPT model. Each judges in both orders; a win only counts if it survives the swap (research/04).
- **Can block:** nothing in normal production; it informs the Director. Its scores are a hard threshold only at Look Lock and in the R&D tune loop.
- **Why multi-family:** judges favor their own family's output, so no single model family judges alone.
- **Claude setup:** Studio Critic subagent plus API calls to the other judges. Skill: critic-panel.

---

## 5. Stages, gates and locks

A lock means downstream work can build on it. Changing a locked artifact needs a change request in `decisions.md` that names the downstream impact, a cost from the Producer, and the EP's approval.

| # | Stage | Main outputs | Accountable | Approves | Signs | Lock |
|---|---|---|---|---|---|---|
| 0 | Studio setup (once per studio version) | Tools, house style, gold and known-bad sets, calibrated QC and critics | Pipeline TD (tools), Creative Director (bar) | Creative Director | EP | Studio Ready |
| 1 | Development | Brief, logline, treatment, script, beat sheet, feasibility check | Head of Story | Director | EP | **Script Lock** |
| 2 | Design | Production style guide, art boards, model sheets, set and prop designs, colour script, scale lineup, continuity baseline | Production Designer | Director | EP | **Design Lock** |
| 3 | Story reel | Boards, animatic with voice, shot list with IDs, frame durations and route per shot | Editor (with Head of Story) | Director | EP | **Animatic Lock** |
| 4 | Fabrication | Approved assets (reference packs, meshes, rigs, mouth sets, LoRAs) | Head of Fabrication | PD (surface), Sup. Animator (function), Director (whole) | n/a | Per-asset approval |
| 5 | Test shot | One shot through the whole pipeline at final quality | Director | Creative Director must concur | EP | **Look Lock** |
| 6 | Production | Approved shots | Director (per shot) | Director | n/a | Per-shot approval |
| 7 | Edit | Picture lock | Editor | Director | EP | **Picture Lock** |
| 8 | Sound | Final voice, effects, music, mix | Sound Supervisor | Director | EP | **Sound Lock** |
| 9 | Finish and delivery | Grade, titles, masters, deliverables, delivery QC | Producer | Director | EP | **Final** |
| 10 | Retro | Lessons folded into skills, style bible, rubric | Creative Director (with Pipeline TD) | EP | n/a | New studio version |

**Exit criteria that matter most:**
- **Script Lock** includes a feasibility check: the Producer, Supervising Animator and DP confirm nothing in the script is beyond the pipeline (crowds, water, long walks, shots longer than a route can hold) or they price it.
- **Animatic Lock** fixes durations. A commercial's edit is "largely fixed by the animatic" because there are no spare takes; the same is true here, because every extra second costs generation.
- **Look Lock** is the studio-grade bar: the test shot passes every code gate; the critic panel's win rate against gold is at or above target on held-out comparisons; a blind human A/B (Chris plus 3 to 5 others) is at or above target; the Creative Director concurs. Targets live in `studio/STYLE_BIBLE.md` and start from research/04 (panel win rate at least 0.40 overall and 0.35 per dimension, where 0.50 means indistinguishable from gold). These are proposed numbers to validate, not industry standards.

---

## 6. The shot cycle

Every shot moves through the same loop. Status values (adapted from ShotGrid and Kitsu conventions, research/06):

| Status | Meaning |
|---|---|
| `wtg` | Waiting: an input isn't ready (asset, animatic lock, voice) |
| `rdy` | Ready: all inputs approved and the kickoff is written |
| `ip` | In progress |
| `pop` | Pop-through ready for review (our addition) |
| `rev` | Final version pending review: QC, critics and continuity are done |
| `rtk` | Retake: open notes. Any open note on the current version puts the shot here |
| `apr` | Approved by the Director |
| `fin` | Final: post done, conformed into the edit |
| `hld` | On hold |
| `omt` | Omitted |

Steps:

1. **Kickoff.** The Director writes `kickoff.md` (Supervising Animator and DP consulted): one-line intent, acting beats with frame ranges, references, do-not-change list, route, generation budget. For hero shots, Chris can act the shot out on his phone as live-action reference; Nick Park did this for every shot of Vengeance Most Fowl.
2. **Layout.** The DP and Camera Operator set camera, lens and light in `shot.json`, and produce a layout frame (anchor frame for the generation route, layout render for the Blender route). DP approves.
3. **X-sheet.** The Animator writes `xsheet.csv`; the Lip Sync Artist adds phonemes for dialogue.
4. **Pop-through.** Key poses as stills, about one every 12 frames, at low cost. Lead Animator reviews, Supervising Animator approves (Director on hero shots). Status `pop`. Nothing final gets made before this approval. The tracker CLI enforces it.
5. **Final.** Generation or Blender render, on twos.
6. **Post.** Compositor runs the clay-post stack.
7. **QC.** Scripts write `qc.json` automatically. A fail goes straight back to step 5 or 6 and counts as a technical retake, not a creative round.
8. **Critics and continuity,** in parallel: `critics.json` and `continuity.json`. Status `rev`.
9. **Dailies.** The Editor drops the shot into a 3 to 5 shot mini-cut. The Director reviews in context with the QC, critic and continuity summaries, then approves (`apr`) or writes notes (`rtk`).
10. **Retake ladder** as in section 3: two creative rounds, then Senior Animator, then simplify, then decide.

---

## 7. Artifacts and required fields

**`brief.md`** (EP): purpose, audience, length, aspect ratio, budget, deadline, must-haves, never-dos.

**`shot.json`:** shot ID, sequence, duration in frames, animatic reference, characters, set, props, dialogue lines and voice take IDs, route (generation, Blender, hybrid), lens, camera move, light spec, generation budget, references, status, owner, current version.

**`kickoff.md`:** intent (one line), acting beats with frame ranges, references, do-not-change list, route, budget, reviewer chain.

**`xsheet.csv`:** one row per frame: frame, action note, hold (`=` for held), pose ID, phoneme, mouth shape, camera note, effects note.

**Model sheet folder:** ID, version, turnaround, expressions, mouth chart, hands, scale lineup, material callouts, character bible (wants, fears, how it moves), approved reference pack, identity embedding reference.

**Version record:** `SQ010_SH020_v003`, parent version, packet used, route, generator and model version, seeds, prompts, cost, QC result.

**`notes.md`** (one per shot), one entry per note:
```
- id: N-SQ010_SH020-007
  shot: SQ010_SH020
  version: v003
  frames: 34-58
  type: creative | technical | continuity | scope
  priority: must | should | could
  from: director
  to: animator
  note: Hold the neutral face 4 more frames, then snap the brows up on frame 41.
  drawover: notes/N-007.png        (optional)
  restated: Hold neutral through 40; brow snap to raised on 41-42.
  reply: Done in v004. Neutral held to 40, brows raised 41.
  status: open | addressed | verified | wontfix
```
Rules: notes live in files, never only in chat. The artist fills `restated` before starting. Only the note's author or the gate owner sets `verified` or `wontfix`. A `scope` note (a change of mind after approval) also goes in `decisions.md` with the Producer's cost.

**`decisions.md`:** date, decision, owner, reason, downstream impact, cost, approvals. Locks, waivers, scope changes, route changes, budget changes.

**`ledger.csv`:** date, role, tool, model, units, cost, shot, version.

---

## 8. How people communicate

**Lines of communication**
- The EP talks to the Director and the Producer. Nobody else.
- The Director talks to department heads, and to animators at kickoff and dailies.
- Heads talk to their own crews, and to each other for consults (the DP, Production Designer and VFX Supervisor on tiering hard shots; the Head of Fabrication and Supervising Animator on asset function; the VFX Supervisor and Head of Fabrication on "plate-ready").
- Artists take notes only from their review chain and the Director. That stops conflicting notes.
- QC, critics and continuity don't talk to anyone. They write reports.

**Files decide; messages coordinate.** Agents may message each other to coordinate, but a decision only exists once it's in a file (`notes.md`, `decisions.md`, `locks.json`, the tracker). Agents start with no memory of the Producer's conversation, so the files are the only reliable record.

**The rituals** (the AI version of studio meetings):

| Ritual | When | Who | Output |
|---|---|---|---|
| Gate review | Each lock | Accountable head presents; Director approves; EP signs | Lock entry in `locks.json` and `decisions.md` |
| Kickoff | Each shot | Director, with Sup. Animator and DP consulted | `kickoff.md` |
| Pop-through review | Each shot | Lead, then Sup. Animator (Director on hero shots) | Approve or notes |
| Dailies | Each batch of finals | Director, with Editor's mini-cuts and reports | Approvals and notes |
| Producer report | Each working session | Producer to EP | One-screen status |
| Retro | Each production | Creative Director, Pipeline TD, heads | Skill and style bible updates |

**How intent survives a big crew.** Real studios rely on voice recorded first, live-action reference, annotated X-sheets, shared reference libraries, a single colour look (Isle of Dogs used one LUT from set to final grade), and an emotional core the team keeps returning to (Travis Knight's phrase). Each has a home here: final voice before lip sync; LAV for hero shots; `xsheet.csv`; the reference packs; one post look per production in clay-post settings; and a one-paragraph "why this film" at the top of every kickoff.

---

## 9. Accountability

### 9.1 RACI

R = does the work, A = accountable and signs, C = consulted, I = informed.

| Deliverable | EP | Dir | Prod | CD | Story | PD | Fab | Anim | DP | VFX | Edit | Sound | Cont. | TD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Brief | A | C | R | C | I | I | I | I | I | I | I | I | I | I |
| Script | I | C | C | I | A/R | C | I | C | C | I | I | I | I | I |
| Production design | I | C | I | C | I | A/R | C | C | C | C | I | I | I | I |
| Model sheets | I | C | I | I | I | A | C | C | I | I | I | I | C | I |
| Animatic and shot list | I | C | C | I | R | I | I | C | C | I | A/R | C | I | I |
| Assets | I | C | C | I | I | C | A/R | C | I | C | I | I | C | C |
| Test shot / Look | C | A | R | C | I | C | R | R | R | R | I | I | C | R |
| Shot kickoff | I | A/R | I | I | I | I | I | C | C | I | I | I | I | I |
| Pop-through | I | C | I | I | I | I | I | A/R | C | I | I | I | I | I |
| Final shot | I | A | I | I | I | I | C | R | R | R | C | I | C | I |
| Continuity report | I | I | I | I | I | I | I | I | I | I | I | I | A/R | I |
| Picture lock | C | A | I | I | C | I | I | I | I | I | R | C | I | I |
| Sound lock | C | A | I | I | I | I | I | I | I | I | C | R | I | I |
| Delivery | A | C | R | I | I | I | I | I | I | C | R | C | I | C |
| Budget and schedule | A | C | R | I | I | I | I | I | I | I | I | I | I | I |
| House style and gold set | A | C | I | R | I | C | I | I | I | I | I | I | I | C |
| Tools and QC | I | I | A | C | I | I | I | I | I | C | I | I | I | R |

Abbreviations: Dir Director, Prod Producer, CD Creative Director, Story Head of Story, PD Production Designer, Fab Head of Fabrication, Anim Supervising Animator, DP Director of Photography, VFX VFX Supervisor, Edit Editor, Cont. Script Supervisor, TD Pipeline TD.

### 9.2 Who can say no

| Role | Can block | Cannot |
|---|---|---|
| Executive Producer | Anything | n/a |
| Director | Any creative work | Spend, schedule |
| Producer | Starting work whose inputs aren't approved; spend over budget; scope creep | Approve or reject creative work |
| Creative Director | Look Lock below the house bar; changes to house style | Direct or approve shots |
| Department head | Work entering its department that misses spec | Overrule the Director |
| Script Supervisor | Approval with open continuity issues (Director can waive in writing) | Fix anything |
| Technical QC | Approval of any version failing a gate. Only the EP, with a Pipeline TD fix filed, can override a proven false positive | Approve anything |
| Critic Panel | Only Look Lock and tune-loop thresholds | Anything in normal production |

### 9.3 Escalation

Artist > Lead > Head > Director (creative) or Producer (schedule, budget) > EP. Any disagreement still open after one exchange moves up one level, so agents don't argue in circles. A Director and Producer conflict goes to the EP with both positions written in `decisions.md`.

### 9.4 Retake reasons

Every retake is tagged, and the Producer reviews the rates after each batch. Categories from animation practice (CGWire), plus one for generated work:
- **Careless error:** the artist missed something in the brief.
- **Style or reference breach:** off model, off style guide.
- **Artistic change:** the Director changed their mind. Logged as scope.
- **Note poorly addressed:** the previous note wasn't fixed.
- **Equipment fault** (our addition): the generator produced a glitch, morph or artifact that no instruction caused.

---

## 10. Studio metrics

| Metric | Why | Reference point |
|---|---|---|
| Reshoots after approval | Approval quality | About 1% on Vengeance Most Fowl |
| First-pass approval rate | Brief and kickoff quality | Track; no published benchmark |
| Retakes by reason | Where the process leaks | CG TV rule of thumb: a batch is done when 3 to 5% of shots are on a third retake |
| Generations per approved shot | Pipeline efficiency | Vendor heuristic of about 3 (unverified) |
| Cost per finished second | Budget | Track per route |
| QC first-pass rate | Tool health | Track |
| Critic win rate against gold (held-out) | Distance from the bar | 0.50 = indistinguishable |
| Continuity issues per shot | Drift | Track |
| Time in status | Stalls | Flag past the limit |
| Approved seconds per session | Throughput | Human studios: 3 to 5 s per animator per week |

---

## 11. Crew size by job

Small studios compress roles; Aardman's Frubes spot ran on 6 people, and One 6th Studio had one person acting as producer, writer-director, DP, editor and set builder. The bible defines every role so nothing is forgotten; a production only spawns the agents it needs.

**30 to 60 second spot (about 14 agents):** EP (Chris), Producer, Director (also Head of Story), Writer, Production Designer (also visual development, character and set design), Head of Fabrication (also fabricator), Supervising Animator, 2 to 3 Animators (one Senior on call), DP (also operator), VFX Supervisor (also compositor and effects), Editor (also animatic and assistant editor), Sound Supervisor, Script Supervisor, Coordinator, plus QC scripts and the Critic Panel.

**2 to 3 minute short:** the full roster, with a Lead Animator per sequence and a Sequence Director past about 40 shots.

**R&D mode (between productions):** Creative Director, Pipeline TD, Researcher, one Animator, one Compositor, QC scripts, Critic Panel. This is the crew that runs the tune loop.
