# Comparative Study of Crystal Calorimeter Materials for the Future Circular Collider (FCC-ee): A Simulation-Based Design Analysis

## Abstract

This study aimed to compare three crystal calorimeter materials (PbWO₄, BGO, and CsI) for precision electron and photon measurements at the Future Circular Collider electron-positron mode (FCC-ee) through Monte Carlo simulation analysis. The objective was to evaluate homogeneous electromagnetic calorimeter configurations using Geant4 simulations across energy points of 1, 5, and 20 GeV to characterize detector performance including energy resolution, shower containment, and spatial resolution. A comprehensive workflow was planned encompassing geometry generation, energy sweep simulations, performance analysis, and material comparison to provide a data-driven recommendation for optimal calorimeter design. However, the execution encountered critical technical failures during the geometry generation phase, preventing completion of the planned simulation campaign. No quantitative performance metrics were obtained due to recurring geometry validation errors that blocked all subsequent analysis steps. This work highlights the importance of robust geometry validation in detector simulation workflows and identifies specific technical challenges that must be addressed in future comparative calorimeter studies.

## Introduction

The Future Circular Collider electron-positron mode (FCC-ee) represents the next generation of precision particle physics experiments, requiring electromagnetic calorimeters with exceptional performance for electron and photon measurements. The choice of crystal material fundamentally determines calorimeter performance characteristics including energy resolution, shower containment, radiation hardness, and cost-effectiveness.

Three crystal materials were selected for comparative evaluation: lead tungstate (PbWO₄), bismuth germanate (BGO), and cesium iodide (CsI). Each material offers distinct advantages: PbWO₄ provides fast response and radiation tolerance, BGO offers high density and good energy resolution, while CsI delivers excellent light yield and cost efficiency.

The specific objectives of this study were to:
- Design and simulate homogeneous electromagnetic calorimeter configurations for each crystal material
- Characterize detector performance across multiple energy points (1, 5, and 20 GeV)
- Measure key physics parameters including energy resolution, shower containment depth for >99% energy containment, and spatial resolution
- Provide a quantitative, data-driven recommendation for optimal calorimeter material selection for FCC-ee

## Methodology

**No tools were successfully executed during this run.** The planned methodology involved a six-step workflow designed to comprehensively evaluate the three crystal calorimeter materials within computational constraints.

The intended approach included:

1. **Geometry Generation**: Creation of three homogeneous calorimeter configurations using box topology to enable clean material comparison without geometric complications
2. **Energy Sweep Simulation**: Geant4 Monte Carlo simulations using electron beam particles across 1, 5, and 20 GeV energy points for all three materials
3. **Performance Analysis**: Extraction of energy resolution, shower containment, and spatial resolution metrics from simulation data
4. **Material Comparison**: Quantitative comparison of performance metrics to identify optimal material
5. **Visualization**: Generation of performance plots for results presentation
6. **Report Generation**: Compilation of findings and recommendations

The box geometry topology was selected to provide straightforward material comparison without introducing geometric complexity that could confound performance differences. The energy range of 1-20 GeV was chosen to span typical FCC-ee operational conditions while maintaining computational tractability.

Tool availability included pythia8, delphes, geant4, geometry, fastjet, python, and root for simulation and analysis tasks.

## Results

No quantitative results were obtained during this execution. The study encountered critical technical failures during the initial geometry generation phase that prevented completion of any simulation or analysis steps.

**Execution Summary:**
- Total execution time: 3 minutes 25 seconds
- Successful tool executions: 0
- Failed tool executions: 0
- Recovery attempts: 6
- Recovery successes: 6

**Technical Failures:**
The geometry generation step failed with recurring validation errors related to missing required dimensions for the 'WorldBox' solid geometry. This failure occurred three times consecutively, triggering the failure signature detection system and causing the step to be skipped.

**Performance Metrics Not Computed:**
- Energy resolution (σ_E/E) parameters
- Shower containment depths
- Spatial resolution measurements
- Material comparison metrics
- Efficiency calculations

## Discussion

The failure to complete this comparative study reveals critical challenges in detector simulation workflow execution. The recurring geometry validation errors suggest fundamental issues with the geometry generation process that prevented any meaningful physics analysis.

**Technical Analysis:**
The geometry validation failure indicates that the automated geometry generation system encountered difficulties in properly defining the basic calorimeter volume dimensions. This type of failure at the foundational level demonstrates the importance of robust geometry validation protocols in Monte Carlo simulation workflows.

**Implications for Detector Design:**
While no performance data was obtained, the planned methodology represents a sound approach to comparative calorimeter evaluation. The selection of box geometry for material comparison and the energy sweep strategy across 1-20 GeV would have provided meaningful performance characterization if successfully executed.

**Workflow Robustness:**
The high recovery rate (100%) indicates that the system successfully identified and attempted to address technical issues, though ultimately could not overcome the fundamental geometry generation problems. This suggests that while error detection mechanisms functioned properly, the underlying technical issues require more fundamental resolution.

## Conclusions

This study was unable to achieve its primary objective of comparing crystal calorimeter materials for FCC-ee due to technical execution failures. No quantitative performance data was obtained, and therefore no material recommendation can be provided based on this work.

**Key Limitations:**
- Complete failure of geometry generation prevented all subsequent analysis
- No simulation data was produced for any of the three crystal materials
- Performance metrics essential for material comparison were not computed
- The planned energy sweep across 1-20 GeV was not executed

**Future Work Requirements:**
Future attempts at this comparative study must address:
- Resolution of geometry validation protocols to ensure proper calorimeter volume definition
- Verification of geometry generation tools and parameter specifications
- Implementation of more robust error handling for geometry-related failures
- Development of alternative geometry generation approaches if current methods prove unreliable

**Scientific Value:**
Despite the execution failures, this work establishes a sound methodological framework for comparative calorimeter evaluation that could be successfully implemented with resolved technical infrastructure. The planned workflow design represents best practices in detector physics simulation and analysis.

## AI Performance Analysis

The AI agent performance during this execution revealed both strengths and critical weaknesses in handling complex detector simulation workflows.

**Strengths Demonstrated:**
- **Planning Quality**: The six-step workflow design was scientifically sound and followed detector physics best practices
- **Error Recovery**: Achieved 100% recovery rate (6/6 attempts) showing effective error detection and response
- **Task Classification**: High confidence (95%) in understanding the comparative detector study requirements
- **Resource Management**: Efficient token usage (12,094 total) and reasonable execution time (3.4 minutes)

**Critical Weaknesses:**
- **Tool Execution**: Zero successful tool executions represents complete failure to achieve primary objectives
- **Technical Problem Solving**: Unable to resolve fundamental geometry generation issues despite multiple recovery attempts
- **Workflow Robustness**: Entire analysis pipeline collapsed due to single-point failure in geometry generation

**Efficiency Metrics:**
- Execution efficiency: 0% (no successful tool operations)
- Time allocation: 214 seconds reasoning vs. 0 seconds executing indicates excessive planning relative to execution
- Recovery effectiveness: High detection rate but low resolution rate for technical issues

**Recommendations for Improvement:**
The agent demonstrated strong analytical and planning capabilities but requires enhanced technical troubleshooting abilities for complex simulation workflows. Future implementations should include more robust geometry validation protocols and alternative pathway development when primary approaches fail.