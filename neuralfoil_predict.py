import neuralfoil as nf
aero = nf.get_aero_from_dat_file("airfoil.dat", alpha=5, Re=1e6)
print(f"CL: {aero['CL']}, CD: {aero['CD']}, CM: {aero['CM']}")