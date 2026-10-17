# Gold references: what the judges compare against

Owner: the **Creative Director**. Sources: research/04 (eval harness), research/10 section c (look-dev matching).

## Why this matters

The critic panel and the human A/B tests compare our renders against "gold" references. A win rate of 0.40 against gold means "hard to tell apart from our gold set," not "as good as the best studios." So the gold set is the ceiling on what we can honestly claim, and every report that says the bar was met must also say which gold set it was measured against.

## Sources, in order of preference

### 1. A real clay shoot by Chris (strongly recommended, about 1 to 2 hours)
This is different from the material-texture shoot Chris deferred: it's a small set of real clay clips and stills for judging, not a texture library.
- **Clay:** non-drying plasticine in 3 or 4 colors close to the earth palette (ochre, terracotta, umber, a chalky off-white).
- **Set:** a tabletop with a piece of felt or linen, some wood or card, ideally things from our material families.
- **Light:** one small hard lamp as the key, a white card as fill, room lights off, curtains closed (daylight causes flicker).
- **Camera:** phone on a tripod or a solid prop; a stop-motion app that shoots one frame at a time; focus, exposure and white balance locked; no zoom.
- **Clips:** 4 to 6 clips of 2 to 4 seconds, posed on twos (12 poses per second, exported at 24 fps with each pose held two frames). Ideas: a simple character turning its head and blinking, a squash-and-stretch hop, a hand pressing clay and leaving prints, an object sliding in with a settle.
- **Probes for shader matching** (research/10 section c), shot as stills with the same locked settings: a clay ball about 3 cm across, a finger-thick clay cylinder, thin clay sheets about 1, 2 and 3 mm thick backlit by the lamp, a fingerprint pressed into flat clay, a ruler in frame, a mid-grey card (a printed 18% grey card or grey cardboard), and a color checker card if available.
- **Macro stills:** close-ups of thumbprints, seams and tool marks.
Without this shoot, the clay shader's subsurface settings can't be settled by matching (LOOK_DEV.md section 2.1), and the bar is measured against older or less relevant footage.

### 2. Openly licensed modern clay stop motion
CC0 or CC BY clips from Wikimedia Commons, Vimeo's Creative Commons listings and the Internet Archive. Verify each license on its own page, record URL, license, author and date in the provenance file, and prefer recent color work. Public-domain clay from the 1920s is mostly black and white and only useful for cadence checks.

### 3. Studio stills (not in the judged set)
Not used in the gold set sent to judge APIs. Optionally, after Chris checks with counsel, a small local set shown only to human raters on Chris's own machine, never uploaded and never on a hosted page.

## Sizes and splits
- At least 30 gold items (clips and crops) and at least 30 known-bad items (see the kickoff prompt, Phase 5).
- A held-out slice of the gold set lives in the private R&D repo with the held-out benchmark briefs and the hidden judge configuration, outside anything the tune loop reads.

## Raters
- **Tune-loop checkpoints:** Chris alone. His votes on pairs that include his own footage are recorded but don't count toward Studio Bar, because he'd recognize it.
- **Studio Bar and a production's Final:** 3 to 5 outside raters who didn't make the gold footage, through the A/B page.
- **A production's Look Lock:** Chris, plus outside raters if available.

## Data use
Before sending Chris's footage or any gold item to the Gemini or OpenAI judges, check each provider's current API data-use terms (training use and retention), record the result in `decisions.md`, and exclude anything Chris doesn't want shared.
