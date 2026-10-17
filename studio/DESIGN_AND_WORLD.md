# Design and world building

Owner: the **Production Designer**, with the Look Development Supervisor (materials), the Character Designer, and the Set and World Designer. Sources: research/13 (sets and world), research/15 (material language), research/12 (character design flow), and `studio/CREATIVE_DIRECTION.md`.

## 1. Why this matters

Studios that make worlds feel intentional build them on a making process, not a look. Robin Robin chose needle felt and then used felt for fire, smoke and snow too. Kubo put woodblock grain on every surface, even raindrops. Pinocchio wrote "perfectly imperfect" as its test and rationed a slice of color for special moments. Coraline's handbooks had swatches for everything so separate teams stayed consistent. Every production here writes that rulebook before it designs anything.

## 2. The four layers (house rules from Chris)

Every production carries all four (`studio/CREATIVE_DIRECTION.md`):

| Layer | What the production must decide | Check |
|---|---|---|
| Palette: earth pigments only | 8 to 12 chips, each named for its pigment or dye; one accent with a frame budget | Palette check on renders (section 7) |
| Process: the maker's hand shows | Allowed marks (thumbprint, tool facet, stitch, brush stroke) and forbidden marks (mold line, print layer, perfect gloss) | Screen test and critic |
| World: made from one place | The place, and the closed list of materials that would exist there | Material allocation matrix |
| Motif: one fiber runs through it | Which fiber, where it appears in each scene, and where it's prominent | Motif log per shot |

Optional, pending Chris: a studio signature fiber that appears in every film.

How to keep the thread visible without hammering it (research/15, section 7): carry it through traces of making rather than objects; repeat it at three scales (silhouette, material, mark); keep one constant anchor location. The motif fiber appears in every scene (Chris's rule), but not in every frame: prominent in roughly a third of frames [U] and quiet elsewhere. Deliberate breaks belong to the palette accent, not the motif.

## 3. The world bible

Each production writes `bible/world.md` before Design Lock. Template (research/13 a merged with research/15 a):

0. **Meta:** title, version, owner, date, change log.
1. **Thread:** one sentence on who made this world, from what, by what process. The rule in 12 words or fewer.
2. **Premise and tone.**
3. **Rules:** what's possible, what's forbidden, the physics.
4. **Geography:** a zone map; each zone gets its own palette slice.
5. **History:** a timeline that maps to wear and age on objects.
6. **Culture:** customs, class, the objects people value.
7. **Era and technology:** what exists, what's obsolete.
8. **Architecture:** structural logic, roof, window and door grammar, shape language, module grid, intended lean and tolerance.
9. **Signage and typography:** hand-lettering style, sign materials, puns budget.
10. **Palette and color script:** chips with pigment or dye source, sRGB and linear values; a 5-step value ladder; the accent and its budget; banned hues; about 3 main colors plus one accent per location, neighboring locations different; one color per story beat.
11. **Material families:** one block each: origin in the world, scale rule in millimetres at puppet scale, surface (roughness, sheen, translucency), fuzz and wear, texture source (CC0 ID or later an owned scan), Blender recipe name, approved uses, never uses.
12. **Allocation matrix:** puppets, costumes, sets, props, effects and titles against each material family (primary, secondary, never).
13. **Motif:** what, where, frequency cap, scheduled breaks.
14. **Scale:** puppet heights, set scale, the prop-to-head rule, minimum visible stitch, grain scale.
15. **Light and camera:** key softness, backlight rules, depth-of-field policy.
16. **Dressing language:** each character's signature objects; gag budget.
17. **Never list.**
18. **Originality:** a do-not-resemble list and the license ledger.
19. **Open questions.**

Research/15 section b has three worked examples (Hearth-Fired, Tidewrack, Season Dye-Bath) that show how one idea ties clay, fibers and earthy materials together. They are illustrations, not house style.

### Palette rules
- Plan value before hue. Every palette passes a greyscale check with 5 to 7 distinct steps.
- Vary temperature inside the earths (cool raw umber against warm burnt sienna) so the palette doesn't go muddy.
- Undyed fleece, linen and jute are the palette's "paper."
- Color is punctuation. The accent stays inside its frame budget (for example under 3%) and is reserved for story moments, the way Pinocchio reserved its warm reds and purples.
- Let light supply glow: felt, paper, leaves and wax glow when backlit.
- Use texture contrast (smooth slip, hairy wool, rough bark) to keep one hue family from going flat.

## 4. Characters

Design flow (research/12, section 2):
1. **Silhouette sheet:** SVG silhouettes from the shape library, many options; Laika picked Boxtrolls' villain from black silhouettes. The Director picks directions.
2. **Grey maquette:** the chosen design built in Blender as untextured clay forms at true scale (FABRICATION.md), rendered as a turnaround. Like Laika's digital sculpt, the Director approves the maquette before anything else is built.
3. **Model sheet:** turnaround (front, three-quarter, side, back), 5 to 7 expressions, mouth chart (Rhubarb A to H plus X), hands, a scale lineup against other characters and props, material callouts (where prints and seams live), and the character bible: wants, fears, movement vocabulary (MOTION.md section 2).

Designing for clay (and for code):
- Chunky forms and simple silhouettes; big readable eyes and brows; brow-led acting works (Gromit has no mouth).
- Vary finger lengths (equal fingers read as rakes); give feet some size.
- Avoid detail that won't hold: busy patterns, text on costumes, thin limbs, tiny jewelry.
- Every costume material comes from the world's material families. The Costume and Textile Artist builds costumes at puppet scale (FABRICATION.md).

## 5. Sets

Principles from real art departments (research/13, section 1):
- **Scale comes from the puppet first.** Props scale to the head or body on cartoon proportions. Fix puppet sizes early; Isle of Dogs used three puppet scales for close, medium and distant shots.
- **Build only what the camera sees.** Each shot gets a frustum cull and wild walls. Shots are sorted into buckets, an idea taken from Missing Link's previs (research/13); our labels are A (full build), B (build plus painted backdrop), C (build plus set extension).
- **Layer depth:** foreground, midground, painted background; forced perspective with smaller-scale buildings behind.
- **Painted cyc skies** with cotton-batting clouds. Haze as bounded cards per depth layer.
- **Lived-in dressing tells story:** Memoir of a Snail's bedroom fills and empties with the story. Hero props placed from story beats, set dressing by rule, filler scattered with clear paths for the puppets.
- **Intentional imperfection:** walls and trees lean (Pinocchio's "perfectly imperfect"), panels gap, edges wobble, hand-lettered signs are slightly off.
- **Practical lights** built into the set where the story allows.

## 6. Effects

Effects get a material like everything else, and that material comes from the world (research/15, 13):
- Fire: felt (Robin Robin), wool tufts swapped per pose (The House), cellophane (Memoir of a Snail).
- Smoke, fog, cloud: cotton wool, cottonwood fluff.
- Water: cling film over perspex.
- Snow: felt, paper, popcorn-style blossoms.
Real studios also use CG for water and fire (Vengeance Most Fowl left water and fog to VFX). Here, a CG effect is allowed only when it is tuned to match the world's handmade material and the Director approves it at the screen test.

## 7. Review checks

**Design Lock checklist:** world bible complete; every character has an approved maquette and model sheet; every set has a design and a bucket; palette passes the greyscale and accent checks; every material family passes the screen test (LOOK_DEV.md section 7); originality check passed.

**Automated checks on renders** (thresholds [U], calibrate on approved frames):
- Palette: k-means in Lab on the shot render; each dominant color within ΔE of a palette chip; off-palette area capped; accent share within budget.
- Scale: bounding boxes of doors, tables, handles and props against the puppet scale table.
- Coverage: rays from the shot camera never leave the built set (no wall tops, floor edges or set undersides in frame).
- Prop density: denser in the focal zone than in the blurred background.
- Motif: logged per shot against its cap and scheduled breaks.

**Originality:** before Design Lock, every character, set and title is compared against a private do-not-resemble reference set (existing films' frames, kept on Chris's machine, used only for this comparison, embeddings computed locally, never uploaded), with embedding similarity plus palette and layout descriptors, and a text pass on names and signage. Chris checks with counsel before assembling that set. A human makes the final call. Agent and skill text that drives making (style rules, recipes, build instructions) cites research file numbers, never real studio, film or character names.
