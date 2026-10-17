# Auto-grading claymation against the studio bar (research, Oct 17, 2026)

Bottom line: split the grader. Code measures what stop motion physically is (cadence, sharpness, surface stability, drift). A blinded pairwise VLM panel judges "does this read as real clay next to a gold clip." Humans calibrate both. Generic video benchmarks mostly measure the wrong thing.

## 1. Generic metrics
- VBench / VBench-2.0 (Vchitect/VBench, Apache-2.0). Subject consistency = DINO cosine to first and previous frame. Temporal flicker valid on static clips only. Motion smoothness rewards interpolable motion, so held-pose cadence scores WORSE (wrong direction). Consistency scores can be gamed by static clips. Keep the DINO idea; drop smoothness. VBench-2.0 catches broken bodies, is silent on style.
- DOVER: technical/aesthetic quality trained on UGC. Use as a floor, not a target.
- EvalCrafter: copy its idea of regressing component metrics onto human ratings.
- FVD: misleading per clip (favors per-frame look over motion; needs ~2k clips). Skip.
- CLIP/SigLIP prompt similarity saturates on style words. Better: embedding kNN to your gold set. Aesthetic Predictor v2.5 (AGPL-3.0) is a weak guard.

## 2. Code-measurable signals (calibrate every cutoff to gold)
- Holds/cadence: downscaled grayscale, mean abs diff or SSIM per frame pair, "same frame" cutoff from compression noise floor (not zero), run-length histogram. Tools: ffmpeg freezedetect / mpdecimate (check params), imagehash (dHash), PySceneDetect to exclude cuts. Also test for blended "ghost" frames (frame near the mean of its neighbors).
- Boil: no ready script. Design: RAFT optical flow (or SAM 2 mask) finds stable regions; measure high-pass (Laplacian/DoG) energy of the inter-frame difference there. Use a gold-derived band.
- Motion blur: compare Laplacian variance in high-flow vs static regions; smear means interpolation.
- Morphing/identity: DINOv2/v3 or SigLIP embeddings of masked character crops vs reference. Face embedding models probably fail on clay faces. RAFT forward-backward consistency or warping error on non-occluded pixels.
- Flicker: per-frame luminance and channel means in a static mask, detrend, residual std.

## 3. VLM judges
- Pairwise beats pointwise (GenArena: Spearman 0.36 pointwise vs 0.86 pairwise; forced choice beats a tie option; count a win only if it survives order swap). MLLM-as-a-Judge: pairwise closest to humans.
- Don't ask "is it AI?" (best VLM 76% vs humans 89%; VLMs lean on watermarks). Normalize encoding, strip watermarks, ask about specific attributes.
- Panels: diverse judges beat one big judge (PoLL). Self-preference tracks self-recognition: never let a model family judge its own output alone. Position bias strongest when quality gaps are small (the late-loop regime).
- Rubrics: per-prompt 1-5 questionnaires beat binary (yes-bias). Claude ran ~1 point stricter than Gemini with the same ordering; never mix judges' absolute scales. Human-human agreement ~67% is a practical ceiling.
- Inputs: Gemini video samples 1 fps by default (can't see 12 Hz holds; use for performance and pacing). Claude takes up to 100 labeled images per request. Prefer 6-12 labeled full-res frames and crops over one mosaic (mosaics downscale away clay grain).

## 4. Reference sets
- Gold, safest first: (1) your own real clay clips at 24 fps on twos plus macro surface stills in target lighting, no rights risk; (2) public domain/CC stop motion (Prelinger 1926 Joseph Sunn clay animations, Wikimedia Commons, verify per item); (3) studio stills: best targets but press-kit terms unverified; keep small, internal, evaluation only (never training or generation references), record provenance, check vendor terms, ask counsel. Not legal advice.
- Known-bad: lazy-prompt outputs from 3+ generators, one set per failure mode, hard negatives from the best generators, and controlled degradations of gold clips (frame interpolation, injected boil, flicker, blur, cross-dissolve morphs) so every metric has ground truth. Match encoding, resolution, fps and crop across pools.

## 5. Optimization loops
- Start with best-of-N plus judge. Add GEPA (gepa-ai/gepa; DSPy) for prompt evolution since critiques are text. Optuna/TPE for numeric params, 3+ seeds per config.
- Reward hacking is real: proxy score climbs while true quality peaks then falls. Guards: code gates as constraints not weights; keep a metric vector, not one scalar; hidden judge and hidden gold subset the optimizer never sees; rotate judge families; canary clips; tune on 5-8 scenes, validate on 10+ unseen.
- Stop when held-out gain stays inside CI for 3 rounds, when hidden judge or humans go flat while the proxy rises, when thresholds hold on held-out scenes, or at budget.

## 6. Human in the loop
- Static blinded A/B page: random left/right, candidate vs gold plus known-bad controls, forced choice with "can't tell" and a one-line reason. ~5 raters per comparison. Start: 3-5 colleagues on 30-60 pairs.
- Judge calibration (Hamel Husain method): ~100 labeled items, balanced; train/dev/test split; report TPR/TNR, aim above 90% (floor 80%); inspect every disagreement; pin dated model IDs.

## Proposed eval harness
Inputs: clips normalized (24 fps, one codec/resolution, no watermark/audio), 3+ seeds per config, 5-8 tuning scenes + 10+ held-out scenes, 30+ gold and 30+ known-bad items.

Layer A, hard gates (code, pass/fail, cutoffs start at gold percentiles):
- Cadence: >= 85% of character-motion runs are length 2 (or the gold mix); run-length spread <= gold p90; ghost-blend frames < 2%.
- Median flow magnitude >= gold p10 (no static cheating).
- Warping error and luma/color flicker <= gold p90.
- Character crop cosine to reference >= gold p10 on every keyframe.
- Boil energy within gold p10-p90; moving-region sharpness >= gold p10; DOVER technical >= gold p10.

Layer B, VLM panel: Claude, Gemini (video + frames), one GPT model. Blind pair candidate vs random gold item, both orders, forced choice per dimension (clay surface, sculpt/character craft, lighting and miniature depth, set/prop scale, pose and performance, handmade cues) with one-sentence evidence. Win counts only if it survives order swap. Score = win rate vs gold (ties half), per dimension, over seeds and judges. Anchored 1-5 scores logged for diagnosis, never optimized.

"Studio-grade" (proposed, unvalidated): all gates pass; panel win rate vs gold >= 0.40 overall and >= 0.35 per dimension (0.50 = indistinguishable), at least 2 of 3 judges agree, on held-out scenes; plus blinded human test (5 raters, 20 pairs) >= 0.40 vs gold.

Judge validity checks (rerun when model or prompt changes): picks gold over known-bad >= 90%; order-flip consistency >= 80%; gold vs gold within 0.50 +/- 0.10; each controlled degradation caught by its code metric (90%) and the panel (80%); >= 75% agreement with human majority on 60+ labeled pairs.

Anti-fooling: hidden holdout judge and gold subset, judge rotation, canary clips that must fail (still-image slideshows with thumbprint noise, texture-injected static clips, CG clay-shader renders), human spot check every 5 iterations and at each threshold crossing, stop on divergence between proxy and hidden judge or humans.

Unverified: studio press-kit terms; ffmpeg filter params; Optuna specifics; whether reference-guided judging helps. All thresholds and the boil/blur/ghost detectors are proposed designs.

## Sources
https://github.com/Vchitect/VBench
https://arxiv.org/abs/2311.17982
https://arxiv.org/abs/2503.21755
https://github.com/VQAssessment/DOVER
https://github.com/EvalCrafter/EvalCrafter
https://github.com/songweige/content-debiased-fvd
https://github.com/discus0434/aesthetic-predictor-v2-5
https://github.com/JohannesBuchner/imagehash
https://github.com/Breakthrough/PySceneDetect
https://github.com/princeton-vl/RAFT
https://arxiv.org/abs/1808.00449
https://arxiv.org/abs/2602.06013
https://github.com/ruihanglix/genarena
https://arxiv.org/abs/2402.04788
https://arxiv.org/abs/2512.13281
https://arxiv.org/abs/2404.18796
https://arxiv.org/abs/2306.05685
https://github.com/moonmath-ai/WorldJen-benchmarking-subsystem
https://ai.google.dev/gemini-api/docs/video-understanding
https://platform.claude.com/docs/en/build-with-claude/vision
https://commons.wikimedia.org/wiki/Category:Films_using_stop-motion_animation
https://www.wiley.law/alert-Copyright-Office-Issues-Key-Guidance-on-Fair-Use-in-Generative-AI-Training
https://arxiv.org/abs/2507.19457
https://github.com/gepa-ai/gepa
https://github.com/stanfordnlp/dspy
https://arxiv.org/abs/2410.07137
https://tessl.io/registry/skills/github/hamelsmu/evals-skills/validate-evaluator
