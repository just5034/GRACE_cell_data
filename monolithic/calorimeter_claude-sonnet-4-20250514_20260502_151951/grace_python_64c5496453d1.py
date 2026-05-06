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
import json
import math

# Design parameters from input requirements
energy_range = [10, 30, 50]  # GeV
particle_types = ['pi+', 'protons']
topologies = ['projective_tower', 'cylinder_barrel', 'segmented']
materials = ['iron', 'steel', 'scintillator']

# Performance targets
energy_resolution_target = '50-100%/sqrt(E)'
containment_efficiency_target = '>95%'
response_linearity_target = '<5% deviation'

# Design Configuration 1: Projective Tower with Iron/Scintillator
config1 = {
    'name': 'projective_tower_iron',
    'topology': 'projective_tower',
    'absorber_material': 'iron',
    'active_material': 'plastic_scintillator',
    'geometry_parameters': {
        'absorber_thickness': 0.020,  # 20mm iron
        'active_thickness': 0.004,    # 4mm scintillator
        'num_layers': 45,             # ~9 interaction lengths
        'inner_radius': 1.5,          # 1.5m inner radius
        'half_length': 2.5,           # 5m total length
        'tower_eta_segments': 32,     # Eta segmentation
        'tower_phi_segments': 64,     # Phi segmentation
        'eta_min': -2.5,
        'eta_max': 2.5
    },
    'design_rationale': 'Projective geometry for collider environment, iron absorber for cost-effectiveness, fine segmentation for position resolution'
}

# Design Configuration 2: Cylinder Barrel with Steel/Scintillator
config2 = {
    'name': 'cylinder_barrel_steel',
    'topology': 'cylinder_barrel',
    'absorber_material': 'steel',
    'active_material': 'plastic_scintillator',
    'geometry_parameters': {
        'absorber_thickness': 0.014,  # 14mm steel
        'active_thickness': 0.003,    # 3mm scintillator
        'num_layers': 64,             # ~9 interaction lengths
        'inner_radius': 2.0,          # 2.0m inner radius
        'half_length': 3.0,           # 6m total length
        'transverse_size': 1.0        # For reference
    },
    'design_rationale': 'Barrel geometry for uniform coverage, steel absorber for mechanical strength, optimized for mid-energy hadrons'
}

# Design Configuration 3: Segmented with Iron/Scintillator (Tile-based)
config3 = {
    'name': 'segmented_tile_iron',
    'topology': 'segmented',
    'absorber_material': 'iron',
    'active_material': 'plastic_scintillator',
    'geometry_parameters': {
        'absorber_thickness': 0.025,  # 25mm iron
        'active_thickness': 0.005,    # 5mm scintillator
        'num_layers': 40,             # ~10 interaction lengths
        'transverse_size': 0.8,       # 80cm transverse size
        'tile_size': 0.1,             # 10cm tiles
        'num_tiles_x': 8,
        'num_tiles_y': 8
    },
    'design_rationale': 'Segmented tile readout for flexibility, thicker sampling for better energy resolution, modular design for maintenance'
}

# Calculate interaction lengths and sampling fractions
def calculate_interaction_length(material, thickness_m):
    # Approximate interaction lengths in meters
    lambda_int = {
        'iron': 0.168,
        'steel': 0.167,
        'scintillator': 0.425
    }
    return thickness_m / lambda_int.get(material, 0.2)

def calculate_sampling_fraction(abs_thick, act_thick):
    return act_thick / (abs_thick + act_thick)

# Add calculated parameters to each configuration
for config in [config1, config2, config3]:
    params = config['geometry_parameters']
    abs_material = config['absorber_material']
    
    # Calculate total depth in interaction lengths
    layer_thickness = params['absorber_thickness'] + params['active_thickness']
    total_depth = layer_thickness * params['num_layers']
    interaction_lengths = calculate_interaction_length(abs_material, total_depth)
    
    # Calculate sampling fraction
    sampling_fraction = calculate_sampling_fraction(
        params['absorber_thickness'], 
        params['active_thickness']
    )
    
    config['calculated_parameters'] = {
        'total_depth_m': total_depth,
        'interaction_lengths': round(interaction_lengths, 1),
        'sampling_fraction': round(sampling_fraction, 3),
        'layer_thickness_m': layer_thickness
    }

# Create summary of all three configurations
configurations_summary = {
    'design_requirements': {
        'energy_range_gev': energy_range,
        'particle_types': particle_types,
        'performance_targets': {
            'energy_resolution': energy_resolution_target,
            'containment_efficiency': containment_efficiency_target,
            'response_linearity': response_linearity_target
        },
        'design_constraints': {
            'compact_design': True,
            'mid_energy_collider': True,
            'no_magnetic_field': True
        }
    },
    'configurations': {
        'config1': config1,
        'config2': config2,
        'config3': config3
    }
}

# Save configurations to JSON file
with open('calorimeter_configurations.json', 'w') as f:
    json.dump(configurations_summary, f, indent=2)

# Print summary for workflow
print('=== CALORIMETER DESIGN CONFIGURATIONS ===')
print(f'Designed {len(configurations_summary["configurations"])} configurations:')

for i, (key, config) in enumerate(configurations_summary['configurations'].items(), 1):
    print(f'\nConfiguration {i}: {config["name"]}')
    print(f'  Topology: {config["topology"]}')
    print(f'  Materials: {config["absorber_material"]} + {config["active_material"]}')
    print(f'  Layers: {config["geometry_parameters"]["num_layers"]}')
    print(f'  Sampling: {config["calculated_parameters"]["sampling_fraction"]}')
    print(f'  Depth: {config["calculated_parameters"]["interaction_lengths"]} λ_int')
    print(f'  Rationale: {config["design_rationale"]}')

# Output results for downstream steps
print('\nRESULT:num_configurations=3')
print('RESULT:config1_name=projective_tower_iron')
print('RESULT:config1_topology=projective_tower')
print(f'RESULT:config1_interaction_lengths={config1["calculated_parameters"]["interaction_lengths"]}')
print(f'RESULT:config1_sampling_fraction={config1["calculated_parameters"]["sampling_fraction"]}')

print('RESULT:config2_name=cylinder_barrel_steel')
print('RESULT:config2_topology=cylinder_barrel')
print(f'RESULT:config2_interaction_lengths={config2["calculated_parameters"]["interaction_lengths"]}')
print(f'RESULT:config2_sampling_fraction={config2["calculated_parameters"]["sampling_fraction"]}')

print('RESULT:config3_name=segmented_tile_iron')
print('RESULT:config3_topology=segmented')
print(f'RESULT:config3_interaction_lengths={config3["calculated_parameters"]["interaction_lengths"]}')
print(f'RESULT:config3_sampling_fraction={config3["calculated_parameters"]["sampling_fraction"]}')

print('\nConfigurations saved to: calorimeter_configurations.json')
print('SUCCESS: Three distinct calorimeter configurations designed with geometry parameters and material specifications')