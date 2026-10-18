"""Exp1 hybrid look: keep the generated mesh's painted texture for colour (smooth gradients, no hard
material borders), drive the surface response (skin, hair, gloss, cloth) from soft masks, and grow
short wool locks over the beard and hair, each strand coloured from the paint at its root.
   <bpy-python> render_hybrid.py in.glb out.png [preview|dailies] [medium|full|face] [neck_frac] [rot_z] [fibers 0|1]"""
import math, os, random, sys, time
import numpy as np
import bpy
from mathutils import Vector, Matrix
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import puppet2 as P

HEIGHT = 0.28
glb, out = sys.argv[1], os.path.abspath(sys.argv[2])
q = sys.argv[3] if len(sys.argv) > 3 else "preview"
shot = sys.argv[4] if len(sys.argv) > 4 else "medium"
neck_frac = float(sys.argv[5]) if len(sys.argv) > 5 else 0.80
rot_z = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
fibers = (sys.argv[7] if len(sys.argv) > 7 else "1") == "1"

t0 = time.time()
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
bpy.ops.import_scene.gltf(filepath=glb)
meshes = [o for o in sc.objects if o.type == "MESH"]
for o in meshes:
    o.data.transform(o.matrix_world); o.matrix_world = Matrix.Identity(4); o.parent = None
for o in [o for o in sc.objects if o.type != "MESH"]:
    bpy.data.objects.remove(o)
bpy.ops.object.select_all(action="DESELECT")
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1: bpy.ops.object.join()
fig = bpy.context.view_layer.objects.active; fig.name = "figure"; me = fig.data
if rot_z: me.transform(Matrix.Rotation(math.radians(rot_z), 4, "Z"))
co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
lo, hi = co.min(0), co.max(0); s = HEIGHT / (hi[2] - lo[2])
co = (co - [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]]) * s + [0, 0, P.FLOOR]
neck_z = P.FLOOR + neck_frac * HEIGHT
co[:, 2] -= neck_z; P.FLOOR -= neck_z
me.vertices.foreach_set("co", co.ravel()); me.update()
for p in me.polygons: p.use_smooth = True
DEC = float(os.environ.get("DECIMATE", "1.0"))
if DEC < 1.0:   # lighter mesh for rigging and animation; collapse keeps the UVs and texture
    dm = fig.modifiers.new("dec", "DECIMATE"); dm.ratio = DEC
    bpy.context.view_layer.objects.active = fig; bpy.ops.object.modifier_apply(modifier="dec")
    me = fig.data
    co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)

# ---- sample the painted texture per vertex (blurred so weave and speckle don't flip the masks)
img = None
for m in me.materials:
    for n in (m.node_tree.nodes if m and m.node_tree else []):
        if n.type == "TEX_IMAGE" and n.image and any(l.to_socket.name == "Base Color" for l in n.outputs["Color"].links):
            img = n.image
assert img is not None
W, H = img.size
px = np.clip(np.array(img.pixels[:], dtype=np.float32).reshape(H, W, 4)[:, :, :3], 0, 1)
tex = np.asarray(Image.fromarray((px * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2)), dtype=np.float32) / 255
def sample(uv):
    xs = np.clip((uv[:, 0] % 1) * W, 0, W - 1).astype(int); ys = np.clip((uv[:, 1] % 1) * H, 0, H - 1).astype(int)
    return tex[ys, xs]
nl = len(me.loops)
luv = np.zeros(nl * 2); me.uv_layers.active.data.foreach_get("uv", luv); luv = luv.reshape(-1, 2)
lv = np.zeros(nl, dtype=np.int64); me.loops.foreach_get("vertex_index", lv)
nv = len(me.vertices)
vcol = np.zeros((nv, 3)); np.add.at(vcol, lv, sample(luv)); vcnt = np.bincount(lv, minlength=nv)[:, None]
vcol /= np.maximum(vcnt, 1)

# ---- soft class probabilities from paint colour (sRGB prototypes), head only for hair/gloss
protos = {"skin": (0.81, 0.57, 0.41), "grey": (0.64, 0.58, 0.54), "brown": (0.45, 0.32, 0.22), "brow": (0.30, 0.22, 0.17),
          "white": (0.92, 0.90, 0.86), "iris": (0.35, 0.50, 0.70), "dark": (0.05, 0.05, 0.06)}
ks = list(protos); Pm = np.array([protos[k] for k in ks])
d2 = ((vcol[:, None, :] - Pm[None]) ** 2).sum(-1)
prob = np.exp(-d2 / (2 * 0.06 ** 2)); prob /= prob.sum(1, keepdims=True)
z = co[:, 2]
head = np.clip((z - (-0.004)) / 0.006, 0, 1)                    # soft: 0 below the neck base, 1 above
hair = (prob[:, ks.index("grey")] + prob[:, ks.index("brown")] + prob[:, ks.index("brow")]) * head
skin = prob[:, ks.index("skin")]
gloss = (prob[:, ks.index("white")] + prob[:, ks.index("iris")] + prob[:, ks.index("dark")]) * head
# smooth the masks across the surface so borders feather instead of speckling
ed = np.zeros(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
deg = np.bincount(ed.ravel(), minlength=nv).astype(np.float64)
def smooth(x, it):
    for _ in range(it):
        acc = np.bincount(ed[:, 0], x[ed[:, 1]], nv) + np.bincount(ed[:, 1], x[ed[:, 0]], nv)
        x = 0.5 * x + 0.5 * acc / np.maximum(deg, 1)
    return x
hair = smooth(hair, 12); skin = smooth(skin, 6); gloss = smooth(gloss, 2)
attr = me.color_attributes.new("masks", "FLOAT_COLOR", "POINT")
attr.data.foreach_set("color", np.column_stack([hair, skin, gloss, np.ones(nv)]).astype(np.float32).ravel())

# ---- surface response from the masks; colour stays the paint
for m in me.materials:
    if not (m and m.node_tree): continue
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    for sock in ("Roughness", "Metallic"):
        for l in list(b.inputs[sock].links): nt.links.remove(l)
    b.inputs["Metallic"].default_value = 0.0
    at = nt.nodes.new("ShaderNodeAttribute"); at.attribute_type = "GEOMETRY"; at.attribute_name = "masks"
    sp = nt.nodes.new("ShaderNodeSeparateColor"); nt.links.new(at.outputs["Color"], sp.inputs[0])
    hairm, skinm, glossm = sp.outputs["Red"], sp.outputs["Green"], sp.outputs["Blue"]
    def lerp(t, a, c):
        mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["To Min"].default_value = a; mr.inputs["To Max"].default_value = c
        mr.clamp = True; nt.links.new(t, mr.inputs["Value"]); return mr.outputs["Result"]
    def mul(a, c):
        mm = nt.nodes.new("ShaderNodeMath"); mm.operation = "MULTIPLY"; mm.use_clamp = True
        nt.links.new(a, mm.inputs[0])
        if isinstance(c, float): mm.inputs[1].default_value = c
        else: nt.links.new(c, mm.inputs[1])
        return mm.outputs[0]
    # roughness: satin skin 0.5, matte hair 0.88, glossy eyes/teeth 0.15, cloth 0.8 below the neck
    hd = nt.nodes.new("ShaderNodeSeparateXYZ"); geo = nt.nodes.new("ShaderNodeNewGeometry"); nt.links.new(geo.outputs["Position"], hd.inputs[0])
    headm = lerp(hd.outputs["Z"], 0.0, 1.0); headm.node.inputs["From Min"].default_value = -0.006; headm.node.inputs["From Max"].default_value = -0.001
    r_base = lerp(headm, 0.80, 0.50)
    r_h = nt.nodes.new("ShaderNodeMix"); r_h.data_type = "FLOAT"; nt.links.new(hairm, r_h.inputs[0]); nt.links.new(r_base, r_h.inputs[2]); r_h.inputs[3].default_value = 0.88
    r_g = nt.nodes.new("ShaderNodeMix"); r_g.data_type = "FLOAT"; nt.links.new(glossm, r_g.inputs[0]); nt.links.new(r_h.outputs[0], r_g.inputs[2]); r_g.inputs[3].default_value = 0.15
    nt.links.new(r_g.outputs[0], b.inputs["Roughness"])
    nt.links.new(mul(mul(skinm, headm), 0.30), b.inputs["Subsurface Weight"])
    b.inputs["Subsurface Radius"].default_value = (1.0, 0.42, 0.25); b.inputs["Subsurface Scale"].default_value = 0.0012
    nt.links.new(mul(glossm, 0.6), b.inputs["Coat Weight"])
    cloth = nt.nodes.new("ShaderNodeMath"); cloth.operation = "SUBTRACT"; cloth.inputs[0].default_value = 1.0; nt.links.new(headm, cloth.inputs[1])
    nt.links.new(mul(cloth.outputs[0], 0.35), b.inputs["Sheen Weight"])
    b.inputs["Sheen Roughness"].default_value = 0.6

# ---- wool locks over beard and hair, coloured from the paint at each root
if fibers:
    me.calc_loop_triangles(); nt_ = len(me.loop_triangles)
    tv = np.zeros(nt_ * 3, dtype=np.int64); me.loop_triangles.foreach_get("vertices", tv); tv = tv.reshape(-1, 3)
    tl = np.zeros(nt_ * 3, dtype=np.int64); me.loop_triangles.foreach_get("loops", tl); tl = tl.reshape(-1, 3)
    A, B, C = co[tv[:, 0]], co[tv[:, 1]], co[tv[:, 2]]
    nrm = np.cross(B - A, C - A); area = np.linalg.norm(nrm, axis=1) / 2; nrm /= np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-12)
    th = hair[tv].mean(1)
    mouth_near = smooth(gloss.copy(), 8)          # keep wool off the lips and teeth
    w = area * np.clip((th - 0.55) / 0.3, 0, 1) * (mouth_near[tv].max(1) < 0.05)
    rng = np.random.default_rng(3)
    n_locks = 3200 if q != "preview" else 1400; per = 12; pts = 5
    pick = rng.choice(nt_, n_locks, p=w / w.sum())
    u, v = rng.random(n_locks), rng.random(n_locks); flip = u + v > 1; u[flip], v[flip] = 1 - u[flip], 1 - v[flip]
    roots = A[pick] + (B[pick] - A[pick]) * u[:, None] + (C[pick] - A[pick]) * v[:, None]
    ruv = luv[tl[pick, 0]] + (luv[tl[pick, 1]] - luv[tl[pick, 0]]) * u[:, None] + (luv[tl[pick, 2]] - luv[tl[pick, 0]]) * v[:, None]
    rcol = sample(ruv)
    curves = bpy.data.hair_curves.new("wool"); curves.add_curves([pts] * (n_locks * per))
    pos, rad, ccol = [], [], []
    R = random.Random(5); down = Vector((0, -0.2, -1)).normalized()
    for i in range(n_locks):
        n = Vector(nrm[pick[i]]); root = Vector(roots[i])
        on_scalp = root.z > 0.045
        L = (0.0012 if on_scalp else 0.0019) * R.uniform(0.8, 1.15)
        g = 0.45 if on_scalp else 0.6
        d = (n * (1 - g) + down * g + Vector((R.gauss(0, 0.10) for _ in range(3)))).normalized()
        if d.dot(n) < 0.25: d = (d + n * 0.6).normalized()
        t1 = d.cross(Vector((0, 0, 1)) if abs(d.z) < 0.9 else Vector((1, 0, 0))).normalized(); t2 = d.cross(t1)
        c = rcol[i]
        for s_ in range(per):
            a = R.uniform(0, 2 * math.pi); rr = 0.00045 * math.sqrt(R.random()); off = (t1 * math.cos(a) + t2 * math.sin(a)) * rr
            ls = R.uniform(0.75, 0.95)
            for k in range(pts):
                t = k / (pts - 1); pos.extend(root + d * (L * ls * t) + off * (1 - 0.85 * t)); rad.append(0.00004 * (1 - 0.75 * t))
            jit = R.uniform(0.85, 1.1); ccol.append((c[0] ** 2.2 * jit, c[1] ** 2.2 * jit, c[2] ** 2.2 * jit, 1.0))
    curves.attributes["position"].data.foreach_set("vector", pos)
    ra = curves.attributes.get("radius") or curves.attributes.new("radius", "FLOAT", "POINT"); ra.data.foreach_set("value", rad)
    ca = curves.attributes.new("root_col", "FLOAT_COLOR", "CURVE"); ca.data.foreach_set("color", np.array(ccol, dtype=np.float32).ravel())
    hm = bpy.data.materials.new("wool_painted"); hm.use_nodes = True; hnt = hm.node_tree
    for n_ in list(hnt.nodes): hnt.nodes.remove(n_)
    o_ = hnt.nodes.new("ShaderNodeOutputMaterial"); hb = hnt.nodes.new("ShaderNodeBsdfHairPrincipled"); hb.parametrization = "COLOR"
    hb.inputs["Roughness"].default_value = 0.5; hb.inputs["Radial Roughness"].default_value = 0.8
    ha = hnt.nodes.new("ShaderNodeAttribute"); ha.attribute_type = "GEOMETRY"; ha.attribute_name = "root_col"
    # the hair BSDF brightens colour a lot; pre-darken so fibers match the paint underneath
    gm = hnt.nodes.new("ShaderNodeGamma"); gm.inputs["Gamma"].default_value = 1.6; hnt.links.new(ha.outputs["Color"], gm.inputs["Color"])
    hnt.links.new(gm.outputs[0], hb.inputs["Color"]); hnt.links.new(hb.outputs[0], o_.inputs["Surface"])
    curves.materials.append(hm); P.link(curves, "wool")

P.set_and_light(sc, shot, q)
print(f"BUILT {time.time()-t0:.1f}s")
sc.render.filepath = out; t = time.time(); bpy.ops.render.render(write_still=True)
print(f"RENDERED {q} {shot} hybrid {time.time()-t:.1f}s -> {out}")
