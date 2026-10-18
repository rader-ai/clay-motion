# 19. Character pipeline experiments (Oct 17 to 18, 2026)

How should the studio build a character that is anatomically convincing, charming and animatable? Chris asked for a puppet of himself in the house style, and two hand-built attempts read as toys. So we ran three approaches side by side on the same set, lights and cameras, then took the winner through motion. Scripts are in `tools/puppet/`. Renders, generated meshes and source photos are kept off this public repo.

## What failed first

- **v1, primitives pressed together:** spheres for body parts. Circles where anatomy should be, a balloon torso, an uneven face.
- **v2, brush-sculpted head and lofted body:** better planes and tailored clothes, but tube limbs with no joints, a small head and a face built from parts. Read as a toy.

## The three experiments

| | 1. Design, then generated 3D | 2. Human anatomy base | 3. Procedural, pushed |
|---|---|---|---|
| Method | Text-only character description, 4 generated 2D designs, best one turned into a mesh by an image-to-3D model, then our materials and wool | Open human base mesh (MakeHuman/MPFB: assets CC0, code GPLv3) shaped toward the subject, puppet proportions set through the rig | puppet2 rebuilt from a proportion sheet: skeleton lofts, jointed hands, mesh locks, folds |
| Anatomy | 4 / 5 | 4 | 3 |
| Likeness | 3 ("a type", no photo used) | 3 | 2.5 |
| Charm, puppet feel | 4 | 2 (CG man in a bodysuit) | 3 |
| Editability | 2 (fused statue, no rig) | 5 (163-bone rig with face bones) | 3 |
| Cost, time | about $2.36, 11 min | $0, builds in 3 s | $0, builds in 25 s |
| Data off-machine | text prompts and our own generated images | none | none |

Scores are the agents' own, checked against the renders by the Producer. One judge only; not a panel result.

**Decision:** approach 1 for the look, with our own rig added. Approach 2's rig-driven proportions and approach 3's body and wardrobe builders are worth keeping for later.

## Making approach 1 look right

- Assigning our materials face by face from the texture colour gave speckled, hard borders around hair and beard. Fix: keep the generated paint for colour (smooth gradients) and drive only the surface response from soft, surface-smoothed masks. Grow short wool locks over beard and hair, each coloured from the paint at its root.
- The figure was then revised by editing our own generated design (younger, salt-and-pepper hair, fewer wrinkles, stronger upper body) and regenerating the mesh at 400k faces. About $1.40.

## Making it move

- A 19-bone skeleton placed from height slices of the mesh; leg IK so planted feet don't slide; a root bone for travel.
- Blender's automatic bone-heat weights failed twice: at puppet scale (0.28 m) and, at 10x scale, on the fused shell. Our own weights (distance to bone segments, gated by body region, smoothed along the surface) worked.
- Artifacts found and fixed: beard fibers and skin sliding apart on head turns (fix: rigid head weights); a crumpled, smeared inner elbow (fix: softer upper-arm to forearm hand-off, corrective smooth only at joints, volume-preserving deform off, gentler bend); a jacket web under a raised arm (fix: perform an elbow-bent wave instead; real fix is separate garments).
- Smile: a shape key that lifts the mouth corners and cheek apples, placed automatically from the painted teeth. Works, but the mustache hides most of it.
- Result: a 6-second walk-in, smile and wave, on twos at 1080x1440, about 30 s a frame at dailies on the M4 Pro.

## Privacy and licenses

- Generation ran through the Higgsfield connector (OpenAI images, Tripo and Tencent 3D). Their policy allows training on inputs and outputs and sharing with model providers. Only text and our own generated images were sent; no photo of a real person. Sending a real photo would likely add about one point of likeness and is Chris's call.
- Commercial-use terms for generated output still need checking before any character made this way ships.
- MPFB code is GPLv3; its assets and outputs are CC0.

## Spend

About $3.76 in generation credits across the experiments and the revision (shared Higgsfield balance). No other paid calls.

## What a studio pipeline needs next

1. Automatic joint placement from the mesh (slices plus landmarks) instead of hand measurement.
2. Generated meshes with garments separate from the body (or a rebuild step), so arms and cloth can move freely.
3. A replaceable mouth and brow kit cut from the face, and blinks, for real performance.
4. Multi-view design input (front, side, back) for a better back of head and body depth.
5. Checking commercial terms for generated output.
