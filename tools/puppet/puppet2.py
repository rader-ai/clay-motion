"""Puppet v2: sculpted head (brush strokes on a dense mesh), lofted tailored body, clumped locks.
   <bpy-python> puppet2.py out.png [preview|dailies] [medium|full|face]
Units: metres, neck base at z=0, figure faces -y."""
import math, os, random, sys, time
import numpy as np
import bpy, bmesh, addon_utils
from mathutils import Vector, Matrix

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # tools/
import clay_test_scene as cts

FLOOR = -0.206
lin = cts.srgb_to_lin


# ------------------------------------------------------------------ mesh helpers
def ell(name, loc, size, rot=(0, 0, 0), segs=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=segs // 2, radius=1.0, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return o


def select_only(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]


def fuse(objs, name, voxel, smooth=4, factor=0.5):
    """Join parts into one volume: voxel remesh, then a gentle smooth. Origin baked to world."""
    select_only(objs); bpy.ops.object.join(); o = bpy.context.active_object; o.name = name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    r = o.modifiers.new("remesh", "REMESH"); r.mode = "VOXEL"; r.voxel_size = voxel
    bpy.ops.object.modifier_apply(modifier="remesh")
    if smooth:
        s = o.modifiers.new("smooth", "SMOOTH"); s.factor = factor; s.iterations = smooth
        bpy.ops.object.modifier_apply(modifier="smooth")
    bpy.ops.object.shade_smooth()
    o.data.materials.clear()
    return o


def link(me, name):
    o = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(o); return o


def superellipse(ax, ay, n, p=2.6, yoff=0.0, phase=0.0):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n + phase
        c, s = math.cos(t), math.sin(t)
        pts.append((ax * math.copysign(abs(c) ** (2 / p), c), yoff + ay * math.copysign(abs(s) ** (2 / p), s)))
    return pts


def loft_z(name, rings, n=64, p=2.6, cap=True):
    """rings: (z, ax, ay, yoff). Builds a closed tube along z with designed cross-sections."""
    me = bpy.data.meshes.new(name); bm = bmesh.new(); loops = []
    for z, ax, ay, yo in rings:
        loops.append([bm.verts.new((x, y, z)) for x, y in superellipse(ax, ay, n, p, yo)])
    for a, b in zip(loops, loops[1:]):
        for i in range(n):
            j = (i + 1) % n; bm.faces.new((a[i], a[j], b[j], b[i]))
    if cap:
        bm.faces.new(loops[0][::-1]); bm.faces.new(loops[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    return link(me, name)


def loft_path(name, pts, radii, n=40):
    """Round tube along a 3D polyline (sleeves, legs, fingers), capped."""
    me = bpy.data.meshes.new(name); bm = bmesh.new(); loops = []
    P = [Vector(p) for p in pts]
    for k, (p, r) in enumerate(zip(P, radii)):
        t = (P[min(k + 1, len(P) - 1)] - P[max(k - 1, 0)]).normalized()
        ref = Vector((0, 1, 0)) if abs(t.y) < 0.9 else Vector((1, 0, 0))
        u = t.cross(ref).normalized(); v = t.cross(u).normalized()
        loops.append([bm.verts.new(p + (u * math.cos(2 * math.pi * i / n) + v * math.sin(2 * math.pi * i / n)) * r) for i in range(n)])
    for a, b in zip(loops, loops[1:]):
        for i in range(n):
            j = (i + 1) % n; bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(loops[0][::-1]); bm.faces.new(loops[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
    return link(me, name)


def spline(ctrl, k=6):
    """Catmull-Rom through control points, k samples per span."""
    C = [Vector(c) for c in ctrl]; C = [C[0]] + C + [C[-1]]; out = []
    for i in range(1, len(C) - 2):
        p0, p1, p2, p3 = C[i - 1], C[i], C[i + 1], C[i + 2]
        for s in range(k):
            t = s / k
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(C[-2]); return out


class Sculpt:
    """Brush strokes on a dense mesh, like a sculptor's thumb: smooth falloff, offsets in metres."""
    def __init__(self, obj):
        self.o = obj; me = obj.data
        self.co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", self.co); self.co = self.co.reshape(-1, 3)
        self.tags = {}

    def surf(self, x, z, front=True):
        self.commit()
        ok, loc, nrm, _ = self.o.ray_cast(Vector((x, -1.0 if front else 1.0, z)), Vector((0, 1 if front else -1, 0)))
        assert ok, (x, z); return np.array(loc)

    def brush(self, c, r, off, tag=None, power=2.0):
        d = np.linalg.norm(self.co - np.asarray(c), axis=1)
        w = np.clip(1 - (d / r) ** 2, 0, 1) ** power
        self.co += w[:, None] * np.asarray(off)
        if tag: self.tags[tag] = np.maximum(self.tags.get(tag, np.zeros(len(self.co))), w)

    def face(self, x, z, r, out, tag=None, dx=0.0, dz=0.0, power=2.0):
        """Push the front surface at (x, z) outward (out > 0) or inward (out < 0)."""
        self.brush(self.surf(x, z), r, (dx, -out, dz), tag, power)

    def commit(self):
        self.o.data.vertices.foreach_set("co", self.co.ravel()); self.o.data.update()


# ------------------------------------------------------------------ materials
def nodes(m):
    if m.node_tree is None: m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt, nt.nodes.new("ShaderNodeOutputMaterial"), nt.nodes.new("ShaderNodeBsdfPrincipled")


def sphere_mask(nt, tc, center, radii):
    """1 at center, 0 at the ellipsoid edge, smooth: object-space mask for painted blush."""
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Location"].default_value = [-c / r for c, r in zip(center, radii)]
    mp.inputs["Scale"].default_value = [1 / r for r in radii]
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"; nt.links.new(mp.outputs["Vector"], ln.inputs[0])
    mr = nt.nodes.new("ShaderNodeMapRange"); mr.interpolation_type = "SMOOTHSTEP"
    mr.inputs["From Min"].default_value = 1.0; mr.inputs["From Max"].default_value = 0.0
    nt.links.new(ln.outputs["Value"], mr.inputs["Value"]); return mr.outputs["Result"]


def mix_rgb(nt, fac, a, b, blend="MIX"):
    m = nt.nodes.new("ShaderNodeMix"); m.data_type = "RGBA"; m.blend_type = blend
    for s, v in ((6, a), (7, b)):   # RGBA A/B sockets (by index: name lookup hits the float sockets)
        if isinstance(v, tuple): m.inputs[s].default_value = (*v, 1)
        else: nt.links.new(v, m.inputs[s])
    if isinstance(fac, float): m.inputs[0].default_value = fac
    else: nt.links.new(fac, m.inputs[0])
    return m.outputs[2]


def noise(nt, tc, scale, detail=3.0, w=0.0):
    n = nt.nodes.new("ShaderNodeTexNoise"); n.noise_dimensions = "4D"
    n.inputs["Scale"].default_value = scale; n.inputs["Detail"].default_value = detail; n.inputs["W"].default_value = w
    nt.links.new(tc.outputs["Object"], n.inputs["Vector"]); return n.outputs["Fac"]


def add(nt, a, b, op="ADD", clamp=True):
    m = nt.nodes.new("ShaderNodeMath"); m.operation = op; m.use_clamp = clamp
    for i, v in enumerate((a, b)):
        if isinstance(v, float): m.inputs[i].default_value = v
        else: nt.links.new(v, m.inputs[i])
    return m.outputs[0]


def bump_from(nt, b, height, strength, dist):
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = strength; bp.inputs["Distance"].default_value = dist
    nt.links.new(height, bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])


def skin_mat(blush_spots, lip):
    """Painted puppet skin: warm base, blush on cheeks/nose/ears, soft mottling, satin finish."""
    m = bpy.data.materials.new("skin"); nt, out, b = nodes(m); tc = nt.nodes.new("ShaderNodeTexCoord")
    base = lin((0.83, 0.62, 0.50)); blush = lin((0.80, 0.44, 0.38)); lipc = lin((0.70, 0.40, 0.36))
    mask = None
    for c, r, s in blush_spots:
        mk = add(nt, sphere_mask(nt, tc, c, r), s, "MULTIPLY")
        mask = mk if mask is None else add(nt, mask, mk, "MAXIMUM")
    mot = add(nt, noise(nt, tc, 1 / 0.006, 3.0, 1.0), 0.35, "MULTIPLY")
    mask = add(nt, mask, add(nt, mot, 0.12, "SUBTRACT"), "ADD")
    col = mix_rgb(nt, mask, tuple(base), tuple(blush))
    col = mix_rgb(nt, add(nt, sphere_mask(nt, tc, lip[0], lip[1]), 0.85, "MULTIPLY"), col, tuple(lipc))
    fine = noise(nt, tc, 1 / 0.0008, 4.0, 3.0)
    col = mix_rgb(nt, add(nt, fine, 0.10, "MULTIPLY"), col, (0.55, 0.35, 0.28), "MULTIPLY")
    nt.links.new(col, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.52
    b.inputs["Subsurface Weight"].default_value = 0.35; b.inputs["Subsurface Radius"].default_value = (1.0, 0.42, 0.25)
    b.inputs["Subsurface Scale"].default_value = 0.0012
    b.inputs["Sheen Weight"].default_value = 0.08
    bump_from(nt, b, add(nt, noise(nt, tc, 1 / 0.0005, 5.0, 7.0), noise(nt, tc, 1 / 0.003, 2.0, 9.0), "ADD", False), 0.08, 0.0002)
    nt.links.new(b.outputs[0], out.inputs["Surface"]); return m


def flat_mat(name, srgb, rough=0.6, coat=0.0, sss=0.0):
    m = bpy.data.materials.new(name); nt, out, b = nodes(m)
    b.inputs["Base Color"].default_value = (*lin(srgb), 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat; b.inputs["Subsurface Weight"].default_value = sss
    nt.links.new(b.outputs[0], out.inputs["Surface"]); return m


def eye_mat(iris_srgb):
    """Iris and pupil painted by angle from the eye's forward axis (-y in object space), under a wet coat."""
    m = bpy.data.materials.new("eye"); nt, out, b = nodes(m); tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeVectorMath"); nz.operation = "NORMALIZE"; nt.links.new(tc.outputs["Object"], nz.inputs[0])
    sp = nt.nodes.new("ShaderNodeSeparateXYZ"); nt.links.new(nz.outputs["Vector"], sp.inputs[0])
    cosv = add(nt, sp.outputs["Y"], -1.0, "MULTIPLY", False)
    ramp = nt.nodes.new("ShaderNodeValToRGB"); cr = ramp.color_ramp
    stops = [(0.0, (0.90, 0.88, 0.84)), (0.875, (0.90, 0.87, 0.83)), (0.885, (0.16, 0.24, 0.32)), (0.895, tuple(x * 0.8 for x in iris_srgb)),
             (0.94, iris_srgb), (0.976, tuple(x * 0.7 for x in iris_srgb)), (0.979, (0.02, 0.02, 0.025)), (1.0, (0.02, 0.02, 0.025))]
    cr.elements[0].position, cr.elements[0].color = stops[0][0], (*lin(stops[0][1]), 1)
    cr.elements[1].position, cr.elements[1].color = stops[-1][0], (*lin(stops[-1][1]), 1)
    for pos, c in stops[1:-1]:
        e = cr.elements.new(pos); e.color = (*lin(c), 1)
    nt.links.new(cosv, ramp.inputs["Fac"])
    streak = noise(nt, tc, 1 / 0.0003, 2.0, 4.0)
    col = mix_rgb(nt, add(nt, streak, 0.25, "MULTIPLY"), ramp.outputs["Color"], (0.95, 0.95, 0.95), "OVERLAY")
    nt.links.new(col, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.25; b.inputs["Coat Weight"].default_value = 1.0; b.inputs["Coat Roughness"].default_value = 0.02
    nt.links.new(b.outputs[0], out.inputs["Surface"]); return m


def cloth_mat(name, srgb, kind, scale=1.0):
    """Woven cloth: tweed (flecked herringbone), denim (twill), chambray (fine weave), wool knit."""
    m = bpy.data.materials.new(name); nt, out, b = nodes(m); tc = nt.nodes.new("ShaderNodeTexCoord")
    base = tuple(lin(srgb))
    def wave(sc, rot, prof="SIN"):
        mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Rotation"].default_value = rot
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        wv = nt.nodes.new("ShaderNodeTexWave"); wv.wave_profile = prof; wv.inputs["Scale"].default_value = sc
        wv.inputs["Distortion"].default_value = 0.5; wv.inputs["Detail"].default_value = 1.0
        nt.links.new(mp.outputs["Vector"], wv.inputs["Vector"]); return wv.outputs["Fac"]
    if kind == "tweed":
        h1 = wave(1800 * scale, (0, 0.6, 0)); h2 = wave(1800 * scale, (0, -0.6, 0))
        band = wave(240 * scale, (0, 0, 0), "SAW")
        weave = mix_rgb(nt, band, h1, h2)
        fl = nt.nodes.new("ShaderNodeTexVoronoi"); fl.inputs["Scale"].default_value = 2600 * scale
        nt.links.new(tc.outputs["Object"], fl.inputs["Vector"])
        sep = nt.nodes.new("ShaderNodeSeparateColor"); nt.links.new(fl.outputs["Color"], sep.inputs[0])
        fleck = add(nt, add(nt, sep.outputs["Red"], 0.975, "GREATER_THAN"), 0.6, "MULTIPLY")
        col = mix_rgb(nt, add(nt, noise(nt, tc, 1 / 0.003), 0.5, "MULTIPLY"), base, tuple(c * 0.7 for c in base))
        col = mix_rgb(nt, add(nt, weave, 0.35, "MULTIPLY"), col, tuple(c * 0.55 for c in base))
        col = mix_rgb(nt, fleck, col, tuple(lin((0.52, 0.36, 0.26))))
        height = weave; strength = 0.45; rough = 0.92; sheen = 0.35
    elif kind == "denim":
        tw = wave(2200 * scale, (0, 0.75, 0.3))
        fade = noise(nt, tc, 1 / 0.02, 2.0, 5.0)
        col = mix_rgb(nt, add(nt, tw, 0.15, "MULTIPLY"), base, (0.60, 0.64, 0.72))
        col = mix_rgb(nt, add(nt, fade, 0.12, "MULTIPLY"), col, (0.35, 0.40, 0.50))
        height = tw; strength = 0.35; rough = 0.88; sheen = 0.2
    elif kind == "chambray":
        w1 = wave(3200 * scale, (0, 0, 0)); w2 = wave(3200 * scale, (0, 1.5708, 0))
        weave = add(nt, w1, w2, "MULTIPLY")
        col = mix_rgb(nt, add(nt, weave, 0.12, "MULTIPLY"), base, (0.80, 0.84, 0.90))
        height = weave; strength = 0.25; rough = 0.85; sheen = 0.15
    else:  # leather
        cr = noise(nt, tc, 1 / 0.0015, 6.0, 2.0)
        col = mix_rgb(nt, add(nt, cr, 0.35, "MULTIPLY"), base, tuple(c * 0.6 for c in base))
        height = cr; strength = 0.15; rough = 0.42; sheen = 0.0
        b.inputs["Coat Weight"].default_value = 0.25
    nt.links.new(col, b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = rough
    b.inputs["Sheen Weight"].default_value = sheen; b.inputs["Sheen Tint"].default_value = (*[min(1, c * 2.0) for c in base], 1)
    bump_from(nt, b, height, strength, 0.0002)
    nt.links.new(b.outputs[0], out.inputs["Surface"]); return m


def hair_mat(name, srgb, var=0.4, rough=0.42):
    m = bpy.data.materials.new(name)
    if m.node_tree is None: m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); h = nt.nodes.new("ShaderNodeBsdfHairPrincipled"); h.parametrization = "COLOR"
    h.inputs["Roughness"].default_value = rough; h.inputs["Radial Roughness"].default_value = 0.7
    info = nt.nodes.new("ShaderNodeHairInfo")
    c = lin(srgb); col = mix_rgb(nt, info.outputs["Random"], tuple(c), tuple(x * (1 - var) for x in c))
    nt.links.new(col, h.inputs["Color"]); nt.links.new(h.outputs[0], out.inputs["Surface"]); return m


# ------------------------------------------------------------------ locks
def grow_locks(src, name, region, n_locks, length, mat, seed, per=18, lock_r=0.0006, gravity=0.4, curl=0.2, root_r=0.00005, pts=6, flow=None):
    """Clumped locks: each lock is `per` strands rooted in a small patch and converging toward a shared tip,
    so hair reads as sculpted tufts, not fuzz."""
    rng = random.Random(seed)
    me = src.data; me.calc_loop_triangles()
    co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    tris, w = [], []
    for t in me.loop_triangles:
        c = Vector(co[list(t.vertices)].mean(axis=0)); n = t.normal
        wt = region(c, n)
        if wt > 0: tris.append((t.vertices[:], n.copy())); w.append(t.area * wt)
    assert tris, name
    picks = rng.choices(range(len(tris)), weights=w, k=n_locks)
    curves = bpy.data.hair_curves.new(name); curves.add_curves([pts] * (n_locks * per))
    pos, rad = [], []
    down = Vector((0, 0, -1))
    for i in picks:
        (ia, ib, ic), n = tris[i]
        u, v = rng.random(), rng.random()
        if u + v > 1: u, v = 1 - u, 1 - v
        A, B, C = (Vector(co[k]) for k in (ia, ib, ic))
        root = A + (B - A) * u + (C - A) * v
        L = length * rng.uniform(0.7, 1.25)
        f = flow(root, n) if flow else down
        d0 = (n * (1 - gravity) + f * gravity + Vector((rng.gauss(0, curl) for _ in range(3)))).normalized()
        if d0.dot(n) < 0.2: d0 = (d0 + n * 0.5).normalized()
        bend = Vector((rng.gauss(0, curl) for _ in range(3))) * 0.8 + f * gravity * 0.6
        spine = [root]; d = d0
        for k in range(1, pts):
            d = (d + bend * (1.0 / pts)).normalized(); spine.append(spine[-1] + d * (L / (pts - 1)))
        tn = (spine[1] - spine[0]).normalized(); ref = Vector((0, 0, 1)) if abs(tn.z) < 0.9 else Vector((1, 0, 0))
        e1 = tn.cross(ref).normalized(); e2 = tn.cross(e1).normalized()
        for s in range(per):
            a = rng.uniform(0, 2 * math.pi); rr = lock_r * math.sqrt(rng.random())
            off = (e1 * math.cos(a) + e2 * math.sin(a)) * rr
            ls = rng.uniform(0.75, 1.05)
            for k in range(pts):
                t = k / (pts - 1)
                q = spine[0] + (spine[k] - spine[0]) * ls + off * (1 - 0.85 * t)
                pos.extend(q); rad.append(root_r * (1 - 0.8 * t))
    curves.attributes["position"].data.foreach_set("vector", pos)
    ra = curves.attributes.get("radius") or curves.attributes.new("radius", "FLOAT", "POINT")
    ra.data.foreach_set("value", rad)
    ob = link(curves, name); curves.materials.append(mat); return ob


# ------------------------------------------------------------------ the puppet
def build_head():
    base = [ell("cranium", (0, 0.003, 0.0465), (0.0236, 0.0245, 0.0255)),
            ell("jaw", (0, -0.0035, 0.0310), (0.0228, 0.0200, 0.0180)),
            ell("earL", (-0.0240, 0.003, 0.0445), (0.0028, 0.0058, 0.0085), (0, 0.25, 0)),
            ell("earR", (0.0240, 0.003, 0.0445), (0.0028, 0.0058, 0.0085), (0, -0.25, 0)),
            ell("neck", (0, 0.003, 0.008), (0.0152, 0.0142, 0.02))]
    head = fuse(base, "head", voxel=0.00028, smooth=2)
    S = Sculpt(head)
    # big planes first: flatten the face front, broaden the jaw, chin forward
    S.face(0, 0.043, 0.020, -0.0018)
    S.face(0, 0.0215, 0.0075, 0.0022, dz=-0.0004)
    for sx in (-1, 1):
        S.brush(S.surf(sx * 0.0175, 0.027), 0.009, (sx * 0.0010, -0.0004, 0))
        S.brush(S.surf(sx * 0.0195, 0.0525), 0.0065, (-sx * 0.0008, 0, 0))     # temples in
    # brow ridge and glabella
    for sx in (-1, 1):
        S.face(sx * 0.0090, 0.0540, 0.0072, 0.0015)
    S.face(0, 0.0530, 0.0045, 0.0007)
    # eye sockets: carve deep, then the cheeks rise into the smile
    for sx in (-1, 1):
        S.face(sx * 0.0094, 0.0470, 0.0060, -0.0034, tag="socket")
    for sx in (-1, 1):
        S.face(sx * 0.0132, 0.0388, 0.0075, 0.0024, dz=0.0006)
    # nose: bridge from the brow, a soft bulb, wings and the dip under it
    for t in np.linspace(0, 1, 9):
        z = 0.0505 - 0.0125 * t
        S.face(0, z, 0.0030 + 0.0018 * t, 0.0008 + 0.0042 * t ** 1.4)
    S.face(0, 0.0372, 0.0050, 0.0030)
    for sx in (-1, 1):
        S.face(sx * 0.0046, 0.0362, 0.0030, 0.0018, dx=sx * 0.0004)
    S.face(0, 0.0338, 0.0022, -0.0006)
    # smile: carve the open mouth along a curve, then build the lips around it
    def mz(x): return 0.0290 + 0.0042 * (abs(x) / 0.0105) ** 2.2
    for x in np.linspace(-0.0100, 0.0100, 15):
        open_amt = 1 - (abs(x) / 0.0105) ** 3
        S.face(x, mz(x), 0.0024, -0.0032 * open_amt - 0.0004, tag="mouth", power=1.5)
    for x in np.linspace(-0.0095, 0.0095, 11):
        S.face(x, mz(x) + 0.0030, 0.0019, 0.0006)                 # upper lip
        S.face(x, mz(x) - 0.0034 - 0.0006 * (1 - abs(x) / 0.0095), 0.0022, 0.0009)   # lower lip
    for sx in (-1, 1):   # corners dig in, nasolabial folds from the nose wings
        S.face(sx * 0.0110, mz(0.0110), 0.0020, -0.0010)
        for t in np.linspace(0, 1, 7):
            S.face(sx * (0.0064 + 0.0052 * t), 0.0360 - 0.0072 * t, 0.0016, -0.0008)
    # ears: carve the bowl on the outside face
    for sx in (-1, 1):
        S.brush(np.array([sx * 0.0270, 0.0025, 0.0445]), 0.0034, (-sx * 0.0016, 0, 0))
        S.brush(np.array([sx * 0.0264, 0.0050, 0.0470]), 0.0030, (sx * 0.0006, 0.0006, 0))   # rim
    S.commit()
    sm = head.modifiers.new("smooth", "SMOOTH"); sm.factor = 0.5; sm.iterations = 3
    select_only([head]); bpy.ops.object.modifier_apply(modifier="smooth")
    return head, S, mz


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    addon_utils.enable("cycles", default_set=True)
    sc = bpy.context.scene
    head, S, mz = build_head()
    # materials on the head: skin, and the dark inside of the mouth from the carve tags
    cheeks = [((sx * 0.0135, -0.019, 0.0385), (0.0085, 0.008, 0.0070), 0.55) for sx in (-1, 1)]
    nose = [((0, -0.028, 0.0375), (0.0065, 0.0065, 0.0070), 0.45)]
    ears = [((sx * 0.024, 0.003, 0.0445), (0.006, 0.008, 0.010), 0.6) for sx in (-1, 1)]
    skin = skin_mat(cheeks + nose + ears, ((0, -0.021, 0.0295), (0.0125, 0.008, 0.0060)))
    mouth_in = flat_mat("mouth_in", (0.22, 0.07, 0.07), 0.5)
    head.data.materials.append(skin); head.data.materials.append(mouth_in)
    mt = S.tags["mouth"]
    mi = np.zeros(len(head.data.polygons), dtype=np.int32)
    for p in head.data.polygons:
        if mt[list(p.vertices)].mean() > 0.55: mi[p.index] = 1
    head.data.polygons.foreach_set("material_index", mi)
    # teeth: a row of small rounded blocks just inside the carve, following the smile
    teeth_mat = flat_mat("teeth", (0.92, 0.89, 0.80), 0.3, coat=0.3, sss=0.1)
    for x in np.linspace(-0.0072, 0.0072, 8):
        hit = S.surf(x, mz(x) + 0.0008)
        t = ell("tooth", (x, hit[1] + 0.0002, mz(x) + 0.0010), (0.00095, 0.0008, 0.0012), segs=16)
        t.data.materials.append(teeth_mat); bpy.ops.object.shade_smooth()
    # eyes set into the sockets, lids that wrap them (smiling: upper lid low, lower lid pushed up)
    eyem = eye_mat((0.42, 0.62, 0.80))
    lid_parts = []
    for sx in (-1, 1):
        ex, ez, R = sx * 0.0094, 0.0471, 0.0041
        floor = S.surf(ex, ez)
        cy = floor[1] - 0.0034 + 0.0006 + R      # front of the ball sits ~0.6 mm proud of the old surface
        e = ell("eye", (ex, cy, ez), (R, R, R), segs=48); e.data.materials.append(eyem); bpy.ops.object.shade_smooth()
        e.rotation_euler = (0.06, 0, -sx * 0.10)  # look slightly toward camera-left and up
        for kind, keep in (("lidU", lambda v: v.z > 0.0004 - 0.10 * v.y), ("lidL", lambda v: v.z < -0.0015 + 0.05 * v.y)):
            me = bpy.data.meshes.new(kind); bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=R + 0.00035)
            dead = [v for v in bm.verts if not (keep(v.co) and v.co.y < 0.0012)]
            bmesh.ops.delete(bm, geom=dead, context="VERTS"); bm.to_mesh(me); bm.free()
            o = link(me, kind); o.location = (ex, cy, ez)
            sol = o.modifiers.new("s", "SOLIDIFY"); sol.thickness = 0.0005; sol.offset = 1
            select_only([o]); bpy.ops.object.modifier_apply(modifier="s"); bpy.ops.object.shade_smooth()
            o.data.materials.append(skin); lid_parts.append(o)
    # ---------------- body: designed cross-sections, not balls
    torso_rings = [(0.010, 0.0168, 0.0158, 0.003), (0.000, 0.0200, 0.0172, 0.003), (-0.006, 0.0290, 0.0190, 0.004), (-0.011, 0.0370, 0.0202, 0.004),
                   (-0.018, 0.0430, 0.0215, 0.005), (-0.034, 0.0425, 0.0225, 0.004), (-0.054, 0.0410, 0.0245, 0.001),
                   (-0.074, 0.0400, 0.0250, 0.000), (-0.092, 0.0375, 0.0225, 0.002), (-0.104, 0.0360, 0.0210, 0.003)]
    shirt = loft_z("shirt", torso_rings, p=2.4)
    chambray = cloth_mat("chambray", (0.36, 0.48, 0.66), "chambray")
    shirt.data.materials.append(chambray)
    grow = lambda rings, g: [(z, ax + g, ay + g, yo) for z, ax, ay, yo in rings]
    jacket_rings = grow(torso_rings[2:], 0.0024) + [(-0.118, 0.0385, 0.0235, 0.002)]
    jacket = loft_z("jacket_body", [(0.002, 0.0222, 0.0192, 0.003)] + jacket_rings, p=2.4)
    sleeves = []
    for sx in (-1, 1):
        path = spline([(sx * 0.0370, 0.005, -0.019), (sx * 0.0470, 0.006, -0.040), (sx * 0.0500, 0.004, -0.068), (sx * 0.0490, -0.004, -0.094), (sx * 0.0470, -0.010, -0.112)], 5)
        rr = np.interp(np.linspace(0, 1, len(path)), [0, 0.35, 0.6, 1.0], [0.0122, 0.0110, 0.0099, 0.0088])
        sleeves.append(loft_path("sleeve", [tuple(p) for p in path], list(rr)))
    blazer = fuse([jacket] + sleeves, "blazer", voxel=0.0006, smooth=12)
    # V opening down to the top button, with notched lapels laid on top
    def prism(tri, y0=-0.06, y1=-0.004):
        me = bpy.data.meshes.new("cut"); bm = bmesh.new()
        f = [bm.verts.new((x, y0, z)) for x, z in tri]; b = [bm.verts.new((x, y1, z)) for x, z in tri]
        bm.faces.new(f); bm.faces.new(b[::-1])
        for i in range(len(tri)):
            j = (i + 1) % len(tri); bm.faces.new((f[i], f[j], b[j], b[i]))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free(); return link(me, "cut")
    for cut in (prism([(-0.0175, 0.010), (0.0175, 0.010), (0.0, -0.060)]), prism([(-0.006, -0.1135), (0.006, -0.1135), (0.022, -0.130), (-0.022, -0.130)])):
        bo = blazer.modifiers.new("cut", "BOOLEAN"); bo.object = cut; bo.operation = "DIFFERENCE"
        select_only([blazer]); bpy.ops.object.modifier_apply(modifier="cut"); bpy.data.objects.remove(cut)
    tweed = cloth_mat("tweed", (0.40, 0.29, 0.20), "tweed")
    blazer.data.materials.clear(); blazer.data.materials.append(tweed)
    def laid(name, outline, host, mat, lift=0.0004, thick=0.0010, cuts=6):
        """A flat cloth piece (outline in x,z) laid onto a host surface: lapels, collar points, pocket flaps."""
        me = bpy.data.meshes.new(name); bm = bmesh.new()
        vs = [bm.verts.new((x, 0, z)) for x, z in outline]; bm.faces.new(vs)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=cuts, use_grid_fill=True)
        bm.to_mesh(me); bm.free(); o = link(me, name)
        for v in o.data.vertices:
            ok, loc, _, _ = host.ray_cast(Vector((v.co.x, -1, v.co.z)), Vector((0, 1, 0)))
            v.co.y = (loc.y if ok else 0) - lift
        sol = o.modifiers.new("s", "SOLIDIFY"); sol.thickness = thick; sol.offset = 1
        bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.0003; bv.segments = 2
        o.data.materials.append(mat); select_only([o]); bpy.ops.object.shade_smooth(); return o
    for sx in (-1, 1):
        lap = [(0.0172, 0.0060), (0.0230, 0.0030), (0.0255, -0.0140), (0.0215, -0.0160), (0.0225, -0.0215), (0.0060, -0.0560), (0.0012, -0.0598), (0.0170, 0.0010)]
        laid("lapel", [(sx * x, z) for x, z in (lap if sx > 0 else lap[::-1])], blazer, tweed, lift=0.0003, thick=0.0011)
        col = [(0.0040, 0.0060), (0.0160, 0.0080), (0.0130, -0.0040)]
        laid("collar", [(sx * x, z) for x, z in (col if sx > 0 else col[::-1])], shirt, chambray, lift=0.0002, thick=0.0006, cuts=3)
        flap = [(0.012, -0.090), (0.031, -0.090), (0.031, -0.096), (0.012, -0.096)]
        laid("pocket", [(sx * x, z) for x, z in (flap if sx > 0 else flap[::-1])], blazer, tweed, lift=0.0002, thick=0.0007, cuts=3)
    wood = flat_mat("button_wood", (0.32, 0.20, 0.12), 0.35, coat=0.4)
    for bz in (-0.062, -0.082):
        ok, loc, _, _ = blazer.ray_cast(Vector((0.0, -1, bz)), Vector((0, 1, 0)))
        b = ell("button", (0.0, loc.y - 0.0005, bz), (0.0024, 0.0009, 0.0024), segs=24); b.data.materials.append(wood); bpy.ops.object.shade_smooth()
    shirt_btn = flat_mat("shirt_button", (0.90, 0.88, 0.82), 0.25, coat=0.3)
    for bz in (-0.024, -0.040):
        ok, loc, _, _ = shirt.ray_cast(Vector((0.0, -1, bz)), Vector((0, 1, 0)))
        b = ell("sbutton", (0.0, loc.y - 0.0002, bz), (0.0010, 0.0004, 0.0010), segs=16); b.data.materials.append(shirt_btn); bpy.ops.object.shade_smooth()
    # shirt cuffs and hands
    hand_parts = []
    for sx in (-1, 1):
        wx, wy, wz = sx * 0.0468, -0.011, -0.116
        cuff = loft_path("cuff", [(wx, wy + 0.001, wz + 0.004), (wx, wy, wz - 0.0015)], [0.0080, 0.0078]); cuff.data.materials.append(chambray)
        palm = ell("palm", (wx, wy - 0.0005, wz - 0.0085), (0.0042, 0.0075, 0.0080))
        hand_parts.append(palm)
        for k, fy in enumerate((-0.0050, -0.0017, 0.0016, 0.0047)):
            L = (0.0085, 0.0095, 0.0090, 0.0075)[k]
            base = Vector((wx + sx * 0.0005, wy + fy, wz - 0.0145))
            mid = base + Vector((-sx * 0.0012, -0.0006, -L * 0.55)); tip = mid + Vector((-sx * 0.0030, -0.0008, -L * 0.40))
            hand_parts.append(loft_path("finger", [tuple(base), tuple(mid), tuple(tip)], [0.0017, 0.0015, 0.0012], n=16))
        hand_parts.append(loft_path("thumb", [(wx - sx * 0.002, wy - 0.006, wz - 0.006), (wx - sx * 0.0035, wy - 0.0095, wz - 0.012), (wx - sx * 0.0045, wy - 0.0105, wz - 0.0165)], [0.0021, 0.0017, 0.0013], n=16))
    hands = fuse(hand_parts, "hands", voxel=0.00025, smooth=4); hands.data.materials.append(skin)
    # trousers and shoes
    legs = [loft_z("seat", [(-0.090, 0.0350, 0.0205, 0.002), (-0.108, 0.0365, 0.0215, 0.002), (-0.122, 0.0345, 0.0200, 0.002)], p=2.3)]
    for sx in (-1, 1):
        legs.append(loft_path("leg", [(sx * 0.0175, 0.002, -0.112), (sx * 0.0185, 0.000, -0.155), (sx * 0.0190, 0.000, FLOOR + 0.010)], [0.0168, 0.0142, 0.0132]))
    jeans = fuse(legs, "jeans", voxel=0.0006, smooth=5); jeans.data.materials.append(cloth_mat("denim", (0.10, 0.13, 0.24), "denim"))
    leather = cloth_mat("leather", (0.34, 0.20, 0.11), "leather")
    sole_m = flat_mat("sole", (0.12, 0.09, 0.07), 0.6)
    for sx in (-1, 1):
        shoe = fuse([ell("toe", (sx * 0.0195, -0.012, FLOOR + 0.0055), (0.0115, 0.0150, 0.0058)),
                     ell("heel", (sx * 0.0190, 0.004, FLOOR + 0.0065), (0.0105, 0.0110, 0.0068))], "shoe", voxel=0.0004, smooth=4)
        shoe.data.materials.append(leather)
        bpy.ops.mesh.primitive_cube_add(size=1, location=(sx * 0.0193, -0.004, FLOOR + 0.0010)); so = bpy.context.active_object
        so.scale = (0.0215, 0.0335, 0.0020); bv = so.modifiers.new("b", "BEVEL"); bv.width = 0.002; bv.segments = 3
        so.data.materials.append(sole_m)
    return sc, head, S, mz, skin, lid_parts


def hair_and_beard(head, mz):
    def lip_zone(p): return abs(p.x) < 0.0125 and mz(p.x) - 0.0058 < p.z < mz(p.x) + 0.0048
    def beard(p, n):
        if n.y > 0.45 or p.z < 0.010 or p.z > 0.046: return 0
        line = 0.0335 + 0.0105 * min(abs(p.x) / 0.022, 1.0) ** 1.5
        if p.z > line or lip_zone(p): return 0
        if abs(p.x) < 0.0075 and p.z > 0.0335: return 0          # under the nose
        if p.z < 0.016 and n.y > -0.3: return 0.35                # thin onto the neck
        return 1.0
    def stache(p, n):
        return 1.0 if abs(p.x) < 0.0130 and mz(p.x) + 0.0028 < p.z < 0.0350 and n.y < -0.35 and not (abs(p.x) < 0.0012) else 0
    def hair(p, n):
        if p.z < 0.040: return 0
        if abs(p.x) > 0.0218 and 0.035 < p.z < 0.055 and n.y < 0.3 and abs(p.y - 0.003) < 0.007: return 0   # ears
        if p.z > 0.061:
            return 0.25 if p.y > -0.010 else 0.08                 # thin crown, receding front
        return 1.0 if (abs(p.x) > 0.0165 or n.y > -0.05) else 0
    def brow(p, n):
        return 1.0 if 0.0042 < abs(p.x) < 0.0150 and 0.0532 < p.z < 0.0560 + 0.0006 * (abs(p.x) < 0.009) and n.y < -0.4 else 0
    down = lambda p, n: Vector((0, -0.25, -1)).normalized()
    out_x = lambda p, n: Vector((math.copysign(0.7, p.x), 0, -0.7)).normalized()
    back = lambda p, n: Vector((math.copysign(0.4, p.x), 0.5, -0.75)).normalized()
    grow_locks(head, "beard", beard, 2800, 0.0033, hair_mat("beard", (0.60, 0.58, 0.55), 0.70), 1, per=16, lock_r=0.00055, gravity=0.6, curl=0.30, root_r=0.000045, flow=down)
    grow_locks(head, "chin_brown", lambda p, n: beard(p, n) * (1 if abs(p.x) < 0.006 and p.z < 0.024 else 0), 260, 0.0042, hair_mat("chin", (0.45, 0.37, 0.30), 0.45), 5, per=14, lock_r=0.0005, gravity=0.7, curl=0.25, root_r=0.000045, flow=down)
    grow_locks(head, "mustache", stache, 420, 0.0042, hair_mat("stache", (0.40, 0.30, 0.22), 0.40), 2, per=16, lock_r=0.0005, gravity=0.75, curl=0.15, root_r=0.000045, flow=out_x)
    grow_locks(head, "hair", hair, 2600, 0.0017, hair_mat("hair", (0.52, 0.50, 0.48), 0.6), 3, per=14, lock_r=0.0005, gravity=0.55, curl=0.25, root_r=0.00004, flow=back)
    grow_locks(head, "brows", brow, 160, 0.0024, hair_mat("brow", (0.40, 0.34, 0.29), 0.35), 4, per=10, lock_r=0.0003, gravity=0.5, curl=0.10, root_r=0.00004, flow=out_x)


def set_and_light(sc, shot, quality):
    # set: slat wall pushed back (falls out of focus), tabletop, a few warm practicals for depth
    wall_y = 0.20
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, wall_y + 0.006, 0.0), rotation=(math.radians(90), 0, 0))
    bk = bpy.context.active_object; bk.scale = (0.8, 0.6, 1); bk.data.materials.append(flat_mat("felt_dark", (0.05, 0.045, 0.04), 0.95))
    oak = cloth_mat("oak", (0.30, 0.20, 0.12), "leather", 0.3)
    x = -0.30
    while x < 0.34:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, wall_y, 0.0)); s = bpy.context.active_object
        s.scale = (0.0060, 0.006, 0.60); s.data.materials.append(oak); x += 0.0095
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.33, wall_y - 0.004, 0)); nv = bpy.context.active_object
    nv.scale = (0.25, 0.008, 0.60); nv.data.materials.append(flat_mat("navy", (0.16, 0.20, 0.32), 0.8))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0.0, FLOOR)); fl = bpy.context.active_object; fl.scale = (1.2, 0.9, 1)
    fl.data.materials.append(cloth_mat("table", (0.50, 0.36, 0.24), "leather", 0.15))
    em = bpy.data.materials.new("bulb"); nt, out, b = nodes(em)
    b.inputs["Emission Color"].default_value = (1.0, 0.62, 0.30, 1); b.inputs["Emission Strength"].default_value = 6
    nt.links.new(b.outputs[0], out.inputs["Surface"])
    rng = random.Random(4)
    for i in range(9):
        o = ell("bulb", (rng.uniform(-0.25, 0.25), wall_y - 0.02, rng.uniform(0.02, 0.15)), (0.0018,) * 3, segs=12); o.data.materials.append(em)
    def area(name, loc, target, w, size, k):
        L = bpy.data.lights.new(name, "AREA"); L.energy = w; L.size = size
        L.use_temperature = True; L.temperature = k
        o = link(L, name); o.location = loc; o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    area("key", (-0.20, -0.22, 0.14), (0, 0, 0.0), 1.6, 0.10, 3800)       # warm key, camera-left, high
    area("fill", (0.26, -0.20, -0.02), (0, 0, -0.02), 0.25, 0.25, 5200)
    area("rim", (0.16, 0.12, 0.12), (0, 0, 0.02), 1.4, 0.05, 8500)        # cool rim, back-right
    area("rimL", (-0.18, 0.10, 0.06), (0, 0, 0.02), 0.9, 0.05, 7000)
    w = bpy.data.worlds.new("w"); sc.world = w
    if w.node_tree is None: w.use_nodes = True
    w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.006, 0.006, 0.008, 1)
    # camera: 3/4 from camera-left of the puppet, eye level for medium, a little higher for full
    shots = {"medium": ((-0.085, -0.205, 0.030), (0.0, 0.0, 0.010), 50.0, 2.8, (0.0, -0.022, 0.044)),
             "full": ((-0.135, -0.430, -0.035), (0.0, 0.0, -0.066), 50.0, 5.6, (0.0, -0.022, -0.02)),
             "face": ((-0.045, -0.140, 0.048), (0.0, 0.0, 0.040), 50.0, 2.8, (0.0, -0.025, 0.044))}
    loc, tgt, lens, fs, focus = shots[shot]
    c = bpy.data.cameras.new("cam"); c.lens = lens; c.sensor_fit = "VERTICAL"; c.sensor_height = 36.0; c.clip_start = 0.001
    c.dof.use_dof = True; c.dof.aperture_fstop = fs
    o = link(c, "cam"); o.location = loc; o.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    c.dof.focus_distance = (Vector(focus) - Vector(loc)).length; sc.camera = o
    sc.render.engine = "CYCLES"; cy = sc.cycles; cy.device = cts.pick_device()
    big = quality != "preview"
    sc.render.resolution_x, sc.render.resolution_y = (1440, 1080) if shot != "full" else (1080, 1440)
    if not big: sc.render.resolution_percentage = 50
    cy.samples = 512 if big else 64; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.008 if big else 0.03
    cy.use_denoising = True; cy.denoising_input_passes = "RGB_ALBEDO_NORMAL"; cy.denoising_prefilter = "ACCURATE"
    sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"; sc.view_settings.exposure = -0.2


if __name__ == "__main__":
    out = os.path.abspath(sys.argv[1]); q = sys.argv[2] if len(sys.argv) > 2 else "preview"; shot = sys.argv[3] if len(sys.argv) > 3 else "medium"
    t0 = time.time()
    sc, head, S, mz, skin, lids = build()
    hair_and_beard(head, mz)
    # turn the head a touch toward camera and tilt it, like a held pose
    pivot = Vector((0, 0.003, 0.010))
    R = Matrix.Translation(pivot) @ Matrix.Rotation(math.radians(-9), 4, "Z") @ Matrix.Rotation(math.radians(-3), 4, "Y") @ Matrix.Translation(-pivot)
    for o in bpy.data.objects:
        if o.name.split(".")[0] in ("head", "eye", "lidU", "lidL", "tooth", "beard", "chin_brown", "mustache", "hair", "brows"):
            o.matrix_world = R @ o.matrix_world
    set_and_light(sc, shot, q)
    print(f"BUILT {time.time()-t0:.1f}s")
    sc.render.filepath = out; t = time.time(); bpy.ops.render.render(write_still=True)
    print(f"RENDERED {q} {shot} {time.time()-t:.1f}s -> {out}")
