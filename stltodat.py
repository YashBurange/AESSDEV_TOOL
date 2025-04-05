#converts .stl to .dat files

import trimesh
import numpy as np

# Load STL file
mesh = trimesh.load_mesh("s1223-airfoil-wing-1.snapshot.6/Product1_AllCATPart.stl")

# Define a slicing plane (YZ plane at mid-span)
plane_origin = [0.5, 0, 0]  # Mid-span along x-axis
plane_normal = [1, 0, 0]    # Normal to the x-axis

# Perform slicing
slice_2D = mesh.section(plane_origin=plane_origin, plane_normal=plane_normal)

# Ensure the sectioning returned a valid object
if slice_2D is None:
    raise ValueError("Sectioning failed. Check the plane position and normal.")

# Convert the section to a set of 2D points
# slice_2D contains multiple paths, we take the first path if multiple exist
polygons = slice_2D.to_2D()
points_2D = np.array(polygons[0].vertices)  # Extract only YZ coordinates

# Sort points along chord direction (Y-axis)
points_2D = points_2D[np.argsort(points_2D[:, 0])]

# Save as .dat file
np.savetxt("airfoil.dat", points_2D, fmt="%.6f", header="Extracted Airfoil Section")

print("Conversion completed! Saved as airfoil.dat")
