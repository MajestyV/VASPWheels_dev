# Set up some imports that we will need
# from IPython.display import Image, display
from pymatgen.analysis.diffraction.xrd import XRDCalculator
from pymatgen.core import Lattice, Structure

# %matplotlib inline

# Create CsCl structure
a = 4.209  # Angstrom
latt = Lattice.cubic(a)
structure = Structure(latt, ["Cs", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])

c = XRDCalculator()
c.show_plot(structure)