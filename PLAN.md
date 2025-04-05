# Project Plan: Automated Wing Aerodynamics Simulation

## Overall Goal

Automate the process of evaluating the aerodynamic performance (Lift-to-Drag ratio) of an aircraft wing across various Angles of Attack (AoA) using FreeCAD for CAD preprocessing and SPHinXsys for fluid simulation.

---

## Part 1: FreeCAD Pre-processing Script (`preprocess_wing.py`)

### Goal
Programmatically load a wing geometry from a `.STEP` file, clean it, and export it as an `.STL` file suitable for SPHinXsys.

### Steps
1.  **Setup:** Configure Python environment with FreeCAD scripting capabilities.
2.  **Load:** Implement script to load a specified `.STEP` file.
3.  **Clean (Optional but Recommended):** Add functions to perform basic geometry checks or cleaning operations (e.g., fuse parts, remove small features if necessary). This might need manual tuning based on typical input models.
4.  **Tessellate & Export:** Convert the cleaned FreeCAD geometry object into a mesh and export it as an `.STL` file with appropriate resolution settings.
5.  **Parameterization:** Allow passing input `.STEP` file path, output `.STL` file path, and mesh resolution as arguments.

### Testing
-   Run the script with a sample `.STEP` file.
-   Visually inspect the output `.STL` file in a mesh viewer (like MeshLab or ParaView) to ensure the geometry is correct and the tessellation is appropriate.
-   Test with different `.STEP` files if available.

---

## Part 2: C++ SPH Simulation Program (`wing_simulation`)

### Goal
Read the `.STL` wing geometry, set up and run SPHinXsys fluid simulations for a range of AoAs, compute aerodynamic forces, and output Cl/Cd values.

### Steps
1.  **Project Setup:**
    *   Create directory structure (`src`, `geometry`, `results`, etc.).
    *   Set up `CMakeLists.txt` to build the C++ executable, linking SPHinXsys, TBB, and any other required libraries.
2.  **Geometry & Particle Generation:**
    *   Implement code to read the `.STL` file generated in Part 1.
    *   Use SPHinXsys utilities to generate SPH particles based on the `.STL` geometry.
3.  **Simulation Case Definition:**
    *   Define fluid properties (density, viscosity).
    *   Define the computational domain (bounding box).
    *   Implement boundary conditions (inflow, outflow, far-field, wall).
    *   **Crucially:** Parameterize inflow velocity/boundary conditions based on the desired Angle of Attack (AoA). This might involve rotating the geometry or adjusting the inflow vector components.
4.  **AoA Iteration Loop:**
    *   Create a loop that iterates through a predefined list or range of AoAs.
    *   Inside the loop:
        *   Adjust the simulation setup for the current AoA.
        *   Initialize/Re-initialize the SPH system.
        *   Run the SPHinXsys simulation for the current AoA.
        *   Use SPHinXsys force observers/methods to extract Lift (L) and Drag (D) forces acting on the wing body.
        *   Calculate Cl/Cd (requires reference area and dynamic pressure).
        *   Store the AoA and corresponding Cl/Cd.
5.  **Output:**
    *   Write the collected AoA vs. Cl/Cd data to a file (e.g., CSV).
    *   Implement basic logging for simulation progress and potential errors.

### Testing
-   **Component Testing:**
    *   Test `.STL` reading and particle generation separately. Ensure particles correctly represent the wing shape.
    *   Test simulation setup for a *single, fixed* AoA (e.g., 0 degrees). Run a short simulation and check if it initializes and runs without crashing. Use ParaView to visualize initial particles and boundary setup if possible.
    *   Test force extraction for the single AoA simulation. Check if the reported force values are physically plausible (even if not accurate yet).
-   **Integration Testing:**
    *   Run the full loop with a small range of AoAs (e.g., 0, 2, 4 degrees).
    *   Verify that the output CSV file is generated correctly and contains the expected data points.
    *   Monitor simulation stability across different AoAs.

---

## Integration

1.  Run the FreeCAD script (`preprocess_wing.py`) to generate the `.STL` file from the source `.STEP` file.
2.  Run the compiled C++ `wing_simulation` executable, providing the path to the generated `.STL` file and any other necessary parameters (like the AoA range).
3.  Analyze the final Cl/Cd vs. AoA results from the output file.

--- 