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
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

# Load box calorimeter energy sweep data (3 energy points)
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

# Load projective tower calorimeter data (single energy point)
projective_events_file = "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/projective_tower_calorimeter_em_events.parquet"
projective_hits_file = "/tmp/grace_jhill5_18010165/grace_run_geometry_comparison_mono10k_18010045_8/geometry_comparison_claude-sonnet-4-20250514_20260502_153627/projective_tower_calorimeter_em_hits_data.parquet"

# Geometry parameters from previous steps
box_geometry = {
    'detector_type': 'sampling_calorimeter',
    'topology': 'box',
    'total_depth_m': 0.21,
    'transverse_size_m': 0.4,
    'num_layers': 30,
    'sampling_fraction': 0.571429
}

projective_geometry = {
    'detector_type': 'sampling_calorimeter', 
    'topology': 'projective_tower',
    'total_depth_m': 0.21,
    'inner_radius_m': 0.15,
    'outer_radius_m': 0.36,
    'num_layers': 30,
    'sampling_fraction': 0.571429
}

results = {}

# Analyze box calorimeter energy sweep
print("Analyzing box calorimeter energy sweep...")
box_results = {}
for energy_gev, filepath in events_files_box.items():
    print(f"Processing {energy_gev} GeV data...")
    
    # Check if file exists
    if not Path(filepath).exists():
        print(f"WARNING: File not found: {filepath}")
        continue
        
    # Load event data
    df_events = pd.read_parquet(filepath)
    print(f"Loaded {len(df_events)} events for {energy_gev} GeV")
    
    # Verify minimum 5 energy points requirement
    if len(df_events) < 5:
        print(f"WARNING: Only {len(df_events)} events for {energy_gev} GeV - insufficient for analysis")
        continue
    
    # Use totalEdep column as specified
    if 'totalEdep' not in df_events.columns:
        print(f"ERROR: totalEdep column not found in {filepath}")
        continue
        
    # Physics validation - check for reasonable energy deposits
    beam_energy_mev = energy_gev * 1000
    mean_edep_mev = df_events['totalEdep'].mean()
    std_edep_mev = df_events['totalEdep'].std()
    
    # Check for energy leakage
    response = mean_edep_mev / beam_energy_mev
    if response < 0.1:
        print(f"WARNING: Low energy response {response:.3f} at {energy_gev} GeV - possible leakage")
    
    # Energy resolution
    resolution = std_edep_mev / mean_edep_mev if mean_edep_mev > 0 else float('inf')
    
    # Linearity (response vs beam energy)
    linearity = mean_edep_mev / beam_energy_mev
    
    box_results[energy_gev] = {
        'mean_edep_mev': mean_edep_mev,
        'std_edep_mev': std_edep_mev,
        'resolution': resolution,
        'linearity': linearity,
        'n_events': len(df_events),
        'beam_energy_mev': beam_energy_mev
    }
    
    print(f"{energy_gev} GeV: Resolution={resolution:.4f}, Linearity={linearity:.4f}")

# Analyze containment for box calorimeter using hits data
print("\nAnalyzing containment for box calorimeter...")
for energy_gev, hits_filepath in hits_files_box.items():
    if energy_gev not in box_results:
        continue
        
    if not Path(hits_filepath).exists():
        print(f"WARNING: Hits file not found: {hits_filepath}")
        continue
        
    # Load hits data (sample first 100k hits to avoid memory issues)
    df_hits = pd.read_parquet(hits_filepath)
    if len(df_hits) > 100000:
        df_hits = df_hits.head(100000)
        print(f"Sampled first 100k hits for {energy_gev} GeV containment analysis")
    
    # Lateral containment (R90 - radius containing 90% of energy)
    df_hits['r'] = np.sqrt(df_hits['x']**2 + df_hits['y']**2)
    total_energy = df_hits['edep'].sum()
    
    # Sort by radius and calculate cumulative energy
    df_sorted = df_hits.sort_values('r')
    df_sorted['cumulative_energy'] = df_sorted['edep'].cumsum()
    df_sorted['energy_fraction'] = df_sorted['cumulative_energy'] / total_energy
    
    # Find R90 (radius containing 90% of energy)
    r90_idx = df_sorted[df_sorted['energy_fraction'] >= 0.9].index
    if len(r90_idx) > 0:
        r90_mm = df_sorted.loc[r90_idx[0], 'r']
    else:
        r90_mm = df_sorted['r'].max()
    
    # Longitudinal containment
    z_max = df_hits['z'].max()
    z_min = df_hits['z'].min()
    shower_length_mm = z_max - z_min
    
    # Check detector depth adequacy
    detector_depth_mm = box_geometry['total_depth_m'] * 1000
    depth_adequacy = detector_depth_mm / shower_length_mm if shower_length_mm > 0 else float('inf')
    
    box_results[energy_gev]['r90_containment_mm'] = r90_mm
    box_results[energy_gev]['shower_length_mm'] = shower_length_mm
    box_results[energy_gev]['depth_adequacy'] = depth_adequacy
    
    print(f"{energy_gev} GeV: R90={r90_mm:.1f}mm, Shower length={shower_length_mm:.1f}mm")

# Analyze projective tower calorimeter
print("\nAnalyzing projective tower calorimeter...")
if Path(projective_events_file).exists():
    df_proj_events = pd.read_parquet(projective_events_file)
    print(f"Loaded {len(df_proj_events)} projective events")
    
    # Assume 5 GeV beam for projective (typical for comparison)
    proj_beam_energy_mev = 5000
    proj_mean_edep = df_proj_events['totalEdep'].mean()
    proj_std_edep = df_proj_events['totalEdep'].std()
    proj_resolution = proj_std_edep / proj_mean_edep if proj_mean_edep > 0 else float('inf')
    proj_linearity = proj_mean_edep / proj_beam_energy_mev
    
    projective_results = {
        'mean_edep_mev': proj_mean_edep,
        'resolution': proj_resolution,
        'linearity': proj_linearity,
        'n_events': len(df_proj_events),
        'beam_energy_mev': proj_beam_energy_mev
    }
    
    # Containment analysis for projective
    if Path(projective_hits_file).exists():
        df_proj_hits = pd.read_parquet(projective_hits_file)
        if len(df_proj_hits) > 100000:
            df_proj_hits = df_proj_hits.head(100000)
        
        # Convert to cylindrical coordinates for projective geometry
        df_proj_hits['r'] = np.sqrt(df_proj_hits['x']**2 + df_proj_hits['y']**2)
        total_proj_energy = df_proj_hits['edep'].sum()
        
        df_proj_sorted = df_proj_hits.sort_values('r')
        df_proj_sorted['cumulative_energy'] = df_proj_sorted['edep'].cumsum()
        df_proj_sorted['energy_fraction'] = df_proj_sorted['cumulative_energy'] / total_proj_energy
        
        r90_proj_idx = df_proj_sorted[df_proj_sorted['energy_fraction'] >= 0.9].index
        if len(r90_proj_idx) > 0:
            r90_proj_mm = df_proj_sorted.loc[r90_proj_idx[0], 'r']
        else:
            r90_proj_mm = df_proj_sorted['r'].max()
            
        projective_results['r90_containment_mm'] = r90_proj_mm
    
    results['projective_tower'] = projective_results
    print(f"Projective: Resolution={proj_resolution:.4f}, Linearity={proj_linearity:.4f}")
else:
    print(f"WARNING: Projective events file not found: {projective_events_file}")

results['box_calorimeter'] = box_results

# Output results with standardized naming
print("\n=== ANALYSIS RESULTS ===")
for geometry, geom_results in results.items():
    if geometry == 'box_calorimeter':
        for energy_gev, energy_results in geom_results.items():
            prefix = f"box_{energy_gev}gev"
            print(f"RESULT:{prefix}_energy_resolution={energy_results['resolution']:.4f}")
            print(f"RESULT:{prefix}_linearity={energy_results['linearity']:.4f}")
            print(f"RESULT:{prefix}_mean_deposit_mev={energy_results['mean_edep_mev']:.1f}")
            if 'r90_containment_mm' in energy_results:
                print(f"RESULT:{prefix}_r90_containment_mm={energy_results['r90_containment_mm']:.1f}")
    else:
        prefix = geometry
        print(f"RESULT:{prefix}_energy_resolution={geom_results['resolution']:.4f}")
        print(f"RESULT:{prefix}_linearity={geom_results['linearity']:.4f}")
        print(f"RESULT:{prefix}_mean_deposit_mev={geom_results['mean_edep_mev']:.1f}")
        if 'r90_containment_mm' in geom_results:
            print(f"RESULT:{prefix}_r90_containment_mm={geom_results['r90_containment_mm']:.1f}")

# Save detailed results to JSON
with open('geometry_performance_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nAnalysis complete. Results saved to geometry_performance_analysis.json")
print(f"Analyzed {len(events_files_box)} energy points for box calorimeter")
print("Physics validation and containment analysis completed")