# Clay / stop-motion craft standards (research, Oct 17, 2026)

(inf) = researcher's inference. See "Unverified" at the end.

## 1. Timing
- Norm: 24 fps playback, poses on twos (12 distinct poses per second).
  - Vengeance Most Fowl: 24 fps on twos; camera moves shot on ones, with a "one-and-a-half" correction so moves don't stutter.
  - Dawn of the Nugget: 12 changes per second (Sam Fell). Fours give a homemade feel.
  - Pinocchio: mostly twos, ~12-15 poses/s.
  - Henry Selick (Wendell & Wild): mixes twos and some threes, accepts slight stutter; performance survives at 12 fps or lower.
- Faces can run faster than bodies at Laika: expressions typically held 2-3 frames; Missing Link pushed to 12-24 face changes/s; Wildwood used ~24 faces for one second. Body on twos, face on ones is plausible (inf).
- Output per animator: 3-5 s of finished footage per week.
  - Vengeance Most Fowl 4.2 s/week avg (up to 5), ~30-32 animators, a bit over 2 min/week total.
  - Pinocchio 3.8 s/week, 41 animators at peak. Missing Link 4.3 s/week target, 31 animators, 92 weeks. Boxtrolls 3.7. Kubo ~3 (up to 6; ~1 s for the giant skeleton). Early Man: hard shot ~0.5 s/day.
  - Memoir of a Snail outlier: 7 animators at ~5-10 s/day; rigid, legless puppets cropped by camera, deliberately "clunky" style.
- Review loop: Aardman screens each week's footage and fully reshoots rejected shots.

## 2. Surface and material
- Newplast (Newclay Products) used by Aardman since the 1970s: non-drying, wax-based, firm under hot lights. Newclay closed March 2023; Aardman bought ~900 lb of remaining stock. Chroma Clay (Animation Supplies, UK) launched May 2026.
- Van Aken Plastalina is oil-based, goes tacky under lights, collects dust. Apoxie Sculpt (epoxy) used on Memoir of a Snail.
- Aardman keeps fingerprints on purpose: a smoothing period "killed the life," prints went back in. Animators told to leave thumbprints on faces. "Evidence of the human hand."
- Aardman is now hybrid: Wallace & Gromit bodies silicone "full of fingerprints," clay heads. Nugget bodies silicone over 3D-printed armatures, clay heads, powdered sugar for matte finish. Feathers McGraw all clay.
- Laika is cleaner but moving toward visible handwork: Coraline faces hand-sanded and painted; ~80% of Missing Link faces needed no sanding; Selick kept face seams on Coraline and says recent stop-motion became "so perfect it might as well be CG"; Wildwood keeps traces of the artists' hands.
- Adam Elliot: lumpy, asymmetric forms, visible fingerprints; thinks Laika can look too refined.
- Boil: only primary source found is fur (Fantastic Mr. Fox, Wes Anderson wanted it). For clay, boil comes from re-touching the surface each pose (inf).
- Contrast: DreamWorks' Flushed Away (CG imitating Aardman) deliberately skipped thumbprints.

## 3. Faces and lip sync
- Aardman: pre-made clay replacement mouths for common shapes, reshaped by animators (Early Man). Wallace's faces sculpted clay. The Pirates! used ~8,000 3D-printed mouths (Captain 257, Darwin ~130). Gromit is brow-only; Shaun almost no mouth. Feathers McGraw blinks sparingly. Norbot: ventriloquist-dummy jaw, fixed brows.
- Eyes: Early Man resin eyes with a pupil pinhole, moved with a pin. Nugget eyes swapped every two frames. Feathers McGraw pin eyes 2.77 mm. Laika keeps eyes/lids on the puppet, trimmed per expression.
- Laika face counts: ~20,000 Coraline, 40,000 ParaNorman, 56,000 Boxtrolls, 64,000 Kubo, 106,000 Missing Link, ~140,000 Wildwood. Kubo: 11,007 mouth and 4,429 brow expressions. Magnet-mounted masks; from Missing Link on, bespoke faces per shot.
- Pinocchio: mostly mechanical silicone heads; deliberate asymmetry.
- Stoopid Buddy (Robot Chicken): clay eyebrows, sticker mouths, sometimes digital mouths, ~100 puppets per episode.

## 4. Camera, lens, light
- Canon bodies (EOS-1D X Mk III on Nugget) with adapted Nikon primes, shot in Dragonframe, which also drives DMX lights and motion control.
- Aardman lighting: tungsten micro-ellipsoidals moving to LED; programmed LED candle flicker; gobos and miniature projectors in camera.
- Laika: DP lights sets like live action; Wildwood LEDs through gauze and laser-cut branches. Pinocchio "layered lighting" passes combined in VFX.
- Scale: Wallace ~6-9 in, Shaun ~6.75 in, Nugget chickens under a foot. Multiple miniature scales blended in one shot.
- Depth of field: model shots traditionally use small apertures (~T11-T16) so models read life-size. Narrow focus reads "miniature" (why tilt-shift fakes work). Real miniature photography is typically deep focus with selective shallow focus (inf).
- Flicker causes (Dragonframe): ambient light, unstable power, reflections, short exposures, auto-iris lenses.
- Motion blur: none by default. Only go-motion or hand-moved moco adds blur.
- Rigs shot then painted out (green screen, sometimes frame by frame). CG used for water, fire, set extensions.

## 5. Motion principles
- Straight-ahead animation, no pre-drawn keys. Animators exaggerate breaths and small movements from the voice track.
- Heel placed too high reads as a limp; walks are hard. Memoir avoids walks with Muppet-style gliding.
- Aardman/Early Man animators work from live-action reference of the director performing the shot.
- Heavy puppets use rigs; weight is faked by support.
- Squash/stretch/overlap from plasticine malleability (inf, no primary quote).

## 6. Failure modes of AI "clay style"
- Cadence drift: AI clips wander between ~8 and 12 fps with inconsistent holds (promotional source).
- Interpolated smoothness vs hard holds and crisp frames.
- Glossy CG sheen, hyperreal faces, texture changing between generations.
- Missing or uniform procedural prints instead of lumps, thumb dents, asymmetry (inf).
- Morphing faces and costumes instead of rigid parts and discrete mouth snaps (inf).
- Continuous lip-flap instead of hold-and-snap mouths.
- Scale tells: tilt-shift blur gradients, props wrong for puppet scale, no practical light logic (inf).
- Physics: floating feet, no contact weight (inf).

## 7. Draft rubric (1-5)
[CODE] measurable by code, [JUDGE] visual judge, [BOTH].
1. Stepped cadence [CODE]: 5 = steady 12 unique poses/s (24 fps duplicate pairs), ones allowed on camera moves/fast action. 3 = mostly stepped, rate drifts. 1 = every frame unique.
2. Hold integrity [CODE]: 5 = held frames identical apart from sensor noise; discrete pose change. 1 = holds keep drifting.
3. Temporal stability [CODE]: 5 = no luminance/color flicker; static set pixel-stable between poses. 1 = exposure pumping, background crawl.
4. Crisp frames, no motion blur [CODE]: 5 = moving parts as sharp as static. 1 = smeared, flow blur.
5. Surface handcraft [JUDGE]: 5 = thumbprints, tool marks, asymmetry that stay put across holds. 3 = generic clay noise. 1 = smooth plastic or repeated texture.
6. Material and sheen [BOTH]: 5 = matte clay/silicone, small soft speculars. 1 = wet or glossy CG sheen.
7. Form consistency [BOTH]: 5 = proportions, costume, face rigid between poses. 1 = morphing identity.
8. Weight and motion [JUDGE]: 5 = contact, arcs, anticipation, overlap, deliberate imperfection. 1 = floaty, sliding feet.
9. Face performance [JUDGE]: 5 = discrete held-and-snapped mouths, sparing blinks, eye/brow-led acting. 1 = continuous lip-flap, morphing face.
10. Scale, lens, DOF [JUDGE]: 5 = believable miniature cues, motivated focus, prop/set scale agree. 1 = tilt-shift gradient, scale contradictions.
11. Light and set craft [JUDGE]: 5 = practical, motivated small-source light; camera moves on ones. 1 = flat or cinematic-CG lighting with no source logic.

## Unverified or conflicting
- Coraline "on ones" (exhibit summary) conflicts with Selick on mixing twos.
- Newplast composition (wax vs nylon fibre) conflicts. Van Aken use at Aardman unverified.
- Wallace's height varies by source (6 vs 9 in).
- Daily output claims (Farmageddon 2 s/day, Mr. Fox 4 s/day, Memoir 10 s/day) are peaks, not norms.
- Vinton-era lip-sync practice, Stoopid Buddy and PES frame rates unsourced.
- Release status: Wildwood premiered BFI London Oct 11, 2026; US release Oct 23. Shaun the Sheep: The Beast of Mossy Bottom Halloween 2026 US via GKIDS.

## Sources
https://postmagazine.com/Publications/Post-Magazine/2024/November-December-2024/Animation-I-Wallace-Gromit-Vengeance-Most-Fowl-I.aspx
https://www.tvbeurope.com/production-post/cracking-creation-fun-facts-from-wallace-gromit-vengeance-most-fowl
https://beforesandafters.com/2025/01/17/a-mix-of-old-and-new/
https://vfxvoice.com/celebrating-the-inventiveness-of-wallace-gromit-vengeance-most-fowl/
https://theasc.com/articles/wallace-gromit-vengeance-most-fowl
https://britishcinematographer.co.uk/charles-copping-emchicken-run-dawn-of-the-nugget-em/
https://www.moviemaker.com/chicken-run-dawn-of-the-nugget-peter-lord/
https://thekidshouldseethis.com/post/the-clay-that-makes-aardman-animations-come-to-life
https://www.mentalfloss.com/entertainment/movies/aardman-animations-clay-shortage-rumor
https://www.cartoonbrew.com/tools/new-stop-motion-plasticine-chroma-clay-260899.html
https://www.vfxvoice.com/aardman-goes-back-to-stop-motion-basics-with-early-man/
https://www.fabbaloo.com/blog/2012/2/8/we-built-about-8000-mouths.html
https://www.cgw.com/Publications/CGW/2006/Volume-29-Issue-10-Oct-2006-/Flushed-with-Success.aspx
https://www.fabbaloo.com/2019/03/106000-3d-printed-faces
https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/
https://www.inverse.com/entertainment/wildwood-laika-set-visit
https://blog.frame.io/2022/12/19/guillermo-del-toro-pinocchio-animation-behind-the-scenes/
https://beforesandafters.com/2022/09/07/i-wanted-to-pull-back-from-that-sort-of-perfection-and-leave-more-mistakes-in/
https://www.cartoonbrew.com/feature-film/henry-selick-wendell-and-wild-interview-222428.html
https://www.austinchronicle.com/screens/how-memoir-of-a-snail-came-out-of-its-shell-13286572/
https://www.bfi.org.uk/sight-and-sound/interviews/audience-will-forgive-bad-animating-theyll-never-forgive-bad-story-adam-elliot-memoir-snail
https://www.denofgeek.com/movies/fantastic-mr-fox-animators-interview-ian-mckinnon-andy-biddle-and-andy-ghent/
https://www.awn.com/print/animationworld/go-behind-scenes-robot-chicken-puppet-and-costume-fabrication
https://www.dragonframe.com/ufaqs/how-to-reduce-flicker-what-are-possible-sources-of-flicker/
https://www.provideocoalition.com/fake_tilt_shift_cinematography/
https://invideo.io/faq/why-does-ai-generated-stop-motion-animation-have/
