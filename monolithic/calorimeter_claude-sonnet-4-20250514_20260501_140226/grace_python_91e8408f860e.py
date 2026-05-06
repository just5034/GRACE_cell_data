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
import numpy as np
import json
from pathlib import Path

# Material properties for hadronic calorimetry
material_properties = {
    'iron': {'density': 7.87, 'lambda_int': 16.8, 'X0': 1.76},  # g/cm³, cm, cm
    'lead': {'density': 11.34, 'lambda_int': 17.1, 'X0': 0.56},
    'scintillator': {'density': 1.032, 'lambda_int': 79.4, 'X0': 42.4}
}

# Energy range and constraints
energy_range = [10, 30, 50]  # GeV
max_depth_cm = 200  # Compact constraint
min_sampling_fraction = 0.03  # Minimum for reasonable resolution

configurations = []

# Configuration 1: Iron-Scintillator Projective Tower
config1 = {
    'name': 'iron_projective_tower',
    'topology': 'projective_tower',
    'absorber_material': 'iron',
    'active_material': 'scintillator',
    'description': 'Compact projective tower design optimized for forward region'
}

# Calculate optimal layer structure for iron
iron_lambda = material_properties['iron']['lambda_int']
scint_lambda = material_properties['scintillator']['lambda_int']

# Target 5-6 interaction lengths for 50 GeV containment
target_lambda = 5.5
iron_thickness_cm = 1.5  # cm per layer
scint_thickness_cm = 0.4  # cm per layer

# Calculate number of layers needed
layer_lambda = (iron_thickness_cm / iron_lambda) + (scint_thickness_cm / scint_lambda)
num_layers_1 = int(target_lambda / layer_lambda)
total_depth_1 = num_layers_1 * (iron_thickness_cm + scint_thickness_cm)

# Sampling fraction calculation
sampling_fraction_1 = scint_thickness_cm / (iron_thickness_cm + scint_thickness_cm)

config1.update({
    'absorber_thickness_cm': iron_thickness_cm,
    'active_thickness_cm': scint_thickness_cm,
    'num_layers': num_layers_1,
    'total_depth_cm': total_depth_1,
    'interaction_lengths': target_lambda,
    'sampling_fraction': sampling_fraction_1,
    'lateral_size_cm': 40.0  # Compact tower size
})

# Configuration 2: Lead-Scintillator Cylinder Barrel
config2 = {
    'name': 'lead_cylinder_barrel',
    'topology': 'cylinder_barrel',
    'absorber_material': 'lead',
    'active_material': 'scintillator',
    'description': 'Cylindrical barrel design for central detector region'
}

lead_lambda = material_properties['lead']['lambda_int']
lead_thickness_cm = 1.2  # cm per layer
scint_thickness_cm_2 = 0.3  # cm per layer

# Calculate for lead configuration
layer_lambda_2 = (lead_thickness_cm / lead_lambda) + (scint_thickness_cm_2 / scint_lambda)
num_layers_2 = int(target_lambda / layer_lambda_2)
total_depth_2 = num_layers_2 * (lead_thickness_cm + scint_thickness_cm_2)

sampling_fraction_2 = scint_thickness_cm_2 / (lead_thickness_cm + scint_thickness_cm_2)

config2.update({
    'absorber_thickness_cm': lead_thickness_cm,
    'active_thickness_cm': scint_thickness_cm_2,
    'num_layers': num_layers_2,
    'total_depth_cm': total_depth_2,
    'interaction_lengths': target_lambda,
    'sampling_fraction': sampling_fraction_2,
    'inner_radius_cm': 150.0,
    'outer_radius_cm': 150.0 + total_depth_2
})

# Configuration 3: Iron-Scintillator Segmented Design
config3 = {
    'name': 'iron_segmented',
    'topology': 'segmented',
    'absorber_material': 'iron',
    'active_material': 'scintillator',
    'description': 'Segmented tile design for flexible readout geometry'
}

# Optimized for better sampling fraction
iron_thickness_cm_3 = 2.0  # cm per layer
scint_thickness_cm_3 = 0.5  # cm per layer

layer_lambda_3 = (iron_thickness_cm_3 / iron_lambda) + (scint_thickness_cm_3 / scint_lambda)
num_layers_3 = int(target_lambda / layer_lambda_3)
total_depth_3 = num_layers_3 * (iron_thickness_cm_3 + scint_thickness_cm_3)

sampling_fraction_3 = scint_thickness_cm_3 / (iron_thickness_cm_3 + scint_thickness_cm_3)

config3.update({
    'absorber_thickness_cm': iron_thickness_cm_3,
    'active_thickness_cm': scint_thickness_cm_3,
    'num_layers': num_layers_3,
    'total_depth_cm': total_depth_3,
    'interaction_lengths': target_lambda,
    'sampling_fraction': sampling_fraction_3,
    'tile_size_cm': 10.0,
    'total_width_cm': 200.0
})

configurations = [config1, config2, config3]

# Calculate expected containment for each energy
for config in configurations:
    containment = {}
    for energy in energy_range:
        # Empirical containment formula for hadronic showers
        # R90 ~ 0.5 * sqrt(E_GeV) * lambda_int (cm)
        lambda_eff = config['interaction_lengths']
        r90_cm = 0.5 * np.sqrt(energy) * iron_lambda  # Use iron as reference
        containment[f'{energy}GeV'] = {
            'r90_cm': round(r90_cm, 1),
            'longitudinal_90': round(0.9 * lambda_eff, 2)
        }
    config['expected_containment'] = containment

# Print results
print('=== HADRONIC CALORIMETER DESIGN CONFIGURATIONS ===')
for i, config in enumerate(configurations, 1):
    print(f'\nConfiguration {i}: {config["name"]}')
    print(f'Topology: {config["topology"]}')
    print(f'Materials: {config["absorber_material"]} + {config["active_material"]}')
    print(f'Layer structure: {config["absorber_thickness_cm"]}cm + {config["active_thickness_cm"]}cm')
    print(f'Number of layers: {config["num_layers"]}')
    print(f'Total depth: {config["total_depth_cm"]:.1f} cm')
    print(f'Interaction lengths: {config["interaction_lengths"]:.1f} λ')
    print(f'Sampling fraction: {config["sampling_fraction"]:.3f}')
    print(f'Description: {config["description"]}')

# Save configurations to JSON
with open('calorimeter_configurations.json', 'w') as f:
    json.dump(configurations, f, indent=2)

# Output key results for downstream steps
print(f'\nRESULT:config1_name={config1["name"]}')
print(f'RESULT:config1_topology={config1["topology"]}')
print(f'RESULT:config1_absorber_material={config1["absorber_material"]}')
print(f'RESULT:config1_active_material={config1["active_material"]}')
print(f'RESULT:config1_absorber_thickness_cm={config1["absorber_thickness_cm"]}')
print(f'RESULT:config1_active_thickness_cm={config1["active_thickness_cm"]}')
print(f'RESULT:config1_num_layers={config1["num_layers"]}')
print(f'RESULT:config1_sampling_fraction={config1["sampling_fraction"]:.3f}')
print(f'RESULT:config1_interaction_lengths={config1["interaction_lengths"]:.1f}')

print(f'\nRESULT:config2_name={config2["name"]}')
print(f'RESULT:config2_topology={config2["topology"]}')
print(f'RESULT:config2_absorber_material={config2["absorber_material"]}')
print(f'RESULT:config2_active_material={config2["active_material"]}')
print(f'RESULT:config2_sampling_fraction={config2["sampling_fraction"]:.3f}')
print(f'RESULT:config2_interaction_lengths={config2["interaction_lengths"]:.1f}')

print(f'\nRESULT:config3_name={config3["name"]}')
print(f'RESULT:config3_topology={config3["topology"]}')
print(f'RESULT:config3_sampling_fraction={config3["sampling_fraction"]:.3f}')
print(f'RESULT:config3_interaction_lengths={config3["interaction_lengths"]:.1f}')

print('\nCalorimeter configurations designed and saved to calorimeter_configurations.json')