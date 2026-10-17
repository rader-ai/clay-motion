# Sound for clay stop motion, in code (research, Oct 17, 2026)

Bottom line: top clay and stop-motion films lock voices first, build all sound from scratch (no production track), keep dynamics restrained, and score mostly as underscore with strong themes. A code-driven studio can automate scratch voices, lip-sync timing, loudness and QA. Final voices, final music and sign-off stay human. [U] = unverified.

## 1. Voice first
- Aardman's Creature Comforts records real conversation first and edits hard (~two hours cut to a 30-second spot, up to ~20 edits). Animators work from the finished track, mining breaths and small shifts for acting.
- Pinocchio: dialogue recorded first with actors directed; animatics plus audio were the blueprint; animators listened on headphones and pushed breaths into caricature.
- Scratch voices fix timing, pitch and emotion for the animatic and often trigger rewrites or restaging. Re-recorded lines must match syllable count and key mouth shapes of finished shots.
- Takes: usually solo at the mic; directors ask for "ABC" reads (same line two or three ways). Stop-motion take counts unsourced [U].
- Reason (inference): a locked track can't be cheaply retimed once frames are shot. Nick Park also acts gags on video for animators.

## 2. Voice tech, October 2026
Hosted
- ElevenLabs Eleven v3: 70+ languages, 5,000-char limit, audio tags, multi-speaker dialogue, timestamps, speed 0.7-1.2. Starter and up carry commercial use; Free is non-commercial. Instant cloning from Starter; Professional from Creator with voice-captcha. You warrant authorization for any uploaded voice.
- Gemini TTS: natural-language style, inline laughs and pauses, two prebuilt speakers, 24 kHz mono; commercial terms unchecked [U].
- OpenAI gpt-4o-mini-tts: instruction steering, 13 voices; must tell users the voice is AI; custom voices need a consent recording.
- Inworld, Cartesia, Hume, MiniMax: terms unchecked [U].
Open weights (licenses from primary pages)
- Kokoro 82M, Apache-2.0, 54 voices, no emotion or rate control: fine scratch, weak comedy.
- Chatterbox, MIT: exaggeration control, Turbo laugh/chuckle tags, ~10 s cloning, PerTh watermark on all output.
- Dia 1.6B, Apache-2.0, English, [S1]/[S2] speakers, nonverbal tags, 5-10 s clone prompt; voice drifts per run without prompt or seed. Dia2 streams, ~2 min max.
- Maya1 3B, Apache-2.0: voice described in text, 20 tags (sarcastic, mischievous, snort); tags mark where, not exact timing; ~16 GB VRAM.
- Qwen3-TTS 0.6B/1.7B, Apache-2.0: voice design, 3 s cloning, emotion and rate instructions.
- Sesame CSM-1B, Apache-2.0: research model, no fixed voice.
- Orpheus 3B: repo says Apache-2.0, a secondary source says Llama 3.2 terms; verify [U].
- Not commercial-safe: F5-TTS weights (CC-BY-NC), Fish Audio S2 Pro (paid commercial license), XTTS-v2, IndexTTS-2.
- Comedy quality: no independent benchmark [U]. Good for scratch; comic timing needs many takes and human picking.
Consent and law
- Dia, CSM, Orpheus bar imitating real people without consent. Tennessee ELVIS Act (July 2024); California AB 2602 voids digital-replica clauses lacking informed consent; Illinois treats voiceprints as biometric. NO FAKES Act cleared Senate Judiciary June 18, 2026 (later status [U]). EU AI Act Article 50 applied Aug 2, 2026: AI content that could pass as authentic must be disclosed.
- Studio rule: clone only people with a written, scoped release; no sound-alikes; log model, prompt, release.
Home recording
- Small soft room (closet of clothes), clap-test the tail, mic 6-10 in away and ~15 deg off-axis, 3 ft from walls, peaks -12 to -6 dBFS. 48 kHz/24-bit WAV, 10 s room tone, slate each take [U]. Record each line two or three ways.

## 3. Sound design and Foley
- Pinocchio (Gershin): delicacy over bombast; Pinocchio is ~eight layers (walnuts, guitar-maker wood, hinge and rubber squeaks); Cricket's steps are crab and lobster shell; effects ghosted under songs; mix opens near-mono and widens; tap dancing followed rhythm, not strict sync.
- The Wrong Trousers: one trouser footstep combined 13 elements, including a motorized camera drive. A dry theatre felt dead until effects, speech and natural reverb went in.
- Early Man: weight so plasticine reads as alive; effects cut tight to animation; Foley from the start; own field recordings over libraries; cloth and fur only where movement needs it; jokes landed with sound and no music.
- Policy (synthesis [U]): life-size weight, small dynamics. Material realism sells the clay; cartoon squelch is for gags. Leave silence before a punchline.
- Libraries: Freesound CC0 (no credit), CC BY (credit), CC BY-NC (not commercial); API license filter works; originals need OAuth2. Sonniss GDC bundles: commercial OK, no credit, no resale, AI/ML training prohibited. BBC Sound Effects: non-commercial, unusable for a commercial film. Pixabay: no standalone redistribution; Content ID unaddressed [U].
- Generation: Stable Audio 3 Small SFX (May 2026) open weights, licensed training data, Community License (free commercial under $1M revenue per one source). Stable Audio Open trained mostly on Freesound CC audio; card cautions against product use. MMAudio and AudioCraft weights CC-BY-NC. HunyuanVideo-Foley license unread [U]. ElevenLabs SFX ownership unclear [U]. Treat generated audio as raw layers.

## 4. Music
- Aardman: Julian Nott's Wrong Trousers score avoided mickey-mousing and played peril straight; villains get the themes. Vengeance Most Fowl: Lorne Balfe scores, Nott's themes return, 70-piece orchestra on the main theme; wrote to unfinished sketches.
- Laika: Coulais (Coraline) wrote from drawings and animatics; music "behind the wall" instead of mirroring. Marianelli joins at the start so music guides animator timing. Desplat's Pinocchio used wooden instruments only.
- Options: (a) commission a composer from the animatic with sync-and-master license, stems, cue sheet (best copyright position); (b) libraries (Incompetech CC BY 4.0, Pixabay), keep receipts; (c) AI: Eleven Music (Merlin and Kobalt licensed); Stable Audio 3 Medium.
- Suno/Udio risk: settlements and ongoing suits in 2025-2026 (UMG and Sony vs Suno ongoing; Sony vs Udio ongoing; one tracker contradicts [U]). Free Suno output is non-commercial. US Copyright Office (Jan 2025): prompts alone aren't authorship; human arrangement and edits can be. Use AI music as temp only.
- Note for this studio's material language: Desplat's all-wooden-instruments score is a precedent for music that shares the film's material thread.

## 5. Mix and delivery
- Targets: Netflix -27 LKFS dialogue-gated (+/-2), -2 dBTP, LRA 4-18. EBU R128 -23 LUFS (+/-0.5), -1 dBTP. ATSC A/85 -24 LKFS. YouTube ~-14 (turns down only), Spotify -14, Apple -16. Web pick: -16 LUFS, -1.5 dBTP, re-measured after encoding.
- Keep dialogue clear by mix choices, not by gutting music. Deliver dialogue, music, effects stems. Web or festival: stereo plus stems. 48 kHz/24-bit WAV [U].
- Tools: ffmpeg loudnorm (6.1.1 defaults I=-24, LRA=7, TP=-2; two-pass with print_format=json then measured values, linear=true). pyloudnorm (MIT, BS.1770-4; matched ffmpeg within 0.1 LU). Pedalboard GPLv3. REAPER ReaScript (EEL2, Lua, Python; $60 personal, $225 commercial over $20k income); reapy (MIT) needs REAPER running. ffmpeg ebur128 isn't dialogue-gated; measure the dialogue stem [U].

## 6. Lip sync (Rhubarb 1.14.0, MIT)
- Input WAV or Ogg plus a dialog text file (always supply). Output TSV, JSON/XML (start, end, value), DAT (24 fps default). Shapes A-F plus G, H, X. PocketSphinx English only; phonetic recognizer for other languages.
- Offset: Rhubarb states none. Mouths lead sound 1-3 frames; B/M/P on or one frame before; puckered shapes need two frames; head anticipation 4-6 frames. Rule: frame = round(t x fps) - 1, minimum hold 2 frames, tune per character.
- Handoff: CSV X-sheet (frame, shape, word) plus waveform and reference video. WhisperX word timing as a cross-check.

## 7. Automated audio QA
- Loudness within +/-1 LU and true peak under ceiling, on the encoded file.
- Clipping: astats peak level, peak count, flat factor.
- Noise floor: RMS of room-tone regions (silencedetect plus volumedetect), threshold near -60 dBFS [U]; astats "Noise floor" unreliable on program audio.
- Dead air: silencedetect.
- Clarity: Whisper WER on dialogue stem vs full mix (gap = masking) [U]; dialogue-minus-bed LU in speech windows; DNSMOS (repo MIT, model terms unchecked); NISQA (CC BY-NC-SA, internal only).
- Sync: audio length within one frame of picture; 2-pop and flash test; stem onsets vs cue list at +/-1 frame (41.7 ms at 24 fps); rerun Rhubarb on final dialogue and diff mouth frames [U].
- Rights: manifest row per file (source, license, URL, date); fail on NC or missing; flag AI audio with model, seed, prompt.

## Recommended pipeline
1. Rights register (`manifest.json`), voice sheets. Owner: Producer.
2. Scratch voices (Kokoro, Chatterbox-Turbo or Maya1), labeled SCRATCH, 48k/24 WAV. Check: no real-person clones. Sign-off: Director approves animatic.
3. Final voices: human actors with written release and ABC takes; AI finals only on a commercial plan or Apache/MIT model, disclosed. Sign-off: Director, Producer.
4. Dialogue lock, then Rhubarb to X-sheet with 1-frame lead. Sign-off: animation lead.
5. Picture lock to a frame-accurate cue list.
6. SFX, Foley, ambience: own recordings, Freesound CC0, Sonniss; generated layers last. Check: license manifest.
7. Music: commissioned or licensed; AI temp only. Sign-off: Director, legal.
8. Mix scripted (REAPER or ffmpeg/pydub), D/M/E stems, stereo master, web -16 LUFS. Listen on monitors, headphones, phone.
9. Auto QA gate writes a report.
10. Human sign-off: Director (creative), Sound Supervisor (technical), Producer (rights, AI disclosure). The agent never approves itself.

## Sources
https://animationobsessive.substack.com/p/perfecting-improv-with-aardman
https://www.motionpictures.org/2022/12/guillermo-del-toros-pinocchio-animation-supervisor-brian-leif-hansen-packs-puppets-with-emotion/
https://www.bfi.org.uk/interviews/guillermo-del-toro-pinocchio-stop-motion-mark-gustafson
https://www.backstage.com/magazine/article/decoding-direction-voiceover-session-1386/
https://www.denofgeek.com/movies/nick-park-interview-early-man-aardman-the-wrong-trousers-the-beano
https://elevenlabs.io/pricing
https://elevenlabs.io/terms-of-use
https://ai.google.dev/gemini-api/docs/speech-generation
https://developers.openai.com/api/docs/guides/text-to-speech
https://huggingface.co/hexgrad/Kokoro-82M
https://github.com/resemble-ai/chatterbox
https://github.com/nari-labs/dia
https://huggingface.co/maya-research/maya1
https://github.com/QwenLM/Qwen3-TTS
https://github.com/SesameAILabs/csm
https://github.com/canopyai/Orpheus-TTS
https://github.com/SWivid/F5-TTS
https://huggingface.co/fishaudio/s2-pro
https://ipwatchdog.com/2026/06/18/senate-judiciary-moves-no-fakes-act-one-step-closer-to-passage/
https://www.kingsleynapley.co.uk/our-insights/articles/the-eu-ai-acts-transparency-rules-are-now-live-what-organisations-need-to-do/
https://filmthreat.com/features/how-to-record-voiceover-at-home-indie-filmmakers-acoustic-guide/
https://www.asoundeffect.com/pinocchio-del-toro-film-sound
https://www.asoundeffect.com/early-man-sound/
https://www.redsharknews.com/post/item/262-audio-brings-life-to-animations
https://designingsound.org/2010/07/29/the-sound-design-of-coraline/
https://freesound.org/help/faq/
https://sonniss.com/gameaudiogdc
https://pixabay.com/service/license-summary/
https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models
https://huggingface.co/stabilityai/stable-audio-open-1.0
https://github.com/facebookresearch/audiocraft
https://www.classicfm.com/discover-music/periods-genres/film-tv/wallace-gromit-composer-julian-nott-interview/
https://www.classical-music.com/articles/wallace-gromit-vengeance-most-fowl
https://focusfeatures.com/article/an_interview_with_coraline_composer_bruno_coulais
https://variety.com/2017/film/awards/dario-marianelli-kubo-and-the-two-strings-score-1201955070
https://slashfilm.com/1098522/the-score-for-guillermo-del-toros-pinocchio-was-performed-with-only-wooden-instruments
https://incompetech.com/music/royalty-free/faq.html
https://www.akingump.com/en/insights/ai-law-and-regulation-tracker/us-copyright-office-releases-part-2-of-ai-report
https://www.production-expert.com/production-expert-1/how-to-optimise-an-audio-mix-for-delivery-to-netflix
https://tech.ebu.ch/docs/r/r128.pdf
https://github.com/csteinmetz1/pyloudnorm
https://github.com/slhck/ffmpeg-normalize
https://www.reaper.fm/sdk/reascript/reascript.php
https://github.com/RomeoDespres/reapy
https://github.com/DanielSWolf/rhubarb-lip-sync
https://brianlemay.com/Pages/animationschool/animation/lipsyncbook/lipsync.html
https://github.com/microsoft/DNS-Challenge
https://github.com/gabrielmittag/NISQA
