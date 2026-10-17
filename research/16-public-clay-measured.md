# What real clay animation measures (public clips, Oct 17, 2026)

Measured, not read: 35 openly licensed clips from Wikimedia Commons were played frame by frame in a browser and measured in code. Per-clip numbers are in `gold/measurements.csv`; the full list of usable clips is `gold/public_catalog.csv`. This file says what the numbers show, how they were taken, and what they change in the kit.

## 1. What was measured

- **Clips:** 36 attempted. Used in the summaries: 24 indie and student clay shorts and 6 segments from the professional Multi-Russia series (plasticine, 25 fps TV). Kept apart: 2 mixed-media puppet films, and one clay test on a pure white background (its timing is normal, but white backgrounds skew the look numbers). Excluded: a trailer that cuts to live action, a behind-the-scenes clip, and one film whose segment was a 2D comic. All CC BY 3.0 or CC BY-SA.
- **Segment:** 20 to 24 seconds per clip, chosen to skip titles. Two 4K clips lost frames during playback; their timing numbers are left out, their look numbers kept.
- **Timing:** every frame was shrunk to 128 by 72 pixels and compared with the one before. A frame counts as "a new pose" when more than 0.2% of its pixels changed by more than 10 levels (out of 255); otherwise it is the same image held. Runs of identical images give the hold lengths (ones, twos, threes, fours). "Poses per second" counts new images per second inside animated stretches (holds of 5 or more frames are counted separately as held shots). A cut is a frame where most of the picture changes at once.
- **Look:** one frame in twelve, shrunk to 320 by 180 with black borders cropped: brightness percentiles, saturation, warmth (red minus blue), colorfulness, edge sharpness, and how much sharper the center is than the edges.
- **Check of the timing detector:** a synthetic clay clip with known timing (twos, ones, threes and a long hold, with per-pose sensor noise) was encoded as web video at 0.6, 1.2 and 2.5 Mbit/s and run through the same detector. It got every frame right at all three bitrates. On the real clips, raising the threshold to 0.4% moves poses per second by a quarter of a pose (median) and the ones share by about one point; one clip (Birthmark) swings from 19 to 25 poses per second, so its timing is uncertain. Both versions are in the CSV.

## 2. Timing: what real clay does

| | Indie clay (22 clips with clean timing) | Pro TV clay (6) |
|---|---|---|
| New poses per second, median (middle half) | 18.1 (11.8 to 23.0) | 20.6 (19.6 to 23.9) |
| Share of animated frames on ones, median | 38% | 70% |
| Share on twos, median | 31% | 14% |
| Clips mostly on ones / mostly twos / mostly threes or slower / mixed | 12 / 7 / 2 / 7 (all 28 clips) | |
| Held stretches (5+ identical frames), share of time | 6% (1% to 31%) | 11% |
| Shot length between cuts, median | 4.0 s | 1.1 s |

What that means:
- **There is no single "clay cadence."** Real clay ranges from pure twos (12 poses per second) through threes (8 to 10) to full ones (24 to 30). Only a quarter of clips are mostly twos. The mix inside a clip is common.
- **Much of the "ones" is camera movement.** Frame-by-frame strips of the pro series showed slow camera moves over clay sets on ones while characters held. The detector can't separate camera from character, so the ones share is an upper bound on character animation on ones. This supports our rule (camera on ones) rather than contradicting it.
- **Upload frame rates distort cadence.** Many clips were uploaded at 30 fps (and one at 15). Twelve poses per second inside a 30 fps file shows up as alternating holds of 2 and 3 frames. Our deliverables stay at 24 fps, where twos are clean.
- **Held frames are exact copies.** Inside a hold, the median difference between frames was 0.03 levels out of 255, which is compression noise only. Real stop motion shows the same photograph twice; nothing shimmers on a hold. This settles a question the research had left open: noise, grain and boil change per pose, never per frame (LOOK_DEV.md 6 already says so; this is the evidence).

## 3. Look: what real clay looks like on screen

| | All 30 clay clips, median (middle half) | Our test render, round 7, medium shot |
|---|---|---|
| Darkest 5% of pixels (0 to 255) | 13 (0 to 20) | 19 |
| Middle brightness | 76 (39 to 106) | 117 |
| Brightest 5% | 198 (182 to 210) | 154 |
| Saturation (0 to 1) | 0.38 (0.27 to 0.56) | 0.28 |
| Warmth, red minus blue | +23 (+7 to +56) | +37 |
| Colorfulness | 45 (30 to 68) | 32 |
| Edge sharpness | 30 (22 to 43) | 7.5 |
| Center sharpness over edge sharpness | 1.6 (1.1 to 2.2) | 9.4 |
| Clipped highlights | 0.02% | 0% |

What that means:
- **Real clay footage is low-key with bright highlights:** darker midtones and a wider range than our renders. Our renders sat in a narrow, safe middle.
- **Real clay footage is sharp across the whole frame.** The center is only about 1.6 times sharper than the edges, so backgrounds stay detailed. Our test render was soft overall and 9 times sharper in the middle: too shallow a focus for the scale, a plain backdrop, and denoiser smoothing. The CG tell here is softness, not razor sharpness.
- **Highlights are rarely clipped.** Under 0.1% of pixels in most clips.
- **Color is moderately saturated and usually warm.** The pro series is cooler and more colorful.
- These look numbers depend on what is in the frame, so treat them as a sanity range for a whole sequence, not a target for any one shot.

## 4. What changed in the kit

- MOTION.md: cadence is authored per pose (holds of 1, 2 or 3) with twos as the default for bodies, not a flat filter; camera moves stay on ones; the measured range above becomes the motion QC reference.
- LOOK_DEV.md: camera defaults move to wider lenses and f/16 so backgrounds stay detailed; white balance to the key is required (an unbalanced 3200 K key turned the whole test scene orange); the CG-tell list now includes "soft overall" and "background much softer than subject"; held frames must be byte-identical.
- GOLD_SET.md: public clips are now the primary gold source; the probe session is optional and short.
- Phase 5 code gates start from these ranges.

## 5. Limits

- 30 clips is enough for ranges, not for fine thresholds. The pro group is one series.
- Web compression hides fine surface detail (fingerprints and crumb under about a millimetre on screen are invisible at these sizes). Surface numbers still need close, high-quality reference, which is what the probe session is for.
- Clip choice was by eye; the judge of "polished" was one person (the R&D pass), not a panel.
- The judge models may have seen these clips in training (GOLD_SET.md).

## 6. What the test renders taught (Oct 17 R&D pass)

A small Blender 5.2 test scene (a clay figure, a 3 cm clay ball, a painted card backdrop, a linen tabletop, a 3200 K key spot, fill and rim, at true metre scale) was rendered with Cycles on CPU, run through a sensor-noise and web-video round trip, measured with the same code as the public clips, and compared by eye with frames from them. Nine rounds. The judge was the R&D pass itself (one model, the same family as the builder), so treat these as leads for the tune loop, not results.

| Round | Change | What it showed |
|---|---|---|
| 0 | Clay shader v1 as specified | Already reads as clay. Tells: dents evenly spread like orange peel; over-saturated orange everywhere |
| 1 | Dents gathered in patches, thumb smears, cleaner face, muted palette | Smears read as fur or wood grain when strong |
| 2 | Camera white balance to the key | The orange cast was missing white balance, not the palette. Now required in LOOK_DEV.md 5 |
| 3 | Softer, patchy smears | Plausible soft clay |
| 4 | Voronoi facets and creases | A regular cell network like cracked leather: a new CG tell, added to the checklist. Reverted |
| 5 | Sculpt asymmetry, sparse specks | Less "perfect primitive"; specks invisible at this size |
| 6 to 7 | More contrast, warmer balance, textured backdrop | Closer to the public clips' contrast; multicolor noise in a set texture reads as confetti, use greyscale |
| 8 | Handling smudges on pale clay | Subtle; matches what pale clay shows in the public close-ups |
| 9 | 24 and 35 mm lenses at f/16, stronger contrast, prints back on the face | Crisper and lower-key, closer to the public range; Blender's 0.1 m near clip cut through the head at close range (fixed) |

Also found: subsurface weight between 0.05 and 0.45 at 0.4 mm distance barely changes a front-lit face at web resolution (LOOK_DEV.md 2.1); the sharpness gap to real footage comes mostly from depth of field and denoiser smoothing, so the denoiser's detail-preserving mode and wide lenses matter more than shader detail at this size.
