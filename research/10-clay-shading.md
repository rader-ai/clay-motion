# Clay and miniature shading in Blender 5.x Cycles (research, Oct 17, 2026)

~20 searches and ~55 fetches (shared search budget ran out). Blender 5.x manual pages returned navigation only; Principled and SSS specifics come from the 3.2 manual, 4.0 and 5.0 release notes, and API knowledge, marked [U]. No measured BRDF/BSSRDF for plasticine was found; every plasticine scattering value is inferred from analogues [U]. Note: research/09 suggests SSS weight 0.05-0.15; this report suggests 0.25-0.45 with a short scatter distance. Settle it by look-dev matching against real reference photos (procedure c).

## 1. Physics
- Composition: water-free blend of fine mineral powder, wax, oil and soap. Studio recipes: mineral oil, petroleum jelly, paraffin or microcrystalline wax, clay or calcium carbonate. Historic formula ~65% gypsum, 10% petroleum jelly, 10% lanolin, 10% stearic acid, 5% lime. FTIR on artist oil clays: CaCO3 main filler in paraffin oil/wax, pigment under 1 wt%. Newclay closed in 2023; Aardman found a new supplier.
- Scattering: filler index higher than binder (CaCO3 ~1.59 vs ~1.45 for wax and oil [U]); strong scattering over very short distances; absorption mostly from pigment.
- Analogue data: Gkioulekas "liquid clay" extinction 37.5/48.3/68.0 per mm RGB (mean free path 15-27 um), albedo ~0.9999, g 0.31-0.51. Milk soap extinction ~8/mm (mfp ~0.12 mm). Glycerine soap 0.2/mm (mfp ~5 mm, the "translucent" end). Jensen marble reduced scattering 2.19/2.62/3.00 per mm, absorption 0.0021/0.0041/0.0071 per mm. Cornell scatterometer couldn't fit microcrystalline wax.
- Translucency: diffusion length (not mfp) sets travel distance; estimate 1-2 mm for white filled material [U]; pigment shortens it. Faint warm glow only through sheets of ~3 mm or less when backlit; fingers and ears of 4-8 mm effectively opaque. The pigment's own hue travels furthest [U].
- Specular: dielectric, IOR ~1.45-1.5 [U]. Fresh clay: broad soft sheen. Handled spots polish to tighter highlights; ridges break highlights into striations.
- Matting: Aardman replaced toxic silica powder with powdered sugar for a matte finish (Nugget puppets, verified).
- Lighting: plasticine softens and stiffens with temperature; ASC notes only so many ways to light it before it loses texture; Vengeance DP tested white, blue and warm light because plasticine and silicone shift differently.
- Bath "Plasticine Shading" (2014): physically based plasticine model, ~20% more accurate than standard surface shaders; method not accessed; worth fetching.
- MERL (100 materials) and EPFL RGL databases: wax/clay entries unconfirmed.

## 2. Principled BSDF in Blender 5.x
- 4.0 (Principled v2): subsurface colour = base colour; Scale multiplies Radius; IOR Level controls specular; Coat is a separate layer; Sheen is microfiber.
- 5.0: random-walk SSS handles multiple bounces (fewer dark artifacts, more cost); thin film supported.
- Prefer plain Random Walk (not the Skin variant [U]) for predictable clay.
- Work in true metres (20 cm puppet = 0.2 BU). Radius x Scale is the scatter distance. If Blender follows Disney's path-traced SSS [U], effective free path is 1.4-2x Radius x Scale.
- Failure modes: wax (SSS weight over ~0.6, mfp over ~2 mm, glow in shadows); soap (uniform saturated glow on smooth forms); plastic (no SSS, sharp uniform hotspot, hard clean bevels). Fixes: SSS weight 0.25-0.45, scatter 0.3-0.8 mm, roughness 0.4-0.55, micro-relief, uneven bevels.

## 3. Surface detail at true scale
- Fingerprint ridge spacing: mean 0.46 mm (male), 0.41 mm (female), range 0.2-0.85 mm (NCJRS, 1,777 measurements).
- Pixel limits: at HD with a 20 cm puppet filling ~70% of frame height, 1 px ~ 0.26 mm, so a ridge period is ~1.8 px and will alias. Aim for 4+ px per period (frame width <= ~0.4 m at 4K, <= ~0.2 m at HD). Fade ridge amplitude toward zero as footprint approaches 0.11 mm/px.
- Texels: 6+ per period (~13 texels/mm); a 1024 px stamp covers ~13 mm. 16-bit or EXR height maps, Non-Color.
- Generating prints (SFinGe-style): orientation field from core and delta points; iterative Gabor filtering with ~+/-20% frequency variation; sinusoidal ridge thickness; pores along ridges, drop ~3%.
- Partial print: elliptical pressure mask ~10-16 x 14-20 mm, soft edge, low-frequency warp, random breakups. Overlaps: later print wins inside its feathered mask; earlier prints blurred. Smudge: directional blur along drag.
- Relief depth: impressions 20-60 um [U].
- Tool marks: loop tool parallel grooves 0.3-1 mm with burrs; ball stylus dimples with raised rim; knife crisp cut with smeared lip; seams 0.1-0.3 mm line with raised lip; cracks as Voronoi edges in stretched areas; marbling as anisotropic domain-warped noise, 3-8 mm streaks.
- Bump vs displacement: bump has no silhouette or self-shadow; use bump under ~0.25 px footprint, true displacement for dents of 0.3 mm+. Bump Distance in scene units (30 um = 0.00003). Bump doesn't change the random-walk geometry, so dmfp over ~0.3 mm washes ridges out of diffuse; ridges then read through specular breakup and shadow [U].
- Adaptive subdivision: no longer experimental in 5.0, lives in the Subdivision modifier, new object-space edge-length option; introspect `bl_rna.properties` for exact 5.x names [U].

## 4. Handmade variation (seeded)
- Seed per part: `int(hashlib.sha1(f"{proj}:{part}".encode()).hexdigest()[:8],16)` into Object Info Random, a custom attribute, or a GN input.
- Per-part jitter: hue +/-1-2%, saturation +/-5%, value +/-4%.
- Contamination: blend 2-6% of a neighbouring part's colour near contact (proximity mask).
- Handled areas: roughness -0.1 to -0.15, slightly darker. Crevice grime from curvature/AO.
- Lint and hair specks: sparse GN curves, ~20 um thick, 1-5 mm long [U], ~1-3 per cm2 on dirty areas only.
- Never mirror detail.

## 5. Boil
- Kin Klei / Klei Krush: Frame Step changes the seed every N frames plus a speed control; must match between material and GN.
- Recommended: seed from a pose hash (quantized bone matrices), not frame number, so held frames stay identical. Re-seed only the touched region (mask from per-vertex motion between poses). Re-seed micro-detail under ~3 mm; keep meso detail (3-15 mm) 70-85% persistent; silhouette wobble 0.1-0.3 mm [U]. Hard switch, no crossfade, no motion blur. Draw from a pool of ~6 variants per region so it reads as one hand repeating.

## 6. Other miniature materials
- Silicone (Gromit's body, Wallace's sleeves): SSS weight 0.6-0.8, scatter 1-3 mm, roughness 0.3-0.45, dust or sheen layer [U].
- Eyes: glossy glass/resin, IOR 1.5-1.55, roughness 0.02-0.05, domed, strong catchlights. Nugget eyes fingernail-sized, swapped every two frames.
- Paint: matte acrylic, roughness 0.5-0.7, directional brush texture, pooling in crevices.
- Felt and wool: sheen weight 0.5-1, roughness 0.8+, short GN fibres 0.5-3 mm.
- Fabric: true-scale weave (0.3-0.8 mm pitch); it reads oversized on a 15 cm puppet, which is the correct tell. Laika weights hems, combs wigs with silicone for matte.
- Set dressing: Aardman crushed walnut, glue and sand for tarmac; scale-correct thatch; skies often digital now.
- Wood and card edges (0.2-0.5 mm) at true scale; foam open-cell with mild SSS; leaves 0.2-0.4 mm thick, veinless [U].
- Reading as miniature: true metric scale, macro DOF, small hard sources (not sky light), slightly clumsy rounded forms, no blown highlights.

## 7. Existing tools
- Clay Doh: $30, Blender 4.4-5.2, Cycles/Eevee, royalty-free; fingerprints, cracks, stones, stop-motion presets, Clay Text, Pottery, Eyes.
- Kin Klei $1 / Kin Kollection $2.50, Blender 4.0+, Cycles; fingerprints, bumps, bits, cracks, smoothing, seed, frame step; "Creative Commons" licence (variant unstated).
- Clay/Plasticine Procedural Shader (KYRA) $15.98, Blender 2.8-4.5.
- Iconprints $4: procedural fingerprint roughness map; no redistribution.
- Free: ambientCG and Poly Haven CC0; ambientCG has no plasticine, only generic Clay and Plastic.
- Owned library path: press prints into 6+ clay colours; fixed camera, 4-8 raking light directions (RTI / photometric stereo) to derive heights; photogrammetry (Meshroom) for larger forms.

## 8. Render settings
- Adaptive sampling noise threshold 0.002-0.01, min samples 32-64, max 512-2048 on close-ups [U].
- Total bounces ~12, diffuse and glossy 4+ [U]. Clamp indirect only; Filter Glossy 0-0.3; never clamp direct.
- Pixel filter Blackman-Harris default; narrower = crisper.
- Denoising: omitting albedo can blur detail; OIDN prefilter detail ranking None > Accurate > Fast. Ridges come from shading, not albedo, so a noisy colour pass can smooth them [U]. Hero shots: skip denoising at 1024+ samples, or compare denoised vs raw high-frequency energy and blend detail back [U]. OptiX not temporally stable; use OIDN for animation.
- Cost: random-walk SSS ~1.5-3x plain diffuse; micropolygon displacement costs memory [U].

## 9. Look-dev from real references
- Shoot the real clay object with grey ball, chrome ball and colour chart in the same light. CAVE Academy mid-grey ~0.19 ACEScg. Grey ball specular ~0.35, roughness 0.4-0.6; chrome ball base 0.7, metal 1, roughness 0.06. Real balls are rarely neutral; tune digital twins.
- Capture: lock focus, WB, ISO, aperture; raw; chrome and grey at subject position, 3 exposures each; Macbeth chart.
- Agent metrics: dE2000, luminance histogram EMD, radial power spectrum of high-passed luminance, edge profiles; DISTS (tolerates resampled texture), sliced-Wasserstein feature loss, LPIPS; FLIP worth a look [U].

## (a) Clay shader v1 (node by node, metres)
1. Coordinates: Texture Coordinate Object to Mapping, object scale applied. Feature sizes in metres: crumb 0.05-0.3 mm, marbling 3-8 mm.
2. Seeds: Object Info Random and `part_seed` into 4D noise W; `pose_seed` into micro-detail W.
3. Colour: base RGB (linear albedo 0.04-0.8); HSV with part jitter (hue +/-0.02, sat +/-0.05, val +/-0.04); mix by marbling noise to a second colour (hue shift 3-6%, factor 0.15-0.35); multiply cavity grime (V x 0.8) by cavity x handling mask.
4. Principled BSDF: Metallic 0. Roughness 0.48 +/-0.06 from 2 mm noise, -0.12 in handled mask, +0.05 on ridges. IOR 1.47 [U], IOR Level 0.5, Specular Tint white. Subsurface Weight 0.35, Random Walk, Scale 0.0006, Radius lerp((1,1,1), normalize(basecolor), 0.6) (warm pink ~ (1, 0.6, 0.4)). Anisotropy 0-0.2. Sheen Weight 0.15, Roughness 0.5, Tint 0.5 (raise to ~0.35 for powdered-sugar matte). Coat 0 by default, 0.06 on handled patches, Coat Roughness 0.25, Coat IOR 1.45.
5. Normal chain, three Bump nodes in series: meso dents Distance 0.0004; micro crumb 0.00005; fingerprint stamp image 0.00003 (16-bit Non-Color).
6. Displacement node: midlevel 0.5, scale 0.0004, meso height only; material Displacement = "Displacement and Bump".
7. Geometry Nodes: pose-seeded stamp placement producing `print_mask`, `handling_mask`, `dent_height`; sparse lint curves; subdivision for dents.

## (b) Ten CG tells and fixes
1. Too-clean surface: relief at three scales (dents 3-15 mm, tool marks 0.5-3 mm, crumb 0.05-0.3 mm).
2. Fake fingerprints (concentric rings, tiling, wrong period): flow-field ridges at 0.41-0.46 mm, partial and overlapping, faded by pixel footprint.
3. Waxy glow: cut SSS weight and distance.
4. Wrong highlight: broad sheen with polished patches plus sheen layer.
5. Perfect symmetry and bevels: uneven bevels, seams, asymmetric placement.
6. Flat colour: per-part shifts, marbling, contamination, grime.
7. Boil absent or global flicker: pose-seeded, touch-masked re-seeding.
8. Wrong scale cues: macro DOF, small hard lights, true-scale weave and fibres.
9. Sterile: sparse specks, lint, crevice dust.
10. Render artifacts: denoiser smoothing, ridge aliasing, clamped highlights, motion blur.

## (c) Look-dev matching procedure for an agent
1. Photograph: clay sphere, finger cylinder, 1/2/3 mm backlit sheets, fingerprint stamp, grey and chrome balls, colour chart, mm scale; production light, locked camera, raw.
2. Recreate camera and lights at true scale; derive lighting from the chrome ball.
3. Calibrate grey ball, chrome ball and chart first; fix exposure and WB until chart patches match.
4. Render clay probes at 256-512 px ROIs, 64 spp for the search loop.
5. Score: dE2000 on flat ROIs, histogram EMD, highlight size and falloff, terminator width, backlit transmission vs thickness, power-spectrum band energy 0.3-2 cycles/mm, DISTS on ROI crops.
6. Optimise with CMA-ES or Optuna over base colour, roughness, SSS weight and scale, coat, sheen, bump strength.
7. Validate on a held-out light angle and distance; reject overfit solutions.
8. Blinded real-vs-CG comparison panel [U].

Note: English docs.blender.org manual pages return only navigation to WebFetch; `/pt/3.2/` manual pages and developer.blender.org release notes 4.0 and 5.0 work.

## Sources
https://developer.blender.org/docs/release_notes/4.0/shading/
https://developer.blender.org/docs/release_notes/5.0/cycles/
https://docs.blender.org/manual/pt/3.2/render/shader_nodes/shader/principled.html
https://docs.blender.org/manual/pt/3.2/render/shader_nodes/shader/sss.html
https://docs.blender.org/manual/pt/3.2/render/cycles/render_settings/sampling.html
https://docs.blender.org/manual/pt/3.2/render/cycles/render_settings/light_paths.html
https://docs.blender.org/manual/pt/3.2/render/cycles/render_settings/subdivision.html
https://docs.blender.org/manual/pt/3.2/render/shader_nodes/vector/bump.html
https://docs.blender.org/manual/en/3.1/render/layers/denoising.html
https://media.disneyanimation.com/uploads/production/publication_asset/153/asset/siggraph2016SSS.pdf
https://graphics.stanford.edu/papers/bssrdf/bssrdf.pdf
https://www.cs.cornell.edu/projects/translucency/
https://graphics.stanford.edu/courses/cs348b-competition/cs348b-04/candle1/index.html
https://en.wikipedia.org/wiki/Plasticine
https://link.springer.com/doi/10.1186/s40494-019-0333-3
https://animationmagazine.net/2023/11/aardman-animations-studio-is-running-out-of-plasticine
https://www.aol.com/inside-making-chicken-run-dawn-180000163.html
https://awn.com/animationworld/aardman-50-inside-clay-felt-and-fingerprints
https://britishcinematographer.co.uk/dave-alex-riddett-bsc-wallace-gromit-vengeance-most-fowl/
https://theasc.com/magazine/oct05/curse/page2.html
https://animationmagazine.net/2016/07/puppet-masters
https://researchportal.bath.ac.uk/en/publications/plasticine-shading/
https://ojp.gov/ncjrs/virtual-library/abstracts/analysis-ridge-ridge-distance-fingerprints
https://arxiv.org/pdf/2002.03809
https://superhivemarket.com/products/claydoh
https://superhivemarket.com/products/kin-klei/docs
https://superhivemarket.com/products/clay-procedural-shader-cycles--eevee/docs
https://superhivemarket.com/products/iconprints-procedural-fingerprint-imperfections/docs
https://polyhaven.com/license
https://docs.ambientcg.com/license/
https://culturalheritageimaging.org/Technologies/RTI/
https://caveacademy.com/wiki/post-production-assets/surfacing/surfacing-training/setting-your-mid-grey-value/
https://www.merl.com/research/downloads/BRDF
https://rgl.epfl.ch/materials
https://github.com/RenderKit/oidn
https://arxiv.org/abs/2006.07229
https://arxiv.org/abs/2004.07728
https://arxiv.org/abs/1801.03924
