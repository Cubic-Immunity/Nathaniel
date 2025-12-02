#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation, PillowWriter


# In[2]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation, PillowWriter


# In[3]:


# Constants 
G       = 6.6743e-11           # Gravitational constant (m^3 kg^-1 s^-2)
M_sun   = 1.989e30             # Solar mass (kg)
R_sun   = 6.957e8              # Solar radius (m)
L_sun   = 3.828e26             # Solar luminosity (W)
sigma   = 5.670374419e-8       # Stefan-Boltzmann constant
M_ch    = 1.44 * M_sun         # Chandrasekhar limit (kg)
AU      = 1.496e11             # Astronomical unit (m)
c       = 3e8                  # Speed of light (m/s)

# Simulation parameters
FILLING_FACTOR = 0.99          # underfill roche-lobe by 1%
M_d_init = 1.0 * M_sun
M_wd_init = 0.8 * M_sun
tau_th = 1e14                  # Thermal timescale (s)
dt = 4.71e14                   # Time step (s)                 (tuned)
n_steps = 1000                 #                                (tuned)
eta_acc = 0.8                  # Accretion efficiency

# Stellar relations
def R_donor(M_d): 
    return R_sun * (M_d / M_sun)**0.8

def L_donor(M_d): 
    return L_sun * (M_d / M_sun)**3.5

def T_donor(M_d): 
    return (L_donor(M_d) / (4 * np.pi * R_donor(M_d)**2 * sigma))**0.25

def R_wd(M_wd):
    term = (M_ch / M_wd)**(2/3) - (M_wd / M_ch)**(2/3)
    return 1e6 if term <= 0 else 0.01 * R_sun * np.sqrt(term)

def L_accretion(M_wd, R_wd, dM_dt): 
    R_wd_safe = max(R_wd, 1e5)  # Prevent division by tiny radius
    L_acc = G * M_wd * abs(dM_dt) / R_wd_safe
    max_luminosity = 1000 * L_sun  # Cap at 1000 L_sun
    return min(L_acc, max_luminosity)

def T_wd(M_wd, R_wd, dM_dt):
    T_base = 5000 + (M_wd / M_sun - 0.6) * 8000  # 5000-15000 K range
    dM_dt_Msun_per_year = abs(dM_dt) / M_sun * 3.15e7
    if dM_dt_Msun_per_year > 1e-12:
        boost_factor = np.log10(dM_dt_Msun_per_year) + 9  # Maps 1e-9 → 0, 1e-7 → 2
        boost_factor = np.clip(boost_factor, 0, 10)  # 0 to 10x boost
        T_accretion_boost = T_base * boost_factor
    else:
        T_accretion_boost = 0

    T_final = T_base + T_accretion_boost
    T_final = np.clip(T_final, 5000, 150000)
    return T_final

# Binary dynamicss
def roche_lobe_radius(a, M_d, M_wd):
    q = M_d / M_wd
    return a * (0.49*q**(2/3)) / (0.6*q**(2/3) + np.log(1 + q**(1/3)))

def mass_transfer_rate(M_d, R_d, R_L, tau_th):
    overflow = max(0, (R_d - R_L) / R_L)
    return -(M_d / tau_th) * overflow

def update_separation(a, M_d, M_wd, dM_d):
    """Conservative mass-transfer induced change in separation."""
    M_d_new = M_d + dM_d
    M_w_new = M_wd - dM_d
    J = M_d * M_wd * np.sqrt(G * a / (M_d + M_wd))
    M_total_new = M_d_new + M_w_new
    return J**2 * M_total_new / (G * M_d_new**2 * M_w_new**2)

# Gravitational wave decay 
def gravitational_wave_da_dt(a, M_d, M_wd):
    """da/dt due to gravitational-wave radiation (Peters 1964)."""
    return -(64/5) * (G**3 * M_d * M_wd * (M_d + M_wd)) / (c**5 * a**3)

def update_with_gravitational_waves(a, M_d, M_wd, dt):
    """Update orbital separation due to gravitational wave emission."""
    da_dt = gravitational_wave_da_dt(a, M_d, M_wd)
    return a + da_dt * dt

def orbital_period(a, M_wd, M_d):
    return 2 * np.pi * np.sqrt(a**3 / (G * (M_wd + M_d)))

def check_chandrasekhar(M_wd):
    return M_wd >= M_ch

# Initial conditions 
def initial_separation_from_Rd(R_d, M_d, M_wd, filling_factor=FILLING_FACTOR):
    q = M_d / M_wd
    f = (0.49*q**(2/3)) / (0.6*q**(2/3) + np.log(1 + q**(1/3)))
    a_rl = R_d / f
    return filling_factor * a_rl

# Main simulation 
def run_simulation_blender(
    M_d_init=M_d_init, M_wd_init=M_wd_init,
    tau_th=tau_th, dt=dt, n_steps=n_steps,
    eta_acc=eta_acc, filling_factor=FILLING_FACTOR):

    # Initialize parameters
    R_d_init = R_donor(M_d_init)
    a_init = initial_separation_from_Rd(R_d_init, M_d_init, M_wd_init, filling_factor)
    a = a_init
    M_d, M_wd = M_d_init, M_wd_init

    blender_data = []

    print("--- Binary Simulation Start ---")
    print(f"Initial separation: {a/AU:.4f} AU | Filling factor = {filling_factor}")
    print(f"Initial donor mass = {M_d/M_sun:.2f} M☉ | WD mass = {M_wd/M_sun:.2f} M☉\n")

    for frame in range(n_steps):
        R_d = R_donor(M_d)
        R_w = R_wd(M_wd)
        R_L = roche_lobe_radius(a, M_d, M_wd)
        dM_dt = mass_transfer_rate(M_d, R_d, R_L, tau_th)
        dM = dM_dt * dt

        # Mass updates
        M_d_new = M_d + dM
        M_wd_new = M_wd - eta_acc * dM

        # Update separation
        a = update_separation(a, M_d, M_wd, dM)
        a = update_with_gravitational_waves(a, M_d, M_wd, dt)

        # Commit updated masses
        M_d, M_wd = M_d_new, M_wd_new

        # Derived quantities
        L_d = L_donor(M_d)
        L_acc = L_accretion(M_wd, R_w, dM_dt)
        T_d = T_donor(M_d)
        T_w = T_wd(M_wd, R_w, dM_dt)
        P = orbital_period(a, M_wd, M_d)

        brightness_d = L_d / L_sun
        brightness_w = L_acc / L_sun

        blender_data.append({
            "frame": frame,
            "a_AU": a / AU,
            "R_d_Rsun": R_d / R_sun,
            "R_wd_Rsun": R_w / R_sun,
            "brightness_d": brightness_d,
            "brightness_w": brightness_w,
            "color_d_K": T_d,
            "color_wd_K": T_w,
            "M_d_Msun": M_d / M_sun,
            "M_wd_Msun": M_wd / M_sun,
            "P_days": P / 86400,
            "is_SN": int(check_chandrasekhar(M_wd))
        })

        if check_chandrasekhar(M_wd):
            print(f"Supernova at frame {frame}")
            break

    # Save results
    df = pd.DataFrame(blender_data)

    # Smooth orbital separation (reduce jitter)
    df["a_AU"] = df["a_AU"].rolling(window=30, min_periods=1, center=True).mean()

    df.to_csv("binary_evolution_blender.csv", index=False)

    # Check end results
    print("Blender data exported --> binary_evolution_blender.csv")
    print(f"Final separation: {a/AU:.4f} AU")
    print(f"Final donor mass: {M_d/M_sun:.3f} M☉, WD mass: {M_wd/M_sun:.3f} M☉")
    return df

# Run simulation
df = run_simulation_blender()

# Better visualization with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Mass evolution (linear time)
axes[0, 0].plot(df["frame"], df["M_wd_Msun"], label="White Dwarf", lw=2)
axes[0, 0].plot(df["frame"], df["M_d_Msun"], label="Donor Star", lw=2)
axes[0, 0].axhline(1.44, color="r", ls="--", label="Chandrasekhar Limit", alpha=0.7)
axes[0, 0].set_xlabel("Frame", fontsize=16)
axes[0, 0].set_ylabel("Mass (M☉)", fontsize=16)
axes[0, 0].set_title("Mass Evolution (Linear Scale)", fontsize=20)
axes[0, 0].tick_params(labelsize=14)
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# Mass evolution (log time) - for better view of early evolution
axes[0, 1].plot(np.log10(df["frame"] + 1), df["M_wd_Msun"], label="White Dwarf", lw=2)
axes[0, 1].plot(np.log10(df["frame"] + 1), df["M_d_Msun"], label="Donor Star", lw=2)
axes[0, 1].axhline(1.44, color="r", ls="--", label="Chandrasekhar Limit", alpha=0.7)
axes[0, 1].set_xlabel("log10(Frame + 1)", fontsize=16)
axes[0, 1].set_ylabel("Mass (M☉)", fontsize=16)
axes[0, 1].set_title("Mass Evolution (Log Scale)", fontsize=20)
axes[0, 1].tick_params(labelsize=14)
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

# Orbital separation
axes[1, 0].plot(df["frame"], df["a_AU"], color='purple', lw=2, label="Orbital Seperation")
axes[1, 0].set_xlabel("Frame", fontsize=16)
axes[1, 0].set_ylabel("Separation (AU)", fontsize=16)
axes[1, 0].set_title("Orbital Separation", fontsize=20)
axes[1, 0].tick_params(labelsize=14)
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)

# Radii evolution
axes[1, 1].plot(df["frame"], df["R_d_Rsun"], label="Donor Radius", lw=2)
axes[1, 1].plot(df["frame"], df["R_wd_Rsun"], label="WD Radius", lw=2)
axes[1, 1].set_xlabel("Frame", fontsize=16)
axes[1, 1].set_ylabel("Radius (R☉)", fontsize=16)
axes[1, 1].set_title("Stellar Radii", fontsize=20)
axes[1, 1].set_yscale('log')
axes[1, 1].tick_params(labelsize=14)
axes[1, 1].legend()
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
# plt.savefig("binary_evolution_complete.png", dpi=150)
plt.show()

# Print verification
print("\n=== Verification ===")
print(f"Initial WD mass: {df['M_wd_Msun'].iloc[0]:.3f} M☉")
print(f"Initial Donor mass: {df['M_d_Msun'].iloc[0]:.3f} M☉")
print(f"Final WD mass: {df['M_wd_Msun'].iloc[-1]:.3f} M☉")
print(f"Final Donor mass: {df['M_d_Msun'].iloc[-1]:.3f} M☉")


# In[3]:


# Mass evolution (log time)
log_frames = np.log10(df["frame"] + 1)
real_frames = np.arange(len(df))

# Scale the animation playback more evenly in log space
frame_indices = np.unique(
    np.geomspace(1, len(df), num=len(df)).astype(int) - 1
)

fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.set_xlim(log_frames.min(), log_frames.max())
ymin = min(df["M_d_Msun"].min(), df["M_wd_Msun"].min()) * 0.98
ymax = max(df["M_d_Msun"].max(), df["M_wd_Msun"].max()) * 1.02
ax1.set_ylim(ymin, ymax)
ax1.set_xlabel("log₁₀(Frame + 1)")
ax1.set_ylabel("Mass (M☉)")
ax1.set_title("Mass Evolution (Log Scale)")
ax1.grid(alpha=0.3)

line_d, = ax1.plot([], [], color='orange', lw=2, label="Donor Star")
line_wd, = ax1.plot([], [], color='blue', lw=2, label="White Dwarf")
ax1.axhline(1.44, color="r", ls="--", alpha=0.7, label="Chandrasekhar Limit")
time_text = ax1.text(0.02, 0.92, "", transform=ax1.transAxes, fontsize=10)
ax1.legend()

def init_mass():
    line_d.set_data([], [])
    line_wd.set_data([], [])
    time_text.set_text("")
    return line_d, line_wd, time_text

def update_mass(i):
    idx = frame_indices[i]
    x = log_frames[:idx]
    y_d = df["M_d_Msun"][:idx]
    y_wd = df["M_wd_Msun"][:idx]
    line_d.set_data(x, y_d)
    line_wd.set_data(x, y_wd)
    time_text.set_text(f"Frame: {idx}")
    return line_d, line_wd, time_text

anim_mass = FuncAnimation(
    fig1, update_mass, frames=len(frame_indices),
    init_func=init_mass, blit=True, interval=15, repeat=False
)

gif_writer = PillowWriter(fps=30)
anim_mass.save("mass_evolution_log.gif", writer=gif_writer)
plt.close(fig1)
print("Saved: mass_evolution_log.gif")

# Orbital seperation
fig2, ax2 = plt.subplots(figsize=(8, 6))
x = df["frame"]
y = df["a_AU"]

x_buffer = 0.05 * (x.max() - x.min())
y_buffer = 0.05 * (y.max() - y.min())

ax2.set_xlim(x.min() - x_buffer, x.max() + x_buffer)
ax2.set_ylim(y.min() - y_buffer, y.max() + y_buffer)
ax2.set_xlabel("Frame")
ax2.set_ylabel("Separation (AU)")
ax2.set_title("Orbital Separation Evolution")
ax2.grid(alpha=0.3)

line_sep, = ax2.plot([], [], color='purple', lw=2, label="Orbital Separation")
time_text2 = ax2.text(0.02, 0.92, "", transform=ax2.transAxes, fontsize=10)
ax2.legend()

def init_sep():
    line_sep.set_data([], [])
    time_text2.set_text("")
    return line_sep, time_text2

def update_sep(i):
    x_ = x[:i]
    y_ = y[:i]
    line_sep.set_data(x_, y_)
    time_text2.set_text(f"Frame: {i}")
    return line_sep, time_text2

anim_sep = FuncAnimation(
    fig2, update_sep, frames=len(df),
    init_func=init_sep, blit=True, interval=15, repeat=False
)

anim_sep.save("orbital_separation.gif", writer=gif_writer)
plt.close(fig2)
print("Saved: orbital_separation.gif")

# Stellar radii
fig3, ax3 = plt.subplots(figsize=(8, 6))
x = df["frame"]
y_d = df["R_d_Rsun"]
y_wd = df["R_wd_Rsun"]

x_buffer = 0.05 * (x.max() - x.min())
ymin_r = min(y_d.min(), y_wd.min()) * 0.8
ymax_r = max(y_d.max(), y_wd.max()) * 1.2

ax3.set_xlim(x.min() - x_buffer, x.max() + x_buffer)
ax3.set_ylim(ymin_r, ymax_r)
ax3.set_xlabel("Frame")
ax3.set_ylabel("Radius (R☉)")
ax3.set_yscale('log')
ax3.set_title("Stellar Radii Evolution")
ax3.grid(alpha=0.3, which='both')

line_rd, = ax3.plot([], [], color='orange', lw=2, label="Donor Radius")
line_rwd, = ax3.plot([], [], color='blue', lw=2, label="WD Radius")
time_text3 = ax3.text(0.02, 0.92, "", transform=ax3.transAxes, fontsize=10)
ax3.legend()

def init_radii():
    line_rd.set_data([], [])
    line_rwd.set_data([], [])
    time_text3.set_text("")
    return line_rd, line_rwd, time_text3

def update_radii(i):
    x_ = x[:i]
    line_rd.set_data(x_, y_d[:i])
    line_rwd.set_data(x_, y_wd[:i])
    time_text3.set_text(f"Frame: {i}")
    return line_rd, line_rwd, time_text3

anim_radii = FuncAnimation(
    fig3, update_radii, frames=len(df),
    init_func=init_radii, blit=True, interval=15, repeat=False
)

anim_radii.save("stellar_radii.gif", writer=gif_writer)
plt.close(fig3)
print("Saved: stellar_radii.gif")


# In[ ]:




