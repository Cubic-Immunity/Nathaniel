#!/usr/bin/env python
# coding: utf-8

# In[1]:


import bpy
import csv
import math

# === CONFIGURATION ===
csv_path = "C:/Users/nsifu/Desktop/Blender Stuff/binary_evolution_blender.csv"   # update this part
AU_SCALE = 1  # scale down 1 AU to Blender units
STAR_NAME = "Star"
WD_NAME = "White Dwarf"

# === LOAD OBJECTS ===
star = bpy.data.objects.get(STAR_NAME)
wd = bpy.data.objects.get(WD_NAME)
if not star or not wd:
    raise ValueError("Could not find 'Star' or 'White Dwarf' in the scene.")

# === BLACKBODY COLOR FUNCTION ===
def kelvin_to_rgb(T):
    """Approximate blackbody color (RGB 0-1) for given temperature in Kelvin."""
    T = max(1000, min(40000, T)) / 100.0
    r = g = b = 0.0
    if T <= 66:
        r = 1.0
        g = min(1.0, 0.39008157876901960784 * math.log(T) - 0.63184144378862745098)
        b = 0.0 if T <= 19 else min(1.0, 0.54320678911019607843 * math.log(T - 10) - 1.19625408914)
    else:
        r = min(1.0, 1.29293618606274509804 * (T - 60)**(-0.1332047592))
        g = min(1.0, 1.12989086089529411765 * (T - 60)**(-0.0755148492))
        b = 1.0
    return (r, g, b, 1.0)

# === READ CSV ===
frames = []
rows = []
with open(csv_path, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        frames.append(int(row["frame"]))
        rows.append(row)

print(f"Loaded {len(rows)} frames from {csv_path}")

# === ENSURE EMISSION MATERIALS ===
def ensure_emission_material(obj, name):
    mat = (bpy.data.materials.get(name) or 
           bpy.data.materials.new(name=name))
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (-200, 0)
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return mat, emission

mat_star, node_star = ensure_emission_material(star, "StarEmission")
mat_wd, node_wd = ensure_emission_material(wd, "WDEmission")

# === ANIMATION ===
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = len(rows)

# === INITIALIZE SMOOTHING VARIABLES ===
a_prev = float(rows[0]["a_AU"]) * AU_SCALE
total_time = 0.0
bright_w_prev = float(rows[0]["brightness_w"])
bright_d_prev = float(rows[0]["brightness_d"])

# Smoothing parameters
ORBIT_SMOOTH = 0.85  # Orbital separation smoothing (0-1, higher = smoother)
BRIGHT_SMOOTH = 0.7  # Brightness smoothing
MIN_WD_TEMP = 5000  

for i, row in enumerate(rows):
    frame = int(row["frame"])
    a_raw = float(row["a_AU"]) * AU_SCALE
    R_d = float(row["R_d_Rsun"])
    R_w = float(row["R_wd_Rsun"])
    bright_d_raw = float(row["brightness_d"])
    bright_w_raw = float(row["brightness_w"])
    T_d = float(row["color_d_K"])
    T_w_raw = float(row["color_wd_K"])

    # SMOOTH ORBITAL SEPARATION
    if i == 0:
        a = a_raw
    else:
        a = (1 - ORBIT_SMOOTH) * a_raw + ORBIT_SMOOTH * a_prev
    a_prev = a

    # SMOOTH BRIGHTNESS
    if i == 0:
        bright_d = bright_d_raw
        bright_w = bright_w_raw
    else:
        bright_d = (1 - BRIGHT_SMOOTH) * bright_d_raw + BRIGHT_SMOOTH * bright_d_prev
        bright_w = (1 - BRIGHT_SMOOTH) * bright_w_raw + BRIGHT_SMOOTH * bright_w_prev
    bright_d_prev = bright_d
    bright_w_prev = bright_w

    # WD TEMPERATURE 
    if T_w_raw < MIN_WD_TEMP or bright_w < 0.05:
        T_w = max(MIN_WD_TEMP, T_d * 0.9)  # Use donor temp as reference
    else:
        T_w = T_w_raw

    # ORBITAL PHASE EVOLUTION
    P_days = float(row["P_days"])
    P_seconds = P_days * 86400
    phase = (2 * math.pi * i / len(rows)) % (2 * math.pi)

    # COMPUTE BARYCENTRIC DISTANCES 
    M_d = float(row["M_d_Msun"])
    M_wd = float(row["M_wd_Msun"])
    M_total = M_d + M_wd

    r_wd = a * (M_d / M_total)
    r_d  = a * (M_wd / M_total)

    # CONVERT RADII TO SAME UNITS AS a
    R_solar_in_AU = 0.00465  # 1 R_solar = 0.00465 AU
    R_d_scaled = R_d * R_solar_in_AU * AU_SCALE
    R_w_scaled = R_w * R_solar_in_AU * AU_SCALE

    # Optional visual exaggeration of WD orbit
    WD_ORBIT_EXAGGERATION = 1.5
    r_wd *= WD_ORBIT_EXAGGERATION
    r_d  /= WD_ORBIT_EXAGGERATION

    # ORBITAL MOTION AROUND BARYCENTER
    VISUAL_SCALE = 1000
    wd.location = ( r_wd * VISUAL_SCALE * math.cos(phase),
                    r_wd * VISUAL_SCALE * math.sin(phase), 0)
    star.location = (-r_d * VISUAL_SCALE * math.cos(phase),
                     -r_d * VISUAL_SCALE * math.sin(phase), 0)

    wd.keyframe_insert(data_path="location", frame=frame)
    star.keyframe_insert(data_path="location", frame=frame)

    # VISUAL SCALING FOR RADII
    WD_VISUAL_SIZE = 20  # Exaggerate WD size for visibility
    star.scale = (R_d_scaled * VISUAL_SCALE, 
                  R_d_scaled * VISUAL_SCALE, 
                  R_d_scaled * VISUAL_SCALE)
    wd.scale   = (R_w_scaled * VISUAL_SCALE * WD_VISUAL_SIZE,
                  R_w_scaled * VISUAL_SCALE * WD_VISUAL_SIZE,
                  R_w_scaled * VISUAL_SCALE * WD_VISUAL_SIZE)

    star.keyframe_insert(data_path="scale", frame=frame)
    wd.keyframe_insert(data_path="scale", frame=frame)

    # COLOR + BRIGHTNESS (EMISSION)
    node_star.inputs["Color"].default_value = kelvin_to_rgb(T_d)
    node_star.inputs["Strength"].default_value = bright_d * 10
    node_star.inputs["Color"].keyframe_insert("default_value", frame=frame)
    node_star.inputs["Strength"].keyframe_insert("default_value", frame=frame)

    node_wd.inputs["Color"].default_value = kelvin_to_rgb(T_w)
    node_wd.inputs["Strength"].default_value = max(bright_w * 10, 0.5)  # Minimum brightness
    node_wd.inputs["Color"].keyframe_insert("default_value", frame=frame)
    node_wd.inputs["Strength"].keyframe_insert("default_value", frame=frame)


# In[ ]:




