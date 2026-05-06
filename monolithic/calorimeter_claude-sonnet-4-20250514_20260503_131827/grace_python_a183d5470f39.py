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

# Design three hadronic calorimeter configurations
# Based on physics constraints for pi+ hadrons at 10-50 GeV

# Nuclear interaction lengths for common absorber materials (cm)
nuclear_lengths = {
    'steel': 16.8,
    'iron': 16.8, 
    'lead': 18.3,
    'tungsten': 9.6,
    'copper': 15.1,
    'brass': 15.2
}

# Design parameters for 95% containment
target_containment = 0.95
max_energy = 50  # GeV

# Calculate required depth for 95% containment (typically 7-8 lambda)
containment_lambdas = 7.5

configurations = []

# Configuration 1: Box topology with steel absorber (compact, cost-effective)
config1 = {
    'name': 'steel_box_compact',
    'topology': 'box',
    'absorber_material': 'steel',
    'active_material': 'plastic_scintillator',
    'description': 'Compact planar sampling calorimeter with steel absorber'
}

# Calculate dimensions for steel
steel_lambda = nuclear_lengths['steel'] / 100  # Convert cm to m
config1['total_depth_m'] = containment_lambdas * steel_lambda
config1['absorber_thickness_mm'] = 20  # 20mm steel plates
config1['active_thickness_mm'] = 4   # 4mm scintillator
config1['num_layers'] = int(config1['total_depth_m'] * 1000 / (config1['absorber_thickness_mm'] + config1['active_thickness_mm']))
config1['transverse_size_m'] = 1.2  # 1.2m x 1.2m face
config1['sampling_fraction'] = config1['active_thickness_mm'] / (config1['absorber_thickness_mm'] + config1['active_thickness_mm'])

configurations.append(config1)

# Configuration 2: Cylindrical barrel with tungsten (high density, compact)
config2 = {
    'name': 'tungsten_barrel_dense',
    'topology': 'cylinder_barrel', 
    'absorber_material': 'tungsten',
    'active_material': 'plastic_scintillator',
    'description': 'Dense cylindrical barrel calorimeter with tungsten absorber'
}

# Calculate dimensions for tungsten
tungsten_lambda = nuclear_lengths['tungsten'] / 100
config2['total_depth_m'] = containment_lambdas * tungsten_lambda
config2['absorber_thickness_mm'] = 5   # Thinner tungsten plates
config2['active_thickness_mm'] = 3     # 3mm scintillator
config2['num_layers'] = int(config2['total_depth_m'] * 1000 / (config2['absorber_thickness_mm'] + config2['active_thickness_mm']))
config2['inner_radius_m'] = 1.5        # 1.5m inner radius
config2['outer_radius_m'] = config2['inner_radius_m'] + config2['total_depth_m']
config2['half_length_m'] = 2.5         # 5m total length
config2['sampling_fraction'] = config2['active_thickness_mm'] / (config2['absorber_thickness_mm'] + config2['active_thickness_mm'])

configurations.append(config2)

# Configuration 3: Projective tower with lead (segmented readout)
config3 = {
    'name': 'lead_tower_projective',
    'topology': 'projective_tower',
    'absorber_material': 'lead', 
    'active_material': 'plastic_scintillator',
    'description': 'Projective tower calorimeter with lead absorber and segmented readout'
}

# Calculate dimensions for lead
lead_lambda = nuclear_lengths['lead'] / 100
config3['total_depth_m'] = containment_lambdas * lead_lambda
config3['absorber_thickness_mm'] = 15  # 15mm lead plates
config3['active_thickness_mm'] = 4     # 4mm scintillator
config3['num_layers'] = int(config3['total_depth_m'] * 1000 / (config3['absorber_thickness_mm'] + config3['active_thickness_mm']))
config3['inner_radius_m'] = 1.8        # 1.8m inner radius
config3['outer_radius_m'] = config3['inner_radius_m'] + config3['total_depth_m']
config3['half_length_m'] = 3.0         # 6m total length
config3['tower_eta_segments'] = 48     # Segmentation in eta
config3['tower_phi_segments'] = 64     # Segmentation in phi
config3['eta_coverage'] = 2.4          # |eta| < 2.4
config3['sampling_fraction'] = config3['active_thickness_mm'] / (config3['absorber_thickness_mm'] + config3['active_thickness_mm'])

configurations.append(config3)

# Print configuration summary
print('=== HADRONIC CALORIMETER CONFIGURATIONS ===')
for i, config in enumerate(configurations, 1):
    print(f'\nConfiguration {i}: {config["name"]}')
    print(f'  Topology: {config["topology"]}')
    print(f'  Absorber: {config["absorber_material"]}')
    print(f'  Active: {config["active_material"]}')
    print(f'  Total depth: {config["total_depth_m"]:.2f} m ({containment_lambdas} lambda)')
    print(f'  Absorber thickness: {config["absorber_thickness_mm"]} mm')
    print(f'  Active thickness: {config["active_thickness_mm"]} mm')
    print(f'  Number of layers: {config["num_layers"]}')
    print(f'  Sampling fraction: {config["sampling_fraction"]:.3f}')
    
    if config['topology'] == 'box':
        print(f'  Transverse size: {config["transverse_size_m"]} x {config["transverse_size_m"]} m')
    elif config['topology'] in ['cylinder_barrel', 'projective_tower']:
        print(f'  Inner radius: {config["inner_radius_m"]} m')
        print(f'  Outer radius: {config["outer_radius_m"]:.2f} m')
        print(f'  Half length: {config["half_length_m"]} m')
        if config['topology'] == 'projective_tower':
            print(f'  Tower segmentation: {config["tower_eta_segments"]} x {config["tower_phi_segments"]} (eta x phi)')

# Save configurations to JSON
with open('calorimeter_configurations.json', 'w') as f:
    json.dump(configurations, f, indent=2)

# Output results for workflow
print(f'\nRESULT:num_configurations={len(configurations)}')
print(f'RESULT:config1_name={config1["name"]}')
print(f'RESULT:config1_topology={config1["topology"]}')
print(f'RESULT:config1_absorber={config1["absorber_material"]}')
print(f'RESULT:config1_depth_m={config1["total_depth_m"]:.3f}')
print(f'RESULT:config2_name={config2["name"]}')
print(f'RESULT:config2_topology={config2["topology"]}')
print(f'RESULT:config2_absorber={config2["absorber_material"]}')
print(f'RESULT:config2_depth_m={config2["total_depth_m"]:.3f}')
print(f'RESULT:config3_name={config3["name"]}')
print(f'RESULT:config3_topology={config3["topology"]}')
print(f'RESULT:config3_absorber={config3["absorber_material"]}')
print(f'RESULT:config3_depth_m={config3["total_depth_m"]:.3f}')

print('\nDesign complete: Three distinct calorimeter configurations defined')
print('Next step: Generate GDML geometries for each configuration')