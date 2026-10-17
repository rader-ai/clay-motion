# LAIKA: character faces and performance in stop motion

Research date: 2026-10-17. Scope: Coraline (2009), ParaNorman (2012), The Boxtrolls (2014), Kubo and the Two Strings (2016), Missing Link (2019), Wildwood (2026, US release 2026-10-23).
Purpose: methods that translate to a CG (Blender, from code) stop-motion pipeline, and where our current rules differ.

## How to read this report

- Every factual line ends with a source link. `[U]` marks anything unverified, single-source, or inferred by me.
- When sources disagree, both values are given.
- Method caveats (important):
  - Most pages were read through a summarizing fetch tool, not raw HTML. Numbers and short quotes are as the tool returned them. Re-check any figure before it goes into a spec or public copy.
  - Direct curl to some hosts (cgw.com) was blocked by the sandbox proxy, so the CGW "ones/twos" sentence was confirmed by asking the fetch tool for verbatim text, twice, with consistent results. It was not read from raw HTML.
  - The web-search budget ran out near the end of the session. Gaps this left: tie-downs (nothing found), a second independent source for "bodies on ones", and duplicate-puppet consistency (only partial).
  - Not readable (blocked or errored): Variety, Deadline, Collider, Yahoo (Wildwood VFX interview), AP original, Entertainment Weekly, American Cinematographer text for Kubo, Hollywood Reporter Coraline piece. The AP piece was read through an AJC copy.
- Quotes are short on purpose. Everything else is paraphrased.

---

## 1. Replacement face systems, film by film

### 1.1 Face counts (the scale trend)

Counts vary by source. Both are listed where they conflict.

- Nightmare Before Christmas baseline: Jack Skellington had roughly 800 faces/expressions. ([Engadget 2012](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html), [Post 2009](https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx))
- Coraline (2009):
  - About 20,000 printed faces. ([Stratasys case study](https://www.stratasys.com/en/resources/case-studies/Laika), [TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/))
  - Alternate figure: 6,333 faces giving 207,000 possible expressions. ([3DPrint.com](https://3dprint.com/119975/laika-academy-awards-3d-print/), [BU](https://www.bu.edu/cfa-magazine/2018/10/10/making-the-moon-beast/)). [U] The 6,333 looks like a character-level or early count, not the film total.
  - Possible expressions: over 205,000 ([Post](https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx)), about 200,000 ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx)).
  - Travis Knight's own description: about 600 mouths and about 300 brows for Coraline. ([Den of Geek](https://www.denofgeek.com/movies/travis-knight-interview-kubo-coraline-laika))
- ParaNorman (2012):
  - Norman alone: about 8,000 faces ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx), [fxguide](https://www.fxguide.com/?p=35589)) or about 8,800 ([Animation Magazine](https://animationmagazine.net/wordpress/features/he-hears-dead-people)). Neil about 3,000 ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx)).
  - Film total: about 30,000 ([Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html)), 31,000 face parts ([fxguide](https://www.fxguide.com/?p=35589)), 33,000 ([Cartoon Brew](https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html)), 40,000 ([Stratasys](https://www.stratasys.com/en/resources/case-studies/Laika), [TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)).
  - Norman about 1.5 million possible expressions ([Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html)); 1.4 million in [Cartoon Brew](https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html).
  - The faces filled 1,257 archival boxes. ([fxguide](https://www.fxguide.com/?p=35589))
- The Boxtrolls (2014):
  - Film total: over 52,000 ([Cartoon Brew](https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html)), over 53,000 ([Vice](https://thecreatorsproject.vice.com/blog/unpacking-the-stop-motion-magic-of-the-boxtrolls)), 55,000 ([Animation Magazine](https://animationmagazine.net/?p=186866)), 56,000 ([Stratasys](https://www.stratasys.com/en/resources/case-studies/Laika), [TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)). About 40% were discarded ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)).
  - Eggs: about 1.4 million possible expressions, about 15,000 printed. ([Vice](https://thecreatorsproject.vice.com/blog/unpacking-the-stop-motion-magic-of-the-boxtrolls)) Eggs' face is built from 66 parts, some printed and some hand-soldered. ([Portland Monthly](https://www.pdxmonthly.com/arts-and-culture/2015/10/what-s-next-for-portland-s-animation-powerhouse-laika))
- Kubo and the Two Strings (2016):
  - Film total 64,000 printed faces. ([Stratasys](https://www.stratasys.com/en/resources/case-studies/Laika), [Guinness](https://www.guinnessworldrecords.com/world-records/693110-most-3d-printed-faces-made-for-a-stop-motion-film), [Screen Daily](https://screendaily.com/features/how-laika-made-ambitious-stop-motion-animation-missing-link/5145578.article))
  - Kubo (the character) 23,197 faces on the Z650 and Monkey 15,581 on the Connex3. ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx)) BU gives 23,187. ([BU](https://www.bu.edu/cfa-magazine/2018/10/10/making-the-moon-beast/)) fxguide says "over 23,000" faces across Kubo puppets. ([fxguide](https://www.fxguide.com/?p=186839)) [U] fxguide's figure most likely means the Kubo character only.
  - Possible expressions: Kubo over 48 million ([fxguide](https://www.fxguide.com/?p=186839), [Den of Geek](https://www.denofgeek.com/movies/travis-knight-interview-kubo-coraline-laika)). fxguide splits this as 11,007 mouth expressions and 4,429 brow expressions. My check: 11,007 x 4,429 = 48.75 million, so the claim is multiplicative upper x lower. Beetle over 13 million, Monkey over 30 million ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx)). Conflict: 3DPrint.com says over 22 million, up from 1.5 million. ([3DPrint.com](https://3dprint.com/140830/laika-3d-printing-kubo/))
  - Moon Beast: 1,417 faces swapped between frames. ([BU](https://www.bu.edu/cfa-magazine/2018/10/10/making-the-moon-beast/))
- Missing Link (2019):
  - 106,000+ faces, a Guinness record. ([Guinness](https://www.guinnessworldrecords.com/world-records/693110-most-3d-printed-faces-made-for-a-stop-motion-film), [AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link), [Fraunhofer](https://www.igd.fraunhofer.de/content/dam/igd/pressemitteilungen/2019/igd-2019-04-11_fraunhofer_3d-printing_technology_impresses_animation_studio_laika.pdf)) Earlier counts: about 102,000 ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)) and "100,000+" ([OPB](https://opb.org/news/article/laika-missing-link-behind-the-scenes-qa-oregon)).
  - Split by character: about 39,000 for Lionel (37%), 27,000 for Link (26%), 13,000 for Adelina (12%); three leads were about 75% of all faces. ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link))
- Wildwood (2026): 140,000 faces, beating the Missing Link record, per Brian McLean. ([Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit)) [U] Single source; Guinness has not been checked for a new entry.
- Derived [U]: faces per second of finished film rose from about 10.6 (Kubo) to about 19.6 (Missing Link) and about 17.7 (Wildwood). My arithmetic from the counts above and runtimes of about 101, 90 and 132 minutes. Runtimes: 132 min for Wildwood ([Wikipedia](https://en.wikipedia.org/wiki/Wildwood_(film))); 90 min for Missing Link ([Fabbaloo](https://www.fabbaloo.com/2019/03/106000-3d-printed-faces)); Kubo's 101 min is from memory and unsourced here.

### 1.2 Upper/lower face split and how faces are partitioned

- Faces are split into separate pieces so combinations multiply. ([Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html))
- ParaNorman: mouth and eyebrow parts were the main expression pieces; kits also had foreheads and cheeks. Internal mechanisms moved the eyes, eyelids and ears; the outer face was a magnet-held mask. ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx))
- Coraline: the faint seam was where the head's lower half meets the upper head. ([Post](https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx)) Selick describes the split as a deliberate way to expand facial vocabulary, because brow changes mix with different lower-face shapes. ([BFI 2024](https://www.bfi.org.uk/sight-and-sound/interviews/stop-motion-henry-selick-coraline))
- Boxtrolls: each face has separate sections for brows, eyes and mouth. ([Animation Magazine](https://animationmagazine.net/?p=186866))
- Kubo: the face is split into eyebrow and mouth pieces that swap independently. ([TheWrap](https://thewrap.com/kubo-two-strings-biggest-stop-motion-animation)) The artists decide where the mouth/brow split falls per character. ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx))
- Where the line sits: VFX supervisor Steve Emerson says the faces are split down the center, "right between the eyes", which leaves a horizontal line across every character. ([Intel/LAIKA webinar](https://intel.com/content/dam/www/central-libraries/us/en/documents/2022-08/laika-webinar-customer-spotlight-transcript.pdf))
- Missing Link: printed faces are essentially masks with eye holes; the eyes and eyelids stay on the main head. ([Fabbaloo](https://www.fabbaloo.com/2019/03/106000-3d-printed-faces))
- Wildwood: faces are designed without eyes and pop on magnetically. ([Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit))
- Special case, Link's fur: his face is tied to his fur, so each replacement face carries a printed ring ("driver") with magnets; animators swap a driver on nearly every frame. Developing the driver system took about a year. ([Variety](https://variety.com/2019/artisans/production/laika-missing-link-character-design-1203166298))
- Head internals: Norman's mechanism has 78 parts ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx)); Kubo's head holds 70+ mechanical parts in a head about golf-ball size ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx)); Missing Link heads can have up to 60 inner pieces ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/)).

### 1.3 Library design: base kits versus shot-specific faces

- Early films (Coraline to Kubo) built "kits of expressions" and phoneme-style mouth sets that were reused across shots. ([Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit), [Kennedy Compounds](https://www.thekennedycompounds.com/the-hands-of-laika-2020/2020/2/3/ypgqw86c11pf9fjzbkyk85fl0x644z))
- ParaNorman kits: each kit covered a set of dialogue lines with one emotion (smile, frown). ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx))
- Single-use shot-specific faces appeared sparingly on ParaNorman and heavily on Boxtrolls. ([Cartoon Brew](https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html))
- Kubo: a small digital team built a big expression library; Knight often asked for subtle changes (such as a slight brow tilt), which strained the kit approach, so faces were animated and printed for specific shots. ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx))
- Missing Link: first film to print custom facial performances for every character in every shot. Producer-side phrase: a "clean slate" for facial animators. ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link), [Screen Daily](https://screendaily.com/features/how-laika-made-ambitious-stop-motion-animation-missing-link/5145578.article)) Workflow quote from McLean: animate a unique line of dialogue for one shot. ([Stratasys](https://www.stratasys.com/en/resources/case-studies/Laika))
- Wildwood: each expression has its own bespoke sculpt, faces are never reused, and a boxed "Expression Kit" holds 24 faces, one per frame of a second of film. ([Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit), [JoBlo](https://www.joblo.com/wildwood-behind-the-scenes-tour/))
- The stated reason for the cost: McLean says the only reason for the tech is the performance. ([Stratasys](https://www.stratasys.com/en/resources/case-studies/Laika)) The studio says printing costs more and takes more time and is used for the performance quality it enables. ([Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit))

### 1.4 How faces are animated digitally before printing

- Clay maquette scanned, rough topology in Maya, refined in ZBrush, test print, then retopo in TopoGun. ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx), [CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx))
- Maya facial rigs per puppet (ParaNorman rigger: Michael Laubach). Rigs had to respect print limits, for example a lip stretched too thin could break when printed. ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx))
- Boxtrolls: animators performed each line of dialogue, performances were broken into poses that became facial kits, Photoshop was used for facial textures. ([AWN Boxtrolls](https://awn.com/animationworld/on-set-laikas-boxtrolls))
- Emerson: "We use Maya to create thousands of facial expressions." A new face can be produced in about a day. ([Autodesk](https://www.autodesk.com/customer-stories/laika-blends-digital-and-physical))
- Per-shot approval loop (ParaNorman): animator plus a facial animation specialist build the expressions for a shot and cut a playblast timed to the dialogue; the approved playblast becomes a shopping list for the face librarian. ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx))
- Kubo: Maya playblasts go to editorial; if the director approves, the CG animator orders pre-printed faces or special ones. ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx))
- Missing Link: a dedicated facial animator (Benoit Dubuc) matched Link's face performance to his body movement. ([TheWrap](https://www.thewrap.com/missing-link-laika-hardest-thing))
- Coraline roles: Brian McLean (facial structure supervisor), Martin Meunier (facial animation designer). Facial expression flow was studied in Maya, and Selick directed expressions in previs and during the shoot. ([Post](https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx)) Meunier said they wanted to keep a handmade look, not a too "computery" one. ([3DPrint.com](https://3dprint.com/119975/laika-academy-awards-3d-print/))

### 1.5 Lip sync: planning and timing

- Coraline: dialogue audio was laid out frame by frame; a facial-animation specialist picked faces and made a small movie; each animator got a sheet saying which face to use on each frame. Supervising animator Anthony Scott let animators focus on body nuance because the face was handled separately. ([Post](https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx))
- Phoneme shapes strung together for lip sync were the Coraline-era mouth sets. ([Kennedy Compounds](https://www.thekennedycompounds.com/the-hands-of-laika-2020/2020/2/3/ypgqw86c11pf9fjzbkyk85fl0x644z)) ParaNorman modelers hand-finessed phoneme libraries for each character. ([Animation Magazine](https://animationmagazine.net/wordpress/features/he-hears-dead-people))
- ParaNorman rigs were driven from dialogue samples and 2D drawings. ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx))
- Missing Link: animators work from face kits with hundreds of faces and an X-sheet that says when each face changes. ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/)) ParaNorman: the librarian packed the physical parts with an X-sheet and sent them to the set, after color and registration tests. ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx))
- Kubo: Schiff describes using a line of dialogue from another McConaughey film so Beetle's mouth shapes feel like they come from his voice. ([On Animation](https://onanimation.com/2016/08/19/crafting-the-epic-world-of-kubo-a-conversation-with-laikas-animation-supervisor-brad-schiff/))
- Wildwood: animators work to temporary sound with little Foley and only pieces of the score. ([But Why Tho](https://butwhytho.net/2026/10/wildwood-interview/))
- Face change cadence (see also 2.1): 12 to 24 swaps per second on Boxtrolls ([AWN Boxtrolls](https://awn.com/animationworld/on-set-laikas-boxtrolls)); every other frame on ParaNorman, every frame on Kubo ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx)); up to one new face per frame on Missing Link ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)).

### 1.6 Mounting (magnets) and eyes

- Magnets: ParaNorman outer face is a magnet-held mask ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx)); Boxtrolls faces snap on magnetically ([Cartoon Brew](https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html)); Missing Link: magnets installed during post-processing ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)), with a code system that tracks which face goes in which sequence ([Fabbaloo](https://www.fabbaloo.com/2019/03/106000-3d-printed-faces)); Emerson: animators are basically snapping faces on with magnets ([Intel](https://intel.com/content/dam/www/central-libraries/us/en/documents/2022-08/laika-webinar-customer-spotlight-transcript.pdf)).
- Eyes and eyelids live on the head, not on the swap piece. Boxtrolls: machined internals gave animators direct control of eyeballs and eyelids for subtle moves, squints and blinks ([AWN Boxtrolls](https://awn.com/animationworld/on-set-laikas-boxtrolls)). Eyes and lids moved independently ([Portland Monthly](https://www.pdxmonthly.com/arts-and-culture/2015/10/what-s-next-for-portland-s-animation-powerhouse-laika)). Wildwood: a mechanism behind the faceplate lets the puppet blink, move eyes and make other gestures; parts move independently and are fragile ([JoBlo](https://www.joblo.com/wildwood-behind-the-scenes-tour/)). Nerdist (Missing Link): eyeballs built separately and inserted or removed as needed ([Nerdist](https://nerdist.com/article/missing-link-laika-studios-what-we-learned/)).
- Conflict on who finishes eyelids on Missing Link: BoxOfficePro says animators adjust eyeballs and eyelids with an X-Acto blade during shooting; Fabbaloo says technicians do it to finish each expression. ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/), [Fabbaloo](https://www.fabbaloo.com/2019/03/106000-3d-printed-faces))
- Blink specifics (how many frames, which eases) were not found in any source. [U]

### 1.7 Seam lines: how they are hidden

- Coraline: computers erased the faint seam where lower head meets upper head, plus the rigs ([Post](https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx)). Selick wanted the seams kept; Phil Knight wanted them gone; the studio digitally painted them out, which Selick calls unnecessary expense ([BFI 2024](https://www.bfi.org.uk/sight-and-sound/interviews/stop-motion-henry-selick-coraline)).
- ParaNorman: after editorial, VFX painted out seams between face parts, with rig removal and set reconstruction ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx)); the VFX list names "face replacement line removal" ([fxguide](https://www.fxguide.com/?p=35589)). The in-house VFX team of about 60 worked on an estimated 35-40% of shots ([Animation Magazine](https://animationmagazine.net/wordpress/features/he-hears-dead-people)).
- Boxtrolls: seams removed in post ([Animation Magazine](https://animationmagazine.net/?p=186866)).
- Kubo: seam lines removed and cleaned up in post, which takes less time than the earlier method ([fxguide](https://www.fxguide.com/?p=186839)).
- Missing Link: VFX digitally removed the seam where each faceplate meets the head, across all 106,000 faces ([Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link)); paint artists did seam repair and "de-chattering", fixing frame-to-frame inconsistencies on the printed faces, using Mocha Pro and Silhouette ([Boris FX](https://borisfx.com/news/oscars-2020-best-animated-feature-film-nominee-missing-link/)). Of 1,486 shots, 446 got 2D rig and seam cleanup only ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)). Over 1,000 rigs were removed ([Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link)).
- Emerson on the cost of the split: more expressions from fewer pieces, but a visible line on every face that VFX must clean ([Intel](https://intel.com/content/dam/www/central-libraries/us/en/documents/2022-08/laika-webinar-customer-spotlight-transcript.pdf)).
- Wildwood seam handling: not found. [U]

### 1.8 Printing technology timeline

- Coraline: Objet Eden260 PolyJet, white plastic only, faces hand-sanded then hand-painted, with separate teeth/denture pieces ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/), [Fabbaloo](https://www.fabbaloo.com/2019/03/106000-3d-printed-faces), [Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link)). PolyJet layers about 15 microns; the printer cost about $110,000 then ([Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html)). First stop-motion feature with 3D-printed faces ([3DPrint.com](https://3dprint.com/119975/laika-academy-awards-3d-print/)).
- ParaNorman, Boxtrolls: color powder printers (3D Systems ZPrinter 650; five on site by Boxtrolls). Color is jetted into powder about 1/16 inch deep, giving a soft subsurface look; parts are fragile until hardened ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx), [Cartoon Brew](https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html), [Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html)). ParaNorman was the first stop-motion film made with a color 3D printer ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)).
- Kubo: Z650 for humans; Stratasys Connex3 (beta multi-material resin) for Monkey, Beetle and Moon Beast because the powder process could not do hard edges and fine hair ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx), [fxguide](https://www.fxguide.com/?p=186839)). The Connex3 prints three colors at once, makes color by dithering droplets, and clear resin was added as a color for translucency, a first at LAIKA ([fxguide](https://www.fxguide.com/?p=186839)). Independent developer Jon Hiller wrote custom slicing software for gradients ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx)); the palette grew from 46 to 256 colors via AMF and a spreadsheet ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)).
- Missing Link: Stratasys J750 plus Fraunhofer Cuttlefish voxel driver; the studio got the first five J750 units in 2016 ([Fabbaloo](https://www.fabbaloo.com/2019/03/106000-3d-printed-faces)); six J750 and two Connex3 installed by March 2019 ([Fabbaloo](https://www.fabbaloo.com/2019/03/106000-3d-printed-faces)). Cuttlefish chosen for color consistency and geometric accuracy ([Fraunhofer](https://www.igd.fraunhofer.de/content/dam/igd/pressemitteilungen/2019/igd-2019-04-11_fraunhofer_3d-printing_technology_impresses_animation_studio_laika.pdf)). J750 color combinations: 360,000 ([Stratasys](https://www.stratasys.com/en/resources/case-studies/Laika)) versus over 500,000 ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)). Droplets (voxels) sit side by side rather than overlapping, a pointillist build ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/)).
- Throughput: Boxtrolls, a small character like Eggs yields 100-150 mouths per day, one very large face only 12 per day ([Cartoon Brew](https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html)). Missing Link: five printers often ran 24 hours a day, about 2,000 faces per week ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)); about 90 minutes per row of faces ([Movieweb](https://movieweb.com/missing-link-set-visit-laika-studios/), [U] low-reliability page).
- Team size: RP department about 30 on Coraline, about 90 on Missing Link ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/)); 50 on Boxtrolls, half modeling and half processing ([Cartoon Brew](https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html)); 60-70 on Wildwood ([JoBlo](https://www.joblo.com/wildwood-behind-the-scenes-tour/)).
- Academy recognition: McLean and Meunier won a Scientific and Engineering Award (ceremony 2016-02-13) for rapid prototyping in character animation. The citation names advances in expressiveness, facial animation, motion blur and effects animation ([CGChannel](https://www.cgchannel.com/2016/01/mari-and-tweak-rv-creators-win-academy-awards/), [3DPrint.com](https://3dprint.com/119975/laika-academy-awards-3d-print/), [fxguide](https://www.fxguide.com/?p=186839)).

### 1.9 Sanding, painting, coating

- ParaNorman: parts are sanded and dipped in superglue to harden; new jobs appeared for people who sand and finish, and for face librarians ([Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html)). Rapid prototyping took 10 steps with 5-6 hours of cleaning and coating ([fxguide](https://www.fxguide.com/?p=35589)).
- Boxtrolls: brush and blow off powder, sand, dip in liquid superglue, test, spray clear coats for shape and color stability; sand edges, smooth inconsistencies, apply pastels by hand ([Cartoon Brew](https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html)).
- Kubo: faces are cleaned, sanded and tested before delivery on shoot days ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx)).
- Missing Link: wash off supports, soak in sodium hydroxide solution for an hour, rinse an hour, dry, pick residual support, sand only if needed, clear crystal coat, hand-painted gloss coats ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)). Conflict on finish: AWN lists multiple clear "dull coat" layers ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)).
- Share needing no hand-sanding: about 80% ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)) versus about 90% ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)). Birth.Movies.Death says "no longer need sanding" ([BMD](https://birthmoviesdeath.com/2019/03/18/a-visit-to-the-colorful-and-adventurous-set-of-missing-link.html)), which overstates both. [U]
- Freckles on Coraline: modeled about 1/3000 inch deep and filled with a drop of color by painters ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)). Hand-painted blush shifted between frames, which forced workarounds like physical freckle markers ([Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html)).

### 1.10 Color consistency between printed faces

- ParaNorman: color designed in Photoshop on flattened models so paint is built into the print; Pantone chips printed as a palette; early skin tones printed badly; color matching used 10-15 copies of one smile; face librarian Tim Yates matched parts for continuity ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx), [Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html)). Texture artist Tory Bryant built skin by cross-hatched cyan, magenta and yellow ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/)).
- Boxtrolls: face librarians hand-touch pieces to keep color consistent, since humidity can change prints ([Animation Magazine](https://animationmagazine.net/?p=186866)).
- Motivation for J750: hand-painting and powder printing were inconsistent from frame to frame; McLean calls the J750 workflow repeatable and accurate ([Fabbaloo](https://www.fabbaloo.com/2019/03/106000-3d-printed-faces), [Stratasys](https://www.stratasys.com/en/resources/case-studies/Laika)). Fraunhofer says matching each model's color to earlier frames was LAIKA's main challenge ([Fraunhofer](https://www.igd.fraunhofer.de/content/dam/igd/pressemitteilungen/2019/igd-2019-04-11_fraunhofer_3d-printing_technology_impresses_animation_studio_laika.pdf)).
- Printer-to-printer variance is a standing issue: printed parts vary slightly from print to print, so printer maintenance is a constant priority ([AWN Boxtrolls](https://awn.com/animationworld/on-set-laikas-boxtrolls)).
- Even with that, VFX still "de-chatters" the faces in post ([Boris FX](https://borisfx.com/news/oscars-2020-best-animated-feature-film-nominee-missing-link/)).

---

## 2. Animation timing

### 2.1 Ones and twos

- ParaNorman (CGW, 2012): "Animators typically move the bodies on 'ones' and faces on 'twos'." Bodies are posed 24 times per second; face parts change 12 times per second. ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx))
- Same article, Travis Knight: animating on twos "gives us more pop"; for more subtlety they might animate faces on ones. ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx))
- Kubo: animators changed expressions 24 times per second, rather than every other frame as on ParaNorman, to allow subtler performances. ([CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx), [Kennedy Compounds](https://www.thekennedycompounds.com/the-hands-of-laika-2020/2020/2/3/ypgqw86c11pf9fjzbkyk85fl0x644z))
- Boxtrolls: faces were swapped up to 12-24 times per second. ([AWN Boxtrolls](https://awn.com/animationworld/on-set-laikas-boxtrolls))
- Missing Link: standard stop motion typically holds an expression for two or three frames; Missing Link reached 12 to 24 different faces per second, up to a new face every frame. ([TCT](https://www.tctmagazine.com/famous-faces-3d-printing-laika/))
- Wildwood: an Expression Kit of 24 faces equals one second, one face per frame available. ([JoBlo](https://www.joblo.com/wildwood-behind-the-scenes-tour/), [Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit)) [U] This shows faces are authored for every frame, not that every frame differs.
- Coraline director Selick (2024): "I don't shoot everything on ones", contrasted with many feature-quality stop-motion animators who shoot every frame as a new image. He notes animators have no assistants to fill in between poses. ([BFI 2024](https://www.bfi.org.uk/sight-and-sound/interviews/stop-motion-henry-selick-coraline))
- Not found: any LAIKA statement that bodies are animated on twos as a house rule. The only LAIKA-specific body statement found says bodies on ones (ParaNorman). Body cadence for Coraline, Boxtrolls, Kubo, Missing Link and Wildwood was not stated in any source I could read. [U]
- Camera: motion control was used on nearly every Boxtrolls shot ([AWN Boxtrolls](https://awn.com/animationworld/on-set-laikas-boxtrolls)); more than 50 camera systems run daily ([SIGGRAPH Switaj 2018](https://history.siggraph.org/wp-content/uploads/2022/09/2018-Talks-Switaj_The-Robots-of-LAIKA.pdf)). Each frame is a separate exposure, so a moving camera is effectively on ones. [U] inference; no source states the camera cadence outright.
- Frame rate: 24 fps for all films ([Portland Monthly](https://www.pdxmonthly.com/arts-and-culture/2015/10/what-s-next-for-portland-s-animation-powerhouse-laika), [Fraunhofer](https://www.igd.fraunhofer.de/content/dam/igd/pressemitteilungen/2019/igd-2019-04-11_fraunhofer_3d-printing_technology_impresses_animation_studio_laika.pdf)). Coraline's motion is smoother than older stop motion, and the team still added a little classic stop-motion jitter ([Post](https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx)).

### 2.2 Holds and "moving holds"

- LAIKA's stated goal is that characters never look fully still ("Laika drift"). Earlier films put foam on puppet feet to get drift; Missing Link added mechanized breathers. ([Willamette Week](https://www.wweek.com/arts/2019/04/10/a-local-animator-reflects-on-the-stop-motion-process-in-laikas-new-film-missing-link/))
- Breathers: a chest/belly mechanism that fills with air or is turned by a key so the body rises and falls. Knobs on Link's back move belly or diaphragm only a fraction of an inch per frame. ([Slashfilm](https://www.slashfilm.com/laika-missing-link/), [TheWrap](https://www.thewrap.com/missing-link-laika-hardest-thing), [JoBlo Wildwood](https://www.joblo.com/wildwood-behind-the-scenes-tour/)) Producer Arianne Sutner: they want to see their characters breathing. ([Slashfilm set visit](https://www.slashfilm.com/565038/missing-link-set-visit-report/))
- "Jetpack" rigs on puppets' backs move characters in very small increments so small movements look natural and fluid, and avoid disturbing costumes. ([BMD](https://birthmoviesdeath.com/2019/03/18/a-visit-to-the-colorful-and-adventurous-set-of-missing-link.html), [Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link), [JoBlo Wildwood](https://www.joblo.com/wildwood-behind-the-scenes-tour/))
- Knight on Kubo: the hard part was stillness, not action. Animators must show restraint and choose the right moment to move; characters need an organic, living quality. He also notes a mathematical element (move a body part a set number of millimeters). ([Jim Hill](https://jimhillmedia.com/it-was-kubo-s-moments-of-stillness-rather-than-that-movies-big-action-sequences-which-really-challenged-the-animators-at-laika)) Schiff: on Kubo it was more of a challenge not to move a puppet and keep things subtle. ([On Animation](https://onanimation.com/2016/08/19/crafting-the-epic-world-of-kubo-a-conversation-with-laikas-animation-supervisor-brad-schiff/))
- Missing Link animator Lambden: audiences are tuned to subtle body language and facial expression; you cannot cheat it. ([Willamette Week](https://www.wweek.com/arts/2019/04/10/a-local-animator-reflects-on-the-stop-motion-process-in-laikas-new-film-missing-link/))
- Exact hold lengths (frames) used by LAIKA animators were not stated in any source. [U]

### 2.3 Output per animator

- Coraline-era target: 5-6 seconds per animator per week; previous films just under 5; Kubo averaged just under 3.5. Principal animation on Kubo took just over 90 weeks. ([St. Louis Magazine, Feb 2017](https://www.stlmag.com/news/q-and-a-with-brad-schiff), [On Animation](https://onanimation.com/2016/08/19/crafting-the-epic-world-of-kubo-a-conversation-with-laikas-animation-supervisor-brad-schiff/))
- Boxtrolls: about 4 seconds (96 frames) per week, 5 minutes to 1 hour per frame ([AWN Boxtrolls](https://awn.com/animationworld/on-set-laikas-boxtrolls)); 3.7 seconds per week elsewhere ([Vice](https://thecreatorsproject.vice.com/blog/unpacking-the-stop-motion-magic-of-the-boxtrolls), [Animation Magazine](https://animationmagazine.net/?p=186866)).
- Missing Link: target 4.3 seconds per week; action shots about 2 seconds per week ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/), [Slashfilm set visit](https://www.slashfilm.com/565038/missing-link-set-visit-report/)). 31 animators over 92 weeks of principal photography ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/)). Peak units: 91 ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)) versus 97 ([Slashfilm set visit](https://www.slashfilm.com/565038/missing-link-set-visit-report/)).
- Emerson (2020): about 3.5 to 5 seconds per week when animators do well. ([Intel](https://intel.com/content/dam/www/central-libraries/us/en/documents/2022-08/laika-webinar-customer-spotlight-transcript.pdf))
- Kubo's giant skeleton: about 2 seconds in a good week. ([TheWrap Kubo](https://thewrap.com/kubo-two-strings-biggest-stop-motion-animation))
- One Missing Link animator spent about a year on a few critical minutes at a ship's railing. ([Willamette Week](https://www.wweek.com/arts/2019/04/10/a-local-animator-reflects-on-the-stop-motion-process-in-laikas-new-film-missing-link/))
- Wildwood: 2,804 shots over 231 weeks; up to about 40 animators on one character; Prue had 36 puppets and about 30 animators at a time. ([The Direct](https://thedirect.com/article/laikas-stunning-new-animated-masterpiece-wildwood-took-1000-craftspeople-and-over-2800-shots-to-make)) Per-animator Wildwood output: not found.
- Arithmetic [U]: 3.5 s/week = 84 frames; 5 s/week = 120 frames; 4.3 s/week = 103 frames; 2 s/week = 48 frames.

### 2.4 Process stages and performance reference

- Stages: block (rough staging), rehearsal, final shoot; most Boxtrolls shots animated at least twice; example schedule one day to block, two days to rehearse, about a week and a half to shoot ([AWN Boxtrolls](https://awn.com/animationworld/on-set-laikas-boxtrolls)). Wildwood follows keyframe block, rehearsal, final hero animation ([The Direct](https://thedirect.com/article/laikas-stunning-new-animated-masterpiece-wildwood-took-1000-craftspeople-and-over-2800-shots-to-make)). Schiff: they always shoot the character on set and rehearse it there ([On Animation](https://onanimation.com/2016/08/19/crafting-the-epic-world-of-kubo-a-conversation-with-laikas-animation-supervisor-brad-schiff/)).
- Live-action reference: on Kubo it became mandatory ("Everybody is shooting reference", called LAVs). Schiff warns it is a skill to use reference without rotoscoping it. ([On Animation](https://onanimation.com/2016/08/19/crafting-the-epic-world-of-kubo-a-conversation-with-laikas-animation-supervisor-brad-schiff/))
- Schiff filmed reference of his own daughter to guide the young girl's movement on Kubo. ([St. Louis Magazine](https://www.stlmag.com/news/q-and-a-with-brad-schiff))
- LAIKA animator Kevin Parry films people (himself and others) performing actions as a visual foundation. ([Nerdist](https://nerdist.com/article/a-stop-motion-animator-demos-50-different-ways-to-get-into-a-pool/))
- Schiff on animal performance: Monkey's movement was a mesh of different primates ([On Animation](https://onanimation.com/2016/08/19/crafting-the-epic-world-of-kubo-a-conversation-with-laikas-animation-supervisor-brad-schiff/)); Wildwood animators studied real animal movement, especially wolves ([JoBlo Wildwood](https://www.joblo.com/wildwood-behind-the-scenes-tour/)).
- Wildwood: Schiff describes a "character bible" so the work reads as one animator's ([The Direct](https://thedirect.com/article/laikas-stunning-new-animated-masterpiece-wildwood-took-1000-craftspeople-and-over-2800-shots-to-make)). Lead animator Rachelle Lambden: stop motion is closer to theater and live action than to CG ([The Direct](https://thedirect.com/article/laikas-stunning-new-animated-masterpiece-wildwood-took-1000-craftspeople-and-over-2800-shots-to-make)).
- An unverified fragment from a LAIKA video page ("We try to film ourselves doing the acting, with a certain timing...") exists only on a spam-like mirror. [U] ([old.fbpe.org mirror](https://old.fbpe.org/laika-animating-action-in-missing-link.html))
- Stereo capture: Coraline used one camera repositioned for the second eye ([Post](https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx)); ParaNorman used 63 Canon 5D Mk II cameras, 53 motion-control systems, and the camera department produced 1,770,601 frames (20 h 29 min) ([fxguide](https://www.fxguide.com/?p=35589)). [U] Derived: far more frames were shot than shown, so rehearsal and retakes dominate the shoot.

---

## 3. Puppet technology relevant to performance

### 3.1 Armatures and mechanisms

- Basic joint design (steel balls, sockets, hinges, screws) is largely unchanged since King Kong; Wildwood armatures and musculature are now 3D printed. ([Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit), [Wikipedia](https://en.wikipedia.org/wiki/Wildwood_(film)))
- ParaNorman full-body puppets used metal armatures manipulated through hidden Allen keyholes covered by costumes ([Animation Magazine](https://animationmagazine.net/wordpress/features/he-hears-dead-people)). Norman stood about 9 inches ([Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html)); 178 puppets for 61 characters, Norman had 28 ([fxguide](https://www.fxguide.com/?p=35589)).
- Kubo: human armatures had 17-18 joints; Beetle 30-40 ([TheWrap Kubo](https://thewrap.com/kubo-two-strings-biggest-stop-motion-animation)).
- Missing Link: Link has 250+ components ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/)), about nine months to refine armature design (the armature is called the foundation of performance) ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/)). Puppets were built about 20% smaller than earlier films ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)). Link's body has a belly mover, chest breather and squash/stretch devices ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)).
- Scale-up rigs for close-ups: 500-600% mouth with printed teeth and cheeks, 300% rear end ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link), [Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link)); Kubo had a 200% head for a tear close-up and a half-inch Monkey face at the small end ([fxguide](https://www.fxguide.com/?p=186839)).

### 3.2 Silicone skins and bodies

- Mr. Link: perforated foam latex on metal armature with textured silicone sheets for fur; layered cast urethane "fur petals" at the neck slide past each other rather than buckle ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)). Silicone chosen to hold a consistent look frame to frame ([Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link)).
- Elephant and horse: foam, rubber and plastic muscle under a thin silicone skin; the elephant weighed about 36 lb and its walk shot took almost three months ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)).
- ParaNorman: some characters used flexible silicone skins over animatable facial mechanics ([Animation Magazine](https://animationmagazine.net/wordpress/features/he-hears-dead-people)). Zombies used paddles and gears under silicone ([Engadget](https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html)).
- Kubo's Monkey: four-way stretch Lycra over armature, combed silicone fur layered on top ([TheWrap Kubo](https://thewrap.com/kubo-two-strings-biggest-stop-motion-animation)).

### 3.3 Hair and fur: preventing "boil"

- Terminology: LAIKA people call frame-to-frame fur motion "boil", "crawl" or "chatter". Chris Butler says it can be a deliberate style but "shouldn't happen by accident", so Link's hair was stylized and almost graphic. ([Cartoon Brew](https://www.cartoonbrew.com/stop-motion/laika-reveals-the-hairy-business-of-animating-fur-for-missing-link-172251.html))
- Link fur build: hundreds of silicone/urethane tufts, each cast in a denser silicone and backed with a softer skin, acting like scales that move against each other. For the face, animators swap a printed ring that changes the fur shape. Wiring every tuft was rejected because animators would have to grab the puppet every frame. ([Cartoon Brew](https://www.cartoonbrew.com/stop-motion/laika-reveals-the-hairy-business-of-animating-fur-for-missing-link-172251.html))
- Another account: 200-300 hand-placed fur tiles on a leather cowl with a foam insert to glide, aiming for "fur continuity" and avoiding boil and crawl. ([Nerdist](https://nerdist.com/article/missing-link-laika-studios-what-we-learned/)) A third says stitched strand by strand to avoid "boiling" ([Movieweb](https://movieweb.com/missing-link-set-visit-laika-studios/), [U] low reliability, conflicts with the two cast-tuft accounts).
- Wind on Link's fur is not animated on set: tips were painted with invisible UV paint, each frame got a second exposure under UV, and compositors used the UV pass in Nuke to drive distortion, following a shot-by-shot wind script. ([Cartoon Brew](https://www.cartoonbrew.com/stop-motion/laika-reveals-the-hairy-business-of-animating-fur-for-missing-link-172251.html), [Boris FX](https://borisfx.com/news/oscars-2020-best-animated-feature-film-nominee-missing-link/))
- Earlier approach: wired hair pieces on Monkey in Kubo; it worked less well on Link. ([Cartoon Brew](https://www.cartoonbrew.com/stop-motion/laika-reveals-the-hairy-business-of-animating-fur-for-missing-link-172251.html))
- Kubo: there is no hair or cloth simulation; it is done by hand by an animator, except Kubo's hair in a few underwater shots. Other hair was wired. ([On Animation](https://onanimation.com/2016/08/19/crafting-the-epic-world-of-kubo-a-conversation-with-laikas-animation-supervisor-brad-schiff/))
- Coraline made her hair blow in the wind, described as a first for stop motion ([Portland Monthly](https://www.pdxmonthly.com/arts-and-culture/2015/10/what-s-next-for-portland-s-animation-powerhouse-laika)). ParaNorman moved from Coraline's wire to natural fibers including goat hair ([JoBlo ParaNorman](https://www.joblo.com/set-visit-paranormans-laika-studios/)). Boxtrolls used hemp hair wigs ([Animation Magazine](https://animationmagazine.net/?p=186866)).
- Wildwood: Prue's hair is wired with ball-and-socket joints at the skull and tendrils moved incrementally by hand or tweezers; it is posed to look always windblown. Animating her takes exponentially more time because of hair. Separate wigs for walking, biking and wind; a ponytail for bird-riding and battle because "hair is another character." ([But Why Tho](https://butwhytho.net/2026/10/wildwood-interview/)) Schiff also describes hair as an illusion where the whole hairpiece, such as a ponytail, rotates to show different angles. ([JoBlo Wildwood](https://www.joblo.com/wildwood-behind-the-scenes-tour/)) Knight: birds are hard because the animator moves feathers, hair and cloth on every frame. ([Cartoon Brew Annecy](https://www.cartoonbrew.com/feature-film/wildwood-travis-knight-annecy-263630.html))
- Wildwood eagle: about 9,000 hand-installed feathers per puppet ([AOL/Variety](https://www.aol.com/entertainment/epic-wildwood-pushing-laika-more-152500219.html)); robotic mechanics in clothing and feathers simulate wind in flying scenes ([Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit)).

### 3.4 Costume and cloth control

- Stop motion has no cloth sim; baggy Kubo costumes had to be "foiled or wired" and controlled by hand each frame. ([On Animation](https://onanimation.com/2016/08/19/crafting-the-epic-world-of-kubo-a-conversation-with-laikas-animation-supervisor-brad-schiff/), [St. Louis Magazine](https://www.stlmag.com/news/q-and-a-with-brad-schiff))
- At 24 fps, costumes must stay steady in every frame. ([TheWrap Kubo](https://thewrap.com/kubo-two-strings-biggest-stop-motion-animation))
- Missing Link: custom weighting systems keep cuffs and collars in place; air-blowing syringes; silicone-based costume pieces that return to shape; costumes have internal wires or mesh because nothing moves for free. ([Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link), [Nerdist](https://nerdist.com/article/missing-link-laika-studios-what-we-learned/), [BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/)) Lionel's houndstooth was designed to avoid moire ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link)).
- Wildwood: every stitch accounted for (Deb Cook) ([JoBlo Wildwood](https://www.joblo.com/wildwood-behind-the-scenes-tour/)).

### 3.5 Tie-downs, rigs, mid-air work

- Tie-downs: no LAIKA source found in this pass. [U]
- Rigs are everywhere and removed in post: over 1,000 rig removals on Missing Link ([Movieweb](https://movieweb.com/missing-link-set-visit-laika-studios/), [Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link)); each puppet has a built-in back rig for general movement ([Movieweb](https://movieweb.com/missing-link-set-visit-laika-studios/), [U] low-reliability page, but consistent with the "jetpack" accounts in 2.2).
- Mid-air and big moves: horse on a custom semi-circular rig whose pivot sits outside the puppet; Link swung over a crevasse on mechanical tethers ([AWN](https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link), [Screen Daily](https://screendaily.com/features/how-laika-made-ambitious-stop-motion-animation-missing-link/5145578.article)). Kubo's giant skeleton sat on a hydraulic rig with a second rig for the head and one animator on jaw, fingers and arms ([TheWrap Kubo](https://thewrap.com/kubo-two-strings-biggest-stop-motion-animation)).
- Robotics: robots carry big puppets, drive some shots live with animator-operated input devices (a bowling-ball waldo for the Giant Eye), and move whole sets on small six-degree motion bases ([SIGGRAPH Switaj 2018](https://history.siggraph.org/wp-content/uploads/2022/09/2018-Talks-Switaj_The-Robots-of-LAIKA.pdf), [Cartoon Brew](https://www.cartoonbrew.com/feature-film/laika-used-bowling-ball-animate-giant-eyes-kubo-two-strings-146172.html)).
- Wildwood flight: robotic wind mechanics in clothing and feathers on the eagle ([Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit)).

### 3.6 Keeping puppets and faces consistent across duplicates

- Duplicate counts: Link 11 unclothed and 12 clothed versions ([BMD](https://birthmoviesdeath.com/2019/03/18/a-visit-to-the-colorful-and-adventurous-set-of-missing-link.html)); about 30 puppet models per character on Missing Link ([Slashfilm set visit](https://www.slashfilm.com/565038/missing-link-set-visit-report/)); Prue 36 puppets on Wildwood ([The Direct](https://thedirect.com/article/laikas-stunning-new-animated-masterpiece-wildwood-took-1000-craftspeople-and-over-2800-shots-to-make)); 15-20 per main Boxtroll ([AWN Boxtrolls](https://awn.com/animationworld/on-set-laikas-boxtrolls)).
- Knight on identity: it has to look like Kubo is Kubo, not 20 different Kubos. ([Den of Geek](https://www.denofgeek.com/movies/travis-knight-interview-kubo-coraline-laika))
- Copy-and-repeat casting of fur pieces supported duplicates ([Cartoon Brew](https://www.cartoonbrew.com/stop-motion/laika-reveals-the-hairy-business-of-animating-fur-for-missing-link-172251.html)). A "puppet hospital" repairs damaged puppets ([Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link), [The Direct](https://thedirect.com/article/laikas-stunning-new-animated-masterpiece-wildwood-took-1000-craftspeople-and-over-2800-shots-to-make)). Puppets must survive up to two years of animator use ([Intel](https://intel.com/content/dam/www/central-libraries/us/en/documents/2022-08/laika-webinar-customer-spotlight-transcript.pdf)).
- Face-level consistency: see 1.10.

### 3.7 Motion blur and lighting (support for rules 3 and 5)

- Motion blur: stop-motion plates have none, so compositing adds it in post ([Boris FX](https://borisfx.com/news/oscars-2020-best-animated-feature-film-nominee-missing-link/)). Printed faces can also carry practical blur: Norman's nose printed in triplicate ([CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx)), faces with extra eyes and noses ([JoBlo ParaNorman](https://www.joblo.com/set-visit-paranormans-laika-studios/)). The Academy citation credits RP for advances in motion blur ([fxguide](https://www.fxguide.com/?p=186839)).
- Lighting drift/flicker: Tristan Oliver (ParaNorman DP) says LAIKA had a group of people in VFX whose job was sorting out "overnight fluctuations and flicker" ([Definition](https://definitionmagazine.com/?p=8394)). Pete Kozachik names a bulb slowly dimming as a standard long-shot risk ([AWN Kozachik](https://awn.com/animationworld/advanced-art-stop-motion-animation-interview-pete-kozachik-asc)). LED lights now replace heat-prone older lights on Wildwood ([JoBlo Wildwood](https://www.joblo.com/wildwood-behind-the-scenes-tour/)).
- Missing Link per-frame multi-exposure: beauty, key pass, and blacklight/UV pass each frame ([Boris FX](https://borisfx.com/news/oscars-2020-best-animated-feature-film-nominee-missing-link/)). Intel talk: a second exposure against a green card for background crowds ([Intel](https://intel.com/content/dam/www/central-libraries/us/en/documents/2022-08/laika-webinar-customer-spotlight-transcript.pdf)).

---

## 4. LAIKA's stated philosophy: visible handwork versus invisible craft

Statements, oldest to newest:

- Selick on Coraline (2024 interview about the 2009 film): wanted the face seams kept, believing audiences stop noticing after a few minutes; chasing CG-like realism is "ludicrous"; wants to feel the work "was touched by a real person". ([BFI 2024](https://www.bfi.org.uk/sight-and-sound/interviews/stop-motion-henry-selick-coraline))
- Meunier on Coraline's printed faces: keep a handmade look and avoid a "computery" feel. ([3DPrint.com](https://3dprint.com/119975/laika-academy-awards-3d-print/))
- Coraline kept a little stop-motion jitter on purpose, and some sculptural imperfections were retained. ([Post](https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx))
- Emerson (SIGGRAPH 2015 abstract): Coraline was captured almost entirely in camera; the hybrid approach grew across ParaNorman, Boxtrolls and Kubo; if it is in the film it must be built. ([SIGGRAPH History](https://history.siggraph.org/?p=89845), [Kennedy Compounds](https://www.thekennedycompounds.com/the-hands-of-laika-2020/2020/1/20/vfx-supervisor-steve-emerson))
- Knight (Kubo era): one foot in tradition, one in the future; aims for the next level of performance, nuance and subtlety; success is when audiences stop seeing steel and silicone and connect with the characters as people. ([Den of Geek](https://www.denofgeek.com/movies/travis-knight-interview-kubo-coraline-laika)) Knight also said "most people don't care how it's done." ([TheWrap Kubo](https://thewrap.com/kubo-two-strings-biggest-stop-motion-animation))
- Missing Link: Sutner's rule, "if the imperfections take you out of the film, we want to correct it." ([OPB](https://opb.org/news/article/laika-missing-link-behind-the-scenes-qa-oregon)) Another Sutner line in BoxOfficePro: they want everyone to forget they are puppets. ([BoxOfficePro](https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/)) VFX: "the audience never knows we touched the footage" ([Boris FX](https://borisfx.com/news/oscars-2020-best-animated-feature-film-nominee-missing-link/)); CG lead Wachtman: viewers should not be able to tell physical from VFX; Emerson: human involvement yields "beautiful, subtle imperfections" that they deliberately pull into CG ([SIGGRAPH blog](https://blog.siggraph.org/2020/01/how-laika-missing-link-raised-the-vfx-bar.html/)).
- Emerson, 2020: get as much in camera as possible; imperfections in the performances are part of the appeal; machine learning is artist-reviewed ([Intel](https://intel.com/content/dam/www/central-libraries/us/en/documents/2022-08/laika-webinar-customer-spotlight-transcript.pdf)).
- Wildwood (2026), Knight: "The making of the art leaves fingerprints on the art"; stop motion is "a quiet act of rebellion"; LAIKA is "not Amish" and uses modern tools ([AP via AJC](https://www.ajc.com/news/2026/09/fall-movie-preview-in-an-ai-world-laika-makes-handmade-wonders-and-wildwood/)); "We do use computers, obviously" ([Cartoon Brew Annecy](https://www.cartoonbrew.com/feature-film/wildwood-travis-knight-annecy-263630.html)). Art director Maldonado: everything was made by hand, and non-shot sets were scanned for VFX ([Creative Boom](https://www.creativeboom.com/insight/wildwood-art-director-matthew-maldonado-on-why-laika-still-builds-everything-by-hand-and-why-theyre-coming-to-londons-design-musuem/)). LAIKA aims to use CG as little as possible and still does VFX touch-ups ([Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit), [AOL/Variety](https://www.aol.com/entertainment/epic-wildwood-pushing-laika-more-152500219.html)). The eagle's wings are described as "no AI, no digital trickery" (reporter narration, not a direct quote from the crew) ([JoBlo Wildwood](https://www.joblo.com/wildwood-behind-the-scenes-tour/)).
- Academic reading: LAIKA's films stage reveals of their own construction (Boxtrolls pull-out, Kubo post-credit skeleton build) so the animator's hand stays visible in motion. ([Fantasy/Animation](https://www.fantasy-animation.org/current-posts/laika-and-the-two-worlds-deconstructing-the-illusion-of-stop-motion-animation))

Trend [U], my synthesis from the above:

1. Motion and surface artifacts that read as technical defects (seam lines, face color drift, flicker, accidental fur boil, rigs) were progressively removed from Coraline to Missing Link.
2. Material handmade cues (fabric weave, silicone sheen, hand-wired hair, puppet scale) were kept or made more central, and by Wildwood they are marketed explicitly as the point.
3. Performance intent moved from kit-based vocabulary toward bespoke per-frame facial animation.
4. So the stance is "visible hand in materials and performance, invisible machinery in the image." It is not "visible seams."

---

## 5. Evidence bearing on our five current rules

1. Bodies on twos, camera on ones: the one LAIKA-specific statement found says the opposite split (bodies on ones, faces on twos, ParaNorman). Later films push faces to ones. No source describes bodies on twos as LAIKA practice. Camera on ones is consistent with per-exposure motion control. See 2.1.
2. Mouths may change on ones: supported for Kubo, Missing Link and Wildwood; ParaNorman default was twos. See 2.1.
3. No motion blur: raw plates have none, but LAIKA adds blur in comp and prints blur geometry. See 3.7.
4. Surface boil changes only when pose changes: consistent with physical behavior (new pose, new surface state), and LAIKA works to reduce unintended boil; exceptions are post-driven or mechanically driven wind on holds. See 3.3.
5. Near-zero lighting flicker: consistent; LAIKA treats flicker as a defect fixed in VFX. See 3.7.

---

## Implications for a CG stop-motion pipeline

Concrete rules with a test for each. Source basis is in brackets; thresholds marked [U] are my proposals, not LAIKA numbers.

### Faces

1. Faces are discrete swaps, never blends. Each frame's face mesh must equal exactly one library sculpt. Test: hash each rendered face mesh against the library; zero frames with fractional blendshape weights. [Replacement animation: Guinness, Fabbaloo]
2. Two independent libraries: upper (brow/forehead) and lower (mouth/cheek), with eyes on a third controller. Any (upper, lower) pair must render without cracks. Test: render the full grid of pairs for each character at a fixed light; flag any gap or overlap beyond a set tolerance. [Kubo 11,007 x 4,429 = 48.75M; CGW 2016, fxguide]
3. Eyes and lids are not part of the face swap. Swapping a face sculpt must not change eyeball or lid transforms. Test: diff eye/lid world transforms across a swap; zero delta. Blinks live on their own track. [Missing Link, Wildwood, Boxtrolls: AWN, Inverse]
4. Faces are authored per shot from the dialogue line, not picked from a reusable bank. Keep a base expression bank only as seeds. Test: every dialogue shot has a manifest of sculpt IDs per frame with an audio-aligned exposure sheet. [Missing Link, Wildwood]
5. Exposure sheet drives face timing: one record per frame with sculpt IDs, as in the X-sheet shipped with kits. Test: the sheet round-trips (render from sheet equals render from scene). [Post, BoxOfficePro]
6. Face change cadence is a per-shot parameter {1, 2, 3 frames}. Default hero dialogue close-ups to ones; wides and background to twos. Expect 12 to 24 face changes per second in dialogue. Test: histogram face-hold lengths per shot; hero close-ups should show a meaningful share of one-frame holds. [AWN Boxtrolls, TCT, CGW 2016]
7. Seam is a style switch: `seam_visibility` from 0 (Missing Link-style invisible) to a faint horizontal line at the brow/eye split (Coraline-style, which Selick liked). Default 0. Test: at 0, no luminance step across the split line on any pair; at nonzero, a constant, shot-stable line. [BFI, Intel, Boris FX]
8. Skin material is one shader across all sculpts of a character, with a small subsurface radius. LAIKA's powder prints had color about 1/16 inch deep, about 1.6 mm on a puppet about 229 mm tall, or about 0.7% of body height. Test: SSS radius / body height within about 0.5% to 1%. Sampled skin color in a fixed region must not drift between swaps on a static hold (suggest max 1 dE00). [CGW 2012, Engadget; the dE threshold is [U]]
9. No per-face random variation in color, gloss or geometry beyond the authored sculpt, because LAIKA spends heavy effort removing exactly this (color matching, librarians, de-chatter). Test: material parameter hash identical across all faces of a character. [CGW 2012, Boris FX]

### Body timing and performance

10. Body cadence is a per-shot parameter {1, 2}. The one documented LAIKA default (ParaNorman) is ones; Knight says twos give "pop", so use twos as a deliberate accent, not as the global default, unless we decide the look is ours. Test: poses change only on cadence frames; log cadence per shot. [CGW 2012]
11. Camera moves are on ones whenever the camera is moving (motion control per exposure). Test: camera transform differs on every frame inside a move. [AWN Boxtrolls, SIGGRAPH Switaj; [U] inference]
12. Moving holds: no long hold may be bit-identical in the body. At pose cadence, add small chest/belly/shoulder offsets (breather behavior) of a few tenths of a degree or a fraction of a millimeter in puppet scale. Test: in any hold longer than 8 frames [U threshold], at least one torso channel changes at cadence, and no joint moves more than a small cap per step. [Willamette Week, Slashfilm, JoBlo]
13. Restraint default: stillness is the baseline; movement is placed on purpose. Test (review heuristic): in dialogue shots, non-speaking characters should show breath and eye changes but few large moves. [Jim Hill]
14. Reference is shot or generated per shot, used for timing and key poses, and never traced frame by frame. Test: pose curves must not correlate frame-for-frame with the reference trajectory beyond a set threshold [U]. [On Animation]
15. Budget sanity check: LAIKA animators produce 3.5 to 5 seconds per week (84 to 120 frames), about 2 seconds for action. Use this to estimate effort, not as a quality rule. [St. Louis Magazine, Intel, BoxOfficePro]

### Surfaces, hair, cloth

16. No hair or cloth simulation. Hair, fur and cloth are posed offsets keyed per pose. Test: for two consecutive frames with identical pose cadence state (a held frame under twos), every hair, fur and cloth vertex is identical. [On Animation, Schiff]
17. Fur strand identity is stable across poses; boil amplitude is a material parameter, default near zero for stylized fur (Link), nonzero only where we choose a rougher stop-motion look. Test: per-strand displacement between pose changes stays under the material's cap. [Cartoon Brew fur, Nerdist]
18. Wind is an explicit per-frame offset layer, allowed to change even on a held body pose, as LAIKA does with UV-paint-driven distortion and wind mechanics. Flag it in the shot so it is not mistaken for boil. [Cartoon Brew fur, Inverse]
19. Costume anchor points (cuffs, collars, hems) move only when the underlying joint moves. Test: anchor vertices static on held frames. [Fabbaloo blog, TheWrap Kubo]
20. Scale variants for extreme close-ups (200% to 600% heads, mouths) are allowed as hero assets, with matched materials. Test: albedo and normal-map look matches the base puppet when scaled. [fxguide, AWN]

### Camera and image

21. Motion blur default off, with two optional tools: post blur for fast action, and "multi-feature" smear geometry for faces, as LAIKA's practical blur. Test: blur only appears on frames flagged fast (pixel velocity above a set limit [U]). [Boris FX, CGW 2012]
22. Per-frame lighting jitter near zero: LAIKA treats flicker as a defect. Test: mean luminance in a static background region varies less than a set limit between frames (suggest 0.5% [U]). Separate keyed passes (beauty, key, UV-style mattes) are AOVs, not lighting changes. [Definition, Boris FX]

### Handwork look

23. Define an "imperfection budget": allowed = hand-posing irregularity, silicone sheen, fabric weave, slight pose asymmetry; not allowed = flicker, face color drift, seam steps, accidental fur boil. This mirrors Sutner's rule (correct imperfections that pull you out) alongside Knight's "fingerprints" view. Test: every imperfection in the style guide is tagged allowed or removed. [OPB, AP via AJC]

---

## Conflicts with our current rules

1. Rule "bodies on twos (12 poses per second)": contradicted as a description of LAIKA practice. The only LAIKA source with a clear statement (CGW 2012, ParaNorman) says bodies on ones and faces on twos, and LAIKA later moved faces to ones. Knight frames twos as a stylistic accent ("more pop"), and Selick says he does not shoot everything on ones, so twos are used selectively. Our rule is a style choice we own, not a LAIKA method. Source: [CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx), [CGW 2016](https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx), [BFI 2024](https://www.bfi.org.uk/sight-and-sound/interviews/stop-motion-henry-selick-coraline).
2. Rule "mouths may change on ones for dialogue": not contradicted. It matches Kubo, Missing Link and Wildwood. Note the rhythm mismatch: ParaNorman, the only film with a documented body cadence, had bodies on ones and faces slower (twos). A twos body with a ones mouth is the inverse of that and I found it documented nowhere. Body cadence on Kubo and later films is unknown. [U]
3. Rule "no motion blur": contradicted as an absolute. LAIKA composites motion blur onto plates and prints blur geometry (triplicate noses) on faces, and the Academy citation names motion blur as an RP-enabled advance. Raw capture has no blur, which supports it as a default, not a prohibition. Source: [Boris FX](https://borisfx.com/news/oscars-2020-best-animated-feature-film-nominee-missing-link/), [CGW 2012](https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx), [fxguide](https://www.fxguide.com/?p=186839).
4. Rule "surface boil changes only when the pose changes": mostly consistent, with two LAIKA exceptions where the surface changes on held poses: wind on fur driven by UV-pass distortion in comp (Link), and mechanical wind in clothing and feathers (Wildwood eagle). Also LAIKA treats boil as a thing to minimize or style on purpose, and Link's fur was stylized to avoid accidental boil. We may want to allow a flagged wind layer. Source: [Cartoon Brew fur](https://www.cartoonbrew.com/stop-motion/laika-reveals-the-hairy-business-of-animating-fur-for-missing-link-172251.html), [Inverse](https://www.inverse.com/entertainment/wildwood-laika-set-visit).
5. Rule "per-pose lighting flicker near zero": consistent. LAIKA's real plates contain flicker that VFX removes, so near zero is their intended end state. Source: [Definition](https://definitionmagazine.com/?p=8394).
6. Additional note, "holds": if our holds mean bit-identical frames, that differs from LAIKA's breathers, jetpacks and drift, which exist so characters are never fully still. Source: [Willamette Week](https://www.wweek.com/arts/2019/04/10/a-local-animator-reflects-on-the-stop-motion-process-in-laikas-new-film-missing-link/), [Slashfilm](https://www.slashfilm.com/laika-missing-link/).
7. Additional note, "seams": if we simulate printed faces, LAIKA's end state is no visible seam (Missing Link), while Coraline's director preferred a faint visible one. Decide which era we imitate. Source: [BFI 2024](https://www.bfi.org.uk/sight-and-sound/interviews/stop-motion-henry-selick-coraline), [Fabbaloo blog](https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link).

---

## Open gaps (not found in this pass)

- Any LAIKA statement on body cadence for Coraline, Boxtrolls, Kubo, Missing Link, Wildwood. A second source for the ParaNorman "bodies on ones" sentence.
- Tie-down practice. Blink timing specifics. Hold lengths in frames.
- Wildwood face seam handling, Wildwood per-animator output, and a Guinness entry for 140,000.
- Primary-source verification of the 140,000-face figure.
- Suggested next reads: American Cinematographer Kubo article (Sept 2016), Wildwood VFX pieces at Variety and Yahoo (Steve Emerson), the LAIKA "Animating Action in Missing Link" video and the LAIKA book "The Magic Behind a Stop Motion Dream Factory".

---

## Source list

Trade and press (higher reliability for process detail):
- CGW, "Face Forward", Aug/Sept 2012: https://cgw.com/Publications/CGW/2012/Volume-35-Issue-5-Aug-Sept-2012-/Face-Forward.aspx
- CGW, "Myth in Miniature", Sept/Oct 2016: https://www.cgw.com/Publications/CGW/2016/Volume-39-Issue-5-Sept-Oct-2016-/Myth-in-miniature.aspx
- fxguide, Kubo rapid prototyping (2016-07-13): https://www.fxguide.com/?p=186839
- fxguide, tech behind ParaNorman: https://www.fxguide.com/?p=35589
- Post Magazine, Coraline cover story (Feb 2009): https://www.postmagazine.com/Publications/Post-Magazine/2009/February-1-2009/COVER-STORY-CORALINE-ANIMATED-VIA-STOP-MOTION.aspx
- Animation Magazine, ParaNorman: https://animationmagazine.net/wordpress/features/he-hears-dead-people
- Animation Magazine, Boxtrolls: https://animationmagazine.net/?p=186866
- Animation Magazine, Fraunhofer and Missing Link: https://animationmagazine.net/2019/04/how-fraunhofers-3d-printing-tech-gave-life-to-mr-link
- AWN, Boxtrolls on set: https://awn.com/animationworld/on-set-laikas-boxtrolls
- AWN, Missing Link set visit: https://awn.com/animationworld/set-visit-go-behind-scenes-laikas-missing-link
- AWN, Pete Kozachik interview: https://awn.com/animationworld/advanced-art-stop-motion-animation-interview-pete-kozachik-asc
- Cartoon Brew, Boxtrolls 3D printing: https://www.cartoonbrew.com/feature-film/how-laika-pushed-3d-printing-to-new-heights-with-the-boxtrolls-101512.html
- Cartoon Brew, Missing Link fur: https://www.cartoonbrew.com/stop-motion/laika-reveals-the-hairy-business-of-animating-fur-for-missing-link-172251.html
- Cartoon Brew, Kubo Giant Eye: https://www.cartoonbrew.com/feature-film/laika-used-bowling-ball-animate-giant-eyes-kubo-two-strings-146172.html
- Cartoon Brew, Wildwood at Annecy: https://www.cartoonbrew.com/feature-film/wildwood-travis-knight-annecy-263630.html
- Boris FX, Missing Link VFX: https://borisfx.com/news/oscars-2020-best-animated-feature-film-nominee-missing-link/
- SIGGRAPH blog, Missing Link VFX (2020-01-28): https://blog.siggraph.org/2020/01/how-laika-missing-link-raised-the-vfx-bar.html/
- SIGGRAPH 2018 talk, "The Robots of LAIKA": https://history.siggraph.org/wp-content/uploads/2022/09/2018-Talks-Switaj_The-Robots-of-LAIKA.pdf
- SIGGRAPH 2015 abstract, Emerson: https://history.siggraph.org/?p=89845
- CGChannel, Academy Sci-Tech 2016: https://www.cgchannel.com/2016/01/mari-and-tweak-rv-creators-win-academy-awards/
- Screen Daily, Missing Link: https://screendaily.com/features/how-laika-made-ambitious-stop-motion-animation-missing-link/5145578.article
- BoxOfficePro, LAIKA studio tour (2019): https://www.boxofficepro.com/no-stopping-laika-a-tour-of-the-pioneering-stop-motion-animation-studio-behind-missing-link/
- TCT Magazine, "Famous faces": https://www.tctmagazine.com/famous-faces-3d-printing-laika/
- Definition Magazine, Tristan Oliver on Isle of Dogs (mentions ParaNorman): https://definitionmagazine.com/?p=8394
- BFI Sight and Sound, Selick (2024-08-23): https://www.bfi.org.uk/sight-and-sound/interviews/stop-motion-henry-selick-coraline

Vendor, partner and studio sources:
- Stratasys case study: https://www.stratasys.com/en/resources/case-studies/Laika
- Stratasys PDF: https://recycling.stratasys.com/contentassets/4b44c16668e745e384cfe492092ccab7/cs_pj_en_laika_1218a.pdf?v=48faf6
- Fraunhofer IGD press release (2019): https://www.igd.fraunhofer.de/content/dam/igd/pressemitteilungen/2019/igd-2019-04-11_fraunhofer_3d-printing_technology_impresses_animation_studio_laika.pdf
- Autodesk customer story: https://www.autodesk.com/customer-stories/laika-blends-digital-and-physical
- Intel customer spotlight transcript (Stringer, Emerson): https://intel.com/content/dam/www/central-libraries/us/en/documents/2022-08/laika-webinar-customer-spotlight-transcript.pdf
- Guinness World Records, most 3D printed faces: https://www.guinnessworldrecords.com/world-records/693110-most-3d-printed-faces-made-for-a-stop-motion-film
- LAIKA, Who We Are: https://www.laika.com/who-we-are
- LAIKA, news page: https://www.laika.com/news

Interviews:
- On Animation, Brad Schiff on Kubo: https://onanimation.com/2016/08/19/crafting-the-epic-world-of-kubo-a-conversation-with-laikas-animation-supervisor-brad-schiff/
- St. Louis Magazine, Schiff Q&A (2017-02-10): https://www.stlmag.com/news/q-and-a-with-brad-schiff
- Jim Hill Media, Knight on stillness: https://jimhillmedia.com/it-was-kubo-s-moments-of-stillness-rather-than-that-movies-big-action-sequences-which-really-challenged-the-animators-at-laika
- Den of Geek, Travis Knight: https://www.denofgeek.com/movies/travis-knight-interview-kubo-coraline-laika
- TheWrap, Kubo: https://thewrap.com/kubo-two-strings-biggest-stop-motion-animation
- TheWrap, Missing Link and Link: https://www.thewrap.com/missing-link-laika-hardest-thing
- Variety, Missing Link character design: https://variety.com/2019/artisans/production/laika-missing-link-character-design-1203166298
- OPB, Missing Link Q&A: https://opb.org/news/article/laika-missing-link-behind-the-scenes-qa-oregon
- Willamette Week, local animator: https://www.wweek.com/arts/2019/04/10/a-local-animator-reflects-on-the-stop-motion-process-in-laikas-new-film-missing-link/
- Nerdist, Missing Link: https://nerdist.com/article/missing-link-laika-studios-what-we-learned/
- Nerdist, Kevin Parry reference: https://nerdist.com/article/a-stop-motion-animator-demos-50-different-ways-to-get-into-a-pool/
- Slashfilm, Missing Link set visit: https://www.slashfilm.com/565038/missing-link-set-visit-report/
- Slashfilm, Missing Link breathers: https://www.slashfilm.com/laika-missing-link/
- Engadget, ParaNorman 3D printing: https://www.engadget.com/2012-08-17-how-3D-printing-changed-the-face-of-paranorman.html
- JoBlo, ParaNorman set visit: https://www.joblo.com/set-visit-paranormans-laika-studios/
- Vice Creators, Boxtrolls: https://thecreatorsproject.vice.com/blog/unpacking-the-stop-motion-magic-of-the-boxtrolls
- Portland Monthly (2015): https://www.pdxmonthly.com/arts-and-culture/2015/10/what-s-next-for-portland-s-animation-powerhouse-laika
- 3DPrint.com, Coraline and the Academy award: https://3dprint.com/119975/laika-academy-awards-3d-print/
- 3DPrint.com, Kubo: https://3dprint.com/140830/laika-3d-printing-kubo/
- BU CFA, Moon Beast: https://www.bu.edu/cfa-magazine/2018/10/10/making-the-moon-beast/

Lower-reliability or secondary (use with care):
- Kennedy Compounds, RP evolution (blog reprint of a feature): https://www.thekennedycompounds.com/the-hands-of-laika-2020/2020/2/3/ypgqw86c11pf9fjzbkyk85fl0x644z
- Kennedy Compounds, Emerson page: https://www.thekennedycompounds.com/the-hands-of-laika-2020/2020/1/20/vfx-supervisor-steve-emerson
- Fabbaloo, 106,000 faces: https://www.fabbaloo.com/2019/03/106000-3d-printed-faces
- Fabbaloo, Missing Link blog: https://www.fabbaloo.com/2019/03/3d-printing-provides-the-missing-link-to-missing-link
- Birth.Movies.Death set visit: https://birthmoviesdeath.com/2019/03/18/a-visit-to-the-colorful-and-adventurous-set-of-missing-link.html
- Movieweb set visit (garbled names, treat details as [U]): https://movieweb.com/missing-link-set-visit-laika-studios/
- Fantasy/Animation journal post: https://www.fantasy-animation.org/current-posts/laika-and-the-two-worlds-deconstructing-the-illusion-of-stop-motion-animation
- old.fbpe.org mirror (fragment only): https://old.fbpe.org/laika-animating-action-in-missing-link.html

Wildwood (2026):
- Inverse set visit (2026-09-16): https://www.inverse.com/entertainment/wildwood-laika-set-visit
- JoBlo set tour (2026-09-16): https://www.joblo.com/wildwood-behind-the-scenes-tour/
- Wikipedia, Wildwood (film): https://en.wikipedia.org/wiki/Wildwood_(film)
- AP via AJC, "In an AI world, Laika makes handmade wonders" (2026-09): https://www.ajc.com/news/2026/09/fall-movie-preview-in-an-ai-world-laika-makes-handmade-wonders-and-wildwood/
- The Direct, TIFF 2026: https://thedirect.com/article/laikas-stunning-new-animated-masterpiece-wildwood-took-1000-craftspeople-and-over-2800-shots-to-make
- But Why Tho, Wildwood interview: https://butwhytho.net/2026/10/wildwood-interview/
- Creative Boom, Maldonado: https://www.creativeboom.com/insight/wildwood-art-director-matthew-maldonado-on-why-laika-still-builds-everything-by-hand-and-why-theyre-coming-to-londons-design-musuem/
- AOL (Variety), Wildwood innovation: https://www.aol.com/entertainment/epic-wildwood-pushing-laika-more-152500219.html
- TIFF session page: https://2026.tiffr.com/films/wildwood-inside-the-performance
- TheWrap, Knight on stop motion: https://www.thewrap.com/creative-content/movies/laika-ceo-travis-knight-stop-motion-masters-of-the-universe-interview/
