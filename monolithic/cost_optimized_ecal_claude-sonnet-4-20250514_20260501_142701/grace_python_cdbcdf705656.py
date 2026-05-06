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

# Input data
target_depth_x0 = 20
configurations = ['premium_pbwo4', 'midrange_pb_scint', 'budget_fe_scint']

# Material properties
materials = {
    'pbwo4': {'density': 8.28, 'x0': 0.89, 'cost_per_kg': 3000},
    'lead': {'density': 11.35, 'x0': 0.56, 'cost_per_kg': 2},
    'iron': {'density': 7.87, 'x0': 1.76, 'cost_per_kg': 1},
    'plastic_scintillator': {'density': 1.032, 'cost_per_kg': 20}
}

# Assume 1m x 1m transverse area for calculations
transverse_area_m2 = 1.0

results = {}

# Configuration 1: Premium PbWO4 homogeneous
print('Calculating Premium PbWO4 configuration...')
pbwo4 = materials['pbwo4']
depth_pbwo4_cm = target_depth_x0 * pbwo4['x0']
volume_pbwo4_m3 = transverse_area_m2 * (depth_pbwo4_cm / 100)
mass_pbwo4_kg = volume_pbwo4_m3 * pbwo4['density'] * 1000
cost_pbwo4 = mass_pbwo4_kg * pbwo4['cost_per_kg']

results['premium_pbwo4'] = {
    'depth_cm': depth_pbwo4_cm,
    'depth_m': depth_pbwo4_cm / 100,
    'mass_kg': mass_pbwo4_kg,
    'cost_usd': cost_pbwo4,
    'material': 'PbWO4',
    'type': 'homogeneous'
}

# Configuration 2: Mid-range Pb+scintillator sampling
print('Calculating Mid-range Pb+scintillator configuration...')
lead = materials['lead']
scint = materials['plastic_scintillator']

# Optimize sampling ratio for Pb+scintillator
# Typical sampling: 2mm Pb + 4mm scintillator per layer
absorber_thickness_mm = 2.0
active_thickness_mm = 4.0
layer_thickness_mm = absorber_thickness_mm + active_thickness_mm
layer_x0 = (absorber_thickness_mm / 10) / lead['x0'] + (active_thickness_mm / 10) / 20.0  # Approx scint X0

num_layers = math.ceil(target_depth_x0 / layer_x0)
total_depth_cm = num_layers * layer_thickness_mm / 10

# Calculate masses
absorber_volume_m3 = transverse_area_m2 * num_layers * (absorber_thickness_mm / 1000)
active_volume_m3 = transverse_area_m2 * num_layers * (active_thickness_mm / 1000)

absorber_mass_kg = absorber_volume_m3 * lead['density'] * 1000
active_mass_kg = active_volume_m3 * scint['density'] * 1000
total_mass_kg = absorber_mass_kg + active_mass_kg

cost_pb_scint = absorber_mass_kg * lead['cost_per_kg'] + active_mass_kg * scint['cost_per_kg']

results['midrange_pb_scint'] = {
    'depth_cm': total_depth_cm,
    'depth_m': total_depth_cm / 100,
    'num_layers': num_layers,
    'absorber_thickness_mm': absorber_thickness_mm,
    'active_thickness_mm': active_thickness_mm,
    'mass_kg': total_mass_kg,
    'cost_usd': cost_pb_scint,
    'absorber_material': 'lead',
    'active_material': 'plastic_scintillator',
    'type': 'sampling'
}

# Configuration 3: Budget Fe+scintillator sampling
print('Calculating Budget Fe+scintillator configuration...')
iron = materials['iron']

# Optimize for Fe+scintillator: thicker absorber needed
absorber_thickness_fe_mm = 5.0
active_thickness_fe_mm = 3.0
layer_thickness_fe_mm = absorber_thickness_fe_mm + active_thickness_fe_mm
layer_x0_fe = (absorber_thickness_fe_mm / 10) / iron['x0'] + (active_thickness_fe_mm / 10) / 20.0

num_layers_fe = math.ceil(target_depth_x0 / layer_x0_fe)
total_depth_fe_cm = num_layers_fe * layer_thickness_fe_mm / 10

# Calculate masses
absorber_volume_fe_m3 = transverse_area_m2 * num_layers_fe * (absorber_thickness_fe_mm / 1000)
active_volume_fe_m3 = transverse_area_m2 * num_layers_fe * (active_thickness_fe_mm / 1000)

absorber_mass_fe_kg = absorber_volume_fe_m3 * iron['density'] * 1000
active_mass_fe_kg = active_volume_fe_m3 * scint['density'] * 1000
total_mass_fe_kg = absorber_mass_fe_kg + active_mass_fe_kg

cost_fe_scint = absorber_mass_fe_kg * iron['cost_per_kg'] + active_mass_fe_kg * scint['cost_per_kg']

results['budget_fe_scint'] = {
    'depth_cm': total_depth_fe_cm,
    'depth_m': total_depth_fe_cm / 100,
    'num_layers': num_layers_fe,
    'absorber_thickness_mm': absorber_thickness_fe_mm,
    'active_thickness_mm': active_thickness_fe_mm,
    'mass_kg': total_mass_fe_kg,
    'cost_usd': cost_fe_scint,
    'absorber_material': 'iron',
    'active_material': 'plastic_scintillator',
    'type': 'sampling'
}

# Print results
print('\n=== CALORIMETER CONFIGURATION RESULTS ===')
for config_name, config in results.items():
    print(f'\n{config_name.upper()}:')
    print(f'  Depth: {config["depth_cm"]:.2f} cm ({config["depth_m"]:.3f} m)')
    print(f'  Mass: {config["mass_kg"]:.1f} kg')
    print(f'  Cost: ${config["cost_usd"]:,.0f}')
    if config['type'] == 'sampling':
        print(f'  Layers: {config["num_layers"]}')
        print(f'  Absorber: {config["absorber_thickness_mm"]}mm {config["absorber_material"]}')
        print(f'  Active: {config["active_thickness_mm"]}mm {config["active_material"]}')

# Save results to JSON
with open('calorimeter_configurations.json', 'w') as f:
    json.dump(results, f, indent=2)

# Output key metrics for downstream steps
print(f'\nRESULT:pbwo4_depth_cm={results["premium_pbwo4"]["depth_cm"]:.2f}')
print(f'RESULT:pbwo4_mass_kg={results["premium_pbwo4"]["mass_kg"]:.1f}')
print(f'RESULT:pbwo4_cost_usd={results["premium_pbwo4"]["cost_usd"]:.0f}')

print(f'RESULT:pb_scint_depth_cm={results["midrange_pb_scint"]["depth_cm"]:.2f}')
print(f'RESULT:pb_scint_layers={results["midrange_pb_scint"]["num_layers"]}')
print(f'RESULT:pb_scint_mass_kg={results["midrange_pb_scint"]["mass_kg"]:.1f}')
print(f'RESULT:pb_scint_cost_usd={results["midrange_pb_scint"]["cost_usd"]:.0f}')

print(f'RESULT:fe_scint_depth_cm={results["budget_fe_scint"]["depth_cm"]:.2f}')
print(f'RESULT:fe_scint_layers={results["budget_fe_scint"]["num_layers"]}')
print(f'RESULT:fe_scint_mass_kg={results["budget_fe_scint"]["mass_kg"]:.1f}')
print(f'RESULT:fe_scint_cost_usd={results["budget_fe_scint"]["cost_usd"]:.0f}')

print('\nConfiguration design completed successfully!')