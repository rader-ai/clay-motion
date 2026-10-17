# Procedural 3D claymation, driven by Claude Code (research, Oct 17, 2026)

Tags: [U] = unverified or the researcher's estimate. Vendor claims mostly have no independent benchmark.

## Bottom line
The clay look is mostly solved by off-the-shelf shaders plus a "noise only changes on new poses" trick. The hard parts for an agent are acting, rigging chunky characters, and lip sync, not rendering. Build a pure Cycles pipeline first. Treat AI video-to-video as an optional polish pass; no evidence yet that it holds studio clay quality or respects held frames.

## 1. Clay look in Blender
- Clay Doh (DoubleGum, Superhive, Solo $35): Cycles + Eevee, fingerprints, dents, cracks, stop-motion features. Clay 4.Doh adds Pottery, Eyes, Clay Text, modifiers for mesh/curve/Grease Pencil/VDB. Dedicated boil controls not confirmed.
- Kin Kollection (Kinpraw, $1-2.50): speed slider changes noise seed, Frame Step holds the change. Docs list Blender 4.0/4.1, test on 5.x.
- Smart Wobble ($20, Blender 5.0-5.1): Geometry Nodes velocity-masked wobble with "jittery imperfections" displacement.
- Boil recipe [U, standard technique]: drive a 4D Noise Texture W input (or Mapping rotation) with floor(frame/2)*k so the surface changes only when the pose changes. BlenderNation bird making-of documents a constant-interpolation texture-rotation version. Erindale's claymation fire rotates displacement noise across the frame range.
- Stepped timing: Stop Motion Style Animator (Copperhead, Blender Extensions, GPL, 5.0+) = non-destructive stepped F-curves on twos/threes, noise jitter (0.05-0.3), per-object phase offsets. Stop-Mo (SouthernShotty, free, 3.4-5.1). Stop-O-motion ($15). Built-in Stepped F-Curve modifier also works.
- Shader starting values [U]: roughness 0.45-0.6, subsurface weight 0.05-0.15 (Random Walk, small radius), fingerprint bump, 1-2 mm displacement, slight hue variation per part.
- Tutorials: SouthernShotty clay shader (youtu.be/wTu3Xssw67Q); Joey Carlino GN claymation distortion (youtu.be/Kj-qVMwTTwA).

## 2. Headless automation
- Plain bpy beats MCP for production. Modal example pins bpy==4.5.0, Cycles on L40S, fans frames out with starmap, joins with ffmpeg. 240 frames at 1080p/128 samples in ~3 min on 10 GPUs (~6 s/frame/GPU). Locally: `blender -b -P script.py`.
- Blender 5.0 renamed BLENDER_EEVEE_NEXT to BLENDER_EEVEE. Higgsfield's hosted scene builder pins Blender 5.2 but caps code at 256 KiB and keeps renders small: layout, not finals.
- MCP servers: official Blender Lab server projects.blender.org/lab/blender_mcp (v1.0.3, Blender 5.1+, GPL, no sandbox). Community ahujasid/mcp-for-blender (renamed from blender-mcp Sept 2026, MIT): execute_blender_code, look (viewport/camera renders), generate_3d (Tripo, Hunyuan3D, Rodin), Poly Haven, Sketchfab. Needs GUI add-on running; socket has no auth; safe mode opt-in. A competitor blog claims four 2026 CVEs [U]. Use MCP for interactive look-dev with screenshot feedback only.
- Cycles vs EEVEE: no trustworthy per-frame benchmarks. Estimate for a simple tabletop at 1080p, 64-128 samples + denoise [U]: Cycles 5-30 s/frame, EEVEE 1-3 s.
- Cost saver: render every second frame (frame_step=2) and hold in ffmpeg.
- GPU prices (Mar 2026 snapshot): RunPod 4090 $0.34/h, Vast 4090 ~$0.22/h, L40S ~$0.79/h.

## 3. Asset generation and rigging
- Hosted via Higgsfield generate_3d (confirmed live): Meshy 7 and 6, Tripo H3.1 and P2, Hunyuan3D v3 (image) and v3.1 (text), SAM 3 3D Objects. Meshy adds quad remesh, A/T-pose, humanoid auto-rig, 678 canned animations; warns non-bipeds may rig poorly.
- Open weights: microsoft/TRELLIS.2 (MIT, 4B, 24 GB+ VRAM, ~17 s at 1024^3 on H100); TencentARC/Pixal3D (MIT, SIGGRAPH 2026, on TRELLIS.2); Tencent-Hunyuan/Hunyuan3D-2.1 (~29 GB VRAM shape+texture; license may exclude EU/UK/KR [U]).
- Chunky clay characters: no independent test. Plan [U]: clay-figure concept image -> 3D -> remesh -> keep geometry only, discard AI texture, apply own clay shader.
- Auto-rig: UniRig (VAST-AI-Research/UniRig, MIT, 8 GB+, fragile install, successor SkinTokens). Mixamo/AccuRIG humanoid-only [U]. For short-limbed blobs, skip AI rigs: rigid parts (head, torso, limbs) on a simple bone set, or lattice/shape-key squash.

## 4. Motion and lip sync
- Text-to-motion: HY-Motion 1.0 (Tencent-Hunyuan/HY-Motion-1.0, 1.0B, 26 GB VRAM, Lite 24 GB; prompts under 30 words, clips under 5 s). MoMask is older.
- Video-to-motion: GVHMR (zju3dv/GVHMR, SMPL). MoCapAnything V2 (phongdaot/MocapAnything, MIT) outputs BVH for arbitrary skeletons.
- Reality check: human mocap on a bobble-headed blob retargets badly. No-animator route: Claude Code keyframes 6-12 pose-to-pose beats per shot on twos and picks timing. Mocap only for walks and gestures.
- Stop-motion conversion: sample every second frame, constant interpolation, jitter, hold anticipation poses, small settle offsets.
- Lip sync: Rhubarb (DanielSWolf/rhubarb-lip-sync v1.14.0), mouth shapes A-F + G, H, X; TSV/JSON/XML/DAT output; English recognizer default. scaredyfish add-on unmaintained. Use Rhubarb Lipsync NG (Superhive, $12, Blender 3.3-5.2) or a ~30-line script swapping replacement-mouth meshes from the JSON cues, held on twos.

## 5. Hybrid 3D -> AI restyle
- Playbook3D free Wan 2.2 "graybox to rendered" ComfyUI workflow. Flick: depth/normal/Canny/OpenPose into ControlNet or Wan 2.2 VACE (~24 GB VRAM). invideo uses Blender blocking renders as camera refs. RunComfy clay style-transfer workflow (depth ControlNet + unsampling).
- How well: vendor demos only, no metrics. Video models "don't lock cadence"; stop-motion outputs drift 8-12 fps. Expect [U] per-frame diffusion shimmer, identity drift, fights deliberate holds. Use for backgrounds or a low-denoise pass at most.

## 6. Miniature camera in Blender
- Model at true scale (metric, unit scale 1). Puppets 15-25 cm, camera 40-80 cm away, 24-50 mm lens on 36 mm sensor. Avoid telephoto.
- f/2.8-f/5.6 for visible falloff on a backdrop 20-60 cm behind [U]; tune by eye.
- Lighting: one small hard key (5-15 cm area light) + weak fill, warm practicals, felt/wood/painted-card set box. No HDRI skies.
- Per-frame flicker on held frames [U]: key intensity +/-1-3%, light position +/-1-2 mm, camera nudge +/-0.2 mm.
- Motion blur off.

## 7. Assembly
ffmpeg (noise filter for grain; fps and tpad for holds), Python for cuts and sound. OpenTimelineIO for edit lists. Remotion free only for teams of 3 or fewer (company license needed above that). MoviePy optional.

## 8. CG tells and fixes
| Tell | Fix |
|---|---|
| Perfect uniform surface | Fingerprints, dents, uneven bevels, per-part hue shifts |
| Smooth interpolation | Twos/threes, constant interpolation, jitter |
| Static texture | Boil on held frames only |
| Motion blur | Off |
| Wrong-scale light | Small hard lights, true-scale DoF |
| Frame-perfect camera | Tiny per-frame camera and light jitter |
| Rubbery rig bends | Rigid parts plus squash |

## Recommended toolchain
1. Claude Code writes and runs bpy scripts under Blender 5.x with a scene template and a JSON shot spec.
2. Clay Doh (~$35) shader + Stop Motion Style Animator for stepping and jitter.
3. Characters: image model -> Tripo H3.1 or Meshy 7 (or TRELLIS.2 on cloud GPU) -> remesh -> rigid-part rig. UniRig optional.
4. Voice -> Rhubarb JSON -> replacement mouths.
5. Render on Modal or RunPod, ffmpeg assembly, OTIO handoff.
6. MCP optional, look-dev only.

Effort/compute [U]: 3-5 days to build; 0.5-1 day per character; 1-2 hours of agent time per 10 s shot plus review. 60 s on twos = ~720 unique frames; at 20 s/frame on a 4090-class GPU = ~4 GPU-hours, roughly $1-5 with retries.

## Sources
https://80.lv/articles/clay-d-oh-a-clay-shader-for-blender
https://digitalproduction.com/2025/08/25/clay-4-doh-update-sculpts-blender-workflow/
https://superhivemarket.com/products/kin-klei/docs
https://superhivemarket.com/products/smart-wobble/docs
https://extensions.blender.org/add-ons/stop-motion-style-animator/
https://superhivemarket.com/products/stop-mo/docs
https://infamedavid.gumroad.com/l/Stop-O-motion
https://www.blendernation.com/2019/06/23/bird-claymation-behind-the-scenes/
https://www.blendernation.com/2024/01/22/claymation-style-distortion-with-geometry-nodes/
https://80.lv/articles/nodevember-2025-simulating-a-claymation-fire-in-blender
https://github.com/ahujasid/mcp-for-blender
https://www.blender.org/lab/mcp-server/
https://modal.com/docs/examples/blender_video
https://developer.blender.org/docs/release_notes/5.0/eevee/
https://github.com/microsoft/TRELLIS.2
https://github.com/TencentARC/Pixal3D
https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
https://github.com/VAST-AI-Research/UniRig
https://github.com/Tencent-Hunyuan/HY-Motion-1.0
https://github.com/zju3dv/GVHMR
https://github.com/phongdaot/MocapAnything
https://github.com/DanielSWolf/rhubarb-lip-sync
https://superhivemarket.com/products/rhubarb-lipsync-ng
https://playbook3d.gumroad.com/l/vpjph
https://flick.art/blog/blender-ai-filmmaking
https://invideo.io/faq/why-does-ai-generated-stop-motion-animation-have/
https://www.runcomfy.com/comfyui-workflows/comfyui-workflow-for-consistent-clay-style-transfer
https://nofilmschool.com/how-to-shoot-miniatures
https://www.remotion.dev/docs/license/faq
https://github.com/AcademySoftwareFoundation/OpenTimelineIO
