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
from scipy.optimize import curve_fit
import json

# Event-level data from 'simulate_energy_sweep' (columns: eventID, totalEdep [MeV], nHits)
events_files_simulate_energy_sweep = {
    1.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_1.000GeV/thin_absorber_calorimeter_em_events.parquet",
    5.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_5.000GeV/thin_absorber_calorimeter_em_events.parquet",
    20.0: "/tmp/grace_jhill5_18010107/grace_run_sampling_ecal_mono10k_18010045_7/sampling_ecal_claude-sonnet-4-20250514_20260502_152618/energy_20.000GeV/thin_absorber_calorimeter_em_events.parquet",
}

# Extract energy resolution at each energy point
results = {}
for energy_gev, filepath in events_files_simulate_energy_sweep.items():
    df = pd.read_parquet(filepath)
    mean_edep = df['totalEdep'].mean()  # MeV
    std_edep = df['totalEdep'].std()
    resolution = std_edep / mean_edep if mean_edep > 0 else float('inf')
    results[energy_gev] = {
        'mean_edep_mev': mean_edep, 
        'resolution': resolution, 
        'n_events': len(df)
    }
    print(f"Energy {energy_gev} GeV: Resolution = {resolution:.4f}, Mean = {mean_edep:.1f} MeV")

# Prepare data for fitting
energies = np.array(list(results.keys()))  # GeV
resolutions = np.array([results[e]['resolution'] for e in energies])

# Define fit function: a/sqrt(E) + b/E + c
def resolution_function(E, a, b, c):
    return a / np.sqrt(E) + b / E + c

# Perform fit
try:
    popt, pcov = curve_fit(resolution_function, energies, resolutions)
    stochastic_term, noise_term, constant_term = popt
    
    # Calculate fit quality
    fitted_resolutions = resolution_function(energies, *popt)
    chi2 = np.sum((resolutions - fitted_resolutions)**2)
    
    print(f"\nFit results:")
    print(f"Stochastic term (a): {stochastic_term:.4f}")
    print(f"Noise term (b): {noise_term:.4f}")
    print(f"Constant term (c): {constant_term:.4f}")
    print(f"Chi-squared: {chi2:.6f}")
    
    # Output results for downstream steps
    print(f"RESULT:stochastic_term={stochastic_term:.4f}")
    print(f"RESULT:noise_term={noise_term:.4f}")
    print(f"RESULT:constant_term={constant_term:.4f}")
    print(f"RESULT:fit_chi2={chi2:.6f}")
    
    # Save detailed results
    fit_results = {
        'energy_points_gev': energies.tolist(),
        'measured_resolutions': resolutions.tolist(),
        'fitted_resolutions': fitted_resolutions.tolist(),
        'fit_parameters': {
            'stochastic_term': float(stochastic_term),
            'noise_term': float(noise_term),
            'constant_term': float(constant_term)
        },
        'fit_quality': {
            'chi2': float(chi2),
            'covariance_matrix': pcov.tolist()
        },
        'raw_data': results
    }
    
    with open('energy_resolution_analysis.json', 'w') as f:
        json.dump(fit_results, f, indent=2)
    
    print("\nAnalysis complete. Results saved to energy_resolution_analysis.json")
    
except Exception as e:
    print(f"Fit failed: {e}")
    print("Raw resolution data:")
    for energy_gev in sorted(results.keys()):
        res = results[energy_gev]['resolution']
        print(f"  {energy_gev} GeV: {res:.4f}")