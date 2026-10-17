# Stop-motion acting and timing craft (research, Oct 17, 2026)

~26 searches and ~75 fetches. Studio sources (Aardman, Laika, Anderson, Selick) give strategy: ones vs twos, output rates, performance philosophy. They almost never give frame counts. Hard frame numbers mostly come from 2D/CG teaching sites, marked (T). Williams, Lord/Sibley and Priebe could not be read directly, so nothing is attributed to them. [U] = unverified or inference. All counts at 24 fps.

## Findings

### 1. Ones vs twos
- Aardman animates characters on twos and shoots camera moves on every frame. Under a camera move on twos they use a "one-and-a-half" correction so the character doesn't stutter against the camera, and dislike doing it (Post Magazine).
- Sam Fell: twos add texture and handmade feel; beginners can try twos or fours. Peter Lord wants edge, bite, imperfection, not CG smoothness.
- Isle of Dogs: mostly twos with some single frames, to break up smoothness. Selick doesn't shoot everything on ones; Wendell & Wild used twos and threes. The CG Lego Movie used twos and threes, no motion blur, no squash and stretch.
- Ones for subtle or realistic acting and for speed. Twos at the same speed doubles the distance per pose, which strobes on fast moves.
- Output ~4.2 s/week per animator (VMF), 3.5-4.3 at Laika, half a second a day on one Early Man shot: about 20 poses a day, so every pose has to carry intent. A 5-6 s/day Laika claim conflicts [U].

### 2. Timing (T unless noted)
- Blink: regular 6 frames (2 close, 1 closed, 3 open), fast 5, long 9, flirty 3. Another source: close 3-5, open 2-4.
- Blink mid-to-late in a fast head turn, or at a thought shift. "Every 2 seconds" is outdated; tense characters go 10 s or more.
- Eye dart: 2-3 frames, ~80% of the move in the first frame; lids follow; eyes lead the head.
- Take: anticipation 4, take 7, settle 7. Punchy: anticipation 6, 1-frame pop, settle 7. Double take: head turns 3 frames apart.
- Holds: avoid 3-5 frames (reads as a mis-shoot). Minimum 6 with a moving hold, 12 for an expression to register, 16-18 comfortable, 24+ only for comedy.
- No usable source for head turn, weight shift, sit/stand counts [U].

### 3. Spacing
- Surface-gauge example for a 12-frame arm move: 3 ease-in frames at ~1/4 then 3/4 of the main step, six equal main steps, 3 ease-out frames. In the last frames only the extremity still moves.
- Gauges matter because the camera can't see depth errors. Dragonframe's increment editor plots evenly spaced marks on a path with a Bezier spacing curve.
- Priebe's publisher site names "pop in arc" and "pop in spacing" (spacing suddenly widens for no reason) as serious distractions.
- Whitaker's Timing for Animation recommended for timing charts.

### 4. Acting
- Directors act out shots on video; animators interpret rather than copy; Aardman reports ~1% reshoots. Park filmed himself playing every Early Man shot.
- Gromit's expressions lead from eyes and brow; he has no mouth because Park couldn't animate one.
- Feathers McGraw has no brow; head movement and composition carry him; no blinking unless the story needs it.
- Small things (glances, finger taps) hold an audience; repeating a gesture each time a line repeats emphasises it.
- Crossingham: animators should be actors; thoughts are hardest to animate; pauses can be the best moments; contrast fast and slow.
- McKinnon (Mr. Fox): hold back on very expressive puppets.
- Becher: acting comes after mastering basics; animators cast by strength (comedy vs nuance).
- Laika animators study themselves, colleagues, family; audiences read body language too well to cheat.

### 5. Walks, runs, jumps
- Cadence (T): 12 frames per step natural (2 steps/s), 16 a stroll with attitude, 18 deliberate, 24 tired or sneaking. Keys: contact, down, passing, up.
- Tie-down: supporting foot screwed to the stage; weight stays on it until the other plants. Flexible rig arms now common.
- Park uses silicone bodies for walking shots, clay for expressive close-ups.
- Leaping runs use a rig behind the puppet, painted out. Jumps shot in three parts: take-off, flight, landing.
- Memoir of a Snail avoided walking: cropped at the legs, or slid across the table on a small up-and-down rig.

### 6. Squash, stretch, secondary motion
- Clay allows squash/stretch and expression change by re-sculpting; foam latex limits it.
- Coraline's mouse circus used series of replacement mice; Gromit was built wholly from clay for one hyper-extended flight shot.
- Animators cut a wedge from the upper lip to avoid re-sculpting the whole lip each frame.
- Secondary motion is engineered: foam pads under fabric, wire in skirts, mechanical "breathers" in Missing Link puppets.
- Kubo's costumes and hair hard to control; Mr. Fox animators blew on fur and brushed eyebrows between frames.

### 7. Faces and lip sync
- Closed shapes (B/M/P/F/V) land on the sound frame or 1 frame before; leads of 1-3 frames; never after the sound.
- Hold each shape at least 2 frames. ~8-12 shapes for English; Shaun used 15 per character; Isle of Dogs humans 12-14.
- Key stressed syllables only; keep jaw movement small.
- Head, body or gesture anticipates a line by 4-6 frames. Eye-only close-ups start at least 4 frames before the accent.
- Aardman works from a dope sheet with phonetic breakdown. Early Man used pre-made clay mouths adjusted to the voice; resin eyes with a pinhole, moved with a pin.
- Wildwood: ~140,000 printed faces; a box of 24 faces covers one second, implying faces on ones for dialogue [U].

### 8. Camera
- Aardman: ones for moves, motion control set up before the animator arrives.
- Park likes multiple angles and building new set sections over a static camera.
- Suspense from slow push-ins and stillness; a locked-off shot got the biggest laugh in a Shaun screening.
- No source on ease profiles or handheld feel [U].

### 9. Handmade imperfection
- Elliot: celebrate lumps, bumps, fingerprints; animate from intuition; keep happy accidents (a mid-shot ear fall-off stayed).
- Each Snail character has a movement vocabulary (Grace holds arms in, Gilbert uses bigger poses); set rules for blinks.
- Anderson wanted fur boil and visible handling ("still very smooth, but it breaks it up a little").
- Opposite approach: Were-Rabbit used handle controls to suppress fur movement; Missing Link's fur tiles avoid boil.
- Blender tutorials: a lower frame rate alone gives a low-fps look, not stop motion; it also needs slight irregularity in position.
- Synthesis [U]: irregularity lives in surface texture and uneven increments; arcs, contacts and eye-lines stay clean.

## Draft motion style guide (24 fps)

Frame strategy
1. Bodies on twos (12 poses/s): the handmade texture studios keep.
2. Ones for camera-move shots, actions under 6 frames, eyelid and eye work, fast moves: twos strobe at speed.
3. Camera on ones. A character on twos under a move gets poses offset half a step, or goes to ones: avoids stutter against a smooth camera.
4. One frame grid per puppet; all parts change pose on the same exposure: a real puppet can't update parts independently.

Eyes and face
5. Blink 6 frames (2 close, 1 closed, 3 open); fast 5, long 9; at least 2 frames of half-lid: a one-frame close reads as flicker.
6. Blinks irregular (60-180 frames apart), at thought shifts or mid-to-late in head turns; never blink a tense character: metronomic blinks read as CG.
7. Eye dart 2-3 frames, ~80% in the first frame; eyes arrive 2-4 frames before the head [U]: gaze leads attention.
8. Expression change through brow and eyes first, then hold at least 12 frames: time to register.
9. Thinking beat: eyes settle, hold 12-24 frames before acting [U]: pauses are performance.

Timing
10. Anticipation 4 (6 if punchy), take 7 or a 1-frame pop, settle 7.
11. Small overshoot, return over 6-8 frames with shrinking increments [U on size].
12. Never hold 3-5 frames. Minimum 6, with a moving hold.
13. Moving hold: body drifts along the momentum of the last move, with a breath, eye dart or weight settle every 6-12 frames; don't stop everything on one frame.
14. Defaults [U]: gesture 6-8, head turn 8-12, weight shift 12-18, sit or stand 18-30.

Spacing
15. Increments on an arc: 3 ease-in, even middle, 3 ease-out; roughly 1 : 3 : 4 (main step) : 3 : 1; extremities settle last.
16. No unmotivated spacing jumps. Intentional pops (snap-look, flinch) get 4-6 frames of anticipation and a hold of 6+.
17. Overlap: head lags torso 2-3 frames, hands lag forearm 1-2, ears or cloth lag 2-4 with decaying amplitude [U on counts].

Lip sync
18. Mouth shapes land 1-2 frames before the sound; closed shapes on the sound frame or 1 before; hold every shape at least 2 frames.
19. 8-15 shapes; key stressed syllables, skip or blend the rest; small jaw.
20. Gesture or head starts 4-6 frames before the line; brow accent on the stressed word; blink at phrase ends [U].

Locomotion
21. 16-18 frames per step for chunky or short-legged puppets, 12 for lighter ones [U]; lock the planted foot from contact to passing: sliding feet are the most obvious amateur tell.
22. Avoid walks: crop below the knee, slide on a rig with a small vertical bounce, cut away, or exit frame. The real studios do this.
23. Jump: anticipation 4-6, wide spacing at take-off and landing approach, tight at apex, contact, 2-3 frame squash, settle 6-8 [U].

Clay and handmade
24. Squash and stretch in faces, hands and gags, 1-2 frames of extreme, volume-preserving: full-body deformation breaks the puppet illusion.
25. Imperfection only in surface texture (changing every exposure) and increment sizes (~+/-10-15% on non-critical channels [U]). Never noise on contacts, eye-lines or holds: noise on the main arc reads as wobble.
26. In Blender: pose keys with constant interpolation on twos (or Stepped F-curve modifier), staggered per object. Noise modifiers on surface channels only.

## Acting principles
1. Act it out on video first, then interpret rather than copy.
2. Every shot has one story point; protect it.
3. Eyes and brows lead, body follows.
4. Pause, contrast fast and slow, hold back on expressive puppets.
5. Give each character a movement vocabulary (pose size, speed, blink rate, arm carriage).
6. Repeat gestures to emphasise repeated lines.
7. Small business (glances, finger taps) holds attention.
8. Play it straight; the comedy comes from seriousness.
9. Feel the puppet's weight; plant before you move.

## Sources
https://www.postmagazine.com/Publications/Post-Magazine/2024/November-December-2024/Animation-I-Wallace-Gromit-Vengeance-Most-Fowl-I.aspx
https://www.moviemaker.com/chicken-run-dawn-of-the-nugget-peter-lord/
https://www.cartoonbrew.com/feature-film/isle-dogs-animation-director-mark-waring-explains-animate-wes-anderson-film-157358.html
https://www.dazeddigital.com/film-tv/article/39516/1/isle-of-dogs-animators-wes-anderson-interview
https://www.bfi.org.uk/features/stop-motion-imperfection-why-animation-needs-human-touch
https://www.bfi.org.uk/sight-and-sound/interviews/stop-motion-henry-selick-coraline
https://www.denofgeek.com/movies/fantastic-mr-fox-animators-interview-ian-mckinnon-andy-biddle-and-andy-ghent/
https://www.motionpictures.org/2014/02/how-the-lego-movie-got-its-stop-motion-look/
https://stopmotionanimation.com/11/ANIMATION-BASICS
https://www.brianlemay.com/Pages/animationschool/animation/1stsemesteranimation/walks/walkcycle1a.html
https://www.brianlemay.com/Pages/animationschool/animation/lipsyncbook/timing.html
https://www.schoolofmotion.com/blog/how-to-animate-character-takes
https://www.bloopanimation.com/blinking-animation/
https://www.animationmentor.com/blog/tutorial-animate-blinks-eye-movement/
https://www.animationapprentice.org/blog/how-to-animate-eye-darts.html
https://www.annecyfestival.com/about/archives/2015/2015-meetings/2015-conference-summaries/summary:100000393398
https://www.animateclay.com/animating-walks-in-stop-motion
https://animateclay.com/how-to-use-a-surface-gauge-for-animation
https://bloomsburyonlineresources.com/stop-motion-filmmaking/arcs-and-spacing
https://vfxvoice.com/?p=13144738
https://www.austinchronicle.com/screens/how-memoir-of-a-snail-came-out-of-its-shell-13286572/
https://www.bfi.org.uk/sight-and-sound/interviews/audience-will-forgive-bad-animating-theyll-never-forgive-bad-story-adam-elliot-memoir-snail
https://www.awn.com/print/animationworld/nick-park-stays-true-his-early-style-early-man
https://www.europeananimationjournal.com/2025/01/24/exclusive-directors-nick-park-and-merlin-crossingham-on-wallace-gromit-vengeance-most-fowl
https://hfmakademie.de/en/projects/aardman_masterclass_mit_merlin_crossingham
https://www.skwigly.co.uk/shaun-sheep-movie-interview-directors-richard-starzak-mark-burton/
https://www.empireonline.com/movies/features/inside-laika-studios-one-frame-at-a-time/
https://www.inverse.com/entertainment/wildwood-laika-set-visit
https://www.stlmag.com/news/q-and-a-with-brad-schiff
https://www.screendaily.com/features/laika-animation-wizards-talk-studios-most-ambitious-film-yet-missing-link/5137731.article
https://rondexter.com/stop_motion_animation/puppet_flying_shots.htm
https://www.blendernation.com/2010/11/10/tutorial-faking-stop-motion/
https://extensions.blender.org/add-ons/stop-motion-style-animator/
