# How the best studios handle it, and what we change (research, Oct 17, 2026)

Four Sonnet research agents read published interviews, trade press and conference talks on Laika (faces and performance; camera, light and effects), Aardman (clay craft), and other masters plus CG films that imitated stop motion. Two load-bearing sources were re-read directly in the original pages afterwards (Aardman on twos in Post Magazine; Sam Fell on thumbprints and twos in MovieMaker); the rest rest on the agents' reading. Their full sourced reports are in `research/studios/`; every line there carries a URL and [U] marks anything unverified. This file is the short version: the findings that change how we build, each with its source report, and where our own measurements (research/16) agree or disagree.

One correction to the brief: Laika's films are not clay. Their puppets are silicone, foam and resin with 3D-printed replacement faces. Aardman is the clay studio. Both matter, for different things.

## 1. Two schools, and which one is ours

- **The visible-hand school** (Aardman, Adam Elliot, Henry Selick, Wes Anderson, del Toro's Pinocchio): fingerprints, lumps and asymmetry are kept on purpose; motion steps on twos with threes mixed in; imperfection is part of the pitch. Aardman's word for it is "thumbiness". Aardman smoothed prints away on Chicken Run (2000), decided that drained life from the characters, and reversed it. (aardman-clay 2.4; masters A1 to A4)
- **The invisible-machinery school** (Laika): handmade materials are celebrated, but anything that reads as a technical defect (face seams, color drift between printed faces, flicker, accidental fur boil, rigs) is removed in post. Bodies move on ones; faces change up to every frame; characters are never fully still. (laika-faces 2, 4)
- **Ours:** Chris's direction ("the maker's hand shows") puts us in the visible-hand school for surfaces and timing, with Laika's discipline on defects: no flicker, no color drift, no rigs, no accidental artifacts. Laika's ones-and-breathers style stays available as a per-production choice in the bible.

## 2. Timing

- Aardman, Vengeance Most Fowl: characters on twos at 24 fps, camera moves on ones, kept in sync with a "one-and-a-half" method; Farmageddon used more ones for complex camera moves; Dawn of the Nugget "starts off in doubles" and matches CG elements to doubles. (aardman-clay 4.1)
- Laika, ParaNorman: bodies on ones, faces on twos; Kubo moved faces to every frame. No Laika source describes bodies on twos, and Aardman's own team describes its twos as "unlike perhaps Laika" (Post Magazine, re-read). Wildwood is reportedly on ones (one source [U]). On The Boxtrolls, CG puppets were scripted to hold faces 2 to 3 frames like the real ones. Travis Knight: twos give "more pop", ones give subtlety. (laika-faces 2.1, laika-camera)
- Selick mixes twos and threes on purpose; Anderson shot Mr. Fox and Isle of Dogs mostly on twos; Pinocchio shot lateral camera tracks on ones to avoid strobing. (masters A2 to A4)
- CG that imitated stop motion: The Lego Movie animated on twos and went to threes or fours for fast action because CG "tends to look too smooth"; The Willoughbys ran on twos with occasional threes, effects on threes and fours. (masters B1, B2)
- **Our measurements agree:** real clay ranges from about 9 to 30 new poses per second, only a quarter of public clips are mostly twos, and much of the "ones" is camera movement. Held frames are exact copies. (research/16)
- **Rule:** cadence is authored per pose and per shot. House default: bodies and faces on twos, camera on ones, ones flagged for fast action and complex camera moves, threes allowed for slow or stylized beats. Laika-style ones is a bible-level option.

## 3. Holds

- Laika's goal is that characters never look fully still: breather mechanisms, "jetpack" micro-move rigs. (laika-faces 2.2)
- Real clay clips do hold still: in the public set about 9% of screen time sits in identical frames for 5 or more frames. (research/16)
- **Rule:** keep our moving-hold rule for performance holds (MOTION.md 12 and 13); allow true still holds up to about a second for comic beats and inserts.

## 4. Faces

- Aardman mouths are clay replacements: 14 per puppet on Dawn of the Nugget, 24 for the lead, more than 24 on Early Man, about 20 per character in the 1990s; prebuilt mouths are blended into the face live on set. Eyes are resin or glass with a pinhole, moved with a pin, swapped every two frames on Dawn. Gromit acts with brows and glances, no eyelid animation. (aardman-clay 3)
- Laika splits faces into independent brow and mouth libraries that multiply (Kubo: 11,007 mouths times 4,429 brows); eyes and lids stay on the head; faces mount with magnets; the split line is cleaned in post. Faces are planned in Maya, timed to the dialogue, approved as a playblast, then printed. (laika-faces 1)
- Lego Movie faces were a library of 2D expressions applied like replacement stickers; Flushed Away replaced mouths with sculpted shapes rather than muscle deformation. (masters B1, B2)
- **Rule:** faces are discrete swaps from a library, never blend shapes. Default 14 mouths per character, up to 24 for a hero speaker; brows as a separate small library; eyes and lids stay on the head. Face changes follow the body's grid by default (Aardman shows no evidence of mouths on ones); ones for faces is a per-character option for subtle close-ups (Laika).

## 5. Surfaces: fingerprints, dirt, matte, boil

- **Fingerprints go on faces too.** Prints on Gromit's forehead when his brow creases; Park insisted on keeping prints on Early Man faces; Sam Fell tells animators to leave thumbprints on the faces; prints are even authored into silicone parts. Our rule "faces kept cleaner" was wrong. (aardman-clay 2.4) No source gives a ridge spacing; our 0.41 to 0.46 mm is consistent with real fingertips on a 15 to 18 cm puppet [U].
- **Dirt resets per shot.** Plasticine picks up dirt and dust; animators wipe it with baby wipes or swap in a clean head between shots. (aardman-clay 1.5) Our public-clip close-ups show grey handling smudges on pale clay.
- **Matte.** Dawn of the Nugget dusted puppets with icing sugar for an even matte finish (replacing toxic silica); non-shiny silicone formulas; Aardman tests clay and silicone side by side under white, blue and warm light. Tristan Oliver: there are "only so many ways to light a piece of Plasticine", and the gap between exposed and overexposed is very small. (aardman-clay 1.7, 1.4)
- **Boil is per material.** Aardman stiffens Shaun's fleece with PVA so it doesn't boil, but welcomed twitchy hair on Early Man. Anderson wanted fur boil on Mr. Fox. Laika minimizes boil and stylized Link's fur to avoid it; wind on held poses is added deliberately, in compositing. (aardman-clay 2.5; masters A4; laika-faces 3.3)
- **Asymmetry and jitter.** Elliot's puppets are "very lumpy and asymmetrical"; Flushed Away's director had modelers spend half a day making each model asymmetrical; Lego bricks got a small random placement jitter and over 2,000 bricks were surfaced with scratches and fingerprints from macro photos of real bricks. (masters A1, B1, B2)
- **Rule:** fingerprints on faces, hands and handled areas at real scale, plus authored prints on silicone-class parts; pale clays get handling smudges and sparse dust, regenerated per shot; one matte response for clay and silicone with an optional "sugar dust" sheen; skin never clips (at most 0.1% of skin pixels at white); boil is a per-material parameter (clay: per pose, low to moderate; hair and fur: flag; cast silicone and stiffened fleece: zero).

## 6. Camera and depth of field

- Aardman: close-focus primes, 24 mm as the world lens, often 18 mm for close puppet shots, Were-Rabbit sometimes at T22 with puppets very close to the lens, "stop the lens down as much as possible"; Canon 1D X Mk III bodies, about 60 across 40 sets on Vengeance Most Fowl. (aardman-clay 5.1, 5.2)
- Isle of Dogs: 20 mm default, 28 mm for most close-ups, aperture wound "right down to the bottom" and still short of depth, so planes were shot separately and composited. Pinocchio used lenses from 15 mm up. (masters A3, A4)
- Laika is not a deep-focus school: no Laika f-stop is published; Coraline's DP valued the large sensor for softening backgrounds; Missing Link shot with real tilt-shift lenses (Canon TS-E 17, 24, 45 and 90 mm) to place the plane of focus; Wildwood's DP calibrated depth of field with f-stop tests. (laika-camera 1)
- Real miniature depth of field is shallow even at f/11: a 35 mm lens at 0.4 m has about 80 to 90 mm of depth (agent's and our arithmetic). Deep focus in stop motion comes mostly from wide lenses.
- **Our measurements agree:** real clay footage is only about 1.6 times sharper in the center than at the edges; our test render at 35 mm and f/11 was 9 times sharper in the center. (research/16)
- **Rule:** default lenses 20 to 28 mm for mediums and wides, 18 to 35 mm for close-ups; f/16 default, up to f/22 on close shots; depth of field computed from true scale; focus pulls and soft backgrounds allowed as a choice; plane-split compositing allowed for hero shots. Never a fake tilt-shift gradient added in post (it only "just barely" reads as miniature and an in-focus foreground breaks it; masters B5). A real lens tilt, computed in the camera like Laika's tilt-shift lenses, is an optical choice and allowed with the DP's sign-off.

## 7. Light and flicker

- Aardman's workhorse is a small profile spot (Micro Ellipse) with shutters and gobos, now mostly LED; diffused LED strips for big flat sets; small LEDs on wire for backlight. Consistent exposure per frame is "critically important". Fire and candle flicker is engineered to be repeatable (a stepper-driven disc; bulbs varied between 10 and 11 volts). Dragonframe shoots several exposures per frame (key, ambient, beauty), up to 16 on Dawn. (aardman-clay 5.3 to 5.5)
- Isle of Dogs exteriors were lit "white and nearly always quite flat", with a big diffused source. (masters A4)
- Laika's VFX team removes overnight fluctuations and flicker from plates; on ParaNorman, overheating camera bodies caused black-level flicker, fixed with cooling, voltage regulators and histogram checks. Laika shoots several passes per frame (flat, shaping, UV black-light, green) and lights its CG elements with on-stage HDRIs and survey data so they match the plates. (laika-faces 3.7; laika-camera 2, 4)
- Aardman tried cloning Norbots across positions and it looked wrong because "the lighting doesn't change": real frames carry organic variation. (masters B5)
- **Rule:** stage light near zero variation per pose; our per-pose sensor noise supplies the organic difference between poses; fire and candle sources flicker deterministically on their own light only; light groups per source as our version of multi-exposure. Our "no HDRI skies" rule stands for lighting puppets and sets; Laika's HDRIs exist to match CG to real plates, a problem we don't have.
- Color: Laika graded Kubo separately for 2D, 3D and HDR and ran a 16-bit linear EXR chain on Boxtrolls; no Laika source mentions a single show LUT. Our one-LUT rule comes from Isle of Dogs and stays as our choice. (laika-camera 3)

## 8. Motion blur

- Plates have none. Exceptions in the record: Aardman's chases in The Wrong Trousers, A Close Shave and Were-Rabbit used go-motion to blur the moving background; Laika's compositors add blur when needed ("spot motion blur in post" on Kubo's fights, with clear-plastic smear pieces in camera) and printed smear faces (Norman's triple nose); Lego Batman added partial blur to water; The Willoughbys used a little to hide pans. (aardman-clay 5.7; laika-faces 3.7; laika-camera 4; masters B1, B2)
- **Rule:** never on puppets or props. Allowed per element with VFX Supervisor and Director sign-off: background blur in a chase (go-motion style), liquids and splashes, and printed-style smear replacements for a single fast frame.

## 9. Effects made to match handmade

- Aardman keeps CG water "restrained and rounded" because live-action-looking water in a stop-motion world "doesn't work"; practical water from hair gel, wax and Vaseline; splashes animated frame by frame in clear plastic. (aardman-clay 5.6)
- Pinocchio stripped lateral flow from water sims so the surface moves like a rubber sheet, modelled explosions and clouds on cotton and raindrops on glycerin, and fought sims that don't like holding a pose for two frames. (masters A3)
- Kubo styled its ocean after woodblock prints. (masters B3)
- **Rule:** effects are built from the analogue materials stop motion really uses (cotton smoke, cellophane fire, gel water, resin drops), stepped at the shot cadence; no smooth continuous sims under stepped puppets.

## 10. What gives a fake away (collected)

Too smooth motion and interpolated frames; motion blur on characters; polish ("airbrushed photorealism", Selick); identical frames with no lighting change; perfect symmetry and straight edges; cloth and hair that move on their own; smooth, fluid-looking water; fake tilt-shift; unstable cadence (AI clips drifting between about 12 and 8 poses per second, vendor claim [U]). Laika's own Wildwood trailer drew "too polished" comments. (masters B5)

## 11. Reference and planning

- Laika made live-action reference mandatory on Kubo ("Everybody is shooting reference"), with a warning never to rotoscope it. Park acts every scene on video for the animators; Farmageddon animators filmed 3 or 4 versions per scene. (laika-faces 2.4; aardman-clay 3.2)
- Dawn of the Nugget captured 97% of shots on the first take; Aardman reports about a 1% reshoot rate. (aardman-clay 4.3, 3.2)
- **Rule:** hero shots get acted reference (Chris on a phone, or generated), used for timing and key poses only, never traced frame by frame.

## Changes made in the kit
MOTION.md (cadence, faces, holds, reference), LOOK_DEV.md (fingerprints on faces, dirt per shot, matte, boil per material, camera defaults, motion-blur exceptions, flicker exception, CG tells), FABRICATION.md (clay heads and hands on silicone-class bodies, asymmetry pass, mouth counts), DESIGN_AND_WORLD.md (effects from analogue materials).
