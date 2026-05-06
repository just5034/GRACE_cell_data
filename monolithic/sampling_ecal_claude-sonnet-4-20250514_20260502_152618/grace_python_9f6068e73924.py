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

# Load geometry parameters from previous steps
num_layers = 44
w_thickness_cm = 0.2
scint_thickness_cm = 0.5
total_depth_cm = 30.8
transverse_size_m = 0.2
sampling_fraction_design = 0.7143

# Load simulation data from energy sweep
events_files = {
    1.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_1.000GeV/thin_absorber_calorimeter_em_events.parquet",
    5.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_5.000GeV/thin_absorber_calorimeter_em_events.parquet",
    20.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_20.000GeV/thin_absorber_calorimeter_em_events.parquet"
}

hits_files = {
    1.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_1.000GeV/thin_absorber_calorimeter_em_hits_data.parquet",
    5.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_5.000GeV/thin_absorber_calorimeter_em_hits_data.parquet",
    20.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_20.000GeV/thin_absorber_calorimeter_em_hits_data.parquet"
}

# Calculate sampling fraction from simulation
sampling_fractions = []
for energy_gev, filepath in events_files.items():
    df = pd.read_parquet(filepath)
    beam_energy_mev = energy_gev * 1000
    mean_deposit_mev = df['totalEdep'].mean()
    sampling_fraction = mean_deposit_mev / beam_energy_mev
    sampling_fractions.append(sampling_fraction)
    print(f"Energy {energy_gev} GeV: Sampling fraction = {sampling_fraction:.4f}")

avg_sampling_fraction = np.mean(sampling_fractions)
print(f"Average sampling fraction: {avg_sampling_fraction:.4f}")

# Calculate shower containment (R90) using 5 GeV data
hits_df = pd.read_parquet(hits_files[5.0])

# Calculate radial distance from beam axis (assuming beam along z-axis)
hits_df['r'] = np.sqrt(hits_df['x']**2 + hits_df['y']**2)

# Calculate R90 containment for each event
containment_r90 = []
for event_id in hits_df['eventID'].unique():
    event_hits = hits_df[hits_df['eventID'] == event_id]
    total_energy = event_hits['edep'].sum()
    
    # Sort hits by radial distance
    event_hits_sorted = event_hits.sort_values('r')
    cumulative_energy = event_hits_sorted['edep'].cumsum()
    
    # Find radius containing 90% of energy
    energy_90 = 0.9 * total_energy
    idx_90 = np.where(cumulative_energy >= energy_90)[0]
    if len(idx_90) > 0:
        r90 = event_hits_sorted.iloc[idx_90[0]]['r']
        containment_r90.append(r90)

avg_r90_mm = np.mean(containment_r90)
print(f"Average R90 containment: {avg_r90_mm:.2f} mm")

# Calculate detector mass and volume
# Material densities (g/cm3)
density_tungsten = 19.25  # g/cm3
density_scintillator = 1.032  # g/cm3 for plastic scintillator

# Volume calculations
transverse_area_cm2 = (transverse_size_m * 100)**2  # Convert m to cm
w_volume_cm3 = num_layers * w_thickness_cm * transverse_area_cm2
scint_volume_cm3 = num_layers * scint_thickness_cm * transverse_area_cm2
total_volume_cm3 = w_volume_cm3 + scint_volume_cm3

# Mass calculations
w_mass_kg = (w_volume_cm3 * density_tungsten) / 1000  # Convert g to kg
scint_mass_kg = (scint_volume_cm3 * density_scintillator) / 1000
total_mass_kg = w_mass_kg + scint_mass_kg

print(f"Tungsten volume: {w_volume_cm3:.1f} cm3")
print(f"Scintillator volume: {scint_volume_cm3:.1f} cm3")
print(f"Total volume: {total_volume_cm3:.1f} cm3")
print(f"Tungsten mass: {w_mass_kg:.2f} kg")
print(f"Scintillator mass: {scint_mass_kg:.2f} kg")
print(f"Total mass: {total_mass_kg:.2f} kg")

# Save results
results = {
    'sampling_fraction': avg_sampling_fraction,
    'shower_containment_r90_mm': avg_r90_mm,
    'detector_mass_kg': total_mass_kg,
    'detector_volume_cm3': total_volume_cm3,
    'tungsten_mass_kg': w_mass_kg,
    'scintillator_mass_kg': scint_mass_kg,
    'tungsten_volume_cm3': w_volume_cm3,
    'scintillator_volume_cm3': scint_volume_cm3
}

with open('sampling_metrics.json', 'w') as f:
    json.dump(results, f, indent=2)

# Output results for downstream steps
print(f"RESULT:sampling_fraction={avg_sampling_fraction:.4f}")
print(f"RESULT:shower_containment_r90_mm={avg_r90_mm:.2f}")
print(f"RESULT:detector_mass_kg={total_mass_kg:.2f}")
print(f"RESULT:detector_volume_cm3={total_volume_cm3:.1f}")
print(f"RESULT:tungsten_mass_kg={w_mass_kg:.2f}")
print(f"RESULT:scintillator_mass_kg={scint_mass_kg:.2f}")

print("\nSampling metrics calculation completed successfully!")