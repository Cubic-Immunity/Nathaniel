# Binary Star Evolution to Type Ia Supernova

A numerical simulation of mass transfer in a binary star system leading to a Type Ia supernova explosion when the white dwarf reaches the Chandrasekhar limit.

# Project Overview

This project simulates the evolution of a close binary system consisting of a main-sequence donor star and a white dwarf. As the donor star fills its Roche lobe, mass transfers onto the white dwarf, causing it to grow until it reaches the Chandrasekhar limit (~1.44 M_solar) and explodes as a Type Ia supernova.

# Key Animations

# Primary Visualization
**3D Orbital Animation** - Blender rendering showing the binary system orbiting around their common barycenter, with sizes, colors (temperature-based), and emission brightness.

# Supporting Visualizations
1. **Mass Evolution** - Animated plot showing white dwarf mass increasing and donor star mass decreasing over time
2. **Comprehensive Multi-panel Analysis** - Plots showing:
   - Mass evolution (linear and log scales)
   - Orbital separation decay
   - Stellar radii evolution

# Physics & Equations

# Stellar Structure Relations

**1. Donor Star Radius** (Main sequence)

R_donor = R_solar × (M_donor / M_solar)^0.8

**2. Donor Star Luminosity** (Main sequence)

L_donor = L_solar × (M_donor / M_solar)^3.5

**3. Donor Temperature** (Stefan-Boltzmann)

T_donor = [L_donor / (4π R_donor^2 σ)]^0.25

**4. White Dwarf Mass-Radius Relation**

R_wd = 0.01 R☉ × [(M_Ch/M_wd)^(2/3) - (M_wd/M_Ch)^(2/3)]^0.5

Returns 10^6 m if term ≤ 0 (near Chandrasekhar limit)

**5. Accretion Luminosity**

L_acc = G × M_wd × |dM/dt| / R_wd

**6. White Dwarf Temperature** (Accretion heating)

T_wd = 0.5 × [L_acc / (4π R_wd² σ)]^0.25

# Binary Dynamics

**7. Roche Lobe Radius** (Eggleton 1983)

q = M_donor / M_wd
R_L = a × (0.49 q^(2/3)) / (0.6 q^(2/3) + ln(1 + q^(1/3)))

**8. Mass Transfer Rate** (Thermal timescale)

overflow = max(0, (R_donor - R_L) / R_L)
dM/dt = -(M_donor / τ_thermal) × overflow

**9. Angular Momentum Conservation** (Conservative mass transfer)

J = M_donor × M_wd × √(G a / (M_donor + M_wd))
a_new = J^2 × (M_donor + M_wd) / (G × M_donor^2 × M_wd^2)

**10. Gravitational Wave Radiation** (Peters 1964)

da/dt = -(64/5) × (G^3 M_donor M_wd (M_donor + M_wd)) / (c^5 a^3)

**11. Orbital Period** (Kepler's Third Law)

P = 2π √(a^3 / (G(M_wd + M_donor)))

**12. Initial Separation** (From filling factor)

q = M_donor / M_wd
f = (0.49 q^(2/3)) / (0.6 q^(2/3) + ln(1 + q^(1/3)))
a_initial = (R_donor / f) × filling_factor

**13. Supernova Trigger Condition**

M_wd ≥ M_Ch = 1.44 M☉

# Tools & Libraries

# Python Packages
- **NumPy** - Numerical computations and array operations
- **Pandas** - Data storage and CSV export
- **Matplotlib** - 2D plotting and animation generation
- **SciPy** - Data smoothing (rolling averages)

# 3D Visualization
- **Blender** - 3D rendering and animation
  - Python API (bpy) for automated keyframe generation
  - Emission shaders for temperature-based coloring
  - Eevee render engine with bloom effects

# Usage

# 1. Run the Physics Simulation

python simulation.py

This generates `binary_evolution_blender.csv` with all physical parameters at each timestep.

# 2. Create 2D Animations

python visualization.py

Generates GIF animations of mass evolution, orbital separation, and radii.

# 3. Import to Blender

# In Blender's scripting tab:
# Load blender_animation.py and run
# Make sure "Star" and "White Dwarf" objects exist in scene

# 4. Render the Animation
Set up camera, adjust frame range, specify output in scene menu, and render as video.

# Results

# Initial Conditions
- Donor star mass: 1.0 M☉
- White dwarf mass: 0.8 M☉
- Initial separation: 0.0116 AU
- Filling factor: 0.99 (donor slightly underfills Roche lobe)

# Final State (at Supernova)
- White dwarf mass: 1.443 M☉ (exceeded Chandrasekhar limit)
- Donor star mass: 0.196 M☉
- Final separation: 0.0059 AU
- Frames simulated: 1000

# Key Findings
- Mass transfer rate increases as donor fills Roche lobe
- Orbital separation decreases due to gravitational wave emission
- White dwarf shrinks as it gains mass (counterintuitive!)
- System reaches supernova condition after ~1000 timesteps
- Orbital period decreases from hours to minutes

# Future Enhancements

Due to time constraints, the following were not implemented:
- **Accretion disk visualization** - Particle stream showing mass transfer
- **Supernova explosion effect** - Bright flash and expanding ejecta
- **More refined initial conditions** - Exploring parameter space
- **Bug Fixes** - Some parameters are not quite what I was expecting 

# References

1. Eggleton, P. P. (1983). "Aproximations to the radii of Roche lobes."
2. Peters, P. C. (1964). "Gravitational Radiation and the Motion of Two Point Masses."
3. Chandrasekhar, S. (1931). "The Maximum Mass of Ideal White Dwarfs."
4. Hillebrandt, W., & Niemeyer, J. C. (2000)
5. Blender Foundation. (2025) "Blender Python API Documentation"