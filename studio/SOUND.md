# Sound: voice, effects, music and mix

Owner: the **Sound Supervisor**, with the Sound Designer and the Dialogue Editor. Source: research/14.

## 1. Voice comes first

Clay studios record dialogue before animating, because animation is timed to the voice and a shot can't be cheaply re-timed once it's made. Aardman's animators mine the breaths and small shifts in a recording for acting. So here: scratch voices feed the table read and animatic; final voices lock before lip sync starts.

## 2. Voices

**Scratch voices** (labeled SCRATCH everywhere): open-weight models with permissive licenses, running locally:
- Kokoro (Apache-2.0): fast, many voices, no emotion control. Fine for table reads.
- Chatterbox (MIT): exaggeration control and laugh tags; watermarks its output.
- Maya1 (Apache-2.0): voice described in text, expressive tags; about 16 GB VRAM.
- Qwen3-TTS (Apache-2.0): voice design, emotion and rate instructions.
- Or Chris's own recordings (home setup in research/14 section 2).
Comic timing from these models needs many takes and human picking; no benchmark rates them for comedy.

**Final voices:** human performers with a written, scoped release, recorded as "ABC" reads (each line two or three ways). AI final voices only from a commercially licensed plan or an Apache or MIT model, and disclosed. Not commercial-safe: F5-TTS weights, XTTS-v2, Fish Audio S2 Pro without a paid license.

**Consent rules:** never clone anyone without a written release covering this use; no sound-alikes of real people; log model, prompt and release for every voice. Several US states and the EU AI Act now regulate digital voice replicas and disclosure.

## 3. Lip sync handoff

After Dialogue Lock: Rhubarb 1.14.0 with the dialogue text supplied, JSON out, mapped to the X-sheet with a 1-frame lead and 2-frame minimum hold (MOTION.md section 4.7). WhisperX word timings cross-check it.

## 4. Sound design and Foley

- **Life-size weight, small dynamics.** Clay should sound like the material it's made of, with real weight, not cartoon squelch. Squelch is saved for gags. Pinocchio's sound team used walnuts and luthier's wood for the puppet and kept effects delicate; Early Man's team cut effects tight to animation and used their own field recordings.
- **Material thread in sound:** sound sources come from the film's material families where possible (wool, wood, clay, paper, stone). Desplat scored Pinocchio with wooden instruments only, which is the precedent for music sharing the film's material.
- Leave silence before a punchline.
- **Sources, in order:** our own recordings; Freesound CC0 (CC BY with credit; never CC BY-NC); Sonniss GDC bundles (commercial OK, no AI training); generated layers last, as raw material only. BBC Sound Effects is non-commercial and not allowed.

## 5. Music

- Best: commission a composer from the animatic, with a sync and master license, stems and a cue sheet.
- Acceptable: library music with clear licenses (Incompetech with credit or purchase), receipts kept.
- AI music is temp only until its legal status settles (several label lawsuits against Suno and Udio are ongoing; free Suno output is non-commercial).
- Score as underscore with strong themes rather than mickey-mousing, the way Julian Nott scored The Wrong Trousers.

## 6. Mix and delivery

- Dialogue, music and effects stems plus a stereo master, 48 kHz 24-bit WAV.
- Web target -16 LUFS integrated, -1.5 dBTP, re-measured after encoding. Other targets: YouTube about -14, broadcast EBU R128 -23 LUFS, Netflix -27 LKFS dialogue-gated.
- Scripted mix with ffmpeg (two-pass loudnorm) and pyloudnorm; REAPER scripting optional.
- Keep dialogue clear by mix choices, not by gutting the music. Listen on monitors, headphones and a phone.

## 7. Audio QA (code gate)

Runs on every mix and writes `audio_qa.json`:
- Loudness within 1 LU of target and true peak under the ceiling, measured on the encoded file.
- No clipping (peak count, flat factor).
- Room tone noise floor near -60 dBFS or lower [U].
- No unplanned dead air.
- Dialogue clarity: speech recognition word error rate on the dialogue stem versus the full mix; a big gap means music or effects are masking speech [U].
- Sync: audio length within one frame of picture; effects onsets within one frame of their cues; Rhubarb re-run on final dialogue matches the animated mouth frames.
- Rights: every file has a manifest row (source, license, URL, date); anything non-commercial or missing fails; AI audio flagged with model, seed and prompt.

## 8. Sign-off

Director (creative), Sound Supervisor (technical), Producer (rights and AI disclosure). **Sound Lock** follows Picture Lock; the EP signs.
