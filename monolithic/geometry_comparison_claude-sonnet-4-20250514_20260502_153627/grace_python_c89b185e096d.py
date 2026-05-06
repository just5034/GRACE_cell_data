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
        # Reset index and validate data
        df = pd.read_parquet(filepath)
        df = df.reset_index(drop=True)
        
        # Handle missing data and bounds checking
        if df.empty or 'totalEdep' not in df.columns:
            print(f"Warning: Missing or invalid data for {energy_gev} GeV")
            continue
            
        # Filter out invalid energy deposits
        df_clean = df[df['totalEdep'] > 0].copy()
        
        if len(df_clean) == 0:
            print(f"Warning: No valid energy deposits for {energy_gev} GeV")
            continue
            
        # Calculate energy resolution metrics
        mean_edep = df_clean['totalEdep'].mean()  # MeV
        std_edep = df_clean['totalEdep'].std()
        resolution = std_edep / mean_edep if mean_edep > 0 else float('inf')
        
        # Calculate linearity (beam energy in MeV)
        beam_energy_mev = energy_gev * 1000
        linearity = mean_edep / beam_energy_mev if beam_energy_mev > 0 else 0
        
        box_results[energy_gev] = {
            'mean_edep_mev': mean_edep,
            'std_edep_mev': std_edep,
            'resolution': resolution,
            'linearity': linearity,
            'n_events': len(df_clean)
        }
        
        print(f"Box {energy_gev} GeV: resolution={resolution:.4f}, linearity={linearity:.3f}")
        
    except Exception as e:
        print(f"Error processing box {energy_gev} GeV: {e}")
        continue

# Analyze containment for box calorimeter (using 5 GeV data)
print("\nAnalyzing box calorimeter containment...")
try:
    hits_df = pd.read_parquet(hits_files_box[5.0])
    hits_df = hits_df.reset_index(drop=True)
    
    if not hits_df.empty and 'x' in hits_df.columns and 'y' in hits_df.columns:
        # Calculate radial distance from center
        hits_df['r'] = np.sqrt(hits_df['x']**2 + hits_df['y']**2)
        
        # Calculate containment fractions
        total_energy = hits_df['edep'].sum()
        if total_energy > 0:
            # R90 containment (radius containing 90% of energy)
            sorted_hits = hits_df.sort_values('r')
            cumulative_energy = sorted_hits['edep'].cumsum()
            r90_idx = np.searchsorted(cumulative_energy, 0.9 * total_energy)
            r90_containment = sorted_hits.iloc[r90_idx]['r'] if r90_idx < len(sorted_hits) else sorted_hits['r'].max()
            
            box_results['containment'] = {
                'r90_mm': float(r90_containment),
                'total_energy_mev': float(total_energy)
            }
            
            print(f"Box containment R90: {r90_containment:.1f} mm")
except Exception as e:
    print(f"Error calculating box containment: {e}")

# Analyze projective tower calorimeter
print("\nAnalyzing projective tower calorimeter...")
try:
    proj_df = pd.read_parquet(projective_events_file)
    proj_df = proj_df.reset_index(drop=True)
    
    if not proj_df.empty and 'totalEdep' in proj_df.columns:
        proj_df_clean = proj_df[proj_df['totalEdep'] > 0].copy()
        
        if len(proj_df_clean) > 0:
            mean_edep_proj = proj_df_clean['totalEdep'].mean()
            std_edep_proj = proj_df_clean['totalEdep'].std()
            resolution_proj = std_edep_proj / mean_edep_proj if mean_edep_proj > 0 else float('inf')
            
            # Assume 5 GeV beam for projective (typical test energy)
            linearity_proj = mean_edep_proj / 5000.0
            
            projective_results = {
                'mean_edep_mev': mean_edep_proj,
                'std_edep_mev': std_edep_proj,
                'resolution': resolution_proj,
                'linearity': linearity_proj,
                'n_events': len(proj_df_clean)
            }
            
            print(f"Projective: resolution={resolution_proj:.4f}, linearity={linearity_proj:.3f}")
            
            results['projective_tower'] = projective_results
except Exception as e:
    print(f"Error processing projective data: {e}")

results['box_calorimeter'] = box_results

# Calculate summary metrics
print("\nSummary metrics:")
if box_results:
    # Energy resolution vs energy trend
    energies = sorted(box_results.keys())
    resolutions = [box_results[e]['resolution'] for e in energies if 'resolution' in box_results[e]]
    
    if len(resolutions) >= 2:
        # Fit resolution = a/sqrt(E) + b (stochastic + constant terms)
        sqrt_energies = [np.sqrt(e) for e in energies[:len(resolutions)]]
        if len(sqrt_energies) == len(resolutions):
            # Simple linear fit for a/sqrt(E) term
            coeffs = np.polyfit([1/se for se in sqrt_energies], resolutions, 1)
            stochastic_term = coeffs[0] if len(coeffs) > 0 else 0
            constant_term = coeffs[1] if len(coeffs) > 1 else 0
            
            print(f"Box energy resolution fit: {stochastic_term:.3f}/sqrt(E) + {constant_term:.4f}")
            
            results['box_calorimeter']['resolution_fit'] = {
                'stochastic_term': stochastic_term,
                'constant_term': constant_term
            }

# Output results for downstream steps
for geom_name, geom_results in results.items():
    if isinstance(geom_results, dict):
        for metric, value in geom_results.items():
            if isinstance(value, (int, float)):
                print(f"RESULT:{geom_name}_{metric}={value:.4f}")

# Save detailed results to JSON
with open('energy_resolution_analysis.json', 'w') as f:
    # Convert numpy types to native Python for JSON serialization
    def convert_numpy(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(v) for v in obj]
        return obj
    
    json.dump(convert_numpy(results), f, indent=2)

print("\nAnalysis complete. Results saved to energy_resolution_analysis.json")