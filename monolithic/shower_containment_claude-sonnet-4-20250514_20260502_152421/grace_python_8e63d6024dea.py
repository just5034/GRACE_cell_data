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

# Data from simulate_shallow_depths (16X0 - 14.2cm)
events_files_16x0 = {
    1.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_1.000GeV/pbwo4_16x0_calorimeter_em_events.parquet",
    5.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_5.000GeV/pbwo4_16x0_calorimeter_em_events.parquet",
    20.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_20.000GeV/pbwo4_16x0_calorimeter_em_events.parquet"
}

hits_files_16x0 = {
    1.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_1.000GeV/pbwo4_16x0_calorimeter_em_hits_data.parquet",
    5.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_5.000GeV/pbwo4_16x0_calorimeter_em_hits_data.parquet",
    20.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_20.000GeV/pbwo4_16x0_calorimeter_em_hits_data.parquet"
}

# Data from simulate_deep_depth (25X0 - 22.3cm)
events_files_25x0 = {
    1.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_1.000GeV/pbwo4_25x0_calorimeter_em_events.parquet",
    5.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_5.000GeV/pbwo4_25x0_calorimeter_em_events.parquet",
    20.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_20.000GeV/pbwo4_25x0_calorimeter_em_events.parquet"
}

hits_files_25x0 = {
    1.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_1.000GeV/pbwo4_25x0_calorimeter_em_hits_data.parquet",
    5.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_5.000GeV/pbwo4_25x0_calorimeter_em_hits_data.parquet",
    20.0: "/tmp/grace_jhill5_18010099/grace_run_shower_containment_mono10k_18010045_6/shower_containment_claude-sonnet-4-20250514_20260502_152421/energy_20.000GeV/pbwo4_25x0_calorimeter_em_hits_data.parquet"
}

# Depth configurations
depths = [14.2, 17.8, 22.3]  # cm
depth_configs = {
    14.2: {'events': events_files_16x0, 'hits': hits_files_16x0, 'name': '16X0'},
    22.3: {'events': events_files_25x0, 'hits': hits_files_25x0, 'name': '25X0'}
}

results = {}
target_leakage = 0.01

# Analyze each depth configuration
for depth_cm in [14.2, 22.3]:
    if depth_cm not in depth_configs:
        continue
        
    config = depth_configs[depth_cm]
    results[depth_cm] = {}
    
    print(f"Analyzing depth {depth_cm} cm ({config['name']})...")
    
    # Analyze each energy
    for energy_gev in [1.0, 5.0, 20.0]:
        # Load event data for energy resolution
        events_df = pd.read_parquet(config['events'][energy_gev])
        
        # Calculate energy resolution
        beam_energy_mev = energy_gev * 1000
        mean_edep = events_df['totalEdep'].mean()  # MeV
        std_edep = events_df['totalEdep'].std()
        energy_resolution = std_edep / mean_edep if mean_edep > 0 else float('inf')
        
        # Calculate containment fraction (fraction of beam energy contained)
        containment_fraction = mean_edep / beam_energy_mev
        leakage_fraction = 1.0 - containment_fraction
        
        # Load hit data for shower maximum analysis (sample to avoid memory issues)
        hits_df = pd.read_parquet(config['hits'][energy_gev])
        if len(hits_df) > 100000:
            hits_df = hits_df.sample(n=100000, random_state=42)
        
        # Calculate shower maximum position (z position weighted by energy deposit)
        if len(hits_df) > 0 and hits_df['edep'].sum() > 0:
            shower_max_z = np.average(hits_df['z'], weights=hits_df['edep'])
        else:
            shower_max_z = 0.0
        
        results[depth_cm][energy_gev] = {
            'energy_resolution': energy_resolution,
            'containment_fraction': containment_fraction,
            'leakage_fraction': leakage_fraction,
            'shower_max_z_mm': shower_max_z,
            'mean_edep_mev': mean_edep,
            'n_events': len(events_df)
        }
        
        print(f"  {energy_gev} GeV: Resolution={energy_resolution:.4f}, Containment={containment_fraction:.4f}, Leakage={leakage_fraction:.4f}")

# Determine minimum depth for <1% leakage at 20 GeV
print("\nLeakage analysis at 20 GeV:")
min_depth_for_target = None
for depth_cm in sorted(results.keys()):
    leakage_20gev = results[depth_cm][20.0]['leakage_fraction']
    meets_target = leakage_20gev < target_leakage
    print(f"Depth {depth_cm} cm: Leakage = {leakage_20gev:.4f} ({'PASS' if meets_target else 'FAIL'})")
    
    if meets_target and min_depth_for_target is None:
        min_depth_for_target = depth_cm

# Output results
for depth_cm in results.keys():
    for energy_gev in results[depth_cm].keys():
        res = results[depth_cm][energy_gev]
        depth_name = f"depth{depth_cm:.1f}cm"
        energy_name = f"energy{energy_gev:.0f}GeV"
        
        print(f"RESULT:{depth_name}_{energy_name}_energy_resolution={res['energy_resolution']:.6f}")
        print(f"RESULT:{depth_name}_{energy_name}_containment_fraction={res['containment_fraction']:.6f}")
        print(f"RESULT:{depth_name}_{energy_name}_leakage_fraction={res['leakage_fraction']:.6f}")
        print(f"RESULT:{depth_name}_{energy_name}_shower_max_z_mm={res['shower_max_z_mm']:.2f}")

print(f"RESULT:target_leakage_threshold={target_leakage}")
if min_depth_for_target is not None:
    print(f"RESULT:minimum_depth_for_target_cm={min_depth_for_target}")
    print(f"RESULT:minimum_depth_meets_requirement=True")
else:
    print(f"RESULT:minimum_depth_meets_requirement=False")

# Save detailed results to JSON
with open('containment_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nAnalysis complete. Results saved to containment_analysis_results.json")