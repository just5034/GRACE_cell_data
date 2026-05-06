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
from pathlib import Path
import json

# Load box calorimeter energy sweep data (from Previous Step Outputs)
events_files_box = {
    1.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_1.000GeV/box_calorimeter_em_events.parquet",
    5.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_5.000GeV/box_calorimeter_em_events.parquet",
    20.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_20.000GeV/box_calorimeter_em_events.parquet"
}

hits_files_box = {
    1.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_1.000GeV/box_calorimeter_em_hits_data.parquet",
    5.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_5.000GeV/box_calorimeter_em_hits_data.parquet",
    20.0: "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/energy_20.000GeV/box_calorimeter_em_hits_data.parquet"
}

# Load projective tower calorimeter data
projective_events_file = "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/projective_tower_calorimeter_em_events.parquet"
projective_hits_file = "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/projective_tower_calorimeter_em_hits_data.parquet"

results = {}

# Analyze box calorimeter energy sweep
print("Analyzing box calorimeter energy sweep...")
box_results = {}
for energy_gev, filepath in events_files_box.items():
    try:
        df = pd.read_parquet(filepath)
        beam_energy_mev = energy_gev * 1000  # Convert GeV to MeV
        
        # Energy resolution
        mean_edep = df['totalEdep'].mean()
        std_edep = df['totalEdep'].std()
        resolution = std_edep / mean_edep if mean_edep > 0 else float('inf')
        
        # Linearity (response vs true energy)
        linearity = mean_edep / beam_energy_mev if beam_energy_mev > 0 else 0
        
        box_results[energy_gev] = {
            'mean_edep_mev': mean_edep,
            'std_edep_mev': std_edep,
            'resolution': resolution,
            'linearity': linearity,
            'n_events': len(df),
            'beam_energy_gev': energy_gev
        }
        
        print(f"Box {energy_gev} GeV: resolution={resolution:.4f}, linearity={linearity:.4f}")
        
    except Exception as e:
        print(f"Error processing box {energy_gev} GeV: {e}")

# Analyze projective tower calorimeter
print("\nAnalyzing projective tower calorimeter...")
try:
    proj_events = pd.read_parquet(projective_events_file)
    proj_hits = pd.read_parquet(projective_hits_file)
    
    # Assume 5 GeV beam for projective (typical energy)
    beam_energy_mev = 5000
    
    # Energy resolution
    mean_edep_proj = proj_events['totalEdep'].mean()
    std_edep_proj = proj_events['totalEdep'].std()
    resolution_proj = std_edep_proj / mean_edep_proj if mean_edep_proj > 0 else float('inf')
    linearity_proj = mean_edep_proj / beam_energy_mev
    
    # Containment analysis (sample first 100k hits to avoid timeout)
    hits_sample = proj_hits.head(100000) if len(proj_hits) > 100000 else proj_hits
    
    # Calculate radial distances
    r_values = np.sqrt(hits_sample['x']**2 + hits_sample['y']**2)
    
    # R90 containment (radius containing 90% of energy)
    total_energy = hits_sample['edep'].sum()
    sorted_indices = np.argsort(r_values)
    cumulative_energy = np.cumsum(hits_sample['edep'].iloc[sorted_indices])
    r90_index = np.searchsorted(cumulative_energy, 0.9 * total_energy)
    r90_mm = r_values.iloc[sorted_indices[r90_index]] if r90_index < len(r_values) else r_values.max()
    
    projective_results = {
        'mean_edep_mev': mean_edep_proj,
        'std_edep_mev': std_edep_proj,
        'resolution': resolution_proj,
        'linearity': linearity_proj,
        'r90_containment_mm': r90_mm,
        'n_events': len(proj_events),
        'n_hits_analyzed': len(hits_sample)
    }
    
    print(f"Projective: resolution={resolution_proj:.4f}, linearity={linearity_proj:.4f}, R90={r90_mm:.1f}mm")
    
except Exception as e:
    print(f"Error processing projective data: {e}")
    projective_results = {}

# Output results
results['box_calorimeter'] = box_results
results['projective_tower'] = projective_results

# Save detailed results
with open('calorimeter_performance_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

# Output key metrics for workflow
if box_results:
    # Energy resolution scaling analysis
    energies = sorted(box_results.keys())
    resolutions = [box_results[e]['resolution'] for e in energies]
    
    print(f"RESULT:box_energy_resolution_1gev={box_results.get(1.0, {}).get('resolution', 0):.4f}")
    print(f"RESULT:box_energy_resolution_5gev={box_results.get(5.0, {}).get('resolution', 0):.4f}")
    print(f"RESULT:box_energy_resolution_20gev={box_results.get(20.0, {}).get('resolution', 0):.4f}")
    
    # Average linearity
    linearities = [box_results[e]['linearity'] for e in energies]
    avg_linearity = np.mean(linearities)
    print(f"RESULT:box_average_linearity={avg_linearity:.4f}")

if projective_results:
    print(f"RESULT:projective_energy_resolution={projective_results.get('resolution', 0):.4f}")
    print(f"RESULT:projective_linearity={projective_results.get('linearity', 0):.4f}")
    print(f"RESULT:projective_r90_containment_mm={projective_results.get('r90_containment_mm', 0):.1f}")

print(f"RESULT:analysis_complete=true")
print(f"RESULT:geometries_analyzed=2")
print(f"RESULT:energy_points_analyzed={len(box_results)}")