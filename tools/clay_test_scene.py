"""Clay look test scene, built in true metres. Usage:
   bpyenv/bin/python scene.py params.json out_prefix
Renders a medium shot and a head close-up with Cycles CPU."""
import bpy, addon_utils, json, math, sys, os, time
from mathutils import Vector

P = {
    # clay shader v1 defaults (LOOK_DEV 2.1)
    "clay_rough": 0.48, "clay_rough_var": 0.06, "sss_weight": 0.25, "sss_scale": 0.0004,
    "sss_radius": [1.0, 0.35, 0.2], "ior": 1.47, "sheen": 0.15, "sheen_rough": 0.5, "coat": 0.0,
    "dent_depth": 0.0004, "dent_size": 0.008, "crumb_bump": 0.15, "crumb_size": 0.0002,
    "tool_bump": 0.25, "fp_strength": 0.3, "marble": 0.25, "part_jitter": 0.04,
    # light (LOOK_DEV 4)
    "key_w": 40.0, "key_radius": 0.0175, "key_k": 3200, "key_size_deg": 30, "key_blend": 0.2,
    "fill_w": 1.6, "rim_w": 18.0, "world": 0.004,
    # camera (LOOK_DEV 3)
    "fstop": 11.0, "lens": 35.0,
    "res": [640, 360], "samples": 64, "denoise": True,
}

def srgb_to_lin(c):
    return [((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c]

def node(nt, kind, **kw):
    n = nt.nodes.new(kind)
    for k, v in kw.items():
        if k in n.inputs: n.inputs[k].default_value = v
        else: setattr(n, k, v)
    return n

def clay_material(name, base_srgb, second_srgb, p, seed):
    m = bpy.data.materials.new(name)
    nt = m.node_tree if m.node_tree else None
    if nt is None:
        m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    L = nt.links.new
    out = node(nt, 'ShaderNodeOutputMaterial')
    bsdf = node(nt, 'ShaderNodeBsdfPrincipled')
    bsdf.subsurface_method = 'RANDOM_WALK'
    tc = node(nt, 'ShaderNodeTexCoord')
    # object coords (metres)
    def noise(scale, detail=4.0, rough=0.55, w=0.0):
        n = node(nt, 'ShaderNodeTexNoise', noise_dimensions='4D')
        n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail
        n.inputs['Roughness'].default_value = rough; n.inputs['W'].default_value = w + seed
        L(tc.outputs['Object'], n.inputs['Vector']); return n
    # colour: marbling between two related pigments
    marb = noise(1 / 0.006, 2.0, 0.5, 1.3)
    ramp = node(nt, 'ShaderNodeMapRange'); ramp.inputs['From Min'].default_value = 0.45; ramp.inputs['From Max'].default_value = 0.7
    ramp.inputs['To Max'].default_value = p['marble']
    L(marb.outputs['Fac'], ramp.inputs['Value'])
    mix = node(nt, 'ShaderNodeMix', data_type='RGBA')
    mix.inputs['A'].default_value = (*srgb_to_lin(base_srgb), 1); mix.inputs['B'].default_value = (*srgb_to_lin(second_srgb), 1)
    L(ramp.outputs['Result'], mix.inputs['Factor'])
    # cavity / handled grime from AO
    ao = node(nt, 'ShaderNodeAmbientOcclusion'); ao.inputs['Distance'].default_value = 0.004
    grime = node(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY')
    L(mix.outputs['Result'], grime.inputs['A'])
    aomr = node(nt, 'ShaderNodeMapRange'); aomr.inputs['To Min'].default_value = 0.8; aomr.inputs['To Max'].default_value = 1.0
    L(ao.outputs['AO'], aomr.inputs['Value'])
    comb = node(nt, 'ShaderNodeCombineColor'); L(aomr.outputs['Result'], comb.inputs['Red']); L(aomr.outputs['Result'], comb.inputs['Green']); L(aomr.outputs['Result'], comb.inputs['Blue'])
    L(comb.outputs['Color'], grime.inputs['B']); grime.inputs['Factor'].default_value = 1.0
    col_out = grime.outputs['Result']
    if p.get('specks', 0) > 0:
        sv = node(nt, 'ShaderNodeTexVoronoi', feature='F1', voronoi_dimensions='3D'); sv.inputs['Scale'].default_value = 1 / 0.0015
        L(tc.outputs['Object'], sv.inputs['Vector'])
        # keep only a few cells: random cell colour above a threshold, and only near the cell centre
        sep = node(nt, 'ShaderNodeSeparateColor'); L(sv.outputs['Color'], sep.inputs['Color'])
        th = node(nt, 'ShaderNodeMath', operation='GREATER_THAN'); th.inputs[1].default_value = 1 - p['specks']; L(sep.outputs['Red'], th.inputs[0])
        near = node(nt, 'ShaderNodeMath', operation='LESS_THAN'); near.inputs[1].default_value = 0.12; L(sv.outputs['Distance'], near.inputs[0])
        both = node(nt, 'ShaderNodeMath', operation='MULTIPLY'); L(th.outputs['Value'], both.inputs[0]); L(near.outputs['Value'], both.inputs[1])
        mk = node(nt, 'ShaderNodeMix', data_type='RGBA'); L(both.outputs['Value'], mk.inputs['Factor']); L(col_out, mk.inputs['A'])
        mk.inputs['B'].default_value = (0.05, 0.04, 0.035, 1)
        col_out = mk.outputs['Result']
    if p.get('smudge', 0) > 0:
        # handling stains: patchy grey-brown smudges from fingers and other clays, strongest on light colours
        sm_n = noise(1 / 0.012, 3.0, 0.6, 21.0)
        sm_r = node(nt, 'ShaderNodeMapRange'); sm_r.inputs['From Min'].default_value = 0.52; sm_r.inputs['From Max'].default_value = 0.68
        sm_r.inputs['To Max'].default_value = p['smudge']
        L(sm_n.outputs['Fac'], sm_r.inputs['Value'])
        sm_m = node(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); L(sm_r.outputs['Result'], sm_m.inputs['Factor'])
        L(col_out, sm_m.inputs['A']); sm_m.inputs['B'].default_value = (0.55, 0.50, 0.45, 1)
        col_out = sm_m.outputs['Result']
    L(col_out, bsdf.inputs['Base Color'])
    # roughness 0.48 +/- 0.06 from 2 mm noise
    rn = noise(1 / 0.002, 2.0, 0.5, 2.1)
    rmr = node(nt, 'ShaderNodeMapRange'); rmr.inputs['To Min'].default_value = p['clay_rough'] - p['clay_rough_var']; rmr.inputs['To Max'].default_value = p['clay_rough'] + p['clay_rough_var']
    L(rn.outputs['Fac'], rmr.inputs['Value']); L(rmr.outputs['Result'], bsdf.inputs['Roughness'])
    bsdf.inputs['IOR'].default_value = p['ior']
    bsdf.inputs['Subsurface Weight'].default_value = p['sss_weight']
    bsdf.inputs['Subsurface Scale'].default_value = p['sss_scale']
    bsdf.inputs['Subsurface Radius'].default_value = p['sss_radius']
    bsdf.inputs['Sheen Weight'].default_value = p['sheen']; bsdf.inputs['Sheen Roughness'].default_value = p['sheen_rough']
    bsdf.inputs['Coat Weight'].default_value = p['coat']
    # relief: meso dents (displacement), tool marks + crumb (bump)
    dn = noise(1 / p['dent_size'], 1.0, 0.4, 3.7)
    dmr = node(nt, 'ShaderNodeMapRange'); dmr.inputs['From Min'].default_value = 0.35; dmr.inputs['From Max'].default_value = 0.65
    dmr.inputs['To Min'].default_value = -1.0; dmr.inputs['To Max'].default_value = 1.0
    L(dn.outputs['Fac'], dmr.inputs['Value'])
    h_meso = dmr.outputs['Result']
    if p.get('dent_cluster', 0) > 0:
        # dents gather where hands worked the clay instead of covering every surface evenly
        cl = noise(1 / 0.03, 1.0, 0.4, 9.1)
        cmr = node(nt, 'ShaderNodeMapRange'); cmr.inputs['From Min'].default_value = 0.5 - 0.1; cmr.inputs['From Max'].default_value = 0.5 + 0.1
        cmr.inputs['To Min'].default_value = 1 - p['dent_cluster']; cmr.inputs['To Max'].default_value = 1.0
        L(cl.outputs['Fac'], cmr.inputs['Value'])
        mm = node(nt, 'ShaderNodeMath', operation='MULTIPLY'); L(h_meso, mm.inputs[0]); L(cmr.outputs['Result'], mm.inputs[1]); h_meso = mm.outputs['Value']
    if p.get('smear', 0) > 0:
        # thumb smears: shallow grooves stretched along one direction, 5 to 10 mm long
        mp = node(nt, 'ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.0, 1.0, 0.25); mp.inputs['Rotation'].default_value = (0.4, 0.9, 0.2)
        L(tc.outputs['Object'], mp.inputs['Vector'])
        sn = node(nt, 'ShaderNodeTexNoise', noise_dimensions='4D'); sn.inputs['Scale'].default_value = 1 / p.get('smear_size', 0.0025); sn.inputs['Detail'].default_value = 2.0; sn.inputs['W'].default_value = seed + 11
        L(mp.outputs['Vector'], sn.inputs['Vector'])
        smr = node(nt, 'ShaderNodeMapRange'); smr.inputs['From Min'].default_value = 0.4; smr.inputs['From Max'].default_value = 0.6; smr.inputs['To Min'].default_value = -p['smear']; smr.inputs['To Max'].default_value = p['smear']
        L(sn.outputs['Fac'], smr.inputs['Value'])
        sm_out = smr.outputs['Result']
        if p.get('smear_patch', 0) > 0:
            pn = noise(1 / 0.02, 1.0, 0.4, 13.3)
            pmr = node(nt, 'ShaderNodeMapRange'); pmr.inputs['From Min'].default_value = 0.5; pmr.inputs['From Max'].default_value = 0.6
            pmr.inputs['To Min'].default_value = 1 - p['smear_patch']; pmr.inputs['To Max'].default_value = 1.0
            L(pn.outputs['Fac'], pmr.inputs['Value'])
            spm = node(nt, 'ShaderNodeMath', operation='MULTIPLY'); L(sm_out, spm.inputs[0]); L(pmr.outputs['Result'], spm.inputs[1]); sm_out = spm.outputs['Value']
        ad = node(nt, 'ShaderNodeMath', operation='ADD'); L(h_meso, ad.inputs[0]); L(sm_out, ad.inputs[1]); h_meso = ad.outputs['Value']
    if p.get('face_clean', 0) > 0:
        # faces kept cleaner: fade relief above the neck line (object z > 0.085 m)
        sep = node(nt, 'ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sep.inputs['Vector'])
        fm = node(nt, 'ShaderNodeMapRange'); fm.inputs['From Min'].default_value = 0.082; fm.inputs['From Max'].default_value = 0.09
        fm.inputs['To Min'].default_value = 1.0; fm.inputs['To Max'].default_value = 1 - p['face_clean']
        L(sep.outputs['Z'], fm.inputs['Value'])
        mf = node(nt, 'ShaderNodeMath', operation='MULTIPLY'); L(h_meso, mf.inputs[0]); L(fm.outputs['Result'], mf.inputs[1]); h_meso = mf.outputs['Value']
    if p.get('facets', 0) > 0:
        # sculpted planes: each 8 to 15 mm cell gets a slight planar tilt, with a soft crease where cells meet
        vo = node(nt, 'ShaderNodeTexVoronoi', feature='F1', voronoi_dimensions='3D'); vo.inputs['Scale'].default_value = 1 / p.get('facet_size', 0.011)
        vo.inputs['Randomness'].default_value = 0.9
        L(tc.outputs['Object'], vo.inputs['Vector'])
        sub = node(nt, 'ShaderNodeVectorMath', operation='SUBTRACT'); L(tc.outputs['Object'], sub.inputs[0]); L(vo.outputs['Position'], sub.inputs[1])
        cc = node(nt, 'ShaderNodeVectorMath', operation='SUBTRACT'); L(vo.outputs['Color'], cc.inputs[0]); cc.inputs[1].default_value = (0.5, 0.5, 0.5)
        dot = node(nt, 'ShaderNodeVectorMath', operation='DOT_PRODUCT'); L(sub.outputs['Vector'], dot.inputs[0]); L(cc.outputs['Vector'], dot.inputs[1])
        # dot is in metres times ~0.5; scale to the dent units (-1..1 is about dent_depth)
        fs = node(nt, 'ShaderNodeMath', operation='MULTIPLY'); fs.inputs[1].default_value = p['facets'] / max(p.get('facet_size', 0.011) * 0.25, 1e-6)
        L(dot.outputs['Value'], fs.inputs[0])
        ve = node(nt, 'ShaderNodeTexVoronoi', feature='DISTANCE_TO_EDGE', voronoi_dimensions='3D'); ve.inputs['Scale'].default_value = 1 / p.get('facet_size', 0.011); ve.inputs['Randomness'].default_value = 0.9
        L(tc.outputs['Object'], ve.inputs['Vector'])
        cr = node(nt, 'ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.0; cr.inputs['From Max'].default_value = 0.06
        cr.inputs['To Min'].default_value = -p.get('crease', 0.5); cr.inputs['To Max'].default_value = 0.0
        L(ve.outputs['Distance'], cr.inputs['Value'])
        a1 = node(nt, 'ShaderNodeMath', operation='ADD'); L(h_meso, a1.inputs[0]); L(fs.outputs['Value'], a1.inputs[1])
        a2 = node(nt, 'ShaderNodeMath', operation='ADD'); L(a1.outputs['Value'], a2.inputs[0]); L(cr.outputs['Result'], a2.inputs[1]); h_meso = a2.outputs['Value']
    if p.get('wobble', 0) > 0:
        wn = noise(1 / 0.025, 1.0, 0.3, 17.0)
        wm = node(nt, 'ShaderNodeMapRange'); wm.inputs['From Min'].default_value = 0.3; wm.inputs['From Max'].default_value = 0.7
        wm.inputs['To Min'].default_value = -p['wobble']; wm.inputs['To Max'].default_value = p['wobble']
        L(wn.outputs['Fac'], wm.inputs['Value'])
        aw = node(nt, 'ShaderNodeMath', operation='ADD'); L(h_meso, aw.inputs[0]); L(wm.outputs['Result'], aw.inputs[1]); h_meso = aw.outputs['Value']
    disp = node(nt, 'ShaderNodeDisplacement'); disp.inputs['Scale'].default_value = p['dent_depth']; disp.inputs['Midlevel'].default_value = 0.0
    L(h_meso, disp.inputs['Height'])
    L(disp.outputs['Displacement'], out.inputs['Displacement'])
    crumb = noise(1 / p['crumb_size'], 2.0, 0.6, 5.5)
    tool = node(nt, 'ShaderNodeTexVoronoi', feature='SMOOTH_F1'); tool.inputs['Scale'].default_value = 1 / 0.0015
    L(tc.outputs['Object'], tool.inputs['Vector'])
    # fingerprint-ish ridges: sin(2*pi*d/0.00043) around a few pinch points, distorted
    hgt = node(nt, 'ShaderNodeMath', operation='ADD')
    L(crumb.outputs['Fac'], hgt.inputs[0])
    tw = node(nt, 'ShaderNodeMath', operation='MULTIPLY'); tw.inputs[1].default_value = p['tool_bump']
    L(tool.outputs['Distance'], tw.inputs[0]); L(tw.outputs['Value'], hgt.inputs[1])
    bump = node(nt, 'ShaderNodeBump'); bump.inputs['Strength'].default_value = p['crumb_bump']; bump.inputs['Distance'].default_value = 0.0002
    L(hgt.outputs['Value'], bump.inputs['Height'])
    L(bump.outputs['Normal'], bsdf.inputs['Normal'])
    L(bsdf.outputs['BSDF'], out.inputs['Surface'])
    try:
        m.displacement_method = 'BOTH'
    except Exception:
        pass
    return m

def simple_mat(name, srgb, rough, sheen=0.0, sss=0.0, ior=1.45, coat=0.0, noise_scale=None, noise_amt=0.0, bump=0.0, bump_scale=200.0):
    m = bpy.data.materials.new(name)
    if m.node_tree is None: m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = node(nt, 'ShaderNodeOutputMaterial'); b = node(nt, 'ShaderNodeBsdfPrincipled')
    b.inputs['Base Color'].default_value = (*srgb_to_lin(srgb), 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Sheen Weight'].default_value = sheen; b.inputs['Subsurface Weight'].default_value = sss; b.inputs['IOR'].default_value = ior
    b.inputs['Coat Weight'].default_value = coat
    if noise_scale:
        tc = node(nt, 'ShaderNodeTexCoord'); n = node(nt, 'ShaderNodeTexNoise'); n.inputs['Scale'].default_value = noise_scale; n.inputs['Detail'].default_value = 6
        nt.links.new(tc.outputs['Object'], n.inputs['Vector'])
        mx = node(nt, 'ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); mx.inputs['Factor'].default_value = noise_amt
        mx.inputs['A'].default_value = (*srgb_to_lin(srgb), 1); nt.links.new(n.outputs['Fac'], mx.inputs['B'])
        nt.links.new(mx.outputs['Result'], b.inputs['Base Color'])
        if bump:
            n2 = node(nt, 'ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = bump_scale; n2.inputs['Detail'].default_value = 8
            nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
            bb = node(nt, 'ShaderNodeBump'); bb.inputs['Strength'].default_value = bump; bb.inputs['Distance'].default_value = 0.0005
            nt.links.new(n2.outputs['Fac'], bb.inputs['Height']); nt.links.new(bb.outputs['Normal'], b.inputs['Normal'])
    nt.links.new(b.outputs['BSDF'], out.inputs['Surface'])
    return m

def ellipsoid(name, loc, size, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return o

def build(p):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    addon_utils.enable('cycles', default_set=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    # --- figure: parts joined into one volume, like pressed clay
    parts = [
        ellipsoid('body', (0, 0, 0.048), (0.030, 0.026, 0.040)),
        ellipsoid('head', (0.001, -0.002, 0.103), (0.025, 0.023, 0.024)),
        ellipsoid('armL', (-0.032, -0.002, 0.052), (0.008, 0.008, 0.024), (0, 0.35, 0)),
        ellipsoid('armR', (0.031, -0.004, 0.056), (0.008, 0.008, 0.023), (0, -0.5, 0)),
        ellipsoid('footL', (-0.013, -0.008, 0.007), (0.012, 0.016, 0.007)),
        ellipsoid('footR', (0.014, -0.006, 0.007), (0.012, 0.016, 0.007)),
    ]
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts: o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join(); fig = bpy.context.active_object; fig.name = 'figure'
    r = fig.modifiers.new('remesh', 'REMESH'); r.mode = 'VOXEL'; r.voxel_size = 0.0007
    sm = fig.modifiers.new('smooth', 'CORRECTIVE_SMOOTH'); sm.iterations = 6
    bpy.ops.object.modifier_apply(modifier='remesh'); bpy.ops.object.modifier_apply(modifier='smooth')
    bpy.ops.object.shade_smooth()
    ochre = clay_material('clay_ochre', tuple(p.get('body_srgb', (0.72, 0.50, 0.24))), tuple(p.get('body2_srgb', (0.66, 0.42, 0.20))), p, 0.0)
    fig.data.materials.append(ochre)
    nose = ellipsoid('nose', (0.002, -0.026, 0.100), (0.007, 0.008, 0.006))
    nose.data.materials.append(clay_material('clay_terracotta', (0.62, 0.30, 0.18), (0.58, 0.27, 0.16), p, 7.0))
    bpy.ops.object.shade_smooth()
    resin = simple_mat('resin', (0.92, 0.90, 0.85), 0.04, ior=1.52)
    pupil = simple_mat('pupil', (0.02, 0.02, 0.02), 0.05, ior=1.52)
    for sx in (-0.009, 0.010):
        e = ellipsoid('eye', (sx, -0.019, 0.110), (0.0055, 0.004, 0.0055)); e.data.materials.append(resin); bpy.ops.object.shade_smooth()
        pp = ellipsoid('pupil', (sx, -0.0225, 0.1105), (0.0022, 0.0012, 0.0022)); pp.data.materials.append(pupil); bpy.ops.object.shade_smooth()
    ball = ellipsoid('probe_ball', (0.085, 0.02, 0.015), (0.015, 0.015, 0.015))
    ball.data.materials.append(clay_material('clay_offwhite', (0.80, 0.76, 0.68), (0.76, 0.71, 0.62), p, 3.0)); bpy.ops.object.shade_smooth()
    # --- set: linen tabletop and a painted card backdrop
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0.15, 0)); tab = bpy.context.active_object; tab.scale = (0.8, 0.8, 1)
    tab.data.materials.append(simple_mat('linen', tuple(p.get('table_srgb', (0.60, 0.55, 0.46))), 0.9, sheen=0.4, noise_scale=p.get('table_noise', 900), noise_amt=p.get('table_noise_amt', 0.35), bump=p.get('table_bump', 0.25), bump_scale=p.get('table_bump_scale', 2500)))
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0.32, 0.25), rotation=(math.radians(90), 0, 0)); bd = bpy.context.active_object; bd.scale = (0.9, 0.5, 1)
    bd.data.materials.append(simple_mat('card', tuple(p.get('backdrop_srgb', (0.47, 0.50, 0.46))), 0.85, noise_scale=p.get('bd_noise', 40), noise_amt=p.get('bd_noise_amt', 0.3), bump=p.get('bd_bump', 0.1), bump_scale=p.get('bd_bump_scale', 300)))
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.11, 0.09, 0.03)); blk = bpy.context.active_object; blk.scale = (0.05, 0.04, 0.06)
    blk.rotation_euler = (0, 0, 0.3)
    blk.data.materials.append(simple_mat('wood', (0.55, 0.40, 0.26), 0.7, noise_scale=120, noise_amt=0.4, bump=0.2, bump_scale=600))
    bev = blk.modifiers.new('bev', 'BEVEL'); bev.width = 0.0012; bev.segments = 2
    # --- lights
    def look_at(o, target):
        d = Vector(target) - o.location; o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    key = bpy.data.lights.new('key', 'SPOT'); key.energy = p['key_w']; key.shadow_soft_size = p['key_radius']
    key.spot_size = math.radians(p['key_size_deg']); key.spot_blend = p['key_blend']
    try:
        key.use_temperature = True; key.temperature = p['key_k']
    except Exception: key.color = (1.0, 0.72, 0.45)
    ko = bpy.data.objects.new('key', key); sc.collection.objects.link(ko); ko.location = (-0.55, -0.75, 0.55); look_at(ko, (0, 0, 0.07))
    fill = bpy.data.lights.new('fill', 'AREA'); fill.energy = p['fill_w']; fill.size = 0.35
    try:
        fill.use_temperature = True; fill.temperature = 4300
    except Exception: pass
    fo = bpy.data.objects.new('fill', fill); sc.collection.objects.link(fo); fo.location = (0.6, -0.6, 0.25); look_at(fo, (0, 0, 0.06))
    rim = bpy.data.lights.new('rim', 'SPOT'); rim.energy = p['rim_w']; rim.shadow_soft_size = 0.012; rim.spot_size = math.radians(25); rim.spot_blend = 0.3
    try:
        rim.use_temperature = True; rim.temperature = 3600
    except Exception: pass
    ro = bpy.data.objects.new('rim', rim); sc.collection.objects.link(ro); ro.location = (0.35, 0.55, 0.45); look_at(ro, (0, 0, 0.09))
    world = bpy.data.worlds.new('w'); sc.world = world
    if world.node_tree is None: world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg: bg.inputs['Color'].default_value = (p['world'],) * 3 + (1,)
    # --- render settings
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = p['samples']; cy.use_denoising = p['denoise']
    cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02
    if p.get('denoise_accurate'):
        try:
            cy.denoiser = 'OPENIMAGEDENOISE'; cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.denoising_prefilter = 'ACCURATE'
        except Exception as e: print('denoise settings', e)
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = p.get('look', 'None'); sc.view_settings.exposure = p.get('exposure', 0.0)
    if p.get('wb_k'):
        sc.view_settings.use_white_balance = True; sc.view_settings.white_balance_temperature = p['wb_k']
    sc.render.resolution_x, sc.render.resolution_y = p['res']; sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_depth = '16'
    return sc

def camera(sc, loc, target, lens, fstop, name):
    c = bpy.data.cameras.new(name); c.lens = lens; c.sensor_fit = 'HORIZONTAL'; c.sensor_width = 36.0
    c.clip_start = 0.001  # Blender's 0.1 m default cuts into puppets at true scale
    c.dof.use_dof = True; c.dof.aperture_fstop = fstop
    o = bpy.data.objects.new(name, c); sc.collection.objects.link(o); o.location = loc
    d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler(); c.dof.focus_distance = d.length
    return o

if __name__ == '__main__':
    prm = dict(P)
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]): prm.update(json.load(open(sys.argv[1])))
    prefix = sys.argv[2] if len(sys.argv) > 2 else 'out'
    sc = build(prm)
    shots = {'medium': ((0.03, -0.40, 0.13), (0.01, 0.0, 0.065), 35.0), 'close': ((0.012, -0.16, 0.112), (0.002, 0.0, 0.102), 50.0)}
    # optional wider lenses: move the camera in so the framing stays the same
    for nm, key in (('medium', 'lens_medium'), ('close', 'lens_close')):
        if prm.get(key):
            loc, tgt, lens = shots[nm]; k = prm[key] / lens
            shots[nm] = (tuple(t + (l - t) * k for l, t in zip(loc, tgt)), tgt, prm[key])
    for nm, (loc, tgt, lens) in shots.items():
        if prm.get('only') and nm not in prm['only']: continue
        cam = camera(sc, loc, tgt, lens, prm['fstop'], nm); sc.camera = cam
        t = time.time(); sc.render.filepath = os.path.abspath(f'{prefix}_{nm}.png'); bpy.ops.render.render(write_still=True)
        print(f'RENDERED {nm} {time.time()-t:.1f}s')
