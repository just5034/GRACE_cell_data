# Design and Optimization of Compact Hadronic Calorimeters for Mid-Energy Collider Experiments

## Abstract

This study presents the design and Monte Carlo simulation of compact hadronic calorimeters optimized for mid-energy collider experiments. Three distinct detector configurations were developed: a steel-scintillator sampling calorimeter with box geometry (1.26 m depth), a tungsten-scintillator barrel design (0.72 m depth), and a lead-scintillator projective tower system (1.37 m depth). Monte Carlo simulations using Geant4 were performed with π⁺ particles at energies of 10, 30, and 50 GeV to evaluate detector performance. The sampling calorimeter generated 1.77 billion hits across 30,000 events, while the projective tower configuration produced 1.87 billion hits. Due to technical implementation challenges, the tungsten barrel geometry could not be successfully simulated. The study demonstrates the computational intensity of hadronic shower simulations at mid-range energies, with hit rates scaling approximately linearly with beam energy. While complete performance metrics including energy resolution and shower containment were not computed during execution, the successful generation of extensive simulation datasets provides a foundation for future detailed analysis of calorimeter optimization for compact detector designs.

## Introduction

Hadronic calorimetry represents a critical component of modern particle physics detectors, particularly in collider experiments where accurate energy measurement of hadronic particles is essential for physics analyses. The challenge of designing compact calorimeters for mid-energy collider environments requires careful optimization of detector geometry, material selection, and readout segmentation to achieve optimal performance within spatial constraints.

The primary objectives of this investigation were to: (1) develop three distinct hadronic calorimeter configurations exploring different topological approaches and absorber materials, (2) evaluate their performance through Monte Carlo simulation across the energy range 10-50 GeV, and (3) assess key performance metrics including energy resolution, response linearity, and shower containment efficiency. The study was specifically constrained to mid-energy applications with a maximum energy of 50 GeV to balance physics requirements with computational tractability.

The motivation for this work stems from the need to optimize detector designs for next-generation collider experiments where space limitations and cost considerations demand compact yet high-performance calorimeter systems. Understanding the trade-offs between different absorber materials, geometrical configurations, and sampling strategies is crucial for informed detector design decisions.

## Methodology

The experimental approach employed Monte Carlo simulation using Geant4 for detailed modeling of hadronic shower development in three distinct calorimeter configurations. The methodology was designed to systematically explore different physics approaches: sampling calorimetry for proven performance, dense absorber materials for compactness, and projective tower geometry for collider optimization.

### Detector Configurations

Three calorimeter designs were developed with the following specifications:

**Configuration 1: Steel Box Compact (steel_box_compact)**
- Topology: Box geometry
- Absorber material: Steel (20 mm thickness)
- Active material: Plastic scintillator (4 mm thickness)
- Total depth: 1.26 m (7.5 interaction lengths)
- Number of layers: 52
- Sampling fraction: 0.167
- Transverse dimensions: 1.2 × 1.2 m

**Configuration 2: Tungsten Barrel Dense (tungsten_barrel_dense)**
- Topology: Cylindrical barrel
- Absorber material: Tungsten (5 mm thickness)
- Active material: Plastic scintillator (3 mm thickness)
- Total depth: 0.72 m (7.5 interaction lengths)
- Number of layers: 90
- Sampling fraction: 0.375
- Geometry: Inner radius 1.5 m, outer radius 2.22 m, half-length 2.5 m

**Configuration 3: Lead Tower Projective (lead_tower_projective)**
- Topology: Projective tower geometry
- Absorber material: Lead (15 mm thickness)
- Active material: Plastic scintillator (4 mm thickness)
- Total depth: 1.37 m (7.5 interaction lengths)
- Number of layers: 72
- Sampling fraction: 0.211
- Geometry: Inner radius 1.8 m, outer radius 3.17 m, half-length 3.0 m
- Tower segmentation: 48 × 64 (η × φ)

### Simulation Parameters

Monte Carlo simulations were performed using Geant4 with π⁺ particles as the probe beam. The energy sweep included three points: 10, 30, and 50 GeV, with 10,000 events simulated at each energy point for each successfully implemented configuration. The simplified experimental environment excluded magnetic fields to focus on calorimeter response characteristics.

GDML geometry files were generated for each configuration, with corresponding Geant4 macro files for simulation execution. The simulation framework captured detailed hit-level information including energy deposition patterns and spatial distributions throughout the detector volumes.

## Results

### Geometry Implementation Success

Of the three designed configurations, two were successfully implemented and simulated:

- **Steel box compact**: Successfully generated GDML geometry and simulation macros
- **Tungsten barrel dense**: Failed geometry implementation after multiple retry attempts due to recurring validation errors
- **Lead tower projective**: Successfully generated GDML geometry and simulation macros

### Simulation Statistics

**Steel Box Compact Calorimeter:**
- Total events simulated: 30,000 across three energy points
- Total hits generated: 1,769,877,873
- Total CPU time: 7,862.5 seconds
- Data volume: 102.8 GB

Energy-specific results:
- 10 GeV: 10,000 events, 186,808,375 hits, 10.9 GB data
- 30 GeV: 10,000 events, 588,671,256 hits, 34.2 GB data  
- 50 GeV: 10,000 events, 994,398,242 hits, 57.7 GB data

**Lead Tower Projective Calorimeter:**
- Total events simulated: 30,000 across three energy points
- Total hits generated: 1,873,010,474
- Total CPU time: 10,710.6 seconds
- Data volume: 109.0 GB

Energy-specific results:
- 10 GeV: 10,000 events, 197,534,006 hits, 11.6 GB data
- 30 GeV: 10,000 events, 622,848,288 hits, 36.3 GB data
- 50 GeV: 10,000 events, 1,052,628,180 hits, 61.2 GB data

### Computational Scaling

The hit generation rates demonstrated approximately linear scaling with beam energy for both successfully simulated configurations. The projective tower geometry consistently produced ~5-6% more hits than the box geometry at equivalent energies, likely due to its larger active volume and more complex segmentation structure.

### Performance Metrics

Energy resolution, response linearity, and shower containment metrics were not computed during execution. The simulation phase successfully generated extensive datasets containing detailed hit-level information, but the subsequent analysis steps required to extract these performance parameters were not completed.

## Discussion

### Configuration Comparison

The successful simulation of two distinct calorimeter topologies provides valuable insights into the computational requirements and practical implementation challenges of different design approaches. The steel box compact design, with its simpler geometry and moderate sampling fraction (0.167), demonstrated reliable simulation performance with manageable computational overhead.

The lead tower projective configuration, despite its more complex segmented geometry and higher sampling fraction (0.211), also achieved successful simulation completion. The slightly higher hit generation rate (5-6% increase) compared to the box geometry suggests more detailed shower sampling, which could potentially translate to improved energy resolution, though this metric was not computed during execution.

### Implementation Challenges

The failure to successfully implement the tungsten barrel dense configuration highlights the technical challenges associated with complex cylindrical geometries in GDML generation. Despite multiple retry attempts, recurring geometry validation errors prevented simulation execution for this design. This represents a significant limitation as the tungsten configuration offered the most compact design (0.72 m depth) due to tungsten's high density and short interaction length.

### Computational Considerations

The simulation results demonstrate the substantial computational requirements for detailed hadronic shower modeling. With nearly 2 billion hits generated per configuration and data volumes exceeding 100 GB, the study confirms the computational intensity anticipated for hadronic calorimetry simulations at mid-range energies. The approximately linear scaling of hit rates with energy (factor of ~5.3 increase from 10 to 50 GeV for both configurations) provides useful guidance for future simulation planning.

### Limitations

Several important limitations must be acknowledged:

1. **Incomplete Analysis**: Performance metrics including energy resolution (σ_E/E), response linearity, and shower containment efficiency were not computed during execution, preventing quantitative performance comparison between configurations.

2. **Reduced Configuration Set**: The failure to implement the tungsten barrel geometry reduced the study from three to two configurations, limiting the scope of design optimization insights.

3. **Simplified Environment**: The absence of magnetic fields and other realistic experimental conditions may not fully represent actual collider detector performance.

4. **Limited Energy Range**: The 50 GeV maximum energy constraint, while computationally necessary, may not capture the full performance characteristics relevant to some collider applications.

## Conclusions

This study successfully demonstrated the design and Monte Carlo simulation of compact hadronic calorimeters for mid-energy collider applications. Two of three proposed configurations were successfully implemented and simulated, generating extensive datasets containing detailed shower development information across the 10-50 GeV energy range.

Key achievements include:

- Development of three distinct calorimeter design concepts optimized for compactness
- Successful GDML geometry generation and Geant4 simulation for sampling and projective tower configurations
- Generation of comprehensive simulation datasets totaling over 3.6 billion detector hits
- Demonstration of computational scaling relationships for hadronic shower simulations

The study establishes a foundation for detailed calorimeter performance analysis, though the extraction of key performance metrics remains as future work. The successful simulation datasets provide the necessary input for subsequent analysis of energy resolution, linearity, and shower containment characteristics.

Future work should focus on: (1) completing the performance metric analysis using the generated simulation data, (2) resolving the geometry implementation issues for the tungsten barrel configuration, (3) extending the energy range to higher values with optimized computational strategies, and (4) incorporating realistic experimental conditions including magnetic fields and detector integration constraints.

The results demonstrate both the potential and challenges of Monte Carlo-based calorimeter optimization, providing valuable guidance for future detector design efforts in the mid-energy collider regime.

## AI Performance Analysis

The AI agent execution demonstrated mixed success in achieving the stated objectives. Strengths included successful design conceptualization of three distinct calorimeter configurations with appropriate material choices and geometric parameters, successful GDML geometry generation for two configurations, and completion of computationally intensive Monte Carlo simulations generating extensive datasets.

However, significant limitations were evident in the execution. The failure to implement one of three planned configurations (tungsten barrel) due to recurring geometry validation errors reduced the scope of the comparative study. Most critically, the analysis phase was not completed, leaving key performance metrics (energy resolution, response linearity, shower containment) uncomputed despite this being a primary objective.

The workflow planning appeared appropriate for the task scope, but execution bottlenecks in geometry generation and the absence of analysis steps prevented full objective completion. The agent successfully handled the substantial computational requirements of hadronic shower simulation but failed to extract the physics insights that would enable meaningful calorimeter optimization.

Overall, the execution achieved approximately 60% of the intended objectives, successfully generating valuable simulation datasets but falling short of the complete performance characterization required for informed detector design decisions.