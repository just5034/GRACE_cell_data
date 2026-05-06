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
import pandas as pd
import json
from pathlib import Path

# Get resolution fit parameters from previous step
stochastic_term = 0.0235
noise_term = -0.0137
constant_term = 0.004

# Get sampling metrics from previous step
sampling_fraction = 0.9828
shower_containment_r90_mm = 32.61
detector_mass_kg = 76.84

# Load energy sweep data for resolution vs energy plot
events_files = {
    1.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_1.000GeV/thin_absorber_calorimeter_em_events.parquet",
    5.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_5.000GeV/thin_absorber_calorimeter_em_events.parquet",
    20.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_20.000GeV/thin_absorber_calorimeter_em_events.parquet"
}

# Analyze each energy point
energy_points = []
resolution_points = []
linearity_points = []

for energy_gev, filepath in events_files.items():
    df = pd.read_parquet(filepath)
    mean_edep_mev = df['totalEdep'].mean()
    std_edep_mev = df['totalEdep'].std()
    resolution = std_edep_mev / mean_edep_mev if mean_edep_mev > 0 else 0
    
    # Energy linearity (response vs beam energy)
    beam_energy_mev = energy_gev * 1000
    linearity = mean_edep_mev / beam_energy_mev
    
    energy_points.append(energy_gev)
    resolution_points.append(resolution)
    linearity_points.append(linearity)
    
    print(f"Energy {energy_gev} GeV: Resolution = {resolution:.4f}, Linearity = {linearity:.4f}")

# Create publication-quality plots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Calorimeter Performance Analysis', fontsize=16, fontweight='bold')

# Plot 1: Energy Resolution vs Energy
ax1.scatter(energy_points, resolution_points, color='red', s=60, alpha=0.8, label='Data')

# Plot resolution fit curve
energy_fit = np.logspace(np.log10(0.5), np.log10(25), 100)
resolution_fit = np.sqrt((stochastic_term/np.sqrt(energy_fit))**2 + (noise_term/energy_fit)**2 + constant_term**2)
ax1.plot(energy_fit, resolution_fit, 'b-', linewidth=2, label=f'Fit: {stochastic_term:.3f}/√E ⊕ {noise_term:.3f}/E ⊕ {constant_term:.3f}')

ax1.set_xlabel('Beam Energy (GeV)', fontsize=12)
ax1.set_ylabel('Energy Resolution (σ/E)', fontsize=12)
ax1.set_title('Energy Resolution vs Energy', fontsize=14, fontweight='bold')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)

# Plot 2: Energy Linearity
ax2.scatter(energy_points, linearity_points, color='blue', s=60, alpha=0.8)
ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Perfect Linearity')
ax2.set_xlabel('Beam Energy (GeV)', fontsize=12)
ax2.set_ylabel('Response/Beam Energy', fontsize=12)
ax2.set_title('Energy Linearity', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)

# Plot 3: Sampling Performance Metrics
metrics = ['Sampling\nFraction', 'R90 Containment\n(mm)', 'Detector Mass\n(kg)']
values = [sampling_fraction, shower_containment_r90_mm, detector_mass_kg]
colors = ['green', 'orange', 'purple']

bars = ax3.bar(metrics, values, color=colors, alpha=0.7, edgecolor='black')
ax3.set_ylabel('Value', fontsize=12)
ax3.set_title('Sampling Performance Metrics', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, value in zip(bars, values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
             f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

# Plot 4: Resolution Components
components = ['Stochastic\nTerm', 'Noise\nTerm', 'Constant\nTerm']
comp_values = [abs(stochastic_term), abs(noise_term), abs(constant_term)]
comp_colors = ['red', 'blue', 'green']

bars4 = ax4.bar(components, comp_values, color=comp_colors, alpha=0.7, edgecolor='black')
ax4.set_ylabel('Term Value', fontsize=12)
ax4.set_title('Resolution Fit Components', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')

# Add value labels
for bar, value in zip(bars4, comp_values):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
             f'{value:.4f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('calorimeter_performance_plots.png', dpi=300, bbox_inches='tight')
plt.savefig('calorimeter_performance_plots.pdf', bbox_inches='tight')
print('Saved publication-quality plots: calorimeter_performance_plots.png and .pdf')

# Save summary data
summary_data = {
    'energy_resolution': {
        'stochastic_term': stochastic_term,
        'noise_term': noise_term,
        'constant_term': constant_term,
        'data_points': list(zip(energy_points, resolution_points))
    },
    'energy_linearity': {
        'data_points': list(zip(energy_points, linearity_points)),
        'mean_linearity': np.mean(linearity_points)
    },
    'sampling_performance': {
        'sampling_fraction': sampling_fraction,
        'r90_containment_mm': shower_containment_r90_mm,
        'detector_mass_kg': detector_mass_kg
    }
}

with open('performance_summary.json', 'w') as f:
    json.dump(summary_data, f, indent=2)

print('RESULT:plots_generated=True')
print(f'RESULT:mean_linearity={np.mean(linearity_points):.4f}')
print(f'RESULT:resolution_at_1gev={resolution_points[0]:.4f}')
print(f'RESULT:resolution_at_20gev={resolution_points[2]:.4f}')
print('Performance plots successfully generated with energy resolution, linearity, and sampling metrics')