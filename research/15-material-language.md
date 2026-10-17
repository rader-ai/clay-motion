# Material language: real textures, fibers and earthy materials with one creative thread (research, Oct 17, 2026)

All numeric Blender and palette values are starting points to tune with test renders [U]. Blender manual details come from the raw main-branch manual (5.2 era).

## Bottom line
Intentional worlds are built on a making process, not a look. Robin Robin chose needle felt because it sculpts like plasticine and glows when backlit. Kubo treated Kiyoshi Saito's woodblock prints as its unifying design element. Pinocchio wrote "perfectly imperfect" as its test and rationed a slice of a Pantone guide. A material bible should state who made this world, from what, by which hand process, in which pigments, and which one motif recurs. For fibers, the costume designers' lesson is scale: real weave at puppet size looks like a toy.

## 1. Material language as art direction
- One process, pushed past the obvious: Robin Robin used felt for fire, smoke and snow too (shot multiplane), carved trees, textile leaves; boil kept minimal; detailed feathers pared back to bold shapes. The House (de Swaef chapter) covered everything in fabric and wool except eyes, wrapped wooden sets in cloth, made flames from wool tufts swapped per frame. Kubo put woodblock grain on sets, clothing, water, even raindrops.
- One origin story: Fantastic Mr. Fox used real fur, towelling grass, cotton-wool smoke, corduroy from Anderson's own suit, almost no blues or greens. Isle of Dogs zoned Trash Island by material (rust; white newspaper and appliances; black CRTs and batteries) off Hiroshige and Hokusai.
- One imperfection rule: Memoir of a Snail keeps lumps, brushstrokes, fingerprints; costumes sculpted and painted. Wallace & Gromit keep thumbprints. Wildwood: nothing store-bought.
- Rationed exceptions: Pinocchio reserves red-orange to purple for special moments; blue means hope; cups, glasses, trees, skies share one visual language. Coraline: muted real world, richer Other World.
- Written down: Selick's handbooks with swatches kept separate teams consistent ("nothing is random"). Laika screen-tests every wardrobe item and tests fabrics for dye, drape, durability, scale. Isle of Dogs fixed three puppet sizes early and scaled props to a character's most prominent body part. Titles: no sourced example [U]; make them by the same process.

## 2. Earth palettes
- Shared pigments create cohesion. Zorn's four (yellow ochre, vermilion, black, white) still mix browns, green-golds, neutrals, flesh.
- Behavior: raw umber cool and greenish, burnt umber warm; burnt sienna fairly transparent; raw sienna won't make greens with blue; yellow ochre opaque.
- Plant dyes: indigo dyes cotton, linen, hemp directly; madder, walnut, pomegranate suit wool and silk; iron darkens, alum brightens; berry and cabbage dyes fade.
- Undyed oatmeal, grey and brown fleece, tan linen and jute act as the "paper" of the palette [U].
- Avoiding mud: plan value before hue (check in greyscale, 5-7 steps [U]); vary temperature inside earths (cool raw umber against warm sienna); one thematic plus one accent colour, accent a small share of frame; let light supply glow (felt, paper and wax pass backlight); colour as punctuation (Mary and Max: sepia Melbourne, grey New York, occasional shocks of colour). Kubo's red silk deepened with burnt ochre and umber.
- Avoiding monotony: contrast texture (smooth slip, hairy wool, rough bark) inside one hue family; a colour script with one colour per story beat.

## 3. Fibers at puppet scale
Puppet 15-25 cm vs a ~170 cm person is ~1:7 to 1:11, so a 2-4 mm knitting yarn [U] becomes 0.2-0.5 mm. Coraline's gloves were knitted on needles as fine as hair; Boxtrolls avoided heavy textures and fabricated lace, fur, buttons; Kubo's silk had a weave scaled to an 11-inch body.

| Fiber | Reads as real because | Scale rule [U] |
|---|---|---|
| Needle-felt / roving | halo fuzz, light absorption, slight edge translucency, poke dimples | fuzz 0.5-2 mm; soft light |
| Felt sheet | cut edges, fine nap, no weave | edge fuzz only |
| Knit / yarn | 2-3 visible plies, uneven tension, halo | thread-gauge stitches; hero close-ups only |
| Linen | slubs, uneven threads, crisp creases, matte | hairline weave; vary thread thickness |
| Jute / hemp / burlap | coarse bundled fibers, open weave, long frayed ends | weave gaps ~0.3-0.6 mm |
| Cotton | even, matte, low fuzz | twill diagonal, small hems |
| Raffia / twine | flat strips, split ends; tight 2-ply | 0.3-1 mm |
| Embroidery thread | sheen changes with stitch direction | satin stitch gives anisotropy |
Fiber diameters: wool ~17-40 um, linen 8-32, jute 7-18. Felt frays when pushed; loose thread and stuffing need extra rigging (Lost and Found, Wabi Sabi Studios).

## 4. Rendering fibers in Blender 5.x
- Geometry: Cycles curves as Rounded Ribbons (fast), 3D Curves (accurate close up), Linear 3D Curves (faster on GPU, can differ CPU vs GPU). Blender ships hair node groups on guide curves (Interpolate Curves, Trim Hair Curves).
- Shaders: Principled Hair Chiang (Gaussian) and Huang (microfacet, elliptical cross-section via Aspect Ratio, needs curve normals from GN). Sheen BSDF Microfiber layered on a base; lower roughness looks fuzzier and darker.
- 5.x: 5.0 more accurate random-walk SSS, adaptive subdivision non-experimental, Normal Map uses undisplaced normals with displacement, Linear 3D Curves, Render Time pass, better OptiX denoising. 5.1 ~5-10% GPU speedup.
- Denoising: OIDN with Albedo plus Normal, Accurate prefilter, lower noise threshold for hair-like detail; clamp indirect, Filter Glossy ~1.0.
- Research: Cornell micron-resolution cloth work: a fiber-specific scattering model beat microflake; yarn geometry alone yields satin and velvet highlights; flyaway fibers are a distinct component. A 2026 TOG paper recovers fiber-level weave from one microscope image [U].
- Add-ons: Fuzzy Master (Blender 4.2-5.2, GPL, free tier, Pro $10), Felt Gen (license unstated), Woolly Tools, Knittr, Fabric-o-matic (licenses unstated). Treat unstated licenses as all rights reserved.

## 5. Other earthy materials (shading starts [U])
- Sourced tricks: popcorn blossoms and a baby-sock sweater (Coraline), cellophane fire and cottonwood smoke (Memoir), jade resin tiles with SSS (Kubo).
- Terracotta/bisque: matte, roughness 0.7-0.9, slight iron speckle, no coat; glaze only as an accent.
- Raw and carved wood: tool facets over grain; low roughness variation; darker end grain.
- Cork, bark: macro bump with deep crevices; light SSS on cork.
- Stone, pebbles: low-frequency colour drift plus fine grain; dust in crevices.
- Moss, lichen, leaves, seeds: fuzz curves, thin translucency, curl, edge browning; backlight them.
- Beeswax: strong subsurface, warm, soft highlights.
- Handmade paper: visible fibers, translucency, deckled edge.
- Rope: 3-strand laid twist, hairy halo.

## 6. Owned texture library (later) and CC0 coverage (now)
- Cross-polarize: polarizing film on every light after diffusers; rotate the lens polarizer until glare vanishes. Poly Haven workflow: cross-polarized flash, colour chart in frame, raw to 16-bit TIFF, no sharpening or denoise, normals baked from a scan; roughness estimated.
- Normals without a scan: photometric stereo (Dabarti Capture, free) or Materialize (free, GPL, Windows). Scanning: Meshroom (MPL 2, CUDA), RealityScan (free under $1M revenue), COLMAP (BSD). Macro with a ruler in frame for exact scale [U].
- CC0 coverage today: Poly Haven 869 textures including 43 fabrics (hessian_230, hessian_380, rough_linen, wool_boucle, knitted_fleece, caban), 55 raw wood, 24 bark, 125 rock. ambientCG: 105 fabric results, 11 wool-tagged, rope 3 plus nets, cork 4, Clay001 and Ground026 mud, 10 paper and card, 3 glazed terracotta; no burlap or knit hits.
- Gaps to shoot later: felt, needle-felt, puppet-gauge knit, raffia, bisque terracotta, wax, handmade paper. Most CC0 fabric is human scale: use it for colour breakup and roughness, not as visible weave [U].

## 7. Keeping the thread visible, and reviewing
- Carry the thread through traces of making (grain, stitch, thumbprint), not logos. Kubo's grain works because it's a texture, not an object. Repeat it at three scales: silhouette, material, mark.
- Cap the motif (e.g., visible in about a third of frames [U]) and schedule one deliberate break per act (Pinocchio, Coraline reserve colour).
- Keep one constant anchor (The House's hall and staircase).
- Review: render every new material on a standard chart scene (same lights, camera, grey card, hero puppet swatch), score against the bible. Mirrors Laika's on-camera screen test.

## (a) Material bible template
0. Meta: project, version, owner, date, change log.
1. Thread: one sentence on who made this world, from what, by what process. The rule in 12 words.
2. Making process: in-world tools, allowed marks (thumbprint, tool facet, stitch), forbidden marks (mold line, 3D-print layer, perfect gloss).
3. Palette: 8-12 chips (name, source pigment or dye, sRGB hex, linear RGB); 5-step value ladder; accent budget (hue, max % of frame); banned hues; colour script by sequence.
4. Material families, one block each: name; origin; scale rule (mm at puppet scale); surface (roughness range, sheen, translucency); fuzz and wear spec; capture source (own scan ID or CC0 ID); Blender recipe name; approved uses; never uses; reference photos.
5. Allocation matrix: puppets, costumes, sets, props, FX, titles against families (primary / secondary / never).
6. Motif: what, where, frequency cap, scheduled breaks.
7. Scale: puppet heights, minimum visible stitch, grain scale.
8. Light and camera: key softness, mandatory backlight, DOF range.
9. Never list.
10. Review checklist (pass / pass with note / reject): origin, process, palette, scale, motif, neighbour test, greyscale value, never list.
11. Exceptions log and asset register (ID, status, reviewer, date).

## (b) Three example concepts
A. Hearth-Fired: everything in this village passed through the same fire.
- Palette [U]: bisque #D9B99B, terracotta #B5573A, ash #8E8A82, soot #2B2623, walnut-dyed wool #5A3E2B; accent ember #E8742C (under 3% of frame).
- Materials: unglazed terracotta and slip-trailed clay, walnut- and madder-dyed wool, undyed linen, charred wood, ash and charcoal dust, cork.
- Rule: every surface carries one trace of heat (scorch, soot kiss, slip drip). Motif: the slip line.
- Never: plastic gloss, blues and greens, polished metal, sharp-cut edges.

B. Tidewrack: nothing was made, everything was found and lashed together.
- Palette [U]: chalk #E6E0D2, driftwood grey #9A9588, sand ochre #C9A66B, rope tan #B38F5B, rust #8A4B2C; accent deep indigo #243A5E.
- Materials: river clay pinch pots, hemp and jute cordage, raffia, unravelled wool, bleached driftwood, pebbles, rough linen.
- Rule: every joint is bound, knotted or lashed; no glue or nails visible. Motif: the knot.
- Never: new plastic, clean cuts, saturated hues, screws.

C. Season Dye-Bath: every colour comes from one plant or soil within a day's walk.
- Palette [U]: oatmeal #CDBFA5, madder #A8472F, weld #D2A53A, walnut #5C4332, indigo #2F4A73; accent terre verte #7E8F6A.
- Materials: undyed and plant-dyed wool, linen and cotton, clay slip coloured with the same earths as the dyes, bark, beeswax, handmade paper.
- Rule: the dye that colours the wool also colours the clay slip; mends are visible running stitches. Motif: the mend.
- Never: neon, pure black or white (use iron-black and chalk), glossy surfaces.

## (c) Blender fiber recipe (starting values [U])
Scene: unit scale 1 m, puppet 0.2 m, camera 50-100 mm, strong soft key plus backlight.
1. Base: Principled BSDF roughness 0.85-0.95, Sheen weight 0.4, sheen roughness 0.5, tint lighter than base; Subsurface 0.1, radius ~0.5 mm for felt; per-yarn value variation 5-8% from noise.
2. Weave or knit: tile at target mm pitch with bump or normal; displacement only for close shots.
3. Halo fuzz (GN): 200-500 curves per cm2, length 0.5-2 mm, 4-5 points, radius 0.03 mm (3-5x physical so it survives denoise), taper, noise, slight curl; mask by weight map. A Rookies felt tutorial used two hair systems (many short curly strands, fewer fuzzy strays), 1 mm, 5 segments, Hair Info colour ramp, backlight, 2048 samples.
4. Stray fibers: 1-3% of fuzz count, 3-10 mm, random outward direction.
5. Fuzz shader: Principled Hair Chiang, Direct Coloring from base lightened 10-20%, roughness 0.4, radial roughness 0.5, IOR 1.55, random colour 0.15, random roughness 0.2.
6. Edge fray: curves from boundary edges, 1-4 mm. Pilling: flattened blobs 0.3-0.8 mm radius, 20-60 per cm2 on wear zones.
7. Plies: Curve to Mesh with 2-3 twisted ply helices for hero knits; bake to normal for wides.
8. Render: Cycles 512-1024 samples, noise threshold 0.005, min 64; OIDN Albedo plus Normal, Accurate; indirect clamp 5-10; Filter Glossy 1.0; bounces total 8, diffuse 4, glossy 2; 3D Curves for hero, Rounded Ribbons for wides. If denoise erases stray fibers, render fuzz on a separate view layer and composite.
9. Stop-motion feel: re-seed fuzz per pose (not per frame) with 1-3% jitter; Robin Robin kept boil minimal.

## Sources
https://www.cartoonbrew.com/interviews/the-directors-of-robin-robin-explain-how-they-broke-with-aardmans-house-style-209457.html
https://www.televisual.com/news/behind-the-scenes-aardmans-robin-robin/
https://www.dragonframe.com/blog/robin-robin-by-aardman/
https://www.cartoonbrew.com/stop-motion/styles-in-animation-felt-stop-motion-215313.html
https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx
https://www.motionpictures.org/2017/02/oscar-watch-kubo-costume-designer-infuses-clothes-ancient-japanese-tradition/
https://www.backstage.com/magazine/article/guillermo-del-toro-pinocchio-production-design-interview-75829/
https://vfxvoice.com/stop-motion-breathes-new-life-into-guillermo-del-toros-pinocchio/
https://editorial.rottentomatoes.com/article/wes-anderson-talks-fantastic-mr-fox-rt-interview/
https://www.motionpictures.org/2018/03/production-designer-paul-harrod-building-wes-andersons-isle-dogs/
https://www.core77.com/posts/75943/Behind-the-Scenes-The-Tons-of-Craftwork-That-Went-Into-Wes-Andersons-Isle-of-Dogs
https://eyeondesign.aiga.org/behind-the-scenes-of-the-house-netflixs-new-ode-to-stop-motion-animation/
https://www.dragonframe.com/blog/netflixs-the-house-by-nexus-studios/
https://www.dragonframe.com/blog/lost-found-wabi-sabi-studios/
https://fidmmuseum.org/learn/articles/interview-coraline-costume-designer-deborah-cook
https://www.pdxmonthly.com/articles/how-laika-s-costume-designer-dresses-tiny-puppets-for-the-big-screen
https://www.naturalpigments.com/new-zorn-palette.html
https://www.janeblundellart.com/earth-colours.html
https://kaliko.co/blog/plant-dyeing-directory.html
https://peachpit.com/articles/article.aspx?p=2461896
https://cameo.mfa.org/wiki/Natural_fiber
https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/shader_nodes/shader/hair_principled.rst
https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/shader_nodes/shader/sheen.rst
https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/render/cycles/render_settings/hair.rst
https://studio.blender.org/blog/procedural-hair-nodes
https://research.cs.cornell.edu/ctcloth
https://www.therookies.co/blog/education/creating-a-3d-felt-character-with-blender
https://superhivemarket.com/products/fuzzy-master-realistic-felt-effects/docs
https://blog.polyhaven.com/photoscanned-texture-creation-process/
https://dabarti.gumroad.com/l/Dabart_Capture/friday
https://www.realityscan.com/
https://api.polyhaven.com/categories/textures
https://polyhaven.com/license
https://docs.ambientcg.com/license/
