#!/usr/bin/env python
# coding: utf-8

# In[2]:


import bpy
import csv
import math

# === CONFIGURATION ===
csv_path = "C:/Users/nsifu/Desktop/Blender Stuff/binary_evolution_blender.csv"  # <-- adjust path
AU_SCALE = 1.0
STAR_NAME = "Star"
WD_NAME   = "White Dwarf"

# === LOAD OBJECTS ===
star = bpy.data.objects.get(STAR_NAME)
wd   = bpy.data.objects.get(WD_NAME)
if not star or not wd:
    raise ValueError("Could not find 'Star' or 'White Dwarf' in the scene.")

print(f"Loaded {STAR_NAME} and {WD_NAME}")

# === HELPER: ENSURE BLACKBODY EMISSION MATERIAL ===
def ensure_blackbody_material(obj, name):
    """Create a physically-correct blackbody emission material."""
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    blackbody = nodes.new("ShaderNodeBlackbody")

    blackbody.location = (-400, 0)
    emission.location = (-200, 0)
    links.new(blackbody.outputs["Color"], emission.inputs["Color"])
    links.new(emission.outputs["Emission"], output.inputs["Surface"])

    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return mat, blackbody, emission

mat_star, node_star_bb, node_star_em = ensure_blackbody_material(star, "StarEmission_Blackbody")
mat_wd,   node_wd_bb,   node_wd_em   = ensure_blackbody_material(wd, "WDEmission_Blackbody")

# === READ CSV DATA ===
with open(csv_path, newline='') as f:
    rows = list(csv.DictReader(f))
print(f"Loaded {len(rows)} simulation frames from CSV")

# === ANIMATION SETTINGS ===
scene = bpy.context.scene
scene.frame_start = 0
scene.frame_end   = len(rows)

# === INITIALIZE VARIABLES ===
a_prev        = float(rows[0]["a_AU"]) * AU_SCALE
bright_d_prev = float(rows[0]["brightness_d"])
bright_w_prev = float(rows[0]["brightness_w"])

# Smoothing parameters
ORBIT_SMOOTH  = 0.85
BRIGHT_SMOOTH = 0.7
MIN_WD_TEMP   = 5000
VISUAL_SCALE  = 1000
WD_VISUAL_SIZE = 20
WD_ORBIT_EXAGGERATION = 1.5
R_solar_in_AU = 0.00465  # 1 R_sun = 0.00465 AU

# === MAIN ANIMATION LOOP ===
for i, row in enumerate(rows):
    frame = int(row["frame"])
    a_raw = float(row["a_AU"]) * AU_SCALE
    R_d   = float(row["R_d_Rsun"])
    R_w   = float(row["R_wd_Rsun"])

    # --- linear brightness values (L/Lsun) ---
    bright_d_raw = float(row["brightness_d"])
    bright_w_raw = float(row["brightness_w"])

    T_d     = float(row["color_d_K"])
    T_w_raw = float(row["color_wd_K"])

    # Smooth orbital separation
    a = a_raw if i == 0 else (1 - ORBIT_SMOOTH) * a_raw + ORBIT_SMOOTH * a_prev
    a_prev = a

    # Smooth brightness
    if i == 0:
        bright_d, bright_w = bright_d_raw, bright_w_raw
    else:
        bright_d = (1 - BRIGHT_SMOOTH) * bright_d_raw + BRIGHT_SMOOTH * bright_d_prev
        bright_w = (1 - BRIGHT_SMOOTH) * bright_w_raw + BRIGHT_SMOOTH * bright_w_prev
    bright_d_prev, bright_w_prev = bright_d, bright_w

    # Fix WD temperature if dim
    if T_w_raw < MIN_WD_TEMP or bright_w < 0.05:
        T_w = max(MIN_WD_TEMP, T_d * 0.9)
    else:
        T_w = T_w_raw

    # Orbital phase evolution
    phase = (2 * math.pi * i / len(rows)) % (2 * math.pi)

    # Barycentric distances
    M_d = float(row["M_d_Msun"])
    M_wd = float(row["M_wd_Msun"])
    M_total = M_d + M_wd
    r_wd = a * (M_d / M_total) * WD_ORBIT_EXAGGERATION
    r_d  = a * (M_wd / M_total) / WD_ORBIT_EXAGGERATION

    # Update locations
    wd.location = ( r_wd * VISUAL_SCALE * math.cos(phase),
                    r_wd * VISUAL_SCALE * math.sin(phase), 0)
    star.location = (-r_d * VISUAL_SCALE * math.cos(phase),
                     -r_d * VISUAL_SCALE * math.sin(phase), 0)
    wd.keyframe_insert("location", frame=frame)
    star.keyframe_insert("location", frame=frame)

    # Scale based on radius
    R_d_scaled = R_d * R_solar_in_AU * VISUAL_SCALE
    R_w_scaled = R_w * R_solar_in_AU * VISUAL_SCALE * WD_VISUAL_SIZE
    star.scale = (R_d_scaled, R_d_scaled, R_d_scaled)
    wd.scale   = (R_w_scaled, R_w_scaled, R_w_scaled)
    star.keyframe_insert("scale", frame=frame)
    wd.keyframe_insert("scale", frame=frame)

    # === PHYSICAL COLOR + BRIGHTNESS ===
    node_star_bb.inputs["Temperature"].default_value = T_d
    node_star_em.inputs["Strength"].default_value = min(bright_d * 300, 1000)
    node_star_bb.inputs["Temperature"].keyframe_insert("default_value", frame=frame)
    node_star_em.inputs["Strength"].keyframe_insert("default_value", frame=frame)

    node_wd_bb.inputs["Temperature"].default_value = T_w
    node_wd_em.inputs["Strength"].default_value = max(bright_w * 300, 1.0)
    node_wd_bb.inputs["Temperature"].keyframe_insert("default_value", frame=frame)
    node_wd_em.inputs["Strength"].keyframe_insert("default_value", frame=frame)


# In[ ]:




