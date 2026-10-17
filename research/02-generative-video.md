# Generative AI for claymation video (research, Oct 17, 2026)

Bracketed numbers point to Sources. "Unverified" = found only in third-party or vendor content. Everything here moves monthly; re-check before relying on it.

## Bottom line
- No independent claymation head-to-head exists. Every "model X is best at clay" claim found is vendor content. Treat rankings as priors and run a cheap bake-off.
- No model locks stop-motion cadence. Clips drift between ~8 and 12 fps; Veo, Kling, Seedance expose no fps control. Fix timing in post.
- Landscape shifts: Sora discontinued (app off Apr 26, API off Sep 24, 2026; secondary sources). Veo 3.1 still current; Google steering to Gemini Omni Flash. Wan 2.5-3.0 API-only. Seedance 2.5, Kling 3.0, FLUX 3 Video, MiniMax H3 are the new frontier.

## Ranked shortlist
- Hosted: clay keyframe (Nano Banana 2 or FLUX.2) -> Veo 3.1 Fast image-to-video with first/last frame and up to 3 reference images (~$0.15/s, unverified; Veo 3.1 Lite $0.05/s at 720p on fal). Runner-up for recurring characters: Kling 3.0 / O3 with Elements and multi-shot. Wildcard for pose-to-pose: Luma Ray 3.2, up to 16 keyframes per clip, no audio.
- Bake-off: one clay still, one prompt, 6 s each on Veo 3.1 Fast, Kling 3.0, Seedance 2.0, Omni 1.1, Ray 3.2. ~$1-3 per clip.
- Open-weight: Wan 2.2 14B I2V (Apache 2.0) + clay LoRA (most LoRAs, most mature tooling). To train your own clay LoRA, use LTX-2.5. MiniMax H3 license excludes US: skip.
- Post stack: upscale first, then decimate to 12 fps, hold each frame for 2, add per-drawing grain and flicker. SeedVR2 or Topaz -> ffmpeg or AIMZ ComfyUI node -> EllangoK grain node. Never frame interpolation.

## 1. Hosted models (per-second prices mostly third-party)
| Model | Notes |
|---|---|
| Veo 3.1 / Fast / Lite | Gemini API preview. 4/6/8 s. Up to 3 reference images, lastFrame, extension, native audio. Videos stored only 2 days. |
| Gemini Omni Flash 1.1 | gemini-omni-1.1-flash. Up to 10 s. References, first/last frame, conversational edits. ~$0.10-0.13/s at 720p. Restyle/video-input support conflicting between sources: test. |
| Kling 3.0 / O3 | Start/end frame, up to 6 shots, Elements lock character (images or 3-8 s video), native audio, 3-15 s. fal ~$0.17-0.39/s. |
| Seedance 2.0 / 2.5 | 2.0 on fal $0.30/s 720p, $0.68/s 1080p, end frame. Reference-to-video up to 9 images. 2.5 pricing unconfirmed. |
| Luma Ray 3.2 | Jun 9. 5/10 s. ~$0.06/s 720p, $0.24/s 1080p. Modify Video up to 20 s. HDR/EXR. |
| Runway Gen-4.5 | $0.12/s API, 2-10 s, 720p. Resells Seedance 2.5, Kling, Wan 3.0, Aleph 2.0. |
| FLUX 3 Video | GA Aug 5. Draft $0.06/s, HD $0.17/s. Up to 20 s. Keyframes, native audio. |
| MiniMax H3 | ~$0.16/s at 2K. First/last frame + 5 references. |
| Wan 3.0 | API-only beta. |

Recurring prompt advice (vendor sources): name the material (polymer clay, matte, thumbprints, seams); ban list (no CGI polish, no smooth 3D); locked camera, one subject, one action per clip; "12fps feel, held poses, no motion blur" is a weak hint only.

## 2. Open-weight video and LoRAs
- Wan 2.2 (newest downloadable Wan): 5B ~8 GB; 14B 50 GB+ FP16, ~11-16 GB GGUF Q5, 6-8 GB Q3/Q4 with offload. Ditto (Wan 2.1 restyle, claymation listed example) keeps motion/structure while restyling.
- LTX-2.5 (Aug 11): 22B, native audio, T2V/I2V/first-last-frame in ComfyUI, ltx-trainer for LoRAs. Community License free under $10M revenue, gated (check the revenue cap before any company use). ~66 GiB download, no VRAM figure. LTX-2.3 ~16 GB FP8 (community), 32 GB BF16 official.
- HunyuanVideo 1.5: ~24 GB, 14 GB offloaded.
- Clay/stop-motion video LoRAs: oumoumad/clay-stop-motion-lora-ngtvspc (LTX-2, trigger NGTVSPC); Muapi/ltx-2.3-claymation-style; kabachuha "Claymation Transformation" (Wan 2.2 I2V, morph/melt style, not general clay); tomstein123/WAN_loRA_StopMotion (no card).
- Frame-by-frame stills: ProCreations/stopmotion-consistency-v1-lora (Qwen-Image-2.1 next-frame editor; research pilot, admits geometry jitter).

## 3. Keyframes and character sheets
- Image models: Nano Banana 2 (~$0.067/1K image), 2.1 (~$0.034), GPT Image 2, FLUX.2, Seedream 5.0 (up to 14 references), Ideogram 4.5.
- One May 2026 API test (not clay): FLUX.2 led on consistency, then Gemini 3.1 Flash, then gpt-image-2.
- Multi-reference editing now covers what IP-Adapter/PuLID/ACE++ used to.
- Clay image LoRAs: strangerzonehf/Flux-Claymation-XC-LoRA (FLUX.1-dev, trigger "Claymation"); Qwen clay-doll stop-motion LoRA.
- Technique: one character sheet, pass 1-3 sheets as references for every keyframe, identical material wording in every prompt.

## 4. ComfyUI nodes
- AIMZ "Cel Animation Rate" (github.com/AIMZ-GFX/ComfyUI_AIMZ): holds on twos/threes/fours, keeps duration, passes audio.
- VideoHelperSuite "Select Every Nth Image" to decimate.
- EllangoK ComfyUI-post-processing-nodes: FilmGrain + vignette.
- SeedVR2 upscaler (batch sizes 4n+1, temporal_overlap).
- Interpolation (RIFE, FILM): avoid. Decimate a drifting clip to a fixed rate instead.
- ComfyUI Seedance 2.0 reference-to-video partner node with a stop-motion template (8-12 fps).
- No ready-made boil node exists.

## 5. Post-process recipes (untested)
- On twos: `ffmpeg -i in.mp4 -vf "fps=12,fps=24" out.mp4`
- Boil + flicker before the hold so each drawing gets its own noise: `-vf "fps=12,noise=alls=7:allf=t,eq=brightness='0.012*(random(0)-0.5)':eval=frame,fps=24"`
- Order: upscale -> decimate -> grain and flicker -> slight DOF and vignette.
- Motion blur can't be removed after the fact. Prompt against it and decimate hard.
- Higgsfield has "Video Deflicker" (useful) and "FPS Boost" (interpolation, avoid).

## 6. Lip sync and voice
- Native-audio models (Veo 3.1, Kling 3.0, Seedance, LTX, FLUX 3 Video, Wan 3.0) generate speech and mouths inside the clay render: likeliest way to preserve the look; clay mouth shapes unverified.
- Hedra Character-3: gallery includes a stop-motion clay musician; start frame + audio; 2.5-6.25 cents/s; API.
- Sync: lipsync-2/2-pro 512x512 and no non-humanoid support; sync-3 is 4K. Higgsfield lists Sync Lipsync 3.
- LatentSync 1.6 (Apache 2.0, 18 GB VRAM, 512px). Post-hoc lip sync probably softens clay texture (inference).
- Voice: ElevenLabs v3 / V4 (untested).

## 7. Creators and critics
- Named AI claymation project evidence is thin.
- Critics: AI figure-animation apps show smears, odd timing, no keyframes. BFI: fingerprints, seams, twos/threes are the human signature. Sea Slug festival bans AI. Aardman's Peter Lord says the studio is experimenting (undated). Some say most audiences don't care.
- Consistent "looks fake" signals: smooth or drifting timing, clean CG materials, missing persistent thumbprints and seams, camera and character drift between clips, no weight or contact.

## 8. Agent-drivable tools
- Higgsfield MCP (https://mcp.higgsfield.ai/mcp), already connected to Chris's claude.ai account. Catalog listed (no generations run): Veo 3/3.1/3.1 Lite, Gemini Omni Flash 1.1, Kling 2.6/3.0/3.0 Omni, Seedance 1.5/2.0/2.5, Wan 2.6/2.7/3.0, MiniMax H3, Grok Video 1.5, FLUX 3 Video; Topaz upscale, Video Deflicker, FPS Boost, Sync Lipsync 3; generate_3d; scene builder 3D (Blender). Install in Claude Code: `claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp`
- fal MCP (https://mcp.fal.ai/mcp-relay, OAuth): search_models, run_model, submit_job, get_pricing.
- Replicate hosted MCP (https://mcp.replicate.com/sse).
- Runway MCP repo archived Sep 30, 2026.
- Veo: call the Gemini API directly (community MCP unvetted).
- ComfyUI: artokun/comfyui-mcp best fit (LTX-2.3 video, Wan skills, node search; `/plugin marketplace add artokun/comfyui-mcp`). joenorton/comfyui-mcp-server image/audio only.
- Review any third-party MCP before giving it API keys.

## Version-risk flags
Seedance 2.5 pricing; Omni 1.1 restyle; LTX-2.5 LoRA compatibility; Sora shutdown dates; MiniMax H3 US exclusion.

## Sources
https://www.opus.pro/blog/claymation-ai
https://lumalabs.ai/news/3d-claymation-ai-prompts
https://invideo.io/faq/can-ai-video-generators-produce-stable-frame-rates-for/
https://invideo.io/faq/why-does-ai-generated-stop-motion-animation-have/
https://ai.google.dev/gemini-api/docs/veo
https://ai.google.dev/gemini-api/docs/omni
https://ai.google.dev/gemini-api/docs/pricing
https://fal.ai/models/fal-ai/veo3.1/lite/image-to-video
https://zilliz.com/ai-faq/what-is-the-sora-shutdown-timeline
https://fal.ai/kling-3
https://fal.ai/models/bytedance/seedance-2.0/image-to-video/llms.txt
https://www.atlascloud.ai/blog/guides/seedance-2.5-pricing-guide
https://runway.com/changelog
https://awesomeagents.ai/models/luma-ray3-2/
https://the-decoder.com/black-forest-labs-makes-flux-3-video-generally-available-and-claims-it-beats-seedance-2-0/
https://blog.segmind.com/minimax-h3-release-date-open-weights-and-api-pricing-explained/
https://howaiworks.ai/blog/alibaba-wan-open-weights-stopped-at-2-2
https://rits.shanghai.nyu.edu/ai/minimax-ships-h3-weights-with-the-us-and-eu-excluded/
https://huggingface.co/Lightricks/LTX-2.5
https://github.com/Lightricks/LTX-2
https://insiderllm.com/guides/local-ai-video-generation/
https://huggingface.co/oumoumad/clay-stop-motion-lora-ngtvspc
https://huggingface.co/Muapi/ltx-2.3-claymation-style
https://huggingface.co/ProCreations/stopmotion-consistency-v1-lora
https://huggingface.co/strangerzonehf/Flux-Claymation-XC-LoRA
https://huggingface.co/models?search=claymation
https://github.com/EzioBy/Ditto
https://github.com/AIMZ-GFX/ComfyUI_AIMZ
https://github.com/EllangoK/ComfyUI-post-processing-nodes
https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler
https://www.hedra.com/video-models/hedra-character-3
https://sync.so/docs/models
https://github.com/bytedance/LatentSync
https://www.bfi.org.uk/features/stop-motion-imperfection-why-animation-needs-human-touch
https://www.animateclay.com/post/stop-motion-ai-video-apps
https://github.com/artokun/comfyui-mcp
https://fal.ai/docs/documentation/setting-up/mcp.md
https://mcp.replicate.com/
https://techsy.io/en/blog/higgsfield-mcp-claude-code
