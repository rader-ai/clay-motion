# Fabrication: building characters, sets and props in code

Owner: the **Head of Fabrication**, with Fabricators. Sources: research/09 (code-built characters), research/13 (sets), research/08 (rig), research/15 (materials). Nothing here uses generative image or video services. Values marked [U] are starting points.

## 1. Principle

Real puppets are kits of parts over an armature: clay, silicone, wool and fabric on a skeleton. We build the same way, in code, so every character is a set of parts on the standard rig (MOTION.md section 4.1), every build is reproducible from a seed, and nothing drifts between shots because every shot uses the same model.

## 2. Building a character

From a `puppet.json` spec (proportions, parts, materials, seeds). Recipe (research/09, section a):
1. **Armature first:** the standard ~25-bone rig scaled to the character's proportions.
2. **Bulk with lumps:** capsules and ellipsoids along each bone, the way a sculptor bulks out clay. Per-part scale varies plus or minus 3 to 8% and rotation 2 to 4 degrees. Left and right are never mirrors.
3. **Join like clay:** smooth-union where parts meet (the sculptor's pinch), with a visible seam crease left on at least one joint. Built as SDF fields (Blender 5.x SDF grid nodes, or fogleman/sdf outside Blender, MIT).
4. **Soften and shape:** SDF mean or median smoothing, offset for bulk, fillet; two scales of low-amplitude noise (part-size lumps, thumb-size softness).
5. **Mesh:** grid to mesh, then remesh to even topology.
6. **Hand marks:** dents and thumbprints as real displacement where hands would hold the clay (LOOK_DEV.md 2.1). Faces stay cleaner.
7. **Materials** from the world's material families via the screen-tested recipes.
8. **Replacement sets:** mouth set (A to H plus X) from one parametric lip model, each shape frozen with its own seed; brow and lid sets the same way.
9. **Costume and fibers** from the fiber recipe (LOOK_DEV.md 2.2), at puppet scale.
10. **Register the asset:** version, seeds, part list, scale, material families used, license rows for any textures.

Optional: open-weight image-to-3D (TRELLIS.2, MIT, about 24 GB VRAM on a cloud GPU) only for a blockout of an odd prop, and only from our own Blender render or a hand drawing. Procedural builds win for characters: separate parts for rigging, deterministic seeds, registered mouth sets, no baked lighting.

## 3. Building sets

From a set brief in JSON (shots, camera paths, buckets A/B/C). Pipeline (research/13, section b):
1. **Greybox:** a script builds plan, elevation and shot-camera stills at true scale. Checked for scale, camera coverage and early palette.
2. **Kit:** about 20 parametric Geometry Nodes modules (wall, window, door, roof, chimney, corner, step) on a puppet-scale grid, with per-instance lean and thickness jitter, and visible card or board thickness on edges. Registered in `kit.json` with unit tests (grid fit, manifold meshes, seeded determinism).
3. **Assembly:** layout by constraints (puppet path clearance, scale table), then per-shot cheats (wild walls, frustum cull, proxy backdrops).
4. **Dressing in three tiers:** hero props placed from story beats; set dressing by rule; filler scattered with exclusion zones along puppet paths, resting on surfaces by raycast. Every prop has at least 3 variants so copies never repeat.
5. **Handmade pass:** lean (start plus or minus 1 to 2 degrees [U]), gaps, glue seams, hand-painted variation, coarse brush-sized wear and dust on top faces, edges that wobble.
6. **Look-dev:** materials, painted sky, haze cards, practical lights, tested at shot cameras.
7. **Shot lock:** `dress_manifest.json` per shot (prop id, variant, parent, transform, state, seed), a reference still from the shot camera, and a diff against the previous shot. This is our version of continuity photos and the UK standard's change log.

## 4. Asset approval

Per asset (bible section 5): the Production Designer signs the surface, the Supervising Animator signs function, the Director signs the whole. Automated checks before anyone looks:
- **Reproducible:** rebuilding from the spec and seeds gives an identical mesh.
- **Scale:** matches the scale table.
- **Mesh health:** manifold, no stray geometry, parts parented to the right bones.
- **Rig function:** the 12 base poses compile with no interpenetration (motion QC).
- **Mouth set:** all shapes present, aligned to the shared socket, readable at shot distance.
- **Materials:** every material passed the screen test; texture license rows present.
- **Identity:** silhouettes and turnaround renders match the approved model sheet.
- **Originality:** passed the design originality check.

## 5. Tools policy
- Prefer our own code. Paid add-ons (Clay Doh, Rhubarb Lipsync NG, Fuzzy Master Pro) are optional references, never bundled in the plugin, and never required.
- Free assets only with a license row: Poly Haven, ambientCG and Kenney are CC0; Quaternius allows commercial use without redistribution; Blender Studio assets are CC BY with credit. Assets with unstated licenses are treated as all rights reserved.
- CC0 photo scans look photographic, so they get flattened or repainted before use.
