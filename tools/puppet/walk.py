"""Rig a generated puppet mesh and animate a walk-in, a smile and a wave, on twos (anim),
or a seamless 2-second wave loop (loop).
   GLB=path/to/figure.glb [JOINTS=joints.json] <bpy-python> walk.py outdir [preview|dailies] [posetest|anim|loop]
JOINTS overrides the measured joint positions for a new figure: {"neck_frac": 0.8, "side_limit": [[z...], [x...]],
"joints": {"upperarm.L": [x, y, z], ...}}; missing joints keep the defaults (measured on the first figure).
Body skeleton with leg IK (feet planted, knees reach), a smile shape key, wool fibers on the head bone."""
import json, math, os, random, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXP1 = HERE
outdir = os.path.abspath(sys.argv[1]); os.makedirs(outdir, exist_ok=True)
q = sys.argv[2] if len(sys.argv) > 2 else "preview"
mode = sys.argv[3] if len(sys.argv) > 3 else "posetest"
t_test = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25

src = open(os.path.join(EXP1, "render_hybrid.py")).read().split("P.set_and_light(sc, shot, q)")[0]
CFG = json.load(open(os.environ["JOINTS"])) if os.environ.get("JOINTS") else {}
sys.argv = ["render_hybrid.py", os.environ["GLB"], "unused.png", q, "full", str(CFG.get("neck_frac", 0.80)), "-90", os.environ.get("FIBERS", "1")]
G = {"__name__": "hybrid", "__file__": os.path.join(EXP1, "render_hybrid.py")}
exec(compile(src, "render_hybrid.py", "exec"), G)
import bpy
from mathutils import Vector, Matrix, Quaternion
P, sc, fig, me = G["P"], G["sc"], G["fig"], G["fig"].data
FLOOR = P.FLOOR

# ---------------------------------------------------------------- skeleton (measured from height slices)
J = {"root": (0, 0.004, -0.124), "spine": (0, 0.004, -0.086), "chest": (0, 0.004, -0.046), "neck": (0, 0.003, -0.013),
     "head": (0, 0.001, 0.004), "head_end": (0, 0.0, 0.056), "base": (0, 0.004, FLOOR), "base_end": (0, 0.004, FLOOR + 0.03)}
for s, sx in (("L", -1), ("R", 1)):
    J |= {f"shoulder.{s}": (sx * 0.020, 0.005, -0.020), f"upperarm.{s}": (sx * 0.045, 0.006, -0.031),
          f"forearm.{s}": (sx * 0.061, 0.008, -0.072), f"hand.{s}": (sx * 0.067, 0.002, -0.110), f"hand_end.{s}": (sx * 0.073, -0.004, -0.150),
          f"thigh.{s}": (sx * 0.022, 0.005, -0.128), f"shin.{s}": (sx * 0.026, 0.002, -0.181), f"foot.{s}": (sx * 0.027, 0.009, FLOOR + 0.012),
          f"toe.{s}": (sx * 0.028, -0.026, FLOOR + 0.002), f"pole.{s}": (sx * 0.026, -0.12, -0.181)}
for k_, v_ in CFG.get("joints", {}).items():
    J[k_] = tuple(v_)
DEFORM = [("pelvis", "root", "spine", "base"), ("spine", "spine", "chest", "pelvis"), ("chest", "chest", "neck", "spine"),
          ("neck", "neck", "head", "chest"), ("head", "head", "head_end", "neck")]
for s in ("L", "R"):
    DEFORM += [(f"shoulder.{s}", f"shoulder.{s}", f"upperarm.{s}", "chest"), (f"upperarm.{s}", f"upperarm.{s}", f"forearm.{s}", f"shoulder.{s}"),
               (f"forearm.{s}", f"forearm.{s}", f"hand.{s}", f"upperarm.{s}"), (f"hand.{s}", f"hand.{s}", f"hand_end.{s}", f"forearm.{s}"),
               (f"thigh.{s}", f"thigh.{s}", f"shin.{s}", "pelvis"), (f"shin.{s}", f"shin.{s}", f"foot.{s}", f"thigh.{s}"),
               (f"foot.{s}", f"foot.{s}", f"toe.{s}", f"shin.{s}")]
CONTROL = [("base", "base", "base_end", None)]
for s in ("L", "R"):
    CONTROL += [(f"ik_foot.{s}", f"foot.{s}", f"toe.{s}", None), (f"pole.{s}", f"pole.{s}", None, None)]
arm_data = bpy.data.armatures.new("rig"); arm = bpy.data.objects.new("rig", arm_data); sc.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode="EDIT")
for name, h, t, par in CONTROL + DEFORM:
    eb = arm_data.edit_bones.new(name); eb.head = J[h]
    eb.tail = J[t] if t else Vector(J[h]) + Vector((0, 0, 0.01))
    eb.use_deform = (name, h, t, par) in DEFORM
for name, h, t, par in CONTROL + DEFORM:
    if par: arm_data.edit_bones[name].parent = arm_data.edit_bones[par]
bpy.ops.object.mode_set(mode="OBJECT")
for s in ("L", "R"):
    ik = arm.pose.bones[f"shin.{s}"].constraints.new("IK")
    ik.target = arm; ik.subtarget = f"ik_foot.{s}"; ik.chain_count = 2
    ik.pole_target = arm; ik.pole_subtarget = f"pole.{s}"; ik.pole_angle = math.radians(-90)
    cr = arm.pose.bones[f"foot.{s}"].constraints.new("COPY_ROTATION")
    cr.target = arm; cr.subtarget = f"ik_foot.{s}"; cr.target_space = cr.owner_space = "WORLD"

# ---------------------------------------------------------------- fewer wrinkles: relax the sculpt beside the eyes
co0 = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co0); co0 = co0.reshape(-1, 3)
ed0 = np.zeros(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed0); ed0 = ed0.reshape(-1, 2)
deg0 = np.bincount(ed0.ravel(), minlength=len(co0)).astype(float)
wm = np.zeros(len(co0))
for sx in (-1, 1):
    c = np.array([sx * 0.0195 - 0.003, -0.012, 0.027])
    wm = np.maximum(wm, np.clip(1 - np.linalg.norm((co0 - c) * [1.0, 0.8, 1.3], axis=1) / 0.010, 0, 1))
c = np.array([-0.003, -0.022, 0.044]); wm = np.maximum(wm, 0.6 * np.clip(1 - np.linalg.norm((co0 - c) * [0.6, 1, 1.4], axis=1) / 0.012, 0, 1))  # forehead lines
wm = wm * wm * (3 - 2 * wm)   # smoothstep falloff: no hard edge where the relax stops
for _ in range(10):
    acc = np.zeros_like(co0)
    for k in range(3):
        acc[:, k] = np.bincount(ed0[:, 0], co0[ed0[:, 1], k], len(co0)) + np.bincount(ed0[:, 1], co0[ed0[:, 0], k], len(co0))
    co0 = co0 + (wm[:, None] * 0.35) * (acc / np.maximum(deg0[:, None], 1) - co0)
me.vertices.foreach_set("co", co0.ravel()); me.update()
# ---------------------------------------------------------------- skin weights (distance to bones, gated by region)
co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
x, z = co[:, 0], co[:, 2]
names = [b[0] for b in DEFORM]; nb = len(names)
D = np.zeros((len(co), nb))
for i, (name, h, t, _) in enumerate(DEFORM):
    a, b = np.array(J[h]), np.array(J[t]); ab = b - a
    tt = np.clip(((co - a) @ ab) / (ab @ ab), 0, 1)
    D[:, i] = np.linalg.norm(co - (a + tt[:, None] * ab), axis=1)
SL = CFG.get("side_limit", [[-0.155, -0.085, -0.065, -0.035, -0.014], [0.060, 0.050, 0.052, 0.046, 0.040]])
side_limit = np.interp(z, SL[0], SL[1])
arm_zone = (np.abs(x) > side_limit) & (z < -0.014) & (z > -0.16)
leg_zone = z < -0.140
allow = np.ones_like(D, dtype=bool)
for i, n in enumerate(names):
    part = n.split(".")[0]; side = -1 if n.endswith(".L") else (1 if n.endswith(".R") else 0)
    if part in ("upperarm", "forearm", "hand"): allow[:, i] = arm_zone & (np.sign(x) == side)
    elif part in ("thigh", "shin", "foot"): allow[:, i] = (z < -0.110) & (np.sign(x) == side) & ~arm_zone
    elif part == "shoulder": allow[:, i] = (np.sign(x) == side) & (z > -0.065)
    elif n == "head": allow[:, i] = z > -0.014
    elif n == "pelvis": allow[:, i] = (z < -0.075) & ~arm_zone
    else: allow[:, i] = ~arm_zone & ~leg_zone
D[~allow] = 1.0
W = np.exp(-(D / 0.009) ** 2); W[~allow] = 0
kth = np.partition(W, -3, axis=1)[:, -3][:, None]; W[W < kth] = 0
W /= np.maximum(W.sum(1, keepdims=True), 1e-9)
ed = np.zeros(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
deg = np.bincount(ed.ravel(), minlength=len(co)).astype(float)
def smooth_w(W, it, mask=None, keep=0.5):
    for _ in range(it):
        acc = np.zeros_like(W)
        for i in range(nb):
            acc[:, i] = np.bincount(ed[:, 0], W[ed[:, 1], i], len(co)) + np.bincount(ed[:, 1], W[ed[:, 0], i], len(co))
        Wn = keep * W + (1 - keep) * acc / np.maximum(deg[:, None], 1)
        W = Wn if mask is None else W * (1 - mask[:, None]) + Wn * mask[:, None]
    return W / np.maximum(W.sum(1, keepdims=True), 1e-9)
W = smooth_w(W, 6)
W = smooth_w(W, 25, (arm_zone | leg_zone).astype(float), keep=0.4)   # soft elbows and knees
hz = np.clip((z - (-0.022)) / 0.009, 0, 1)[:, None]                 # rigid head: skin and wool stay locked
onehot = np.zeros(nb); onehot[names.index("head")] = 1; W = W * (1 - hz) + onehot[None] * hz
for i, n in enumerate(names):
    vg = fig.vertex_groups.new(name=n); qw = np.round(W[:, i] * 24).astype(int)
    for k in range(1, 25):
        idx = np.nonzero(qw == k)[0]
        if len(idx): vg.add(idx.tolist(), k / 24, "REPLACE")
mod = fig.modifiers.new("arm", "ARMATURE"); mod.object = arm; mod.use_deform_preserve_volume = False
jm = np.zeros(len(co))
for jn in ("forearm.L", "forearm.R", "upperarm.L", "upperarm.R", "shin.L", "shin.R", "thigh.L", "thigh.R"):
    jm = np.maximum(jm, np.clip(1 - np.linalg.norm(co - np.array(J[jn]), axis=1) / 0.024, 0, 1))
jm = np.maximum(jm, np.clip(1 - np.abs(z - (-0.017)) / 0.010, 0, 1) * (np.abs(x) < 0.03))
jg = fig.vertex_groups.new(name="joint_smooth")
for k in range(1, 11):
    idx = np.nonzero(np.round(jm * 10) == k)[0]
    if len(idx): jg.add(idx.tolist(), k / 10, "REPLACE")
cs = fig.modifiers.new("relax", "CORRECTIVE_SMOOTH"); cs.vertex_group = "joint_smooth"
cs.iterations = 30; cs.factor = 0.9; cs.smooth_type = "LENGTH_WEIGHTED"; cs.rest_source = "ORCO"; cs.use_pin_boundary = True

# ---------------------------------------------------------------- smile shape key, found from the painted teeth
masks = np.zeros(len(co) * 4, dtype=np.float32); me.color_attributes["masks"].data.foreach_get("color", masks); masks = masks.reshape(-1, 4)
teeth = (masks[:, 2] > 0.45) & (co[:, 1] < -0.012) & (co[:, 2] > -0.004) & (co[:, 2] < 0.030) & (np.abs(x) < 0.016)
tz = float(np.median(co[teeth, 2])) if teeth.sum() > 20 else 0.014
txl, txr = (np.percentile(x[teeth], 2), np.percentile(x[teeth], 98)) if teeth.sum() > 20 else (-0.008, 0.008)
print(f"MOUTH teeth={int(teeth.sum())} z={tz:.4f} x=[{txl:.4f},{txr:.4f}]")
fig.shape_key_add(name="Basis", from_mix=False)
sk = fig.shape_key_add(name="smile", from_mix=False); sk.slider_min = -1.0
d = np.zeros_like(co)
for cxp, sgn in ((txl - 0.0015, -1), (txr + 0.0015, 1)):
    c = np.array([cxp, np.median(co[teeth, 1]) if teeth.sum() > 20 else -0.025, tz])
    r = np.linalg.norm((co - c) * [1.0, 1.6, 1.0], axis=1)
    w = np.clip(1 - r / 0.0075, 0, 1) ** 2 * (co[:, 1] < c[1] + 0.006)
    d += w[:, None] * np.array([sgn * 0.0016, 0.0005, 0.0030])          # corners out, back and up
    cc = c + np.array([sgn * 0.0030, 0.002, 0.0065])                     # cheek apples lift
    w2 = np.clip(1 - np.linalg.norm(co - cc, axis=1) / 0.007, 0, 1) ** 2 * (co[:, 1] < cc[1] + 0.004)
    d += w2[:, None] * np.array([sgn * 0.0005, -0.0007, 0.0016])
skd = (co + d).astype(np.float32); sk.data.foreach_set("co", skd.ravel())

wool = bpy.data.objects.get("wool")
if wool:
    pb = arm.pose.bones["head"]
    wool.parent = arm; wool.parent_type = "BONE"; wool.parent_bone = "head"
    wool.matrix_parent_inverse = (arm.matrix_world @ pb.bone.matrix_local @ Matrix.Translation((0, pb.bone.length, 0))).inverted()

# ---------------------------------------------------------------- posing
def rest3(n): return arm.data.bones[n].matrix_local.to_3x3()
def set_rot(n, R):
    M = rest3(n); pb = arm.pose.bones[n]; pb.rotation_mode = "QUATERNION"
    pb.rotation_quaternion = (M.inverted() @ R.to_matrix() @ M).to_quaternion()
def aim(n, target_dir, parent_R=Quaternion()):
    b = arm.data.bones[n]; d0 = (b.tail_local - b.head_local).normalized()
    return d0.rotation_difference(parent_R.inverted() @ Vector(target_dir).normalized())
def axis_rot(axis, deg): return Quaternion(Vector(axis).normalized(), math.radians(deg))
def set_loc(n, world_offset):
    pb = arm.pose.bones[n]; pb.location = rest3(n).inverted() @ Vector(world_offset)
def ease(a, b, u): u = min(max((u - a) / (b - a), 0), 1); return u * u * (3 - 2 * u)

T_TOTAL = 6.0
STEP = 0.034; STEPS = [("L", 0.00, 0.60, -STEP), ("R", 0.60, 1.20, -2 * STEP), ("L", 1.20, 1.80, -2 * STEP), ("R", 1.80, 2.40, -STEP)]
Y0 = 0.105   # start this far behind the mark (toward the wall)
def foot_state(side, t):
    """y offset (relative to rest), lift height and pitch for one foot at time t."""
    y = Y0; lift = 0.0; pitch = 0.0
    for s, a, b, dy in STEPS:
        if s != side: continue
        if t >= b: y += dy
        elif t > a:
            u = (t - a) / (b - a); e = u * u * (3 - 2 * u)
            y += dy * e; lift = 0.010 * math.sin(math.pi * u); pitch = 18 * math.sin(math.pi * u) - 10 * math.sin(math.pi * min(u * 1.6, 1)) * (u < 0.6)
    return y, lift, pitch

def pose(t, rng=None, jit=0.0):
    J_ = lambda: rng.gauss(0, jit) if rng else 0.0
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"; pb.rotation_quaternion = Quaternion(); pb.location = (0, 0, 0)
    # feet and body travel
    yl, ll, pl = foot_state("L", t); yr, lr, pr = foot_state("R", t)
    set_loc("ik_foot.L", (0, yl, ll)); set_rot("ik_foot.L", axis_rot((1, 0, 0), pl))
    set_loc("ik_foot.R", (0, yr, lr)); set_rot("ik_foot.R", axis_rot((1, 0, 0), pr))
    set_loc("pole.L", (0, yl, 0)); set_loc("pole.R", (0, yr, 0))
    walking = 1 - ease(2.25, 2.6, t)
    phase = math.sin(math.pi * ((t % 0.6) / 0.6))           # 0 at contact, 1 at passing
    which = 1 if (t % 1.2) < 0.6 else -1                   # +1 while L swings
    body_y = (yl + yr) / 2 + (-0.006 * walking)             # lean the body a touch ahead of the feet
    bob = (0.0022 * phase - 0.0018) * walking - 0.0010 * ease(2.4, 2.7, t) * (1 - ease(2.7, 3.1, t))
    set_loc("base", (0, body_y, bob))
    set_rot("pelvis", axis_rot((0, 0, 1), 5 * which * walking + J_()) @ axis_rot((0, 1, 0), -3 * which * phase * walking))
    set_rot("spine", axis_rot((0, 0, 1), -3 * which * walking) @ axis_rot((1, 0, 0), 3 * walking))
    # wave and smile timing
    up = ease(3.35, 3.85, t) * (1 - ease(5.35, 5.85, t))
    wave = math.sin((t - 3.85) / 1.5 * 3 * 2 * math.pi) * ease(3.8, 3.95, t) * (1 - ease(5.2, 5.4, t))
    set_rot("chest", axis_rot((0, 0, 1), -2 * which * walking + 5 * up + J_()) @ axis_rot((0, 1, 0), -2 * up))
    set_rot("neck", axis_rot((1, 0, 0), -2 * walking + J_()))
    look = ease(2.3, 3.0, t)
    set_rot("head", axis_rot((0, 0, 1), 2 * which * walking + 8 * up) @ axis_rot((0, 1, 0), 8 * up + 2.5 * wave * up + J_())
            @ axis_rot((1, 0, 0), 3 * walking - 4 * look * (1 - up) - 3 * up + J_()))
    # arms: swing while walking, left arm relaxes, right arm waves
    swing = 14 * which * phase * walking
    rL = aim("upperarm.L", (-0.25, 0.05, -1.0)); set_rot("upperarm.L", axis_rot((1, 0, 0), -swing) @ rL)
    set_rot("forearm.L", aim("forearm.L", (-0.12, -0.25 - 0.2 * walking, -1.0), rL))
    rest_dir = Vector((0.30, 0.05, -1.0)); up_dir = Vector((0.42, -0.30, -0.86))
    rU = aim("upperarm.R", rest_dir.lerp(up_dir, up).normalized())
    set_rot("upperarm.R", axis_rot((1, 0, 0), swing * (1 - up)) @ rU)
    fdir = Vector((0.15, -0.25 - 0.2 * walking, -1.0)).lerp(Vector((0.30, -0.80, 0.50)), up).normalized()
    set_rot("forearm.R", axis_rot(rU.inverted() @ Vector((0, -1, 0)), 25 * wave) @ aim("forearm.R", fdir, rU))
    set_rot("hand.R", axis_rot((0, -1, 0), 10 * wave + J_()))
    set_rot("shoulder.R", axis_rot((0, 1, 0), -8 * up))
    # smile: soft while walking, grows into a full grin when he stops
    fig.data.shape_keys.key_blocks["smile"].value = -0.6 + 1.6 * ease(2.7, 3.4, t)

def pose_loop(t, period=2.0):
    """Seamless loop: the waving arm stays up, two waves per period, gentle sway and head tilt."""
    w = 2 * math.pi * t / period
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"; pb.rotation_quaternion = Quaternion(); pb.location = (0, 0, 0)
    set_loc("base", (0, 0, 0.0008 * math.sin(2 * w)))
    set_rot("pelvis", axis_rot((0, 1, 0), 1.5 * math.sin(w)))
    set_rot("spine", axis_rot((0, 1, 0), -1.0 * math.sin(w)) @ axis_rot((0, 0, 1), 3.0))
    set_rot("chest", axis_rot((0, 0, 1), 4.0) @ axis_rot((0, 1, 0), -2.0 + 0.8 * math.sin(w + 0.6)))
    set_rot("head", axis_rot((0, 1, 0), 7.0 + 3.0 * math.sin(w + 1.0)) @ axis_rot((0, 0, 1), 8.0) @ axis_rot((1, 0, 0), -3.0 + 1.5 * math.sin(2 * w + 0.4)))
    rL = aim("upperarm.L", (-0.25, 0.05, -1.0)); set_rot("upperarm.L", axis_rot((1, 0, 0), 2.0 * math.sin(w)) @ rL)
    set_rot("forearm.L", aim("forearm.L", (-0.12, -0.25, -1.0), rL))
    rU = aim("upperarm.R", (0.42, -0.30, -0.86)); set_rot("upperarm.R", rU)
    wave = math.sin(2 * w)
    rF = aim("forearm.R", (0.30, -0.80, 0.50), rU)
    set_rot("forearm.R", axis_rot(rU.inverted() @ Vector((0, -1, 0)), 25 * wave) @ rF)
    set_rot("hand.R", axis_rot((0, -1, 0), 12 * math.sin(2 * w - 0.5)))
    set_rot("shoulder.R", axis_rot((0, 1, 0), -8))
    fig.data.shape_keys.key_blocks["smile"].value = 0.0

def key(f):
    for pb in arm.pose.bones:
        pb.keyframe_insert("rotation_quaternion", frame=f); pb.keyframe_insert("location", frame=f)
    fig.data.shape_keys.key_blocks["smile"].keyframe_insert("value", frame=f)

P.set_and_light(sc, "full", q)
cam = sc.camera
cam.location = Vector(cam.location) + Vector((-0.02, -0.07, 0.010))
for pb in arm.pose.bones: pb.rotation_mode = "QUATERNION"

def focus_on_head():
    hb = arm.pose.bones["head"]; hp = arm.matrix_world @ hb.head
    cam.data.dof.focus_distance = (hp + Vector((0, -0.02, 0.02)) - cam.location).length

if mode == "posetest":
    for i, tt in enumerate([float(v) for v in str(t_test).split(",")] if isinstance(t_test, str) else [t_test]):
        pass
    if os.environ.get("FACE"):
        cd = bpy.data.cameras.new("fc"); cd.lens = 50; cd.sensor_fit = "VERTICAL"; cd.sensor_height = 36; cd.clip_start = 0.001
        fc = bpy.data.objects.new("fc", cd); sc.collection.objects.link(fc); sc.camera = fc; cam = fc
        for val, nm in ((-0.6, "soft"), (1.0, "grin")):
            pose(4.4); fig.data.shape_keys.key_blocks["smile"].value = val; bpy.context.view_layer.update()
            hp = arm.matrix_world @ arm.pose.bones["head"].head
            fc.location = hp + Vector((-0.02, -0.11, 0.02)); fc.rotation_euler = (hp + Vector((0, 0, 0.02)) - fc.location).to_track_quat("-Z", "Y").to_euler()
            cd.dof.use_dof = False
            sc.render.filepath = os.path.join(outdir, f"face_{nm}.png"); bpy.ops.render.render(write_still=True)
        sys.exit(0)
    for tt in (0.3, 0.9, 1.5, 4.4):
        pose(tt); bpy.context.view_layer.update(); focus_on_head()
        sc.render.filepath = os.path.join(outdir, f"pose_{tt:.1f}.png"); bpy.ops.render.render(write_still=True)
        print(f"RENDERED pose {tt}", flush=True)
elif mode == "loop":
    fps = 24; nposes = 24; rng = random.Random(3)
    cam.location = Vector(cam.location) + Vector((0.0, 0.03, -0.004))
    for i in range(nposes):
        pose_loop(i / nposes * 2.0); bpy.context.view_layer.update(); focus_on_head()
        for L in [o for o in sc.objects if o.type == "LIGHT"]:
            base = L.get("base_energy") or L.data.energy; L["base_energy"] = base
            L.data.energy = base * rng.uniform(0.985, 1.015)
        sc.render.filepath = os.path.join(outdir, f"p{i:03d}.png"); bpy.ops.render.render(write_still=True)
        print(f"POSE {i}", flush=True)
    print("RENDERED loop")
else:
    fps = 24; nframes = int(fps * T_TOTAL); rng = random.Random(7)
    for f in range(1, nframes + 1, 2):
        pose((f - 1) / fps, rng, 0.3); key(f)
        hb = arm.pose.bones["head"]
    sc.frame_set(3); sc.frame_set(1)
    for f in range(1, nframes + 1, 2):
        sc.frame_set(f); bpy.context.view_layer.update(); focus_on_head()
        for L in [o for o in sc.objects if o.type == "LIGHT"]:
            base = L.get("base_energy") or L.data.energy; L["base_energy"] = base
            L.data.energy = base * rng.uniform(0.985, 1.015)
        sc.render.filepath = os.path.join(outdir, f"f{f:03d}.png"); bpy.ops.render.render(write_still=True)
        print(f"FRAME {f}", flush=True)
    print("RENDERED anim")
