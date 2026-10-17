# Gold references: what the judges compare against

Owner: the **Creative Director**. Sources: research/04 (eval harness), research/10 section c (look-dev matching), research/16 (what the public clips measure).

## Why this matters

The critic panel and the human A/B tests compare our renders against "gold" references. A win rate of 0.40 against gold means "hard to tell apart from our gold set," not "as good as the best studios." So the gold set is the ceiling on what we can honestly claim, and every report that says the bar was met must also say which gold set it was measured against.

## Sources, in order of preference

### 1. Openly licensed clay animation (primary, ready now)
- **Where:** the Wikimedia Commons categories "Clay animation" and "Multirussia". On Oct 17, 2026 they held 366 files, every one under an open license. After dropping fan work that uses other people's characters (Frozen, Spider-Man, Pingu and similar) and anything under 1280 pixels wide, 199 clips remain. They're listed in `gold/public_catalog.csv` with license, author, source, size and length.
- **Licenses:** almost all CC BY 3.0 (use freely, credit the maker). A few are CC BY-SA, which adds share-alike for anything we derive and publish from them; comparing against them is fine, publishing edited versions is not unless we follow share-alike. Most Vimeo imports carry a license review on Commons with an archived copy of the original page.
- **Shortlist:** `gold/shortlist.md` lists the clips that passed a visual check (real clay on screen, no titles or 2D sections in the chosen segment, no third-party characters) and the segment times. The Multi-Russia series is the only professional studio work in the set; the rest is indie, student and small-studio work.
- **What a gold item is:** a 2 to 4 second segment from a shortlisted clip, or a crop from one for look items, recorded with title, start time, license and author in the provenance file.
- **Spread:** at least 15 different clips, at most 3 items from one maker, and a mix of close-ups, mediums and wides.
- **Quality ceiling:** 720p to 1080p web encodes of indie and TV clay. Passing against this set means "hard to tell from good indie and TV clay at web quality," and reports say exactly that.
- **Held-out slice:** drawn only from shortlisted clips that were never used during tuning. `gold/shortlist.md` marks the clips already used in the Oct 17 R&D pass so they stay in the tuning set.
- **Known risk:** the judge models may have seen some of these clips in training. Run the gold-against-gold check (research/04) and watch for a judge that rates gold suspiciously consistently.
- **Getting the files:** Commons API (`Special:FilePath/<title>`), keep a local copy with a checksum, never re-host.

### 2. A 20-minute probe session by Chris (recommended)
Public footage can't settle the shader's numbers: nobody recorded the lights or camera settings, and web compression smears detail under about 1 mm on screen. A short session of still photos fixes that. No animating needed.
- **Clay:** non-drying plasticine in 3 or 4 earth colors (ochre, terracotta, umber, a chalky off-white).
- **Light:** one small hard lamp as the key, a white card as fill, room lights off, curtains closed.
- **Camera:** phone on a tripod or a solid prop; focus, exposure and white balance locked; no zoom; RAW if the phone offers it.
- **Probes:** a clay ball about 3 cm across, a finger-thick clay cylinder, thin clay sheets about 1, 2 and 3 mm thick backlit by the lamp, a fingerprint pressed into flat clay, a ruler in frame, a mid-grey card (printed 18% grey or grey cardboard), and a color checker card if available.
- **Macro stills:** close-ups of thumbprints, seams and tool marks.
This settles subsurface strength and distance, roughness and the fingerprint scale by measurement (LOOK_DEV.md section 7). Without it those stay judgment calls tuned by eye against the public clips.

Optional: if Chris also wants his own animated clips in the set, the earlier plan still works (4 to 6 clips of 2 to 4 seconds on twos, exported at 24 fps). His votes on pairs that include his own footage are recorded but don't count toward Studio Bar.

### 3. Studio stills (not in the judged set)
Not used in the gold set sent to judge APIs. Optionally, after Chris checks with counsel, a small local set shown only to human raters on Chris's own machine, never uploaded and never on a hosted page.

## Sizes and splits
- At least 30 gold items and at least 30 known-bad items (kickoff prompt, Phase 5).
- The held-out slice lives in the private R&D repo with the held-out benchmark briefs and the hidden judge configuration, outside anything the tune loop reads.

## Raters
- **Tune-loop checkpoints:** Chris.
- **Studio Bar and a production's Final:** 3 to 5 outside raters through the A/B page.
- **A production's Look Lock:** Chris, plus outside raters if available.

## Measured reference ranges
research/16 has what the shortlisted clips measure: poses per second and how often they hold, shot length, contrast, saturation, sharpness and depth of field. The code gates in Phase 5 start from those ranges instead of guesses.

## Data use
Before sending any gold item to the Gemini or OpenAI judges, check each provider's current API data-use terms (training use and retention) and record the result in `decisions.md`. The public clips are already public, but the same check applies to anything Chris shoots.
