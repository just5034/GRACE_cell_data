import json as _json_orig
class _NumpySafeEncoder(_json_orig.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'tolist') and hasattr(obj, 'shape'):
            if getattr(obj, 'ndim', 0) > 0:
                return obj.tolist()
            return obj.item()
        if hasattr(obj, 'item'):
            return obj.item()
        return super().default(obj)
_orig_dumps = _json_orig.dumps
def _safe_dumps(*args, **kwargs):
    kwargs.setdefault('cls', _NumpySafeEncoder)
    return _orig_dumps(*args, **kwargs)
_json_orig.dumps = _safe_dumps
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import json

# Data from analyze_containment_performance step outputs
depths_cm = [14.2, 22.3]
depths_x0 = [16, 25]
energies_gev = [1, 5, 20]

# Containment fractions
containment_data = {
    14.2: {1: 0.969556, 5: 0.949706, 20: 0.919867},
    22.3: {1: 0.991632, 5: 0.99171, 20: 0.99022}
}

# Energy resolutions
resolution_data = {
    14.2: {1: 0.026168, 5: 0.031937, 20: 0.043364},
    22.3: {1: 0.011732, 5: 0.011105, 20: 0.010262}
}

# Shower maximum positions (mm)
shower_max_data = {
    14.2: {1: -21.04, 5: -6.92, 20: 2.16},
    22.3: {1: -58.58, 5: -45.66, 20: -32.41}
}

# Target leakage threshold
target_leakage = 0.01
minimum_depth_cm = 22.3

# Create figure with subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Containment fraction vs depth
colors = ['blue', 'green', 'red']
for i, energy in enumerate(energies_gev):
    containment_values = [containment_data[depth][energy] for depth in depths_cm]
    ax1.plot(depths_cm, containment_values, 'o-', color=colors[i], 
             label=f'{energy} GeV', linewidth=2, markersize=8)

# Add target line
ax1.axhline(y=1-target_leakage, color='black', linestyle='--', 
            label=f'Target (99% containment)', linewidth=2)
ax1.axvline(x=minimum_depth_cm, color='gray', linestyle=':', 
            label=f'Min depth ({minimum_depth_cm} cm)', alpha=0.7)

ax1.set_xlabel('Calorimeter Depth (cm)', fontsize=12)
ax1.set_ylabel('Containment Fraction', fontsize=12)
ax1.set_title('Electromagnetic Shower Containment vs Depth', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0.9, 1.0)

# Plot 2: Energy resolution vs depth
for i, energy in enumerate(energies_gev):
    resolution_values = [resolution_data[depth][energy] for depth in depths_cm]
    ax2.plot(depths_cm, resolution_values, 's-', color=colors[i], 
             label=f'{energy} GeV', linewidth=2, markersize=8)

ax2.axvline(x=minimum_depth_cm, color='gray', linestyle=':', 
            label=f'Min depth ({minimum_depth_cm} cm)', alpha=0.7)
ax2.set_xlabel('Calorimeter Depth (cm)', fontsize=12)
ax2.set_ylabel('Energy Resolution (σ/μ)', fontsize=12)
ax2.set_title('Energy Resolution vs Depth', fontsize=14, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

# Plot 3: Shower maximum vs energy
for i, depth in enumerate(depths_cm):
    shower_max_values = [shower_max_data[depth][energy] for energy in energies_gev]
    ax3.plot(energies_gev, shower_max_values, '^-', 
             label=f'{depth} cm ({depths_x0[i]} X₀)', linewidth=2, markersize=8)

ax3.set_xlabel('Beam Energy (GeV)', fontsize=12)
ax3.set_ylabel('Shower Maximum Position (mm)', fontsize=12)
ax3.set_title('Shower Maximum vs Energy', fontsize=14, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_xscale('log')

# Plot 4: Leakage fraction vs depth
for i, energy in enumerate(energies_gev):
    leakage_values = [1 - containment_data[depth][energy] for depth in depths_cm]
    ax4.semilogy(depths_cm, leakage_values, 'o-', color=colors[i], 
                 label=f'{energy} GeV', linewidth=2, markersize=8)

ax4.axhline(y=target_leakage, color='black', linestyle='--', 
            label=f'Target ({target_leakage*100}% leakage)', linewidth=2)
ax4.axvline(x=minimum_depth_cm, color='gray', linestyle=':', 
            label=f'Min depth ({minimum_depth_cm} cm)', alpha=0.7)

ax4.set_xlabel('Calorimeter Depth (cm)', fontsize=12)
ax4.set_ylabel('Leakage Fraction (log scale)', fontsize=12)
ax4.set_title('Energy Leakage vs Depth', fontsize=14, fontweight='bold')
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('containment_analysis_plots.png', dpi=300, bbox_inches='tight')
plt.savefig('containment_analysis_plots.pdf', bbox_inches='tight')
print('Saved containment analysis plots to containment_analysis_plots.png and .pdf')

# Save summary data
summary_data = {
    'minimum_depth_requirement': {
        'depth_cm': minimum_depth_cm,
        'depth_x0': 25,
        'target_leakage_fraction': target_leakage,
        'meets_requirement': True
    },
    'containment_performance': containment_data,
    'energy_resolution': resolution_data,
    'shower_maximum_mm': shower_max_data
}

with open('containment_summary.json', 'w') as f:
    json.dump(summary_data, f, indent=2)

print('RESULT:plots_generated=True')
print('RESULT:minimum_depth_cm=22.3')
print('RESULT:minimum_depth_x0=25')
print('RESULT:target_containment_achieved=True')
print('Generated publication-quality plots showing containment and resolution vs depth')
print(f'Minimum depth requirement: {minimum_depth_cm} cm (25 X₀) for <1% leakage')