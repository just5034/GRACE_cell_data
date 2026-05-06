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
import pandas as pd

# Define the three dense scintillating crystal materials with their properties
materials_data = {
    "CsI(Tl)": {
        "density_g_cm3": 4.51,
        "light_yield_photons_MeV": 54000,
        "radiation_length_cm": 1.86,
        "moliere_radius_cm": 3.5,
        "description": "Cesium Iodide with Thallium activator - highest light yield"
    },
    "PbWO4": {
        "density_g_cm3": 8.28,
        "light_yield_photons_MeV": 200,
        "radiation_length_cm": 0.89,
        "moliere_radius_cm": 2.0,
        "description": "Lead Tungstate - most compact, shortest radiation length"
    },
    "BGO": {
        "density_g_cm3": 7.13,
        "light_yield_photons_MeV": 8200,
        "radiation_length_cm": 1.12,
        "moliere_radius_cm": 2.3,
        "description": "Bismuth Germanate - intermediate properties"
    }
}

# Create comparison table
df = pd.DataFrame(materials_data).T
print("Dense Scintillating Crystal Materials Comparison:")
print("=" * 60)
print(df.to_string())
print("\n")

# Calculate derived properties for comparison
print("Material Trade-offs Analysis:")
print("-" * 40)
for material, props in materials_data.items():
    compactness = 1.0 / props["radiation_length_cm"]  # Higher = more compact
    light_per_density = props["light_yield_photons_MeV"] / props["density_g_cm3"]
    print(f"{material}:")
    print(f"  Compactness factor: {compactness:.3f} cm^-1")
    print(f"  Light yield per density: {light_per_density:.1f} photons/(MeV*g/cm3)")
    print(f"  {props['description']}")
    print()

# Save material properties to JSON for downstream use
with open('crystal_materials.json', 'w') as f:
    json.dump(materials_data, f, indent=2)

print("Material properties saved to crystal_materials.json")

# Output key results for workflow
print("RESULT:materials_defined=3")
print("RESULT:highest_light_yield_material=CsI(Tl)")
print("RESULT:most_compact_material=PbWO4")
print("RESULT:intermediate_material=BGO")
print("RESULT:csi_light_yield=54000")
print("RESULT:pbwo4_light_yield=200")
print("RESULT:bgo_light_yield=8200")
print("RESULT:csi_density=4.51")
print("RESULT:pbwo4_density=8.28")
print("RESULT:bgo_density=7.13")