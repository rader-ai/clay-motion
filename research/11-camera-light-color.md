# Camera, lens, light and colour chain for a photographed-miniature look (research, Oct 17, 2026)

~24 searches before the shared budget ran out. Blender manual body pages fetched as navigation only, so Blender 5.x specifics come from release notes, dev posts, an API-migration commit and knowledge. [U] = unverified. "Derived" = researcher's arithmetic. At run time, introspect the live build (bpy.app.version_string, view_transform and look enums, CompositorNode* types) before trusting property names.

## 1. Real capture chain
- Bodies: Aardman shoots Canon EOS-1D X Mk III (Vengeance Most Fowl ~60 cameras across 40 sets; Chicken Run 2 45 units). Isle of Dogs used 80 1D X bodies. Mk III: 20 MP, 5472x3648 on 36x24 mm (~6.6 um pixels, derived). Pinocchio: Canon 5D Mk IV (first 4K film). 5D bodies overheated in live view and caused magenta shadow flicker on ParaNorman; the 1D X avoided it.
- Raw per frame in Dragonframe; Isle of Dogs also generated a LUT'd JPEG per raw. ISO unsourced; exposures of several seconds at f/16 imply base ISO [U].
- Lenses: manual Nikon stills primes, rehoused for close focus and manual iris. Pinocchio: Micro-NIKKOR 55 f/2.8, Zeiss 25/28/35 Distagon, Laowa 15 f/4 and 100 f/2.8 macro; 28-85 mm live-action range; ~60% second-hand. Vengeance used 20 mm for the submarine.
- Aperture: Vengeance DP shoots ~f/16 for depth, sometimes two exposures (characters, then background). Anderson demands extreme deep focus. No source states T11 and none documents a deliberately shallow clay look [U]. Shallow reads likely come from long or macro lenses on close-ups, split-focus exposures or comp [U].
- Scale rule (derived): to match full-scale DOF at f/N, a 1:k set with the camera k times closer needs f/(N*k). 1:4 at f/2.8 = f/11; 1:6 = f/17. That reconciles f/11-f/16. Example (35 mm at 35 cm, c = 13 um): DOF 7 mm at f/2.8, 26 mm at f/11, 38 mm at f/16. Cost: diffraction, Airy ~2.2 px at f/11, 3.3 px at f/16 (Gaussian sigma ~0.4-0.6 px).

## 2. Lighting
- Fixtures: Altman Micro Ellipse profiles (shutters, gobos; moving to LED, ETC Source Four Mini equivalent), ARRI 300/650 Plus and 1K-5K fresnels, Dedolights, cyc lights, a 10K through polyboard with butterfly and fill for Isle of Dogs exteriors (one big source unifies shadows; haze for atmosphere), diffused LED strips, tiny LEDs on wire for backlight, LED eyelights, practicals with internal LEDs (three sequenced LEDs make a candle).
- Pinocchio: tungsten keys only, all fill and bounce LED; cloud gobos on a 10x5 ft frame; sunrise key tracked 7-10 ft over ~10 s. Silver-board moon bounce and cucoloris on Vengeance. Pre-light, then final light after dressing.
- Layered exposures: Vengeance alternate key and ambient plus a beauty pass; Chicken Run 2 up to 16 exposures per frame; Pinocchio merged passes in comp. CG equivalent: Cycles light groups, summed linearly.
- Looks: Anderson flat and even; Pinocchio warm key with cool fill, reversed for austerity; Coraline flat real world, high-contrast other world. Ratios unpublished; convention 3:1-4:1 key:fill, rim near key level [U].
- Falloff (derived): lamp at 0.8 m vs 0.3 m = 2.8 stops. A 25 cm puppet with head 0.40 m and feet 0.60 m from the lamp spans 1.2 stops. A 15 cm fresnel at 1.2 m subtends ~7 deg (soft); a 4 cm micro lens at 1 m ~2 deg. Micro fixtures keep shadow hardness scale-consistent.
- Flicker (Dragonframe): block daylight, steady mains, no bright clothing, longer exposures (1 s beats 1/100 s), capture blackout, manual-aperture lenses. LED PWM: shutter whole PWM cycles, drivers ~2 kHz+, avoid 5-20% dim levels. Pinocchio moved lateral tracking shots from twos to ones to stop 4K strobing.

## 3. Lens character
- Cycles gives thin-lens DOF and bladed bokeh (aperture_blades, rotation, ratio). Not: breathing, vignette, distortion, CA, diffraction, flare. Compositor or ffmpeg must add those.
- Breathing (derived): image distance f(1+m), m = f/(s-f). Set Blender lens = f(1+m) and aperture_fstop = N(1+m) so aperture diameter stays f/N. 35 mm at 35 cm = 38.9 mm. Verify with a bokeh test render [U].
- Vignette: natural cos^4 falloff isn't cured by stopping down; optical vignetting is (2-3 stops). Keep mild at f/11-16.
- Bokeh polygonal when stopped down (7-9 blades [U]). CA sub-pixel. Distortion under ~1% on primes [U].
- Diffusion: Black Pro-Mist adds warm halation; Black Satin gentler. Pinocchio used a soft Pro-Mist look on its fireplace effect. No source shows whole-film diffusion on clay films [U]; 1/8-1/4 equivalent at most. Halation is a film-stock effect, absent from digital.
- Rule: CA, flare, bloom, vignette and grain should only be noticeable when toggled off.

## 4. Sensor character
- Shot noise scales with sqrt(signal); read noise sets the shadow floor; chroma noise cleaned harder than luma.
- Assumed model (70,000 e- well, 8 e- read noise [U]): SNR ~112 at 18% grey, 27 at -4 EV, 8 at -7 EV. At base ISO noise is a shadow phenomenon amplified by the tone curve.
- Match a sensor, not film grain: signal-dependent Poisson-Gaussian noise in scene-linear before the view transform, blurred 0.6-0.8 px (demosaic correlation), chroma lower than luma, then downscale to delivery.

## 5. Colour pipeline
- Blender 5.x: AgX default since 4.0; Filmic legacy (5.x status [U]); Standard clips; ACES 1.3/2.0 views; Linear Rec.709 working space, ACEScg optional; Convert Colorspace and Convert to Display nodes.
- Use Linear Rec.709, AgX, look none or one contrast look, plus one show LUT. Isle of Dogs ran one LUT across floor monitors, projection, VFX and first grade. Clone it: OCIO config with AgX plus the show LUT as a view; bake the same LUT to .cube (65^3) for ffmpeg lut3d (tetrahedral).
- White balance: tungsten 3200 K, LED 5600 K; Blackbody light colours; one compositor WB gain per scene. Keep gels desaturated; RGB rendering exaggerates saturated gels [U].
- Colour scripts: per-sequence WB, fill hue and LUT strength in JSON driving Blender and ffmpeg.

## 6. Compositing in code
- 5.x API (from a migration commit): `scene.compositing_node_group`, NodeGroupOutput replaces Composite, ShaderNodeMix replaces MixRGB, use_nodes no-op.
  ```
  tree=bpy.data.node_groups.new("Comp","CompositorNodeTree"); scene.compositing_node_group=tree
  tree.nodes.new("NodeGroupOutput"); tree.interface.new_socket("Image",in_out="OUTPUT",socket_type="NodeSocketColor")
  rl=tree.nodes.new("CompositorNodeRLayers"); rl.scene=scene
  ```
- Glare (4.4+): Threshold, Strength, Size, Saturation, Tint, Smoothness, Maximum; Bloom energy-conserving.
- Keep passes: Combined with denoising data, Alpha, Depth, Mist, light groups, Cryptomatte, Render Time.
- Order (scene-linear): denoise, light-group gains, WB, veiling glare (large bloom 0.5-2%), Pro-Mist glow, lens distortion plus dispersion, vignette, diffraction blur, sensor noise, then view transform and LUT. No signal-dependent grain node found; do noise in numpy or OIIO.
- Cadence: a held pose is one exposure duplicated, so noise and flicker are per pose, not per output frame. Render once per pose (seed = pose index), write EXR, duplicate with ffmpeg. Motion blur off. Flicker, if any, per-pose gain sigma ~0.3-0.8% [U]; productions fight it.

## 7. Calibration references
18% grey ball, chrome ball, ColorChecker Classic 24, bracketed HDRI of the set. Pinocchio LIDAR-scanned every set and puppet for VFX.

## (a) Recommended chain
- Camera: sensor_width 36, sensor_fit HORIZONTAL, 3840x2160, lens 25-50 mm (35 default), true-metre focus_distance, aperture_fstop = N(1+m) with N = 11 (16 for deep wides), aperture_blades 7-9, motion blur off.
- Cycles: 256-512 samples, adaptive threshold 0.01, OIDN with albedo and normal, pixel filter Gaussian or Blackman-Harris width 1.8-2.2, sample_clamp_indirect ~10, seed per pose.
- Lights (metres): key SPOT 3200 K, shadow_soft_size 0.015-0.02 m, spot_size 25-35 deg, blend 0.15-0.3, 0.8-1.2 m away. Start ~125 W at 1 m for 0.18 on a 0.18 card [U, derived]; scale as P*d^2 and calibrate on a card. Fill: wide area light, -2 EV, 5600 K. Rim: small spot behind, 0 to +1 EV. Flags and negative fill via light linking; gobo as image texture on the spot [U]; haze only when a beam is motivated (homogeneous scatter 0.02-0.1/m, anisotropy 0.4 [U]); IES only with a real photometric file.
- Colour: AgX, look none, exposure so the key-lit grey card reads 0.18.
- ffmpeg (16-bit PNGs at pose rate; tested on ffmpeg 6.1.1):
  ```
  ffmpeg -framerate 12 -i f_%04d.png -filter_complex "[0:v]format=gbrp16le,lut3d=file=show.cube:interp=tetrahedral,split=2[b][h];[h]lutrgb=r='if(gt(val,40000),val,0)':g='if(gt(val,40000),val,0)':b='if(gt(val,40000),val,0)',colorchannelmixer=rr=1:gg=0.4:bb=0.15,gblur=sigma=18[g];[b][g]blend=all_mode=screen:all_opacity=0.12,vignette=angle=PI/5:eval=init,fps=24[o]" -map "[o]" -c:v libx264 -crf 14 -pix_fmt yuv420p10le -colorspace bt709 -color_primaries bt709 -color_trc bt709 out.mp4
  ```
  Radial CA (tested): extractplanes, lenscorrection k1 +/-0.01 on R and B, mergeplanes=0x001020:gbrp. Noise (numpy, scene-linear, per pose): sigma = sqrt(a*x + b), a = 1/70000, b = (8/70000)^2 until measured; blur 0.6 px; chroma sigma 60% of luma.

## (b) Calibration procedure
1. Shoot raw: ColorChecker, grey ball, chrome ball in the real set, real lights, final f-stop; two identical frames for noise; one flat-field.
2. Decode linear with camera WB, no curve; fit a 3x3 matrix on the 24 patches (colour-checker-detection).
3. Digital twin: chart, balls, lights at measured positions; light directions from chrome-ball highlights; source size from highlight extent.
4. Optimise EV, WB, key power, fill ratio with scipy least_squares on CIEDE2000 over 24 patches. Accept mean below 2 and max below 5 [U] (~1 = one JND).
5. Tone: compare the six neutral patches in stops; tune AgX contrast within ~0.1 stop; check roll-off on a clipped practical.
6. Texture: match noise (variance vs mean per patch; lag 1-3 autocorrelation) and sharpness (edge-spread sigma, radial power-spectrum slope) via filter width, blur, noise.
7. Guard with LPIPS and DISTS on aligned 256 px crops as regression alarms, not optimisation targets.
8. Freeze parameters in JSON; rerun on every new set or light change.

## (c) Top 10 CG tells in the image chain (ranked, judgement)
1. Infinite or ambient lighting (sun, HDRI): small true-distance fixtures, flags, negative fill, falloff.
2. DOF wrong for scale (all sharp or toy-shallow): scale-equivalent f-stop plus breathing.
3. Clipped or hue-skewed speculars: AgX, emissive bulbs above 1.0, finite glow.
4. Razor sharpness: pixel filter 1.8-2.2, diffraction blur, delivery downscale.
5. Zero or denoiser-plastic noise: re-add Poisson-Gaussian noise after denoise.
6. Too-clean shadows: tinted bounce from set walls, veiling glare lifting blacks 0.5-2% [U], shadow noise.
7. No lens signature: mild vignette, sub-pixel CA, ~1% distortion.
8. Motion blur, or fresh noise on held frames: blur off; noise per pose.
9. Over-pure colour, inconsistent grade: desaturated gels, one show LUT, colour script.
10. Over-processing: bloom, grain, flare at toggle-off visibility; Pro-Mist 1/8 at most.

## Sources
https://britishcinematographer.co.uk/dave-alex-riddett-bsc-wallace-gromit-vengeance-most-fowl/
https://theasc.com/articles/wallace-gromit-vengeance-most-fowl
https://britishcinematographer.co.uk/charles-copping-emchicken-run-dawn-of-the-nugget-em/
https://www.canon-europe.com/pro/stories/stop-motion-secrets/
https://definitionmagazine.com/features/dogged/
https://filmmakermagazine.com/?p=104366
https://beforesandafters.com/2022/12/14/how-does-cinematography-work-on-a-stop-motion-film/
https://pastemagazine.com/movies/guillermo-del-toro/guillermo-del-toros-pinocchio-frank-passingham-cinematographer-interview
https://www.cgw.com/Publications/CGW/2022/October-November-December-2022/Guillermo-del-Toro-s-Pinocchio.aspx
https://vfxvoice.com/?p=13144738
https://www.empireonline.com/movies/features/inside-laika-studios-one-frame-at-a-time/
https://www.dragonframe.com/ufaqs/how-to-reduce-flicker-what-are-possible-sources-of-flicker/
https://support.enttec.com/pixel/pixel-general-knowledge/why-do-leds-flicker-on-camera
https://nofilmschool.com/how-to-shoot-miniatures
https://tiffen.com/pages/diffusion-guide
https://en.wikipedia.org/wiki/Depth_of_field
https://en.wikipedia.org/wiki/Image_noise
https://en.wikipedia.org/wiki/Vignetting
https://projects.blender.org/blender/blender/pulls/106355
https://developer.blender.org/docs/release_notes/5.0/cycles/
https://devtalk.blender.org/t/using-a-photometric-based-workflow-for-lighting/11708
https://arxiv.org/abs/1801.03924
https://arxiv.org/abs/2004.07728
https://github.com/colour-science/colour-checker-detection
