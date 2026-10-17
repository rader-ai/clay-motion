# R&D tools (Oct 17, 2026)

Scripts from the first measurement and look-tuning pass (research/16). Starting points for Phase 4 and 5, not production code.

| File | What it does |
|---|---|
| `measure_clips.js` | Browser-console code that plays a Commons clay clip frame by frame and returns timing (poses per second, ones, twos, threes, holds, cuts) and look numbers |
| `look_stats.py` | The same look numbers in Python, for our own renders |
| `validate_hold_detector.py` | Builds a synthetic stop-motion clip with known timing, encodes it as web video, and checks the hold detector gets every frame right |
| `clay_test_scene.py` | Blender 5.2 test scene in true metres: a clay figure, a 3 cm clay ball, backdrop, tabletop, key, fill and rim; renders a medium shot and a head close-up with Cycles. `python clay_test_scene.py params.json out_prefix` |
| `clay_test_params_round9.json` | The settings from the last test round |
| `post_web.py` | Per-pose sensor noise, vignette, and a VP9 web-video round trip so renders are compared with the public clips on equal terms |

Notes: `clay_test_scene.py` needs Blender's Python module (`bpy` 5.2.2) and enables Cycles itself. Values marked [U] in LOOK_DEV.md are still starting points; the test rounds were judged by one model, not the critic panel.
