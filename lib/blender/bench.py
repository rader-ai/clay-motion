"""Phase 0 render benchmark: seconds per frame on this machine.

    <bpy-env>/bin/python lib/blender/bench.py out_dir [tiers...]

Builds the clay test scene (tools/clay_test_scene.py) with the round-9 params,
adds a fuzzy undyed-wool yarn collar on the figure, and times one frame per tier:
  pop_eevee  - medium shot, EEVEE, 854x480        (LOOK_DEV pop-through)
  pop_cycles - medium shot, Cycles 24 spp, 854x480
  dailies    - close-up with fiber, Cycles 256 spp, adaptive 0.01, 1920x1080
  final      - close-up with fiber, Cycles 1024 spp, adaptive 0.005, OIDN accurate, 1920x1080
Prints one JSON line per tier.
"""
import json, math, os, random, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import bpy  # noqa: E402
import clay_test_scene as cts  # noqa: E402


def yarn_collar(sc, center=(0.0, 0.0, 0.083), radius=0.018, strands=20000, seed=7):
    # neck seam of the test figure: body ellipsoid is ~16 mm wide there, so 18 mm sits on the clay
    """A ring of wool: core plies plus short stray fuzz, as hair curves with Principled Hair."""
    rng = random.Random(seed)
    curves = bpy.data.hair_curves.new("yarn_collar")
    pts_per = 4
    curves.add_curves([pts_per] * strands)
    pos = []
    for i in range(strands):
        a = rng.uniform(0, 2 * math.pi)
        # yarn body: 3 mm thick tube around the neck
        r_off, z_off = rng.gauss(0, 0.0012), rng.gauss(0, 0.0012)
        base = (center[0] + (radius + r_off) * math.cos(a), center[1] + (radius + r_off) * math.sin(a), center[2] + z_off)
        # most fibers follow the ply direction; ~15% are stray fuzz sticking out
        stray = rng.random() < 0.15
        length = rng.uniform(0.003, 0.008) if not stray else rng.uniform(0.0008, 0.0025)
        if stray:
            d = (rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))
        else:
            twist = 0.6
            d = (-math.sin(a) + rng.gauss(0, 0.2), math.cos(a) + rng.gauss(0, 0.2), twist + rng.gauss(0, 0.2))
        n = math.sqrt(sum(c * c for c in d)) or 1
        d = [c / n for c in d]
        for k in range(pts_per):
            t = k / (pts_per - 1) * length
            wob = 0.0002 * k
            pos.extend((base[0] + d[0] * t + rng.gauss(0, wob), base[1] + d[1] * t + rng.gauss(0, wob), base[2] + d[2] * t + rng.gauss(0, wob)))
    curves.attributes["position"].data.foreach_set("vector", pos)
    radius_attr = curves.attributes.get("radius") or curves.attributes.new("radius", "FLOAT", "POINT")
    radius_attr.data.foreach_set("value", [0.00002] * (strands * pts_per))  # ~40 micron wool fiber
    ob = bpy.data.objects.new("yarn_collar", curves)
    sc.collection.objects.link(ob)
    m = bpy.data.materials.new("undyed_wool")
    nt = m.node_tree if m.node_tree else None
    if nt is None:
        m.use_nodes = True
        nt = m.node_tree
    for nd in list(nt.nodes):
        nt.nodes.remove(nd)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    hair = nt.nodes.new("ShaderNodeBsdfHairPrincipled")
    hair.parametrization = "COLOR"
    hair.inputs["Color"].default_value = (0.62, 0.55, 0.44, 1)
    hair.inputs["Roughness"].default_value = 0.45
    nt.links.new(hair.outputs[0], out.inputs["Surface"])
    curves.materials.append(m)
    return ob


TIERS = {
    "pop_eevee": dict(engine="BLENDER_EEVEE", shot="medium", res=(854, 480)),
    "pop_cycles": dict(engine="CYCLES", shot="medium", res=(854, 480), samples=24, adaptive=0.02, accurate=False),
    "dailies": dict(engine="CYCLES", shot="close", res=(1920, 1080), samples=256, adaptive=0.01, accurate=False),
    "final": dict(engine="CYCLES", shot="close", res=(1920, 1080), samples=1024, adaptive=0.005, accurate=True),
}


def main(out_dir, tiers):
    prm = dict(cts.P)
    prm.update(json.load(open(os.path.join(ROOT, "tools", "clay_test_params_round9.json"))))
    sc = cts.build(prm)
    yarn_collar(sc)
    shots = {"medium": ((0.03, -0.40, 0.13), (0.01, 0.0, 0.065), 35.0), "close": ((0.012, -0.16, 0.112), (0.002, 0.0, 0.102), 50.0)}
    for nm, key in (("medium", "lens_medium"), ("close", "lens_close")):
        if prm.get(key):
            loc, tgt, lens = shots[nm]
            k = prm[key] / lens
            shots[nm] = (tuple(t + (l - t) * k for l, t in zip(loc, tgt)), tgt, prm[key])
    cams = {nm: cts.camera(sc, loc, tgt, lens, prm["fstop"], nm) for nm, (loc, tgt, lens) in shots.items()}
    for name in tiers:
        t = TIERS[name]
        sc.camera = cams[t["shot"]]
        sc.render.engine = t["engine"]
        sc.render.resolution_x, sc.render.resolution_y = t["res"]
        if t["engine"] == "CYCLES":
            cy = sc.cycles
            cy.samples = t["samples"]
            cy.adaptive_threshold = t["adaptive"]
            cy.denoising_prefilter = "ACCURATE" if t["accurate"] else "FAST"
        sc.render.filepath = os.path.join(out_dir, f"bench_{name}.png")
        start = time.time()
        bpy.ops.render.render(write_still=True)
        print("BENCH " + json.dumps({"tier": name, "seconds": round(time.time() - start, 1), "engine": t["engine"],
                                     "res": t["res"], "samples": t.get("samples"), "device": sc.cycles.device}), flush=True)


if __name__ == "__main__":
    out = os.path.abspath(sys.argv[1])
    os.makedirs(out, exist_ok=True)
    main(out, sys.argv[2:] or list(TIERS))
