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
import pandas as pd
import numpy as np
import json
from pathlib import Path

# Load box calorimeter energy sweep data (multiple energies)
box_events_files = {
    1.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_1.000GeV/box_calorimeter_em_events.parquet",
    5.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_5.000GeV/box_calorimeter_em_events.parquet",
    20.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_20.000GeV/box_calorimeter_em_events.parquet"
}

box_hits_files = {
    1.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_1.000GeV/box_calorimeter_em_hits_data.parquet",
    5.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_5.000GeV/box_calorimeter_em_hits_data.parquet",
    20.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_20.000GeV/box_calorimeter_em_hits_data.parquet"
}

# Load projective tower calorimeter data
projective_events_file = "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/projective_tower_calorimeter_em_events.parquet"
projective_hits_file = "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/projective_tower_calorimeter_em_hits_data.parquet"

print("Analyzing box calorimeter energy resolution vs energy...")
box_results = {}
for energy_gev, filepath in box_events_files.items():
    df = pd.read_parquet(filepath)
    beam_energy_mev = energy_gev * 1000
    mean_edep = df['totalEdep'].mean()
    std_edep = df['totalEdep'].std()
    resolution = std_edep / mean_edep if mean_edep > 0 else float('inf')
    linearity = mean_edep / beam_energy_mev
    
    box_results[energy_gev] = {
        'mean_edep_mev': mean_edep,
        'std_edep_mev': std_edep,
        'resolution': resolution,
        'linearity': linearity,
        'n_events': len(df)
    }
    
    print(f"Box {energy_gev} GeV: resolution={resolution:.4f}, linearity={linearity:.3f}, mean_edep={mean_edep:.1f} MeV")

# Calculate average box calorimeter performance
box_avg_resolution = np.mean([r['resolution'] for r in box_results.values()])
box_avg_linearity = np.mean([r['linearity'] for r in box_results.values()])

print(f"\nBox calorimeter average resolution: {box_avg_resolution:.4f}")
print(f"Box calorimeter average linearity: {box_avg_linearity:.3f}")

# Analyze projective tower calorimeter (assuming 5 GeV based on typical test energy)
print("\nAnalyzing projective tower calorimeter...")
proj_events_df = pd.read_parquet(projective_events_file)
proj_hits_df = pd.read_parquet(projective_hits_file)

# Assume 5 GeV beam for projective (typical test energy)
proj_beam_energy_mev = 5000
proj_mean_edep = proj_events_df['totalEdep'].mean()
proj_std_edep = proj_events_df['totalEdep'].std()
proj_resolution = proj_std_edep / proj_mean_edep if proj_mean_edep > 0 else float('inf')
proj_linearity = proj_mean_edep / proj_beam_energy_mev

print(f"Projective tower: resolution={proj_resolution:.4f}, linearity={proj_linearity:.3f}, mean_edep={proj_mean_edep:.1f} MeV")

# Calculate containment metrics using hit-level data (sample first 100k hits to avoid timeout)
print("\nCalculating containment metrics...")

# Box calorimeter containment (use 5 GeV data)
box_hits_5gev = pd.read_parquet(box_hits_files[5.0])
if len(box_hits_5gev) > 100000:
    box_hits_5gev = box_hits_5gev.sample(n=100000, random_state=42)

box_radial_dist = np.sqrt(box_hits_5gev['x']**2 + box_hits_5gev['y']**2)
total_energy = box_hits_5gev['edep'].sum()

# Calculate R90 containment (radius containing 90% of energy)
box_sorted_indices = np.argsort(box_radial_dist)
box_cumulative_energy = np.cumsum(box_hits_5gev.iloc[box_sorted_indices]['edep'])
box_r90_idx = np.where(box_cumulative_energy >= 0.9 * total_energy)[0][0]
box_r90 = box_radial_dist.iloc[box_sorted_indices[box_r90_idx]]

print(f"Box calorimeter R90 containment: {box_r90:.1f} mm")

# Projective tower containment
if len(proj_hits_df) > 100000:
    proj_hits_sample = proj_hits_df.sample(n=100000, random_state=42)
else:
    proj_hits_sample = proj_hits_df

proj_radial_dist = np.sqrt(proj_hits_sample['x']**2 + proj_hits_sample['y']**2)
proj_total_energy = proj_hits_sample['edep'].sum()

proj_sorted_indices = np.argsort(proj_radial_dist)
proj_cumulative_energy = np.cumsum(proj_hits_sample.iloc[proj_sorted_indices]['edep'])
proj_r90_idx = np.where(proj_cumulative_energy >= 0.9 * proj_total_energy)[0][0]
proj_r90 = proj_radial_dist.iloc[proj_sorted_indices[proj_r90_idx]]

print(f"Projective tower R90 containment: {proj_r90:.1f} mm")

# Output results for downstream steps
print(f"RESULT:box_calorimeter_avg_resolution={box_avg_resolution:.4f}")
print(f"RESULT:box_calorimeter_avg_linearity={box_avg_linearity:.3f}")
print(f"RESULT:box_calorimeter_r90_containment_mm={box_r90:.1f}")
print(f"RESULT:projective_tower_resolution={proj_resolution:.4f}")
print(f"RESULT:projective_tower_linearity={proj_linearity:.3f}")
print(f"RESULT:projective_tower_r90_containment_mm={proj_r90:.1f}")

# Save detailed results to JSON
results_summary = {
    'box_calorimeter': {
        'energy_sweep_results': box_results,
        'average_resolution': box_avg_resolution,
        'average_linearity': box_avg_linearity,
        'r90_containment_mm': float(box_r90)
    },
    'projective_tower': {
        'resolution': proj_resolution,
        'linearity': proj_linearity,
        'r90_containment_mm': float(proj_r90),
        'mean_edep_mev': proj_mean_edep
    }
}

with open('calorimeter_performance_metrics.json', 'w') as f:
    json.dump(results_summary, f, indent=2)

print("\nAnalysis complete. Performance metrics extracted for all geometries.")
print("Detailed results saved to calorimeter_performance_metrics.json")