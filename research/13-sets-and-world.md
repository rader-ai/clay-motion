# Set design and world building for clay stop motion, in code (research, Oct 17, 2026)

~45 searches and 60 fetches. [U] = unverified or inference. Note: this report says bpy 5.1.1 is on PyPI; a direct check in our workspace on Oct 17 showed bpy 5.2.2 available. Blender 5.2 LTS released July 2026.

Bottom line: studios design for the camera and the animator's hands, not realism. They build only what a shot sees, extend with CG from physical references, and treat imperfection as a rule. Agent research solves "plausible rooms" at real-world scale; none solves "handmade miniature at puppet scale", so that layer has to be written.

## 1. How stop-motion art departments build sets
- Chain: production designer owns the look; art directors run departments and references; concept artists and set designers draw it (Laika: concept to shop drawings in Vectorworks; model shop, carpentry, greens, parts). Pinocchio: two production designers, art director, set designer, maquette builder. Missing Link's four concept artists picked 4-5 template locations and "Frankenstein-ed" the rest.
- Scale from the puppet first: Isle of Dogs used three puppet scales (~12-13 in, 7 in, 3.5 in) for close, medium, distant; props scale to head or body on cartoon proportions. Pinocchio 9 in; Vengeance puppets ~9 in with a 1/10-scale valley and a half-scale train. Wildwood's Pittock Mansion 50% scale (~13 ft); 136 sets, 231 puppets. Missing Link shrank puppets and sets ~5-7%.
- Animator access drives construction: Kubo sets ~42 in high, modular "dollhouses"; Laika animators need ~18 in reach; Wildwood platforms roll away; trap doors and rails (Isle of Dogs); pull-away walls (Missing Link); removable walls with 4 in doorways (Were-Rabbit).
- Layering and cheating: Isle of Dogs long dolly set with forced perspective across three puppet scales; Coraline tilted real-world sets and hid it with angles; Wildwood built a short path with smaller-scale buildings behind; Missing Link sorted shots into buckets (foreground over matte, background miniature, CG); Aardman reconfigured two-thirds of one big set and keeps a stock of in-scale buildings.
- Backdrops, extensions, greens: Memoir painted skies on giant canvases; Pinocchio 38-40 keyframed skies with cotton-batting clouds; Kubo (~80 sets) mixed full builds, miniatures with matte paintings and CG extensions tuned to the physical look (woodblock textures in the digital ocean); Wildwood scanned physical builds as background assets; Vengeance built the top of a rail bridge and extended the legs digitally; Wildwood trees resin, lit through a sheet and laser-cut metal branches.
- Materials: wood, foam, resin, paper, clay; perspex with cling film for water, cotton wool for cloud, fog and smoke, cellophane for fire; real machine parts for Trash Island; popcorn for Coraline's blossoms. Wood moves with lamp heat (micro-stutters, Pinocchio).
- Practical lights: micro ellipsoidals with gobos, LED candles on thin wires with programmed flicker, 12 V bulbs; lights placed so rig shadows miss the puppets.
- Props: Isle of Dogs graphics miniaturised, up to 25 iterations per approval, seven people on one evidence board. Memoir ~5,000-7,000 props. Aardman: props give "richness".
- What reads as handmade: visible process (Aardman thumbiness; Elliot's brush strokes and lumps); intentional flaws (Wildwood blemishes, Pinocchio's leaning trees and buildings, mis-spaced dog tags, Missing Link's speckled ice to show scale). Two schools: Aardman and Elliot show the hand; Laika wants viewers to forget they're puppets. Pick one in the bible.

## 2. World building
- Wallace & Gromit: northern English two-up-two-down with pulleys and trap doors for the morning routine; Ealing comedy and Norman Wisdom influences; writers sketch gags so the art department can build them in; pun-filled signage; Lord wants sets with "history".
- Kubo: Saito woodblock prints and origami; shared mark-making via stencils and paint; printed-ink wood grain on every surface.
- Missing Link: Victorian 1890-1910 from antique postcards; ~3 main colours per location plus a contrast object; colour script keeps neighbouring locations different; muted environments so characters read; sets echo character shapes (Link avocado, Lionel tubes).
- Wildwood: Portland as a "predesigned model railway"; thousands of reference photos; "a cup in Wildwood feels different from a cup in Portland."
- Pinocchio: limited palette, warm reds, oranges and purples used sparingly, blue for hope; one design vocabulary for cups, trees, even water.
- Memoir: Grace's bedroom stood 16 weeks, filling with snail memorabilia then emptying: dressing is the story arc. Clothes painted or sculpted, no fabric. Cages and kintsugi as motifs.
- Isle of Dogs: 1963 Japan projected 20 years forward; Metabolist architecture; Old Town pre-war; mansion pushed vertical so it looms; Trash Island colour-coded by waste type; two Japanese designers did all text; 240 sets across 44 stages.
- Shape language: Coraline's real world tilted and claustrophobic, Other World right-angled and deep; Isle of Dogs verticals loom.
- Coraline's handbooks fixed the look of every item so separate designers stayed consistent.

## 3. Doing it in code (Blender 5.2 LTS)
- API: 5.0 added Bundles, Closures, SDF/grid nodes; removed "Use Nodes" for materials and worlds. 5.1 shader Raycast node. 5.2: Mesh Bevel node, Lists, reusable node-group Functions, Thin Wall in Principled BSDF (paper, leaves), Cycles texture cache, experimental cloth/hair node physics. Breaking: 5.2 GN modifier inputs moved to `modifier.properties.inputs`; Compare and Random Value socket identifiers changed; compositor tree at `scene.compositing_node_group` [U]. Pin the version, add a smoke test.
- Scripting: `node_groups.new(..., "GeometryNodeTree")`, `interface.new_socket`, `nodes.new("GeometryNodeInstanceOnPoints")`, `links.new`, NODES modifier; realize instances before output.
- Kit: ~20 parametric GN modules (wall, window, door, roof, chimney, corner, step) on a puppet-scale grid; Curve to Points, Instance on Points, Pick Instance; per-instance lean and thickness jitter; Mesh Bevel with variable radius and visible sheet thickness for card and MDF edges.
- Dressing in three tiers: hero props placed from story beats; set dressing rule-based; filler scattered with exclusion zones along puppet paths (Distribute Points on Faces, Raycast to rest). Python prop library with 3 variants per prop.
- Weathering: edge wear from Bevel and AO masks, dust on up-facing normals; brush-sized and coarse, not photographic [U].
- Materials at puppet scale: felt as instanced curve fibres (commercial GN felt generators exist); Laika makes its own fabrics for scale and hand-knits with hair-thin needles; paint as directional streaks with fixed brush width and visible overlaps; wood grain scaled to the model. Calibrate fibre, weave and brush sizes from photos of real models [U].
- Sky and haze: curved cyc with painted procedural sky and cotton-batting clouds; haze as bounded volume cards per depth layer, not global fog.
- Camera: Were-Rabbit shot at T22 with an 18 mm lens and exposures up to 4 s (deep focus plus focus pulls). A PLoS ONE paper finds blur-gradient orientation relative to the ground plane is the key miniature cue. Set lens and aperture policy in the bible.
- Cheating per shot: shot file holds camera, frustum cull (keep what the camera sees plus margin), wild-wall displacements, proxy backdrops; tag each shot bucket A, B or C.
- Continuity: `dress_manifest.json` per shot (prop id, variant, parent, transform, state, seed), a reference still from the shot camera, and a diff against the previous shot. Mirrors continuity photos and strike packs. In git.
- Free assets: Poly Haven CC0 (live API needs "Powered by Poly Haven" credit; scraping banned); ambientCG CC0; Kenney CC0; Quaternius custom license (commercial OK, no redistribution); Blender Studio Wing It CC BY 4.0 (credit, no logos); Poly Pizza often CC-BY; Infinigen BSD-3; Blender 5.2 online asset library licenses unstated [U]. CC0 photo scans read as "real", so repaint or flatten them.

## 4. Agent scene-generation research
| System | Planning | Limits |
|---|---|---|
| Infinigen Indoors (CVPR 2024) | Python constraint DSL (~15 lines/room), simulated annealing, floorplan grammar | Photoreal focus; pins Python 3.11 (Blender 5.x support [U]) |
| Holodeck | LLM writes floor plan and picks from 10 relations; DFS solver; CLIP retrieval from Objaverse | Weak on complex layouts |
| LayoutGPT | CSS-style layouts via in-context examples | Indoor counts and relations |
| SceneCraft | Scene graph, 0-1 scoring per relation, Blender script, GPT-4V critique, library learning | First tries often wrong |
| 3D-GPT | Agents set Infinigen parameters | Weak on curves and shading |
| LL3M (2025) | Planner, retriever, coder, critic, verifier write Blender Python; docs RAG | ~10 min to create; misses spatial artifacts; closest template for Claude Code |
| SceneSmith (2026) | Staged architecture, furniture, small objects; 96% physically stable | Uses text-to-3D |
| PhyScensis (2026) | LLM writes spatial and physical predicates; solvers verify | Genesis engine, not Blender |
| SimWorlds (2026) | Planner, coder, reviewer with a deterministic verifier and runtime-state inspection | Verifier pattern worth copying |
Shared pattern: LLM chooses relations and parameters, a solver places, a critic checks. None enforce puppet scale or handmade style. To push toward handmade: our own kit and materials; constraints for puppet-path clearance and the scale table; a deterministic handmade pass after layout (lean, gaps, glue seams, hand-painted variation); a VLM critic against the tells list.

## 5. Reviewing sets and worlds
Production designer checks: coverage (nothing visible past set edges), scale vs puppet, palette and colour script, silhouette against characters, shape language, light positions, dressing that tells story, period and cultural accuracy (Lowry hired a sensitivity consultant).
Automated checks (thresholds [U]):
- Scale: bounding boxes vs the puppet reference table (doors, tables, handles in head and body terms).
- Palette: render shot camera, k-means in Lab, dE vs zone palette; cap off-palette area; check accent share.
- Prop density: props per visible floor area; focal zone denser than blurred background.
- Camera coverage: ray grid per shot, flag rays exiting the built set; stray wall tops, floor edges, underside; camera and light collisions.
- Continuity: diff manifests between adjacent shots; flag unexplained prop moves; SSIM on static regions.
- Originality: private reference set of existing films' frames for comparison only; CLIP/DINOv2/DreamSim similarity plus palette and layout descriptors; text pass on names and signage; human makes the final call.
- Layout soundness: settle and collision tests.

## (a) World bible template
0 Premise and tone. 1 Rules (possible, forbidden, physics). 2 Geography (zone map, palette per zone). 3 History (timeline mapped to wear and age). 4 Culture (customs, class, valued objects). 5 Era and technology. 6 Architecture (structural logic, roof/window/door grammar, shape language, module grid, intended lean and tolerance). 7 Signage and typography (languages, hand-lettering, puns, sign materials). 8 Palette and colour script (global palette, ~3 colours plus one accent per location, neighbours differ, forbidden colours). 9 Materials (card, MDF, felt, clay, paint; brush rules; wear rules). 10 Scale (puppet heights, set scale, prop-to-head rule, texture-scale table). 11 Light and atmosphere. 12 Dressing language (character object signatures, gag budget). 13 Camera (lens, aperture, DOF policy). 14 Originality (do-not-resemble list, license ledger). 15 Open questions and change log.

## (b) Set pipeline
0 Bible (markdown plus `palette.yml`, `scale.yml`, `materials.yml`); sign-off director and production designer.
1 Shot and set brief (JSON per set with shots, camera paths, buckets A/B/C); production designer.
2 Greybox (script produces .blend plus plan, elevation, shot-camera stills; checks scale, coverage, access, early palette); production designer.
3 Kit build (parametric GN modules, `kit.json` registry; unit tests for grid fit, manifold meshes, seeded determinism; license ledger).
4 Assembly (constraint layout with puppet clearance, then shot cheats; `set.blend` plus `dress_manifest.json`; collisions, clearance, soundness).
5 Dressing and handmade pass (tiered scatter, graphic props, tolerance and wear; density, scale).
6 Look-dev (materials from the scale table, sky, haze cards, practicals; EEVEE tests at shot cameras; VLM critic plus palette, coverage and tells checks); production designer and DP.
7 Shot lock (per-shot manifest, reference still, diff, git tag); continuity.
8 Originality and licenses (similarity report plus ledger); producer, human.

## (c) Top 10 tells that a miniature set reads as CG
1. Razor-straight uniform edges: variable bevels, edge wobble, visible card thickness, warped panels.
2. Wrong texture scale or tiling: scale to the model, per-instance UV offsets, printed or painted grain (Kubo), speckle to show scale (Missing Link).
3. Uniform cleanliness or random-noise wear: story-driven, brush-sized wear and top-face dust.
4. Perfect symmetry and square alignment: lean, droop, gaps (Pinocchio); start at +/-1-2 deg [U].
5. Wrong DOF cue: physical camera at puppet scale with blur gradient aligned to the ground plane, or deep focus with pulls.
6. Soft global light, no practicals: small hard lamps, gobos, cucolorises, rig-shadow avoidance.
7. Real-looking sky and smooth haze: painted cyc, cotton-batting clouds, layered haze cards.
8. Natural-looking sim water, fire, smoke: cling-film water, cellophane fire, cotton-wool smoke, or restrained sims tuned to match.
9. Smooth boil-free motion: twos, phase offsets, small jitter, boil on clay surfaces only; keep light flicker out.
10. Even prop density and copy-paste assets: tiered props, variants, props scaled to head and body, imperfect hand-lettered graphics, character-specific objects.

## Sources
https://www.motionpictures.org/2018/03/production-designer-paul-harrod-building-wes-andersons-isle-dogs/
https://www.dezeen.com/2018/03/28/wes-anderson-isle-of-dogs-sets-metabolist-architecture-paul-harrod-interview/amp/
https://www.motionpictures.org/2018/04/graphic-designer-erica-dorn-sweats-the-details-for-wes-andersons-isle-of-dogs/
https://www.cartoonbrew.com/how-to/how-they-did-it-missing-link-production-designer-nelson-lowry-on-the-complexities-of-hybrid-production-184010.html
https://www.slashfilm.com/missing-link-set-visit-report
https://www.vectorworks.net/newsroom/how-laika-creates-the-foundation-for-their-films-with-vectorworks
https://thewrap.com/kubo-two-strings-biggest-stop-motion-animation
https://awn.com/vfxworld/explore-vfx-laika-s-kubo-and-two-strings
https://metropolismag.com/programs/behind-the-scenery/
https://www.creativeboom.com/insight/wildwood-art-director-matthew-maldonado-on-why-laika-still-builds-everything-by-hand-and-why-theyre-coming-to-londons-design-musuem/
https://www.joblo.com/wildwood-behind-the-scenes-tour/
https://www.pdxmonthly.com/arts-and-culture/2026/09/laika-film-wildwood
https://www.backstage.com/magazine/article/guillermo-del-toro-pinocchio-production-design-interview-75829/
https://vfxvoice.com/stop-motion-breathes-new-life-into-guillermo-del-toros-pinocchio/
https://www.dragonframe.com/blog/guillermo-del-toros-pinocchio/
https://vfxvoice.com/?p=13144738
https://www.rogerebert.com/interviews/living-forward-adam-elliot-on-memoir-of-a-snail
https://theasc.com/articles/wallace-gromit-vengeance-most-fowl
https://theasc.com/magazine/oct05/curse/page3.html
https://scriptmag.com/interviews-features/light-on-feet-of-clay-a-visit-with-nick-park-and-merlin-crossingham-of-wallace-gromit-vengeance-most-fowl
https://www.acmi.net.au/stories-and-ideas/inside-aardman/
https://awn.com/animationworld/aardman-50-inside-clay-felt-and-fingerprints
https://developer.blender.org/docs/release_notes/5.0/geometry_nodes/
https://developer.blender.org/docs/release_notes/5.2/python_api/
https://digitalproduction.com/2026/07/21/blender-5-2-lts-lands-with-node-physics/
https://blog.cg-wire.com/blender-scripting-geometry-nodes-2/
https://80.lv/articles/check-out-a-new-procedural-felt-generator-for-blender
https://doaj.org/article/0874e0d679dc4531b9051a740a30e70e
https://polyhaven.com/license
https://docs.ambientcg.com/license/
https://studio.blender.org/projects/wing-it/pages/licensing/
https://kenney.nl/support
https://quaternius.com/license.html
https://github.com/princeton-vl/infinigen
https://arxiv.org/html/2406.11824v1
https://arxiv.org/html/2312.09067v2
https://arxiv.org/abs/2305.15393
https://arxiv.org/html/2403.01248v1
https://arxiv.org/html/2310.12945v2
https://arxiv.org/html/2508.08228v1
https://arxiv.org/abs/2602.09153
https://ukstandards.org.uk/en/nos-finder/SKSPRP10/maintain-the-continuity-of-props-and-re-dress--sets-during-production
