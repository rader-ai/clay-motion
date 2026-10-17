# Clay Studio Bible

How this AI clay studio is organized: every role, what it owns, what good looks like, how work and notes move, and who answers for what. Version 0.2.

**The studio docs**
| File | Covers | Owner |
|---|---|---|
| `STUDIO_BIBLE.md` (this file) | Roles, seniority, gates and locks, shot cycle, notes, communication, accountability | Producer and Creative Director |
| `CREATIVE_DIRECTION.md` | Chris's direction: real textures, fibers, earthy materials, one connecting thread | Executive Producer |
| `CLAUDE_MAPPING.md` | Which model, feature and skill each role uses | Pipeline TD |
| `STORY.md` | Story drafts, thumbnails, boards, animatic, layout, edit drafts | Head of Story, Editor |
| `DESIGN_AND_WORLD.md` | World and material bible, characters, sets, effects, originality | Production Designer |
| `FABRICATION.md` | Building characters, sets and props in code | Head of Fabrication |
| `LOOK_DEV.md` | Materials, fibers, boil, camera, light, color, post, screen test | Look Development Supervisor, DP, VFX Supervisor |
| `MOTION.md` | Motion style guide, animation engine, motion QC | Supervising Animator, Animation TD |
| `SOUND.md` | Voice, effects, music, mix, audio QA | Sound Supervisor |
| `ENGINEERING.md` | Repos, Blender pinning, tracker CLI, hooks, compute, review site, tests | Pipeline TD |

Sources: `research/01` to `research/15`, gathered Oct 17, 2026. Where this bible adds something real studios don't do, it says "our addition" and why. Real stop-motion credit lists, postings and interviews document roles and throughput well but rarely document formal sign-off rules, so the accountability lines here are a design informed by that evidence.

---

## 1. What this studio is for

Original clay stop-motion films and spots that hold up next to work from Aardman, Laika and their peers, made by Claude agents as the crew, rendered in Blender from code. Generative video is not part of the default pipeline.

Two facts from real studios shape everything:
1. **Stop motion is progressive, not iterative** (Travis Knight, Annecy 2026). A shot can only be fixed by reshooting it, so real studios approve the cheap things first: script, boards, animatic, maquette, camera and light test, pop-through. We do the same: cheap previews get approved before expensive renders.
2. **One named person approves each shot.** On Vengeance Most Fowl the directors reviewed the previous week's footage and approved or rejected every shot; the reshoot rate after approval was about 1% (research/05). Every deliverable here has one accountable owner.

---

## 2. Org chart

```
Executive Producer (Chris, human)
├── Creative Director (house style and the bar, across all productions)       [our addition]
├── Producer (main Claude Code session)                          PRODUCTION LINE
│   ├── Production Coordinator
│   └── Pipeline TD (tools, tracker, hooks, render, QC code)
│       ├── Animation TD (the animation engine)                  [our addition]
│       ├── Researcher
│       └── Technical QC (code gates)
└── Director                                                      CREATIVE LINE
    ├── (optional) Co-director / Sequence Director
    ├── Head of Story
    │   ├── Writer
    │   ├── Storyboard Artist
    │   └── Animatic Editor
    ├── Production Designer
    │   ├── Visual Development Artist (art boards, mood boards, concept)
    │   ├── Character Designer
    │   ├── Set and World Designer (sets, props, signage, world bible draft)
    │   └── Look Development Supervisor (materials, screen test)  [our addition]
    │       └── Look Development Artist
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
    │   └── Sound Designer and Dialogue Editor
    └── Script Supervisor (Continuity)                            [our addition]

Advisory, reports to nobody, writes reports only: Critic Panel
```

**Creative line vs production line.** Story, design, fabrication, look development, animation, camera, VFX, editorial and sound answer to the Director. Schedule, budget, staffing, tracking and tools answer to the Producer. The Director says no on performance, design and shot acceptance; the Producer says no on schedule, budget, headcount and scope. Real studios split it the same way (research/05; the exact split is partly inferred there).

---

## 3. The seniority ladder

Real postings show the same ladder in every department (research/05): Head or Supervisor (10+ years; owns the department plan) > Lead (5+ years; sets tasks, mentors) > Senior (the hardest work) > Artist (owns assigned work) > Assistant or Junior (prep, maintenance).

Here, seniority is four things at once:
| Level | Model and effort | Authority | Reviewed by | Typical work |
|---|---|---|---|---|
| Head / Supervisor | Opus 5.5, high or xhigh | Approves work in its department; writes standards; can refuse incoming work that misses spec | Director (creative) or Producer (production) at gates | Standards, casting work, cross-shot consistency |
| Lead | Opus 5.5, high | First review of a sequence; breaks work into tasks | Head | Owns a sequence or area |
| Senior | Opus 5.5, high | Same as Artist, plus the hardest work and third attempts | Lead, then Head | Hard shots, retakes |
| Artist | Sonnet 5.5, medium | Owns assigned work; approves nothing | Lead | Volume work to a clear spec |
| Assistant | Haiku 5.5, low | None; never delivers final work | Artist or Lead | Prep, contact sheets, renaming, checks |

Deliberate exceptions, with reasons, are listed in CLAUDE_MAPPING.md.

**The retake ladder.** Real studios give the hardest shots to their most senior animators (Gromit shots were the hardest on Vengeance Most Fowl). Here, counted in creative rounds (notes of type creative or scope), not versions, so code-QC re-renders don't use up rounds:
1. Rounds 1 and 2: the Animator.
2. Round 3: the Senior Animator, with every prior note.
3. Still failing: the Supervising Animator and DP simplify the shot (restage, crop, change the move, avoid the walk).
4. Still failing: the Director and Producer choose redesign, cut, or accept with a written waiver.
The two-round cap is our rule, informed by agent-film research (FilmAgent capped loops at three, AnimeAgent at two) and CG TV practice; no published stop-motion figure exists.

---

## 4. Roles

Each role lists what it owns, where it sits, what it can and can't decide, what good looks like, how it fails, and its Claude setup (models per CLAUDE_MAPPING.md).

### 4.1 Studio level

#### Executive Producer (Chris)
- **Owns:** why the production exists, the brief, budget ceiling, deadline, and the final yes. Signs every build gate and production lock (section 5).
- **Sits:** top. Gives notes only to the Director and Producer, never directly to crew, so artists never get conflicting instructions (real studios route EP and client notes the same way).
- **Decides:** greenlight, budget, deadline, locks, kill or cut, raising the budget, overriding a proven QC false positive.
- **Good looks like:** a one-page brief; gate decisions within a day; changes after a lock accepted with the Producer's cost estimate; judging shots in context.
- **Fails when:** notes go straight to artists; the brief changes after a lock without paying for it.
- **Claude setup:** human. Asked at gates through AskUserQuestion and the review site; decisions recorded with `studio decide`.

#### Creative Director (our addition)
- **Why:** film crews don't have this title, but multi-production studios and agencies do. This studio holds one bar across productions, so someone owns the bar.
- **Owns:** the house style (`STYLE_BIBLE.md`, built from CREATIVE_DIRECTION.md), the gold and known-bad reference sets with provenance, the scoring rubric, judge calibration, and folding each production's lessons into the skills. Co-leads the R&D tune loop with the Pipeline TD.
- **Sits:** reports to the EP. Advises Directors; never directs a shot. Must concur before Look Lock and Studio Bar are signed.
- **Cannot:** give shot notes, approve shots, or move the bar mid-production.
- **Good looks like:** every style rule has a frame example and a reason; rubric changes are versioned with evidence; can say in one sentence why a frame fails.
- **Fails when:** writes adjectives instead of rules; tunes the bar to one production's look.
- **Claude setup:** Opus 5.5, high, `memory: user`.

### 4.2 Production line

#### Producer (main Claude Code session)
- **Owns:** plan, schedule, budget and ledgers, tracker, staffing (which agent, which model), handoff packets, gate logistics, risk log, the EP's status report. Covers what a line producer would do, with the Coordinator.
- **Decides:** order of work, who does it, spend within budget, when to stop a loop, which shots go to which bucket or route (with the DP and Supervising Animator), omit proposals (Director agrees on creative impact).
- **Cannot:** approve or reject creative work, change a locked artifact, or commit the EP to anything over budget.
- **Good looks like:** no agent waits on an input that exists; nothing gets a final render before its pop-through is approved; the ledger matches reality; the EP gets a one-screen status. Laika's producer re-sequenced shots when puppets ran late; ours re-sequences when assets aren't approved.
- **Fails when:** shots outrun their assets (Missing Link's units ran ahead of puppet readiness); it does creative work itself; its context fills with raw output instead of files and workflows.
- **Claude setup:** main session, Opus 5.5, high. Skills: studio-charter, make, production-tracking.

#### Production Coordinator
- **Owns:** tracker hygiene, notes recorded with IDs, packets, reminders, stalled-work flags.
- **Good looks like:** every note has an ID, shot, version, frames, type, author and status; nothing sits in a status past its limit unflagged.
- **Fails when:** paraphrases a note into something the Director didn't say.
- **Claude setup:** Haiku 5.5, low.

#### Pipeline TD
- **Owns:** every tool: the tracker CLI, hooks, Blender environment and adapter, render infrastructure, QC code, the review site, tests (ENGINEERING.md). Root-causes technical failures.
- **Decides:** how a technical requirement is met. Can declare a QC result a false positive only with a filed fix and the EP's sign-off.
- **Good looks like:** every check is proven on controlled degradations; no tool change ships without the regression suites.
- **Fails when:** fixes symptoms per shot instead of fixing the tool; loosens a QC threshold to pass a shot.
- **Claude setup:** Opus 5.5, xhigh.

#### Animation TD (our addition)
- **Why:** with no human animators touching puppets, the animation engine is the puppet workshop and the animator's hands at once. CG studios have animation and character TDs for this.
- **Owns:** the standard rig, pose library format, beat sheet, timing compiler, contact solver, secondary layers, lip-sync mapper, camera rig, motion QC (MOTION.md).
- **Sits:** reports to the Pipeline TD; takes requirements from the Supervising Animator.
- **Good looks like:** every approved shot recompiles identically; the Supervising Animator's notes turn into engine changes, not per-shot hacks.
- **Claude setup:** Opus 5.5, high.

#### Researcher
- **Owns:** keeping tools, versions, prices and licenses current. Every claim with a source and a date.
- **Claude setup:** Sonnet 5.5, medium.

#### Technical QC (code gate)
- **Owns:** pass or fail on measurable signals for every version: motion QC, cadence, hold integrity, flicker, blur, palette, audio QA.
- **Can block:** any version from approval. **Cannot:** approve anything.
- **Claude setup:** scripts, run by `studio version add`.

### 4.3 Direction

#### Director
- **Owns:** the production's vision, every creative call, kickoffs, notes and shot approval. Approves every production lock before the EP signs.
- **Sits:** reports to the EP; peer of the Producer. Takes notes only from the EP. Takes evidence from QC, critics, continuity and the Creative Director.
- **Gives notes to:** department heads, and directly to animators at kickoff and dailies (del Toro briefed animators like actors; Nick Park acted shots out on video).
- **Decides:** approve or retake every shot; design and performance choices; continuity waivers; the cut, with the Editor.
- **Cannot:** spend, change the schedule, or make the work. The Director judges; makers make.
- **Good looks like:** kickoffs with a one-line intent, acting beats with frame ranges, references and a do-not-change list; specific, frame-tied notes marked must, should or could; judging shots inside 3 to 5 shot mini-cuts; one animator kept on a sequence where possible; few reshoots after approval.
- **Fails when:** vague notes; changing its mind after approval (that's a scope change, logged and costed); approving because metrics passed although the shot feels dead; tolerating slow drift.
- **Claude setup:** Opus 5.5, xhigh, `memory: user` (taste journal). Writes only through `studio` (kickoff, note, decide, status).

#### Co-director / Sequence Director (optional)
- **Use when:** a production passes about 40 shots or runs sequences in parallel (Pinocchio split vision and emotion between two directors; Vengeance Most Fowl had two directors and a second unit).
- **Owns:** shot approval for an assigned sequence under the Director's kickoffs. The Director keeps picture lock and can overrule.
- **Claude setup:** Opus 5.5, high.

### 4.4 Story (STORY.md)

#### Head of Story
- **Owns:** story structure and clarity across script, beat board, boards and animatic; runs the story room and the table read.
- **Good looks like:** every scene has a want, an obstacle and a turn; boards read in silhouette; boards only ask for what the pipeline can build.
- **Fails when:** story problems survive into production, where they cost the most.
- **Claude setup:** Opus 5.5, high.

#### Writer
- **Owns:** loglines, beat sheet, treatment, script drafts, dialogue.
- **Good looks like:** one idea, one want, a visual payoff; sparse dialogue; writing toward what clay does well (physical comedy, small worlds, props, reactions). Adam Elliot's standard: audiences forgive rough animation, never a weak story.
- **Fails when:** talking heads, crowds, long walks, jokes that depend on perfect lip sync.
- **Claude setup:** Opus 5.5, high (exception: an artist on Opus, because story can't be fixed later and scripts are short).

#### Storyboard Artist
- **Owns:** SVG thumbnails from the symbol library, beat-board panels, and boards rendered from the Blender greybox with line-art ink and move arrows.
- **Good looks like:** shot IDs follow naming; each panel has size, lens and move; screen direction holds; panel JSON is complete.
- **Claude setup:** Sonnet 5.5, medium.

#### Animatic Editor
- **Owns:** building the animatic and `timing.csv`. The Editor owns Animatic Lock.
- **Claude setup:** Sonnet 5.5, medium.

### 4.5 Design (DESIGN_AND_WORLD.md)

#### Production Designer
- **Owns:** the world bible (with its material bible and the four layers), palette and color script, scale rules, sign-off on every design and every surface, and tiering hard shots by cost with the DP and VFX Supervisor (Missing Link's designer did this to avoid overbuilding).
- **Good looks like:** every design cites the world bible; one connecting thread visible at three scales; designs that hold up across hundreds of frames.
- **Fails when:** designs look great as stills but shimmer or drift in motion (busy patterns, text, thin limbs); the material list grows by exception.
- **Claude setup:** Opus 5.5, high.

#### Visual Development Artist
- **Owns:** art boards, mood boards, concept frames, material studies, lighting moods, rendered from Blender and assembled as boards. Feeds the Production Designer.
- **Good looks like:** distinct directions per question, each labeled with what it tests.
- **Claude setup:** Sonnet 5.5, medium.

#### Character Designer
- **Owns:** silhouette sheets, the grey maquette spec, model sheets (turnaround, expressions, mouth chart, hands, scale lineup, material callouts) and the character bible (wants, fears, movement vocabulary).
- **Claude setup:** Sonnet 5.5, high.

#### Set and World Designer
- **Owns:** the world bible draft, set designs and buckets, props lists, signage and hand-lettering, dressing language.
- **Claude setup:** Sonnet 5.5, medium.

#### Look Development Supervisor (our addition)
- **Why:** real clay studios get their look from physical materials and the DP; we have to build every material in code, so someone has to own materials the way CG studios' look-dev departments do.
- **Owns:** every material recipe, the screen test, look regression baselines, texture licenses (LOOK_DEV.md).
- **Can block:** any material that fails the screen test or the material bible.
- **Claude setup:** Opus 5.5, high. Look Development Artist: Sonnet 5.5, medium.

### 4.6 Fabrication (FABRICATION.md)

#### Head of Fabrication
- **Owns:** every character, set and prop asset from approved design to camera, and above all consistency across every shot and copy (Pinocchio's puppet supervisor ran daily cross-studio calls to keep copies matched).
- **Asset approval:** Production Designer signs the surface, Supervising Animator signs function, Director signs the whole (Laika's director approves the sculpt before anything else is built).
- **Good looks like:** rebuilds from spec and seed are identical; assets documented so any animator can use them.
- **Fails when:** an asset depends on undocumented tweaks; textures fight the material recipes.
- **Claude setup:** Opus 5.5, high.

#### Fabricator / Rigger
- **Owns:** building assets to spec: puppets from lumps on the standard rig, mouth and brow sets, kit modules, dressing, manifests.
- **Claude setup:** Sonnet 5.5, medium.

### 4.7 Animation (MOTION.md)

#### Supervising Animator
- **Owns:** performance quality and consistency; casting shots by difficulty; the motion style guide; pop-through approval.
- **Good looks like:** pop-throughs reviewed before finals; timing reads the same across shots; retakes rare and their reasons logged.
- **Claude setup:** Opus 5.5, high.

#### Lead Animator
- **Owns:** a sequence; breaks it into shots; first review of pop-throughs and finals.
- **Claude setup:** Opus 5.5, high.

#### Senior Animator
- **Owns:** the hardest shots and every shot on its third creative round.
- **Claude setup:** Opus 5.5, high.

#### Animator
- **Owns:** a shot from kickoff to approval: writes `shot.yaml` (beats, poses, holds, contacts), makes the pop-through, makes the final, answers every note.
- **Good looks like:** every note restated before work starts; poses read in silhouette; holds and timing follow the style guide; handoff note written.
- **Fails when:** asks for a final before pop-through approval; regenerates without changing the plan; drifts off model.
- **Claude setup:** Sonnet 5.5, medium.

#### Lip Sync Artist
- **Owns:** phoneme breakdown and mouth swaps on the X-sheet; mouths snap and hold, never melt.
- **Claude setup:** Sonnet 5.5, low.

#### Animation Assistant
- **Owns:** prep, filmstrips, test renders, file wrangling. Never final work.
- **Claude setup:** Haiku 5.5, low.

### 4.8 Camera and lighting (LOOK_DEV.md sections 3 and 4)

#### Director of Photography
- **Owns:** lens, framing, depth of field, light design and light continuity; keeper of miniature truth (true-scale depth of field around f/11 to f/16, small hard sources, motivated practicals, no motion blur, camera moves on ones). Approves layout and light for every shot before its pop-through.
- **Fails when:** cinematic CG lighting, telephoto compression, tilt-shift blur, sky lighting.
- **Claude setup:** Opus 5.5, high.

#### Camera and Lighting Operator
- **Owns:** executing the DP's spec per shot.
- **Claude setup:** Sonnet 5.5, medium.

### 4.9 VFX and post

#### VFX Supervisor
- **Owns:** the post chain and frame-level technical quality: per-pose noise, lens character, color pipeline and show LUT application, cleanup, and a joint "plate-ready" check with the Head of Fabrication so a shot doesn't leave animation until post can finish it.
- **Good looks like:** post makes shots consistent without making them smooth; never frame interpolation.
- **Claude setup:** Opus 5.5, high.

#### Compositor
- **Claude setup:** Sonnet 5.5, medium. Runs the post stack per shot.

#### Effects Artist
- **Owns:** fire, smoke, water, snow, dust, made from the world's materials: Robin Robin made fire and smoke from felt, The House swapped wool-tuft flames per frame, Memoir of a Snail used cellophane fire. Real studios also use CG for water and fire (Vengeance Most Fowl did); here a CG effect must match the world's handmade materials and pass the screen test.
- **Claude setup:** Sonnet 5.5, medium.

#### Editor
- **Owns:** the cut from animatic to Picture Lock; drops shots in as they land; builds 3 to 5 shot mini-cuts for dailies.
- **Claude setup:** Opus 5.5, high.

#### Assistant Editor
- **Claude setup:** Haiku 5.5, low. Conform, versions, OTIO, deliverables.

### 4.10 Sound (SOUND.md)

#### Sound Supervisor
- **Owns:** scratch and final voices (voice comes first), effects and Foley, music decisions, mix, audio QA, Sound Lock.
- **Good looks like:** final voices locked before lip sync; tactile, life-size sound with small dynamics; every audio file licensed and logged.
- **Claude setup:** Opus 5.5, high.

#### Sound Designer and Dialogue Editor
- **Claude setup:** Sonnet 5.5, medium. Builds voices, effects layers and the scripted mix.

### 4.11 Quality

#### Script Supervisor (Continuity), our addition
- **Why:** the roles research found no script supervisor credit in stop motion; puppets stay on model physically, and animators and coordinators carry continuity. Code-built shots still drift in what's dressed, where things sit, and how they're lit, so this studio keeps a dedicated role.
- **Owns:** `continuity.json` per version, built mostly from data (dress manifests, puppet specs, camera and light specs) plus a visual check of neighbors: proportions, costume, prop state and position, screen direction, eyelines, light direction, time of day.
- **Can block:** approval with open continuity issues unless the Director waives in writing. **Cannot:** fix anything.
- **Claude setup:** Sonnet 5.5, high (exception: a reviewer on Sonnet, because the manifests do most of the checking).

#### Critic Panel
- **Owns:** blind, pairwise judgments of each version against gold references, from three model families: a Studio Critic agent (Claude), Gemini and one OpenAI model. Each judges in both orders; a win only counts if it survives the swap (research/04). Gemini's votes count only on performance and pacing, because it samples video at about 1 frame per second.
- **Can block:** nothing in normal production. Its scores are thresholds only at Look Lock, Studio Bar and in the tune loop.

---

## 5. Gates and locks

A lock means downstream work can build on it. Changing a locked artifact needs a change request (`studio decide --type scope`) naming the downstream impact and cost, and the EP's approval.

### 5.1 Build gates (once per studio version)
| Gate | When | Owner | Concurs | Signs |
|---|---|---|---|---|
| Spec Lock | The studio's spec is reviewed and revised | Producer | Pipeline TD, Creative Director | EP |
| Studio Ready | Tools built, tests pass, gold and known-bad sets assembled, judges calibrated | Pipeline TD | Creative Director | EP |
| Studio Bar | The tune loop meets the bar on held-out benchmark shots and in Chris's blind A/B | Creative Director | Pipeline TD | EP |

### 5.2 Production locks (every production)
| # | Lock | Main outputs | Owner | Approves | Signs |
|---|---|---|---|---|---|
| 1 | Script Lock | Script, beat sheet, table read, feasibility check | Head of Story | Director | EP |
| 2 | Design Lock | World bible with material bible, maquettes and model sheets, set designs and buckets, color script, screen-tested materials, originality check | Production Designer | Director | EP |
| 3 | Animatic Lock | Boards, animatic with voice, shot list with IDs and frame durations | Editor | Director | EP |
| 4 | Look Lock | One test shot from this production through the whole pipeline, meeting the studio bar | Director | Creative Director concurs | EP |
| 5 | Picture Lock | Final cut | Editor | Director | EP |
| 6 | Sound Lock | Final voices, effects, music, mix, audio QA | Sound Supervisor | Director | EP |
| 7 | Final | Masters, deliverables, delivery QC, rights manifest | Producer | Director | EP |

Per-asset approvals (Head of Fabrication's assets) and per-shot approvals (the Director) happen between locks and need no EP signature.

**Look Lock evidence:** the test shot passes every code gate; the critic panel's win rate against gold meets the studio bar thresholds (stored in `STYLE_BIBLE.md`, starting from research/04: at least 0.40 overall and 0.35 per dimension, where 0.50 means indistinguishable); Chris's blind A/B meets its threshold; the Creative Director concurs. These thresholds are proposals to validate, not industry standards.

**After every production:** a retro (Creative Director with the Pipeline TD and heads) folds lessons into the skills, style bible and rubric, and bumps the studio version.

---

## 6. The shot cycle

| Status | Meaning |
|---|---|
| `wtg` | Waiting: an input isn't ready |
| `rdy` | Ready: inputs approved and kickoff written |
| `ip` | In progress |
| `pop` | Pop-through ready for review (our addition) |
| `rev` | Final pending review: QC, critics and continuity done |
| `rtk` | Retake: open notes on the current version |
| `apr` | Approved by the Director |
| `fin` | Final: post done, conformed into the edit |
| `hld` | On hold |
| `omt` | Omitted |

1. **Kickoff.** The Director writes the kickoff (Supervising Animator and DP consulted): intent, acting beats with frames, references, do-not-change list, bucket, render budget. For hero shots, Chris can record a live-action reference.
2. **Layout.** `build_shot(shot.json)` builds the shot from its board; the DP and Operator refine camera and light; the DP approves.
3. **Beat sheet.** The Animator writes `shot.yaml`; the Lip Sync Artist adds mouth timing.
4. **Pop-through.** Key poses rendered fast as a filmstrip and stepped playblast (MOTION.md section 5). Lead Animator reviews; Supervising Animator approves (Director on hero shots); recorded with `studio pop approve`. No final render before this.
5. **Final.** Compiled exposures, rendered per unique pose at dailies quality.
6. **Post.** The Compositor runs the post chain.
7. **QC.** `studio version add` runs code QC and writes `qc.json`. A fail goes straight back to step 5 or 6 and doesn't count as a creative round.
8. **Critics and continuity** in parallel: `critics.json`, `continuity.json`. Status `rev`.
9. **Dailies.** The Editor drops the shot into a mini-cut; the Director reviews it in context with the reports, then approves (`apr`) or writes notes (`rtk`).
10. **Retake ladder** as in section 3.

---

## 7. Artifacts and notes

Schemas live in the plugin; the main ones:
- `brief.md`: purpose, audience, length, aspect ratio, budget, deadline, must-haves, never-dos.
- `shot.json`: ID, sequence, frames, animatic reference, characters, set, props, dialogue and voice takes, bucket, lens, camera move, light spec, render budget, status, owner, current version.
- `kickoff.md`, `shot.yaml` (MOTION.md 4.3), `exposures.json`, `dress_manifest.json`.
- Version record `SQ010_SH020_v003`: parent version, packet, seeds, render settings, render time, QC result.
- `notes.md`, one entry per note:
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
  restated: Hold neutral through 40; brow snap to raised on 41-42.
  reply: Done in v004. Neutral held to 40, brows raised 41.
  status: open | addressed | verified | wontfix
```
Rules: notes live in files, never only in chat. The artist fills `restated` before starting (catches misreadings). Only the note's author or the gate owner verifies or closes it. A scope note also goes in `decisions.md` with the Producer's cost.
- `decisions.md`: date, decision, type, owner, reason, impact, cost, approvals.
- Ledgers: `ledger.csv` per production; the R&D loop keeps its own in the plugin repo's `rnd/` folder. Every compute-hour and paid call is a row.

---

## 8. How people communicate

**Lines.** The EP talks to the Director and Producer only. The Director talks to department heads, and to animators at kickoff and dailies. Heads talk to their crews, and to each other for consults (DP, Production Designer and VFX Supervisor on tiering; Head of Fabrication and Supervising Animator on asset function; Look Dev Supervisor and DP on materials under light). Artists take notes only from their review chain and the Director. QC, critics and continuity write reports and talk to no one.

**Files decide; messages coordinate.** A decision exists only once it's in a file. Agents start with no memory of the Producer's conversation, so every spawn gets a packet (`studio packet`), and every agent ends with a handoff note.

**Rituals**
| Ritual | When | Who | Output |
|---|---|---|---|
| Gate review | Each lock | Owner presents; Director approves; EP signs | `studio lock`, `decisions.md` |
| Table read | Script drafts | Head of Story, Director | Notes on the draft |
| Board pitch | Each sequence | Head of Story to Director | Notes, re-board |
| Screen test | Each new material | Look Dev Supervisor | Pass or reject |
| Kickoff | Each shot | Director, with Sup. Animator and DP | `kickoff.md` |
| Pop-through review | Each shot | Lead, then Sup. Animator | Approve or notes |
| Dailies | Each batch | Director with Editor's mini-cuts | Approvals and notes |
| Producer report | Each session | Producer to EP | `STATUS.md` and the review site |
| Retro | Each production | Creative Director, Pipeline TD, heads | Skill and style updates |

**How intent survives.** Real studios rely on voice recorded first, live-action reference, annotated X-sheets, shared references, one color look (Isle of Dogs used one LUT from set to final grade), and an emotional core the team keeps returning to (Travis Knight's phrase). Here: final voice before lip sync, phone reference for hero shots, `shot.yaml`, the world bible, one show LUT per production, and a one-paragraph "why this film" at the top of every kickoff.

---

## 9. Accountability

### 9.1 RACI
R = does the work, A = accountable owner (exactly one), C = consulted, I = informed. Approvals and signatures are in section 5.

| Deliverable | EP | Dir | Prod | CD | Story | PD | LD | Fab | Anim | DP | VFX | Edit | Snd | Cont | TD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Brief | A | C | R | C | I | I | I | I | I | I | I | I | I | I | I |
| Script | I | C | C | I | A/R | C | I | I | C | C | I | I | C | I | I |
| World and material bible | I | C | I | C | C | A/R | R | C | I | C | C | I | I | I | I |
| Model sheets and maquettes | I | C | I | I | I | A | C | R | C | I | I | I | I | C | I |
| Animatic and shot list | I | C | C | I | R | I | I | I | C | C | I | A/R | C | I | I |
| Materials and screen test | I | C | I | C | I | C | A/R | C | I | C | C | I | I | I | C |
| Assets | I | C | C | I | I | C | C | A/R | C | I | C | I | I | C | C |
| Look Lock test shot | C | A | R | C | I | R | R | R | R | R | R | I | I | C | R |
| Shot kickoff | I | A/R | I | I | I | I | I | I | C | C | I | I | I | I | I |
| Pop-through | I | C | I | I | I | I | I | I | A/R | C | I | I | I | I | I |
| Final shot | I | A | I | I | I | I | C | C | R | R | R | C | I | C | I |
| Continuity report | I | I | I | I | I | I | I | I | I | I | I | I | I | A/R | I |
| Picture Lock | C | C | I | I | C | I | I | I | I | I | I | A/R | C | I | I |
| Sound Lock | C | C | I | I | I | I | I | I | I | I | I | C | A/R | I | I |
| Delivery | C | C | A/R | I | I | I | I | I | I | I | C | R | R | I | C |
| Budget and schedule | C | C | A/R | I | I | I | I | I | I | I | I | I | I | I | I |
| House style and gold set | C | C | I | A/R | I | C | C | I | I | I | I | I | I | I | C |
| Tools, QC and engine | I | I | C | C | I | I | C | I | C | I | C | I | I | I | A/R |

Abbreviations: Dir Director, Prod Producer, CD Creative Director, Story Head of Story, PD Production Designer, LD Look Dev Supervisor, Fab Head of Fabrication, Anim Supervising Animator, DP Director of Photography, VFX VFX Supervisor, Edit Editor, Snd Sound Supervisor, Cont Script Supervisor, TD Pipeline TD.

### 9.2 Who can say no
| Role | Can block | Cannot |
|---|---|---|
| Executive Producer | Anything | n/a |
| Director | Any creative work | Spend, schedule |
| Producer | Work whose inputs aren't approved; spend over budget; scope creep | Approve or reject creative work |
| Creative Director | Look Lock or Studio Bar below the house bar; house-style changes | Direct or approve shots |
| Department head | Incoming work that misses its department's spec | Overrule the Director |
| Look Dev Supervisor | Any material that fails the screen test | Change the world bible |
| Script Supervisor | Approval with open continuity issues (Director can waive in writing) | Fix anything |
| Technical QC | Approval of any version failing a gate (only the EP, with a filed fix, overrides a proven false positive) | Approve anything |
| Critic Panel | Only Look Lock, Studio Bar and tune-loop thresholds | Anything in normal production |

### 9.3 Escalation
Artist > Lead > Head > Director (creative) or Producer (schedule, budget) > EP. A disagreement still open after one exchange moves up one level, so agents don't argue in circles. A Director and Producer conflict goes to the EP with both positions in `decisions.md`.

### 9.4 Retake reasons
Every retake is tagged and reviewed after each batch. From animation practice (CGWire): careless error; style or reference breach; artistic change (logged as scope); note poorly addressed. Our addition: **tool fault** (the engine, a shader or a script did something nobody asked for), which goes to the Pipeline TD, not the artist.

---

## 10. Studio metrics
| Metric | Why | Reference point |
|---|---|---|
| Reshoots after approval | Approval quality | About 1% on Vengeance Most Fowl |
| First-pass approval rate | Brief and kickoff quality | Track |
| Retakes by reason | Where the process leaks | CG TV rule of thumb: a batch is done when 3 to 5% of shots are on a third retake |
| Render hours per approved second | Pipeline efficiency | Track by bucket |
| Cost per finished second | Budget | Track |
| QC first-pass rate | Tool health | Track |
| Critic win rate against gold (held-out) | Distance from the bar | 0.50 = indistinguishable |
| Continuity issues per shot | Drift | Track |
| Time in status | Stalls | Flag past the limit |
| Approved seconds per session | Throughput | Human studios: 3 to 5 s per animator per week |

---

## 11. Crew size by job

Small studios compress roles (Aardman's Frubes spot ran on 6 people). A production spawns only the agents it needs.

**30 to 60 second spot (about 16 agents):** EP (Chris), Producer, Director (also Head of Story), Writer, Production Designer (also visual development, set and world design), Look Dev Supervisor, Character Designer, Head of Fabrication (also fabricator), Supervising Animator, 2 Animators (Senior on call), DP (also operator), VFX Supervisor (also compositor and effects), Editor (also animatic and assistant editor), Sound Supervisor (also sound designer), Script Supervisor, Coordinator, plus the Pipeline TD and Animation TD on call, QC code and the Critic Panel.

**2 to 3 minute short:** the full roster, with a Lead Animator per sequence and a Sequence Director past about 40 shots.

**R&D mode (between productions):** Creative Director, Pipeline TD, Animation TD, Look Dev Supervisor, Researcher, one Animator, one Compositor, QC code and the Critic Panel. This crew runs the tune loop.
