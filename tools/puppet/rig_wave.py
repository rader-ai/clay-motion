"""Motion test: rig a generated puppet mesh and animate a short greeting on twos.
   GLB=path/to/figure.glb DECIMATE=0.15 <bpy-python> rig_wave.py outdir [preview|dailies] [full|medium] [posetest|anim] [blend]
Builds the hybrid-look puppet (render_hybrid.py), places a 19-bone skeleton from measured joint
positions, computes smooth skin weights, parents the wool fibers to the head bone, then either renders
one test pose or the animation (every second frame = stop motion on twos, with per-pose jitter)."""
import math, os, random, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
outdir = os.path.abspath(sys.argv[1]); os.makedirs(outdir, exist_ok=True)
q = sys.argv[2] if len(sys.argv) > 2 else "preview"
shot = sys.argv[3] if len(sys.argv) > 3 else "full"
mode = sys.argv[4] if len(sys.argv) > 4 else "posetest"
save_blend = len(sys.argv) > 5 and sys.argv[5] == "blend"

# build the puppet with the hybrid look (everything before lighting)
src = open(os.path.join(HERE, "render_hybrid.py")).read().split("P.set_and_light(sc, shot, q)")[0]
sys.argv = ["render_hybrid.py", os.environ["GLB"], "unused.png", q, shot, "0.79", "-90", "1"]
G = {"__name__": "hybrid", "__file__": os.path.join(HERE, "render_hybrid.py")}
exec(compile(src, "render_hybrid.py", "exec"), G)
import bpy
from mathutils import Vector, Matrix, Quaternion
P, sc, fig, me = G["P"], G["sc"], G["fig"], G["fig"].data

# ---------------------------------------------------------------- skeleton (metres, neck base z=0, faces -y)
J = {"root": (0, 0.004, -0.112), "spine": (0, 0.004, -0.078), "chest": (0, 0.004, -0.042), "neck": (0, 0.003, -0.014),
     "head": (0, 0.001, 0.004), "head_end": (0, 0.0, 0.058)}
for s, sx in (("L", -1), ("R", 1)):
    J |= {f"shoulder.{s}": (sx * 0.018, 0.005, -0.018), f"upperarm.{s}": (sx * 0.040, 0.006, -0.027),
          f"forearm.{s}": (sx * 0.060, 0.008, -0.064), f"hand.{s}": (sx * 0.068, 0.002, -0.099), f"hand_end.{s}": (sx * 0.074, -0.004, -0.140),
          f"thigh.{s}": (sx * 0.020, 0.005, -0.118), f"shin.{s}": (sx * 0.023, 0.003, -0.168), f"foot.{s}": (sx * 0.024, 0.009, -0.205),
          f"toe.{s}": (sx * 0.026, -0.024, -0.217)}
BONES = [("pelvis", "root", "spine", None), ("spine", "spine", "chest", "pelvis"), ("chest", "chest", "neck", "spine"),
         ("neck", "neck", "head", "chest"), ("head", "head", "head_end", "neck")]
for s in ("L", "R"):
    BONES += [(f"shoulder.{s}", f"shoulder.{s}", f"upperarm.{s}", "chest"), (f"upperarm.{s}", f"upperarm.{s}", f"forearm.{s}", f"shoulder.{s}"),
              (f"forearm.{s}", f"forearm.{s}", f"hand.{s}", f"upperarm.{s}"), (f"hand.{s}", f"hand.{s}", f"hand_end.{s}", f"forearm.{s}"),
              (f"thigh.{s}", f"thigh.{s}", f"shin.{s}", "pelvis"), (f"shin.{s}", f"shin.{s}", f"foot.{s}", f"thigh.{s}"),
              (f"foot.{s}", f"foot.{s}", f"toe.{s}", f"shin.{s}")]
arm_data = bpy.data.armatures.new("rig"); arm = bpy.data.objects.new("rig", arm_data); sc.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode="EDIT")
for name, h, t, par in BONES:
    eb = arm_data.edit_bones.new(name); eb.head = J[h]; eb.tail = J[t]
    if par: eb.parent = arm_data.edit_bones[par]; eb.use_connect = False
bpy.ops.object.mode_set(mode="OBJECT")

# ---------------------------------------------------------------- skin weights: distance to bone segments,
# limited by body side and region, then smoothed across the surface
co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
x, z = co[:, 0], co[:, 2]
names = [b[0] for b in BONES]; nb = len(names)
D = np.zeros((len(co), nb))
for i, (name, h, t, _) in enumerate(BONES):
    a, b = np.array(J[h]), np.array(J[t]); ab = b - a
    tt = np.clip(((co - a) @ ab) / (ab @ ab), 0, 1)
    D[:, i] = np.linalg.norm(co - (a + tt[:, None] * ab), axis=1)
allow = np.ones_like(D, dtype=bool)
# arms: near the shoulder anything outboard of the chest; lower down only what is outboard of the
# jacket side (slices show a clear gap at |x| ~ 0.055 below z = -0.085)
side_limit = np.interp(z, [-0.15, -0.085, -0.060, -0.030, -0.012], [0.056, 0.055, 0.050, 0.040, 0.036])
arm_zone = (np.abs(x) > side_limit) & (z < -0.012) & (z > -0.15)
leg_zone = z < -0.122
for i, n in enumerate(names):
    side = -1 if n.endswith(".L") else (1 if n.endswith(".R") else 0)
    if n.split(".")[0] in ("upperarm", "forearm", "hand"):
        allow[:, i] = arm_zone & (np.sign(x) == side)
    elif n.split(".")[0] in ("thigh", "shin", "foot"):
        allow[:, i] = (z < -0.100) & (np.sign(x) == side)
    elif n.split(".")[0] == "shoulder":
        allow[:, i] = (np.sign(x) == side) & (z > -0.06)
    elif n == "head":
        allow[:, i] = z > -0.012
    elif n == "pelvis":
        allow[:, i] = z < -0.07
    else:
        allow[:, i] = ~arm_zone & ~leg_zone
D[~allow] = 1.0
W = np.exp(-(D / 0.009) ** 2)
W[~allow] = 0
# keep the strongest 3 bones per vertex
if nb > 3:
    kth = np.partition(W, -3, axis=1)[:, -3][:, None]; W[W < kth] = 0
W /= np.maximum(W.sum(1, keepdims=True), 1e-9)
ed = np.zeros(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
deg = np.bincount(ed.ravel(), minlength=len(co)).astype(float)
for _ in range(6):
    acc = np.zeros_like(W)
    for i in range(nb):
        acc[:, i] = np.bincount(ed[:, 0], W[ed[:, 1], i], len(co)) + np.bincount(ed[:, 1], W[ed[:, 0], i], len(co))
    W = 0.5 * W + 0.5 * acc / np.maximum(deg[:, None], 1)
W /= np.maximum(W.sum(1, keepdims=True), 1e-9)
# soften the upper-arm/forearm hand-off so the elbow bends like a sleeve instead of folding
am = arm_zone.astype(float)
for _ in range(25):
    acc = np.zeros_like(W)
    for i in range(nb):
        acc[:, i] = np.bincount(ed[:, 0], W[ed[:, 1], i], len(co)) + np.bincount(ed[:, 1], W[ed[:, 0], i], len(co))
    Wn = 0.4 * W + 0.6 * acc / np.maximum(deg[:, None], 1)
    W = W * (1 - am[:, None]) + Wn * am[:, None]
W /= np.maximum(W.sum(1, keepdims=True), 1e-9)
# the head moves as one piece: skin, beard paint and the wool fibers (parented to the head bone) stay locked
hz = np.clip((z - (-0.021)) / 0.009, 0, 1)[:, None]
onehot = np.zeros(nb); onehot[names.index("head")] = 1
W = W * (1 - hz) + onehot[None] * hz
levels = 24
for i, n in enumerate(names):
    vg = fig.vertex_groups.new(name=n)
    qw = np.round(W[:, i] * levels).astype(int)
    for k in range(1, levels + 1):
        idx = np.nonzero(qw == k)[0]
        if len(idx): vg.add(idx.tolist(), k / levels, "REPLACE")
mod = fig.modifiers.new("arm", "ARMATURE"); mod.object = arm; mod.use_deform_preserve_volume = False
# joints crease and pinch when they bend; relax them back toward the rest surface, only near the joints
jm = np.zeros(len(co))
for jn in ("forearm.L", "forearm.R", "upperarm.L", "upperarm.R"):   # elbows and shoulders (bone heads)
    jm = np.maximum(jm, np.clip(1 - np.linalg.norm(co - np.array(J[jn]), axis=1) / 0.024, 0, 1))
jm = np.maximum(jm, np.clip(1 - np.abs(z - (-0.016)) / 0.010, 0, 1) * (np.abs(x) < 0.03))   # neck band
jg = fig.vertex_groups.new(name="joint_smooth")
for k in range(1, 11):
    idx = np.nonzero(np.round(jm * 10) == k)[0]
    if len(idx): jg.add(idx.tolist(), k / 10, "REPLACE")
cs = fig.modifiers.new("relax", "CORRECTIVE_SMOOTH"); cs.vertex_group = "joint_smooth"
cs.iterations = 30; cs.factor = 0.9; cs.smooth_type = "LENGTH_WEIGHTED"; cs.rest_source = "ORCO"; cs.use_pin_boundary = True

# wool fibers follow the head bone
wool = bpy.data.objects.get("wool")
if wool:
    pb = arm.pose.bones["head"]
    wool.parent = arm; wool.parent_type = "BONE"; wool.parent_bone = "head"
    wool.matrix_parent_inverse = (arm.matrix_world @ pb.bone.matrix_local @ Matrix.Translation((0, pb.bone.length, 0))).inverted()

# ---------------------------------------------------------------- posing helpers (armature-space intent)
def rest3(n): return arm.data.bones[n].matrix_local.to_3x3()
def set_rot(n, R):
    """R: rotation expressed in the bone's rest frame orientation, as armature-space intent."""
    M = rest3(n); pb = arm.pose.bones[n]; pb.rotation_mode = "QUATERNION"
    pb.rotation_quaternion = (M.inverted() @ R.to_matrix() @ M).to_quaternion()
def aim(n, target_dir, parent_R=Quaternion()):
    """Rotation that turns bone n from its rest direction to target_dir, given its parent's posed rotation."""
    b = arm.data.bones[n]; d0 = (b.tail_local - b.head_local).normalized()
    local_target = parent_R.inverted() @ Vector(target_dir).normalized()
    return d0.rotation_difference(local_target)
def axis_rot(axis, deg): return Quaternion(Vector(axis).normalized(), math.radians(deg))
def key_all(f):
    for pb in arm.pose.bones:
        pb.keyframe_insert("rotation_quaternion", frame=f)

def pose(t, jit=0.0, rng=None):
    """Greeting: settle, anticipation dip, arm up, three waves, head tilt and nod, settle back. t in 0..1."""
    def ease(a, b, u): u = min(max((u - a) / (b - a), 0), 1); return u * u * (3 - 2 * u)
    up = ease(0.10, 0.30, t) * (1 - ease(0.82, 0.98, t))
    dip = math.sin(math.pi * ease(0.02, 0.14, t)) * (1 - up)
    wave = math.sin((t - 0.30) / 0.52 * 3 * 2 * math.pi) * ease(0.28, 0.36, t) * (1 - ease(0.74, 0.82, t))
    J_ = lambda: rng.gauss(0, jit) if rng else 0.0
    for pb in arm.pose.bones: pb.rotation_mode = "QUATERNION"; pb.rotation_quaternion = Quaternion()
    # body: weight shift and a lean into the wave
    set_rot("pelvis", axis_rot((0, 1, 0), 2.0 * up + J_()) @ axis_rot((1, 0, 0), -2.0 * dip))
    set_rot("spine", axis_rot((0, 1, 0), -2.5 * up + J_()) @ axis_rot((1, 0, 0), 3.0 * dip))
    set_rot("chest", axis_rot((0, 0, 1), 6.0 * up + J_()) @ axis_rot((0, 1, 0), -2.0 * up))
    set_rot("neck", axis_rot((1, 0, 0), -4.0 * dip + J_()))
    set_rot("head", axis_rot((0, 1, 0), 9.0 * up + 3.0 * wave * up + J_()) @ axis_rot((1, 0, 0), -5.0 * up + 4.0 * dip + J_()) @ axis_rot((0, 0, 1), 10.0 * up))
    # resting arm (L, screen-left) comes in from the A-pose
    rL = aim("upperarm.L", (-0.25, 0.05, -1.0)); set_rot("upperarm.L", rL.slerp(Quaternion(), 0.0) @ axis_rot((0, 1, 0), J_()))
    set_rot("forearm.L", aim("forearm.L", (-0.12, -0.25, -1.0), rL))
    # waving arm (R, screen-right): upper arm out and up, forearm vertical, hand waves about the facing axis
    rest_dir = Vector((0.30, 0.05, -1.0)); up_dir = Vector((0.42, -0.30, -0.86))
    d = rest_dir.lerp(up_dir, up).normalized()
    rU = aim("upperarm.R", d); set_rot("upperarm.R", rU @ axis_rot((0, 1, 0), J_()))
    fdir = Vector((0.15, -0.25, -1.0)).lerp(Vector((0.30, -0.80, 0.50)), up).normalized()
    rF = aim("forearm.R", fdir, rU)
    set_rot("forearm.R", axis_rot(rU.inverted() @ Vector((0, -1, 0)), 25 * wave) @ rF)
    set_rot("hand.R", axis_rot((0, -1, 0), 10 * wave + J_()))
    set_rot("shoulder.R", axis_rot((0, 1, 0), -8 * up))

P.set_and_light(sc, shot, q)
cam = sc.camera
if shot == "full":   # pull back a touch so the raised hand stays in frame
    cam.location = Vector(cam.location) + Vector((-0.02, -0.06, 0.012))

if mode == "posetest":
    pose(0.45)
    sc.render.filepath = os.path.join(outdir, "posetest.png"); bpy.ops.render.render(write_still=True)
    for nm, loc, tgt in (("face", (-0.03, -0.15, 0.03), (0.0, 0.0, 0.02)), ("elbow", (0.02, -0.17, -0.05), (0.06, 0.0, -0.05))):
        cd = bpy.data.cameras.new(nm); cd.lens = 50; cd.sensor_fit = "VERTICAL"; cd.sensor_height = 36; cd.clip_start = 0.001
        co_ = bpy.data.objects.new(nm, cd); sc.collection.objects.link(co_); co_.location = loc
        co_.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y").to_euler(); sc.camera = co_
        sc.render.filepath = os.path.join(outdir, f"posetest_{nm}.png"); bpy.ops.render.render(write_still=True)
    print("RENDERED posetest")
else:
    fps, secs = 24, 3.0; nframes = int(fps * secs)
    rng = random.Random(11)
    for f in range(1, nframes + 1, 2):          # one pose per two frames: stop motion on twos
        pose((f - 1) / (nframes - 1), jit=0.35, rng=rng); key_all(f)
    if save_blend: bpy.ops.wm.save_as_mainfile(filepath=os.path.join(outdir, "puppet_rigged.blend"))
    sc.frame_set(3); sc.frame_set(1); bpy.context.view_layer.update()   # warm-up: first pose evaluates fully
    for f in range(1, nframes + 1, 2):
        sc.frame_set(f)
        # lights breathe a hair between poses, like a real stage (boil)
        for L in [o for o in sc.objects if o.type == "LIGHT"]:
            base = L.get("base_energy") or L.data.energy; L["base_energy"] = base
            L.data.energy = base * rng.uniform(0.985, 1.015)
        sc.render.filepath = os.path.join(outdir, f"f{f:03d}.png"); bpy.ops.render.render(write_still=True)
        print(f"FRAME {f}", flush=True)
    print("RENDERED anim")
