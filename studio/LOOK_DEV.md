# Look development: materials, light, lens, color and post

Owners: the **Look Development Supervisor** owns materials and the screen test. The **Director of Photography** owns camera and light. The **VFX Supervisor** owns the post chain. Sources: research/10 (clay shading), research/11 (camera, light, color), research/15 (material language), research/13 (set tells). Values marked [U] are starting points to tune by the procedures in sections 7 and 8, never facts.

## 1. The look in one paragraph

Every frame should read as a photograph of a small, handmade world: clay that holds the marks of the hands that shaped it, real fibers and earthy materials from one place, colored only with earth pigments, lit by small hard lamps at true miniature distances, in deep focus, with no motion blur, and a surface that shifts slightly each time a pose changes and never on a held frame. Creative direction lives in `studio/CREATIVE_DIRECTION.md`; this file is how it gets rendered.

## 2. Materials

### 2.1 Clay shader v1
Built in code, in true metres (a 20 cm puppet is 0.2 units). Node chain (research/10, section a):
1. **Coordinates:** object-space texture coordinates, object scale applied. Feature sizes in metres: crumb 0.05 to 0.3 mm, marbling streaks 3 to 8 mm.
2. **Seeds:** `part_seed` (per part, from a hash of project and part name) drives large-scale variation. `pose_seed` (from the pose index, see 2.4) drives micro detail.
3. **Color:** base pigment color from the production palette; per-part jitter (hue plus or minus 0.02, saturation 0.05, value 0.04); marbling to a second, related color (hue shift 3 to 6%, factor 0.15 to 0.35) where colors were blended by hand; cavity grime (value times 0.8) in crevices and handled areas.
4. **Principled BSDF:** metallic 0; roughness 0.48 plus or minus 0.06 from 2 mm noise, minus 0.12 where handled (handling polishes clay), plus 0.05 on ridges; IOR 1.47 [U]; subsurface Random Walk. **Subsurface weight and distance are unsettled:** research/09 suggests weight 0.05 to 0.15, research/10 suggests 0.25 to 0.45 at 0.3 to 0.8 mm. Start at weight 0.25 and scale 0.0004, and settle it with the screen test (section 7). Sheen weight 0.15, roughness 0.5 (raise to about 0.35 weight for a powdered-sugar matte, which Aardman used on Dawn of the Nugget). Coat 0, except 0.06 on handled patches.
5. **Relief at three scales:** meso dents 3 to 15 mm (true displacement, about 0.4 mm deep), tool marks 0.5 to 3 mm, crumb 0.05 to 0.3 mm (bump). Material displacement set to "Displacement and Bump".
6. **Fingerprints:** flow-field ridges at 0.41 to 0.46 mm spacing (real human averages), partial and overlapping, 1 to 3 per touched part, placed where hands would hold the clay (pinch points, neck, waist, sides and top of the head, shoulders, backs of limbs; faces kept cleaner). Generated as 16-bit height stamps (about 13 texels per mm). **Fade ridge strength by pixel footprint:** at HD a ridge period can be under 2 pixels and will shimmer, so ridges fade toward zero as a pixel approaches about 0.11 mm on the puppet.
7. **Seams and tool marks:** 0.1 to 0.3 mm seam lines with a raised lip where parts join; loop-tool grooves, stylus dimples with raised rims, knife cuts with a smeared lip.

The ten CG tells this shader must avoid (research/10 b): too-clean surfaces, fake fingerprints (rings, tiling, wrong spacing), waxy glow, a single sharp highlight, perfect symmetry and bevels, flat color, missing or global boil, wrong scale cues, a sterile surface with no lint or dust, and render artifacts (denoiser smoothing, ridge aliasing, clipped highlights, motion blur).

### 2.2 Fibers and textiles
Puppets are 1:7 to 1:11 of human scale, so a 2 to 4 mm yarn becomes 0.2 to 0.5 mm. Real weave at full size reads as a toy; Laika knits on hair-thin needles for this reason. Recipe (research/15, section c; values [U]):
- Base: Principled BSDF roughness 0.85 to 0.95, sheen 0.4 (roughness 0.5, tint lighter than base), subsurface 0.1 with about 0.5 mm radius for felt, per-yarn value variation 5 to 8%.
- Weave or knit: tile at the target pitch in millimetres with bump; displacement only on close shots.
- Halo fuzz (Geometry Nodes curves): 200 to 500 per square cm, 0.5 to 2 mm long, 4 to 5 points, radius 0.03 mm (3 to 5 times physical so it survives denoising), tapered, slightly curled. Stray fibers: 1 to 3% of the count, 3 to 10 mm. Edge fray 1 to 4 mm. Pilling 0.3 to 0.8 mm blobs on wear zones.
- Fuzz shader: Principled Hair (Chiang), base color lightened 10 to 20%, roughness 0.4, radial roughness 0.5, IOR 1.55.
- Hero knits get 2 to 3 twisted plies as real geometry; wides get a baked normal.
- Fuzz re-seeds per pose, never per frame, at 1 to 3% (Robin Robin kept boil minimal).
- If the denoiser erases stray fibers, render fuzz on its own view layer and composite.

### 2.3 Other materials (starting points [U])
| Material | Shading start | Reads as real because |
|---|---|---|
| Silicone (bodies) | Subsurface 0.6 to 0.8, 1 to 3 mm, roughness 0.3 to 0.45, dust or sheen layer | Soft translucency, fingerprints cast in |
| Eyes (resin or bead) | IOR 1.5 to 1.55, roughness 0.02 to 0.05, domed, pupil pinhole | Strong catchlight from the key |
| Matte paint | Roughness 0.5 to 0.7, directional brush streaks, pooling in crevices | Visible strokes, fixed brush width |
| Felt and wool | See 2.2 | Halo, edge translucency, poke dimples |
| Linen | Hairline weave, slubs, crisp creases, matte | Uneven threads |
| Jute, hemp, burlap | Coarse bundles, open weave gaps 0.3 to 0.6 mm, long frayed ends | Fray and gaps |
| Terracotta and bisque | Roughness 0.7 to 0.9, iron speckle, no coat | Dry matte, speckle |
| Raw and carved wood | Tool facets over grain scaled to the model, darker end grain | Facets, not perfect planes |
| Cork and bark | Deep macro crevices, light subsurface on cork | Crevice shadow |
| Stone and pebbles | Low-frequency color drift, fine grain, crevice dust | Variation |
| Moss, lichen, leaves, seeds | Fuzz curves, thin translucency, curl, browned edges; backlight them | Glow when backlit |
| Beeswax | Strong subsurface, warm, soft highlights | Glow |
| Handmade paper and card | Visible fibers, translucency, deckled or cut edges with 0.2 to 0.5 mm thickness | Edges and fibers |
| Rope and twine | 3-strand laid twist, hairy halo | Twist and halo |

### 2.4 Boil
The surface changes when the puppet is touched, and only then (research/10, section 5):
- `pose_seed` comes from a hash of the quantized pose, never the frame number, so held frames are identical.
- Re-seed only the region that moved (mask from per-vertex motion between poses).
- Micro detail under about 3 mm re-seeds; meso detail (3 to 15 mm) stays 70 to 85% the same; silhouette wobble 0.1 to 0.3 mm [U].
- Hard switch, no crossfade. Draw from a pool of about 6 variants per region so it reads as one pair of hands.
- Robin Robin kept boil minimal; start low and raise it only if the Director asks.

### 2.5 Texture sources
CC0 only for now (Chris's decision). Poly Haven and ambientCG cover clay, wood, bark, rock and human-scale fabrics, but no plasticine, felt, needle-felt, puppet-gauge knit, raffia, bisque, wax or handmade paper. Use CC0 scans for color breakup and roughness, flattened so baked-in lighting doesn't show; build fine detail procedurally; never show human-scale weave at puppet scale. Every texture gets a row in the license ledger. A real material shoot can replace these later (research/15, section 6 has the capture method).

## 3. Camera and lens (DP)
- Sensor 36 mm wide, horizontal fit; lenses 25 to 50 mm (35 default); true-metre focus distance; 7 to 9 aperture blades; **motion blur off**.
- **Aperture by scale rule:** to match life-size depth of field at f/N on a 1:k miniature, use f/(N times k). That's why real clay films shoot around f/11 to f/16. Default f/11, f/16 for deep wides. Selective shallow focus only when motivated (a macro close-up), never as a tilt-shift gradient across the whole frame.
- **Focus breathing:** set the lens to f(1+m) and the f-stop to N(1+m), where m = f/(focus distance minus f). 35 mm at 35 cm becomes 38.9 mm. Verify with a bokeh test render [U].
- Lens character added in post, all subtle enough to notice only when switched off: mild vignette, sub-pixel chromatic aberration, about 1% distortion, a small diffraction blur at f/11 to f/16, Pro-Mist 1/8 equivalent at most.

## 4. Light (DP)
- Small hard sources at true distances: key spot about 1.5 to 2 cm across, 0.8 to 1.2 m away, 3200 K, spot size 25 to 35 degrees, blend 0.15 to 0.3. Fill a wide soft source about 2 stops under the key. Rim a small spot behind. Practical lamps in the set where the story allows.
- No sun lamps, no HDRI skies. Painted cyc backdrops lit like a stage.
- Flags, negative fill and gobos (cucoloris breakup, window patterns) as real objects or light-linked textures.
- Light groups per source so the DP can rebalance in compositing, the way Vengeance Most Fowl and Dawn of the Nugget shot separate exposures.
- Haze only where a beam is motivated, as bounded volume cards per depth layer, never global fog.
- Flicker: real productions fight it. Default none. If the Director asks for life, a per-pose gain of 0.3 to 0.8% at most [U], never per frame.
- Calibrate key power on a digital grey card so it reads 0.18; scale power with distance squared.

## 5. Color (DP and VFX Supervisor)
- Working space Linear Rec.709; view transform AgX, look none.
- **One show LUT per production,** built from the production palette and used everywhere: previews, dailies, finals (Isle of Dogs ran one LUT from set to final grade). Stored as OCIO config plus a baked 65-cube `.cube` for ffmpeg.
- White balance by source type (tungsten 3200 K, LED 5600 K); one WB gain per scene; desaturated gels.
- Color script per sequence in JSON (WB, fill hue, LUT strength, accent budget), read by Blender and ffmpeg.
- Palette compliance is checked on renders (DESIGN_AND_WORLD.md section 4).

## 6. Post chain (VFX Supervisor)
Order, in scene-linear: denoise, light-group gains, white balance, veiling glare (large bloom, 0.5 to 2%), diffusion glow, lens distortion and dispersion, vignette, diffraction blur, sensor noise, then view transform and LUT.
- **Sensor noise, not film grain:** signal-dependent noise in scene-linear (sigma = sqrt(a*x + b), starting a = 1/70000, b = (8/70000)^2 [U]), blurred about 0.6 pixels, chroma at 60% of luma. Done in numpy or OIIO.
- **Per pose, not per frame:** render each unique pose once with its own seed, then hold it for two frames with ffmpeg. Noise and any flicker therefore change only when the pose changes.
- **Never frame interpolation, never motion blur.**
- A tested ffmpeg chain for LUT, glow and vignette is in research/11, section a.

## 7. The screen test (Look Dev Supervisor)
Laika screen-tests every material on camera before approval. Ours is a fixed Blender scene:
- Same camera, lens and lights every time; a digital grey card, grey ball, chrome ball and ColorChecker; a hero puppet swatch; a 1, 2 and 3 mm backlit clay sheet; a fingerprint stamp; a millimetre ruler.
- Every new or changed material renders here before it can be used. It is scored against the material bible checklist (origin, making process, palette, scale, motif, neighbor test, greyscale value, never list) and against the approved baseline.
- When real reference photos exist (a later material shoot, or Chris's own clay), run the matching procedure in research/10 section c: recreate the photo setup, calibrate on the chart, then optimize base color, roughness, subsurface, sheen and bump with Optuna or CMA-ES against ΔE2000, histogram, power-spectrum and DISTS scores, and validate on a held-out light angle.

## 8. Look regression tests (Pipeline TD with Look Dev)
- A small set of fixed scenes (screen test, one character turnaround, one set corner, one fiber close-up) re-renders after every shader, light or post change.
- Each is compared with its approved baseline: ΔE on chart patches, high-frequency energy (catches denoiser smoothing), DISTS and LPIPS on crops as alarms. A change that moves an approved scene needs the Look Dev Supervisor's sign-off and a new baseline.

## 9. Render tiers
| Tier | Use | Settings |
|---|---|---|
| Board | Storyboards, layout | Workbench, outlines, Line Art ink |
| Pop-through | Key poses for animation review | EEVEE if it runs headless on the box, else Cycles 16 to 32 samples at 480p |
| Dailies | Finals for review | Cycles 256 samples, adaptive threshold 0.01, OIDN with albedo and normal |
| Final | Delivery | Cycles 512 to 1024 samples on close-ups, adaptive threshold 0.005, OIDN Accurate prefilter; skip denoising or blend raw detail back on hero close-ups if fingerprints soften |
Render only unique poses; holds are duplicated in post, which halves render cost on twos.

## 10. Combined CG-tell checklist
Used by the Look Dev Supervisor, DP and the critic panel (research/10 b, 11 c, 13 c):
1. Ambient or sky lighting instead of small sources.
2. Depth of field wrong for scale (everything sharp, or toy-shallow tilt-shift).
3. Clipped or hue-shifted highlights.
4. Razor sharpness and zero noise.
5. Too-clean surfaces and shadows.
6. Uniform, tiled or wrong-scale texture (fingerprints, weave, grain).
7. Perfect symmetry, straight edges, square alignment.
8. Waxy or plastic clay.
9. Motion blur, or noise that changes on held frames.
10. Over-processing: bloom, grain, flare you notice before you switch them off.
