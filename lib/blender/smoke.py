"""Blender API smoke test (ENGINEERING.md section 3).

Run with the pinned interpreter:
    <bpy-env>/bin/python lib/blender/smoke.py [out_dir]

Checks the version string, the node types and engine IDs the studio relies on,
the 5.x APIs models often get wrong, and renders one frame with EEVEE and with
Cycles on the best device. Prints JSON; exits 1 on any failure. Unknown names fail loudly.
"""
import json, os, sys, tempfile, time

EXPECTED_VERSION = (5, 2, 2)
REQUIRED_NODES = [
    "ShaderNodeBsdfPrincipled", "ShaderNodeTexNoise", "ShaderNodeTexVoronoi",
    "ShaderNodeMix", "ShaderNodeMapRange", "ShaderNodeAmbientOcclusion",
    "ShaderNodeBump", "ShaderNodeDisplacement", "ShaderNodeTexImage",
    "ShaderNodeHairInfo", "ShaderNodeBsdfHair", "ShaderNodeBsdfHairPrincipled",
    "CompositorNodeRLayers", "CompositorNodeGlare", "CompositorNodeLensdist",
]
ENGINES = ["BLENDER_EEVEE", "CYCLES", "BLENDER_WORKBENCH"]
# Workbench isn't a Python add-on; its enum item can be absent from bl_rna in a bpy build, so it's checked by assignment.


def main(out_dir):
    import bpy, addon_utils
    addon_utils.enable("cycles", default_set=True)  # engine list is dynamic; Cycles registers on enable
    res = {"ok": True, "checks": {}, "renders": {}}

    def check(name, cond, detail=""):
        res["checks"][name] = {"pass": bool(cond), "detail": str(detail)}
        if not cond:
            res["ok"] = False

    check("version", tuple(bpy.app.version) == EXPECTED_VERSION, bpy.app.version_string)

    for n in REQUIRED_NODES:
        check(f"node:{n}", hasattr(bpy.types, n))

    for e in ENGINES:
        try:
            bpy.context.scene.render.engine = e
            check(f"engine:{e}", bpy.context.scene.render.engine == e)
        except TypeError as ex:
            check(f"engine:{e}", False, ex)

    # 5.x API shapes the adapter depends on
    check("api:slotted_actions", "slots" in bpy.types.Action.bl_rna.properties)
    check("api:scene.compositing_node_group", "compositing_node_group" in bpy.types.Scene.bl_rna.properties)
    check("api:grease_pencil_v3", hasattr(bpy.types, "GreasePencilv3") or hasattr(bpy.data, "grease_pencils"))

    # Minimal scene: a sphere, a plane, a light, a camera
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(0, 0, 0.03))
    bpy.ops.mesh.primitive_plane_add(size=0.5)
    light_data = bpy.data.lights.new("key", "AREA"); light_data.energy = 20
    light = bpy.data.objects.new("key", light_data); light.location = (0.2, -0.2, 0.3)
    scene.collection.objects.link(light)
    cam_data = bpy.data.cameras.new("cam"); cam = bpy.data.objects.new("cam", cam_data)
    cam.location = (0, -0.3, 0.12); cam.rotation_euler = (1.35, 0, 0)
    scene.collection.objects.link(cam); scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = 320, 180

    # Cycles device: prefer Metal, then OptiX, then CUDA
    device = "CPU"
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for kind in ("METAL", "OPTIX", "CUDA"):
            try:
                prefs.compute_device_type = kind
            except TypeError:
                continue
            prefs.get_devices()
            gpus = [d for d in prefs.devices if d.type == kind]
            if gpus:
                for d in prefs.devices:
                    d.use = d.type == kind
                device = kind
                break
    except Exception as ex:  # noqa: BLE001 - report, don't hide
        res["checks"]["cycles_prefs"] = {"pass": False, "detail": repr(ex)}
    res["cycles_device"] = device

    for engine in ("BLENDER_EEVEE", "CYCLES"):
        scene.render.engine = engine
        if engine == "CYCLES":
            scene.cycles.device = "GPU" if device != "CPU" else "CPU"
            scene.cycles.samples = 16
        path = os.path.join(out_dir, f"smoke_{engine.lower()}.png")
        scene.render.filepath = path
        t = time.time()
        try:
            bpy.ops.render.render(write_still=True)
            ok = os.path.exists(path)
            res["renders"][engine] = {"pass": ok, "seconds": round(time.time() - t, 2), "path": path}
            if not ok:
                res["ok"] = False
        except Exception as ex:  # noqa: BLE001
            res["renders"][engine] = {"pass": False, "error": repr(ex)}
            res["ok"] = False

    print(json.dumps(res, indent=2))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="clay-smoke-")
    os.makedirs(out, exist_ok=True)
    sys.exit(main(out))
