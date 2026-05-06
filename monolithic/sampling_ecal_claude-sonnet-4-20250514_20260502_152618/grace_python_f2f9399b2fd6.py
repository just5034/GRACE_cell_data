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

# Input parameters
target_depth_x0 = 25
tungsten_x0_cm = 0.35

configurations = [
    {
        "name": "thin_absorber",
        "w_thickness_mm": 2,
        "scint_thickness_mm": 5
    },
    {
        "name": "balanced",
        "w_thickness_mm": 3.5,
        "scint_thickness_mm": 3.5
    },
    {
        "name": "thick_absorber",
        "w_thickness_mm": 5,
        "scint_thickness_mm": 2
    }
]

results = []

print("Calculating layer configurations for tungsten-scintillator calorimeter")
print(f"Target depth: {target_depth_x0} X₀")
print(f"Tungsten X₀: {tungsten_x0_cm} cm")
print("\n" + "="*60)

for config in configurations:
    name = config["name"]
    w_thickness_mm = config["w_thickness_mm"]
    scint_thickness_mm = config["scint_thickness_mm"]
    
    # Convert mm to cm
    w_thickness_cm = w_thickness_mm / 10.0
    scint_thickness_cm = scint_thickness_mm / 10.0
    
    # Calculate X₀ per tungsten layer
    x0_per_layer = w_thickness_cm / tungsten_x0_cm
    
    # Calculate number of layers needed
    num_layers = math.ceil(target_depth_x0 / x0_per_layer)
    
    # Calculate actual total X₀ achieved
    actual_x0 = num_layers * x0_per_layer
    
    # Calculate layer thickness (absorber + active)
    layer_thickness_cm = w_thickness_cm + scint_thickness_cm
    
    # Calculate sampling fraction (active material thickness / total layer thickness)
    sampling_fraction = scint_thickness_cm / layer_thickness_cm
    
    # Calculate total detector depth
    total_depth_cm = num_layers * layer_thickness_cm
    
    config_result = {
        "name": name,
        "w_thickness_mm": w_thickness_mm,
        "w_thickness_cm": w_thickness_cm,
        "scint_thickness_mm": scint_thickness_mm,
        "scint_thickness_cm": scint_thickness_cm,
        "x0_per_layer": x0_per_layer,
        "num_layers": num_layers,
        "actual_x0": actual_x0,
        "sampling_fraction": sampling_fraction,
        "layer_thickness_cm": layer_thickness_cm,
        "total_depth_cm": total_depth_cm
    }
    
    results.append(config_result)
    
    print(f"\nConfiguration: {name}")
    print(f"  Tungsten thickness: {w_thickness_mm} mm ({w_thickness_cm} cm)")
    print(f"  Scintillator thickness: {scint_thickness_mm} mm ({scint_thickness_cm} cm)")
    print(f"  X₀ per layer: {x0_per_layer:.3f}")
    print(f"  Number of layers needed: {num_layers}")
    print(f"  Actual X₀ achieved: {actual_x0:.2f}")
    print(f"  Sampling fraction: {sampling_fraction:.3f} ({sampling_fraction*100:.1f}%)")
    print(f"  Layer thickness: {layer_thickness_cm} cm")
    print(f"  Total detector depth: {total_depth_cm:.1f} cm")

# Save results to JSON file
with open('calorimeter_configurations.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "="*60)
print("Summary of all configurations:")
for result in results:
    print(f"{result['name']}: {result['num_layers']} layers, {result['sampling_fraction']:.3f} sampling fraction")

# Output results for next workflow step
for result in results:
    name = result['name']
    print(f"RESULT:{name}_num_layers={result['num_layers']}")
    print(f"RESULT:{name}_sampling_fraction={result['sampling_fraction']:.4f}")
    print(f"RESULT:{name}_actual_x0={result['actual_x0']:.2f}")
    print(f"RESULT:{name}_total_depth_cm={result['total_depth_cm']:.1f}")
    print(f"RESULT:{name}_w_thickness_cm={result['w_thickness_cm']:.2f}")
    print(f"RESULT:{name}_scint_thickness_cm={result['scint_thickness_cm']:.2f}")

print("\nConfiguration calculations completed successfully!")