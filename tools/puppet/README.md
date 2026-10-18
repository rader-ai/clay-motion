# Puppet pipeline (R&D, Oct 17 to 18, 2026)

Scripts from the character experiments in `research/19-character-pipeline-experiments.md`. Starting points for Phase 4 (fabrication and the animation engine), not production code. All run with the pinned Blender env (`~/.local/share/clay-studio/bpy-5.2.2/bin/python`, or `studio env` to find it).

| File | What it does |
|---|---|
| `puppet2.py` | Procedural puppet (brush-sculpted head, lofted body, clumped wool locks) and the shared pieces the others reuse: cloth, skin, eye and hair materials, and `set_and_light()` (slat-wall set, warm key, cool rim, shallow depth of field) |
| `render_hybrid.py` | Loads a generated GLB figure, scales it to puppet size (0.28 m), keeps its painted texture for colour, drives surface response (skin, hair, gloss, cloth) from soft masks, and grows short wool locks coloured from the paint at each root |
| `rig_wave.py` | Rigs a generated figure (19-bone skeleton, distance weights gated by body region, rigid head, joint relax) and animates a 3-second greeting on twos |
| `walk.py` | Same rig plus leg IK (planted feet), a root bone, a smile shape key found from the painted teeth, wrinkle relax beside the eyes, and a 6-second walk-in, smile and wave on twos |

Usage:
```
<bpy-python> render_hybrid.py figure.glb out.png [preview|dailies] [medium|full|face] [neck_frac] [rot_z] [fibers 0|1]
GLB=figure.glb DECIMATE=0.15 <bpy-python> rig_wave.py outdir [preview|dailies] [full|medium] [posetest|anim]
GLB=figure.glb <bpy-python> walk.py outdir [preview|dailies] [posetest|anim]     # FACE=1 for smile close-ups
```
Frames come out one per pose (every second frame). Assemble on twos with ffmpeg: `-framerate 12 -i seq/%03d.png -vf fps=24`.

Known limits:
- Joint positions in `rig_wave.py` and `walk.py` are measured by hand from height slices of one mesh each. A new figure needs re-measuring (automating this is the next step).
- Generated meshes fuse sleeves to the jacket, so big overhead arm raises stretch the jacket. Keep arm poses modest or rebuild the mesh with separate garments.
- Bone-heat automatic weights fail at puppet scale and on fused meshes; the scripts use their own distance weights.
- Generated figures, renders and the photos they were designed from never go in this repo.
