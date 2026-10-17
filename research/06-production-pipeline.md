# Stop-motion production pipeline (research, Oct 17, 2026)

[U] = unverified or inferred. Public stop-motion sources document stages, crew and throughput well; they rarely document status names, note formats or review-round counts, which come from ShotGrid, Kitsu, ftrack and VFX practice.

## Headline findings
1. Stop motion is progressive, not iterative (Travis Knight, Wildwood, Annecy 2026). You can't revise a shot after shooting without reshooting it, so approvals sit BEFORE the shoot: animatic, pop-through, camera and lighting test. Cheap artifacts do the job revision rounds do in CG.
2. One named person approves each shot. The daily or weekly review is where approval is recorded.
3. Throughput is low and well documented: ~3-5 s per animator per week on features. Schedule from it.
4. Transferable rules for AI agents: lock upstream artifacts, require a cheap preview approval before expensive generation, make every note a tracked object.

## 1. Stages, gates, locks
- Development: pitch, treatment, script, greenlight. Wildwood: 500+ page novel to ~120 page script; no meaningful design until script approved. Script lock = design may begin.
- Pre-production: designs, colour script, boards, animatic/story reel with scratch voice, then final voice. Aardman records voice first because animation is timed to dialogue (20+ hours of takes for Wallace; Park picked the best). Laika: puppet designs sculpted digitally, director approves before armature team; puppet manufacture ~9 months. Pinocchio story reel took ~12 months to lock. Commercials: script approved, then animatic to client before any animation; approval layers director, agency, client. Design lock = director signs the sculpt/maquette. Animatic lock = timing fixed (commercial edit "largely fixed by the animatic"). Look: Kubo physical effects tests reviewed by department heads and production designer before directors; Isle of Dogs used one LUT on set, in projection, and in the DI; complex camera moves on Early Man got weeks of tests.
- Production: Laika's script_splitter imports a Final Draft script and creates sequences, scenes, characters, sets, dialogue lines in the tracker; each scene gets a task sized at ~4 s/animator/week. Per-shot cycle: director or animation director briefs animator, animator makes pop-through/blocking, director approves, animator shoots, result goes to dailies. Nightmare pop-through: first pass poses ~every 12th frame while working out angle, lens, light; after review, second pass every 2-4 frames; pop-through 1-2 days, shot a week or more; major changes need another pop-through. Pinocchio chain: storyboard, rough-puppet camera pass, animator acting reference, blocking every 5-10 frames, final. UK NOS: pop-through and keys "agreed with the director."
- Post: frames treated as plates for rig removal and cleanup. Pinocchio's editor recut every shot as it arrived; one project held boards through final. Sequences delivered on separate deadlines and assembled into 10-20 min reels with handles. Coraline sound team cut to stills. Picture lock = cut final, goes to online and mix. Sound lock follows picture lock [U]. A 3-spot commercial yielded 24 deliverables (aspect ratios, languages).

## 2. Core artifacts
- X-sheet: header with sequence/scene/page; one row per frame; columns for action notes, dialogue broken into phonemes at the frame each sound lands, level/part numbers, background, camera. Stop motion: puppet parts and replacement pieces take the level columns. Dragonframe X-sheet has per-frame reminders, post notes, waveforms, track reads, CSV export.
- Naming: Dragonframe scene_take_exposure_frame. Blender Studio SSS_SSSS incremented by 10 (010_0030). VFX notes example SEQ_010_SHOT_0040_v012.
- Laika tracker entities: departments, shops, sequences, shots, tasks, notes; physical builds are Assets (puppet builds, set builds, face kits).
- Character bible: Aardman's covers feelings as well as look.
- Colour script: one small painting per key scene.
- Mouth/face libraries: Pirates! ~8,000 mouths (257 for the Captain); Missing Link ~106,000 faces, ~30 puppet models per character; Early Man 3,000 hand-made mouths.
- Continuity (UK NOS): photos of prop and dressing positions, log of every change, records for items that age or deplete, strike packs and exact duplicates.

## 3. Review and notes culture
- Cadence: Nightmare daily morning review (director speaks first, shots looped). Vengeance Most Fowl weekly review; directors approve or reject; rejected shots redone. Pinocchio: del Toro reviewed mini-cuts of 3-5 shots. Isle of Dogs: Anderson reviewed remotely; one sequence shot 16 lighting variations per frame so he could pick later.
- Sweatbox: director approval at rough, cleanup, final; scene judged inside the reel, in context.
- Notes (VFX practice): coordinator transcribes live; each note has shot ID and version, creative or technical tag, optional drawover on a paused frame.
- Tracking to closure (CGWire): one decision-maker; notes attach to timecode and screenshot; notes live in the tracker, not chat; a note triggers a status change and stays open until done; disagreements go to a short follow-up; artists restate notes to confirm understanding.
- Retake taxonomy (CGWire): careless error; reference or style breach; artistic change (treat as scope change); note poorly addressed.
- Round counts: no published stop-motion figure. CG TV rule of thumb: done when ~3-5% of shots remain in a third retake.

## 4. Status tracking
- ShotGrid: wtg Waiting, rdy Ready, ip In Progress, hld On Hold, omt Omit, cbb Could Be Better, fin Final. Version statuses: Pending Review, Pending Director Review, Viewed, Final Approved. Notes: Open, In Progress, Closed. Automation: a Final Approved version sets the shot to Final Approved.
- Kitsu: TODO, WIP, Waiting For Approval, Retake (increments a retake counter), Done; "feedback request" routes to supervisor queue.
- Toon Boom: Standby, Pending, Need Assistance, In Progress, To Validate, Revise, Approved.
- ftrack maps statuses onto Not Started, In Progress, Done, Blocked.
- Handoff: version status "Ready for Next Department" puts current task on hold and sets the next to ready.
- Task dependencies: finish-to-start default, plus start-to-start, finish-to-finish, start-to-finish.

## 5. Throughput
| Production | Units / animators | Rate |
|---|---|---|
| Coraline | 28+ animators | 90-100 s/week total (~3.5 per animator); target 5-6 |
| Kubo | n/a | just under 3.5 s/animator/week; ~90 weeks |
| Missing Link | 97 units, 31 animators | budget 4.3 s/week; ~2 for action; 92 weeks |
| Isle of Dogs | 44 units, ~30 animators | 87 weeks |
| Early Man | 33 animators, ~40 sets | under 1 s/day |
| Vengeance Most Fowl | 30-35 animators, ~40 stages | 4.2 s/animator/week; ~2 min/week |
| Pinocchio | ~60 units | ~1,000 shooting days |
- Aardman 40 s Thatchers spot: 480+ animator-hours, 40-person team (~12 animator-hours per second).
- Producer tracking: Laika leveled 12,000 tasks across 60 resources in Shotgun; Aardman's CORE tool cut shot turnover from ~1.5 days to ~10 minutes; CGWire flags stalled shots at 5 days, tracks estimate vs actual and burn rate.

## 6. Communication patterns
- Aardman animation directors brief art and camera crews first, then animators; they split the floor so one is always available.
- Park acted out every shot on video; animator reviewed it with the animation director.
- Kubo's animation supervisor attended every editorial brief with the director, then followed up with animators.
- Pinocchio: director briefed animators like actors; one animator stayed on each sequence for acting consistency.
- Producers own budget and schedule; coordinators schedule reviews, take notes, track delivery.
- Intent survives through: voice-first records, live-action reference, annotated X-sheets, reference libraries, a shared LUT, an "emotional core" the team returns to (Knight), and the work reel mixing boards, blocking and finals.

## 7. Lessons from hybrid and AI productions
- Laika is physical-first; default is in-camera, VFX covers shortfalls; pipeline took ~10 years to mature.
- Spider-Verse adopted on-twos and strong posing; cost ~1 week per second vs ~4 s/week typical CG. Price handmade constraints up front.
- Blender Studio: blocking reviewed before polish ("changes are cheap"); delivery checklist before handoff; edit stays mixed-stage.
- FilmAgent (arXiv 2501.12909): Critique-Correct-Verify and Debate-Judge loops with a director agent as judge, capped at 3 iterations; group 3.98 vs solo 3.04 (authors' own eval).
- AnimeAgent (arXiv 2602.20664): director agent writes a structured "textual dope sheet"; reviewer checks consistency at a 0.8 threshold, max two revision rounds; removing the director agent degraded every metric.
- Vendor guidance: lock script, shot order, character sheets, location refs, style block; approve each scene's anchor frame before generating motion; budget ~3 generations per usable shot.

## 8. Proposed pipeline spec (researcher's draft)
| # | Stage | Gate owner | Lock |
|---|---|---|---|
| 1 | Development | Director | Script lock |
| 2 | Design | Director | Design lock (model sheets) |
| 3 | Animatic (scratch then final voice) | Director | Animatic lock (shot IDs and durations) |
| 4 | Look and test shots | Look lead, then Director | Look lock |
| 5 | Shot breakdown | Producer | Shot list lock |
| 6 | Shot brief, then pop-through | Director | Pop-through approved |
| 7 | Shoot or generate | Animator | n/a |
| 8 | Daily review | Director | Shot final |
| 9 | Post: cleanup, comp, edit | Editor | Picture lock |
| 10 | Sound and music | Sound lead | Sound lock |
| 11 | Grade and deliverables | Producer | QC pass |

Statuses: wtg, rdy, ip, rev, rtk, apr, fin, hld, omt. Version statuses add Pending Director Review and Viewed. Notes: Open, In Progress, Closed. Any note on a version moves the shot to rtk.
Notes: ID; shot and version; frame or timecode; type (creative, technical, continuity, scope change); text; drawover link; author; status. Only the note's author or the gate owner closes it.
Rules: locked artifacts immutable, changes via change request naming downstream impact; no generation without approved pop-through; one decision-maker per review; cap two retake rounds then escalate with a scope decision [U]; log retakes by taxonomy and review weekly.

## Sources
https://www.autodesk.com/autodesk-university/article/Shotgun-Production-Management-LAIKAs-Animated-Features-2019
https://www.postmagazine.com/Publications/Post-Magazine/2024/November-December-2024/Animation-I-Wallace-Gromit-Vengeance-Most-Fowl-I.aspx
https://scriptmag.com/interviews-features/light-on-feet-of-clay-a-visit-with-nick-park-and-merlin-crossingham-of-wallace-gromit-vengeance-most-fowl
https://www.vfxvoice.com/aardman-goes-back-to-stop-motion-basics-with-early-man/
https://awn.com/animationworld/team-effort-bringing-aardmans-early-man-big-screen
https://www.creativebloq.com/features/inside-aardman-animations
https://aardman.com/latest-news/2023/may/aardman-produces-pint-sized-perfection-commercial-for-thatchers-cider/
https://cartoonresearch.com/index.php/capture-lightning-in-a-bottle-animation-production-on-the-nightmare-before-christmas/
https://www.awn.com/animationworld/set-coraline-where-motion-doesnt-stop
https://www.awn.com/print/vfxworld/stop-motion-and-vfx-converge-vast-oceans-kubo-and-two-strings
https://www.slashfilm.com/565038/missing-link-set-visit-report/
https://theasc.com/articles/animal-kingdom-isle-of-dogs
https://borisfx.com/blog/aotc/holly-klein-discuss-editing-the-stop-motion-animated-guillermo-del-toros-pinocchio/
https://awn.com/animationworld/why-travis-knight-waited-16-years-make-wildwood
https://www.cartoonbrew.com/feature-film/wildwood-travis-knight-annecy-263630.html
https://www.ukstandards.org.uk/en/nos-finder/SKSANIM14/create-stop-motion-animation
https://ukstandards.org.uk/en/nos-finder/SKSPRP10/maintain-the-continuity-of-props-and-re-dress--sets-during-production
https://helpwiki.evergreen.edu/wiki/index.php/X-Sheet_-_Dragonframe
https://en.wikipedia.org/wiki/Exposure_sheet
https://en.wikipedia.org/wiki/Sweat_box
https://help.autodesk.com/cloudhelp/ENU/SG-Tutorials/files/SG_Tutorials_tu_tracking_statuses_html.html
https://developers.shotgridsoftware.com/python-api/cookbook/tasks/task_dependencies.html
https://mintlify.wiki/cgwire/kitsu/tasks/task-status
https://blog.cg-wire.com/manage-dailies
https://blog.cg-wire.com/how-to-handle-animation-retakes-in-a-cartoon-tv-show
https://blog.cg-wire.com/how-animation-producers-track-production
https://studio.blender.org/tools/naming-conventions/introduction
https://studio.blender.org/tools/artist-guide/shot-production/animation
https://lbbonline.com/news/the-case-for-stop-motion-animation-in-advertising
https://slashfilm.com/into-the-spider-verse-technique
https://arxiv.org/html/2501.12909v1
https://arxiv.org/html/2602.20664v1
https://invideo.io/faq/should-i-lock-my-storyboard-before-starting-ai-video/
