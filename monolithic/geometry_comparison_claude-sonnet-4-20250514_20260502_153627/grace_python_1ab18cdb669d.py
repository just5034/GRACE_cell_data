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

# Load box calorimeter energy sweep data
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

# Analysis results storage
results = {}

# Analyze box calorimeter energy sweep
box_results = []
for energy_gev in sorted(box_events_files.keys()):
    try:
        # Load event data
        events_df = pd.read_parquet(box_events_files[energy_gev])
        
        # Energy resolution calculation
        mean_edep = events_df['totalEdep'].mean()  # MeV
        std_edep = events_df['totalEdep'].std()
        resolution = std_edep / mean_edep if mean_edep > 0 else float('inf')
        
        # Linearity calculation (beam energy in MeV)
        beam_energy_mev = energy_gev * 1000
        linearity = mean_edep / beam_energy_mev if beam_energy_mev > 0 else 0
        
        # Load hits data for containment analysis (sample first 100k hits if large)
        hits_df = pd.read_parquet(box_hits_files[energy_gev])
        if len(hits_df) > 100000:
            hits_df = hits_df.head(100000)
        
        # Lateral containment (R90 - radius containing 90% of energy)
        hits_df['r'] = np.sqrt(hits_df['x']**2 + hits_df['y']**2)
        total_energy = hits_df['edep'].sum()
        
        # Sort by radius and calculate cumulative energy
        hits_sorted = hits_df.sort_values('r')
        hits_sorted['cumulative_energy'] = hits_sorted['edep'].cumsum()
        hits_sorted['energy_fraction'] = hits_sorted['cumulative_energy'] / total_energy
        
        # Find R90 (radius containing 90% of energy)
        r90_idx = hits_sorted[hits_sorted['energy_fraction'] >= 0.9].index
        r90_mm = hits_sorted.loc[r90_idx[0], 'r'] if len(r90_idx) > 0 else 0
        
        # Uniformity (RMS of energy deposits)
        uniformity_rms = hits_df['edep'].std() / hits_df['edep'].mean() if hits_df['edep'].mean() > 0 else 0
        
        box_results.append({
            'energy_gev': energy_gev,
            'mean_edep_mev': mean_edep,
            'resolution': resolution,
            'linearity': linearity,
            'r90_containment_mm': r90_mm,
            'uniformity_rms': uniformity_rms,
            'n_events': len(events_df)
        })
        
        print(f"Box calorimeter {energy_gev} GeV: resolution={resolution:.4f}, linearity={linearity:.3f}, R90={r90_mm:.1f}mm")
        
    except Exception as e:
        print(f"Error processing box calorimeter {energy_gev} GeV: {e}")
        continue

results['box_calorimeter'] = box_results

# Analyze projective tower calorimeter (assuming 5 GeV beam from context)
try:
    # Load projective data
    proj_events_df = pd.read_parquet(projective_events_file)
    proj_hits_df = pd.read_parquet(projective_hits_file)
    
    # Sample hits if too large
    if len(proj_hits_df) > 100000:
        proj_hits_df = proj_hits_df.head(100000)
    
    # Energy resolution
    proj_mean_edep = proj_events_df['totalEdep'].mean()
    proj_std_edep = proj_events_df['totalEdep'].std()
    proj_resolution = proj_std_edep / proj_mean_edep if proj_mean_edep > 0 else float('inf')
    
    # Linearity (assume 5 GeV beam based on typical calorimeter tests)
    proj_beam_energy_mev = 5000  # 5 GeV
    proj_linearity = proj_mean_edep / proj_beam_energy_mev
    
    # Lateral containment
    proj_hits_df['r'] = np.sqrt(proj_hits_df['x']**2 + proj_hits_df['y']**2)
    proj_total_energy = proj_hits_df['edep'].sum()
    
    proj_hits_sorted = proj_hits_df.sort_values('r')
    proj_hits_sorted['cumulative_energy'] = proj_hits_sorted['edep'].cumsum()
    proj_hits_sorted['energy_fraction'] = proj_hits_sorted['cumulative_energy'] / proj_total_energy
    
    proj_r90_idx = proj_hits_sorted[proj_hits_sorted['energy_fraction'] >= 0.9].index
    proj_r90_mm = proj_hits_sorted.loc[proj_r90_idx[0], 'r'] if len(proj_r90_idx) > 0 else 0
    
    # Uniformity
    proj_uniformity_rms = proj_hits_df['edep'].std() / proj_hits_df['edep'].mean() if proj_hits_df['edep'].mean() > 0 else 0
    
    proj_results = {
        'energy_gev': 5.0,
        'mean_edep_mev': proj_mean_edep,
        'resolution': proj_resolution,
        'linearity': proj_linearity,
        'r90_containment_mm': proj_r90_mm,
        'uniformity_rms': proj_uniformity_rms,
        'n_events': len(proj_events_df)
    }
    
    results['projective_tower'] = proj_results
    print(f"Projective tower: resolution={proj_resolution:.4f}, linearity={proj_linearity:.3f}, R90={proj_r90_mm:.1f}mm")
    
except Exception as e:
    print(f"Error processing projective tower calorimeter: {e}")

# Output results for downstream steps
for geometry, data in results.items():
    if isinstance(data, list):  # Box calorimeter with multiple energies
        for point in data:
            energy = point['energy_gev']
            print(f"RESULT:{geometry}_{energy}gev_resolution={point['resolution']:.4f}")
            print(f"RESULT:{geometry}_{energy}gev_linearity={point['linearity']:.3f}")
            print(f"RESULT:{geometry}_{energy}gev_r90_mm={point['r90_containment_mm']:.1f}")
            print(f"RESULT:{geometry}_{energy}gev_uniformity={point['uniformity_rms']:.4f}")
    else:  # Single energy point
        print(f"RESULT:{geometry}_resolution={data['resolution']:.4f}")
        print(f"RESULT:{geometry}_linearity={data['linearity']:.3f}")
        print(f"RESULT:{geometry}_r90_mm={data['r90_containment_mm']:.1f}")
        print(f"RESULT:{geometry}_uniformity={data['uniformity_rms']:.4f}")

# Save detailed results to JSON
with open('calorimeter_performance_metrics.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Analysis complete. Results saved to calorimeter_performance_metrics.json")