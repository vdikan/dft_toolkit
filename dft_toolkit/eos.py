"""Murnaghan equation of state (energy as a function of volume).
From PRB 28,5480 (1983).

Thank you Javier Junquera,
https://personales.unican.es/junqueraj/siesta-tutorial.html

"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit


# Volume factors for each lattice type
factor = {
    'cubic': 1.,
    'bcc': 1./2.,
    'fcc': 1./4.,
    'diamond': 1./4.
}

def eos_murnaghan(vol, E0, B0, BP, V0):
    """Murnaghan equation of state (energy as a function of volume).
    From PRB 28,5480 (1983)."""
    return E0 + B0 * vol / BP * (((V0 / vol) ** BP) / (BP - 1) + 1) - V0 * B0 / (BP - 1)


def read_data(filename):
    """Function that reads the results from a data file and returns the
    lattice type and the volume and energy vectors as numpy arrays."""
    # Read the first word at the first line
    with open(filename, 'r', encoding="utf-8") as infile:
        lattice = infile.readline().split()[0]

    # Read volume and energy results
    data = np.loadtxt(filename, skiprows=1)

    return lattice, factor[lattice] * data[:, 0] ** 3, data[:, 1]


def fit_murnaghan(volume, energy):
    """Function that fits the results to a Murnaghan EOS."""
    # Fit a parabola for initial parameter guess
    p_coefs = np.polyfit(volume, energy, 2)
    # Minimum of the parabola dE/dV = 0 ( p_coefs = [c, b, a] )
    p_min = -p_coefs[1] / (2. * p_coefs[0])
    # Warn if the minimum volume is not in the result range
    if (p_min < volume.min() or p_min > volume.max()):
        print("Warning: minimum volume not in the range of results")
    # Groundstate energy estimation from parabola minimum
    E0 = np.polyval(p_coefs, p_min)
    # Bulk modulus estimation
    B0 = 2. * p_coefs[2] * p_min

    # Initial parameters (BP is usually small)
    init_par = [E0, B0, 4, p_min]
    best_par, cov_matrix = curve_fit(eos_murnaghan, volume, energy, p0=init_par)

    return best_par


def fit_and_plot(filename):
    """Function that reads data from a filename and fits a Murnaghan EOS.
    The fitted parameters and a plot are returned."""
    # Read data from file
    lattice, volume, energy = read_data(filename)
    # Fit data to Murnaghan EOS
    best_par = fit_murnaghan(volume, energy)
    # Print optimal parameters
    print("Fit parameters:")
    print("V0     =  {:1.4f} A^3 ".format(best_par[3]))
    print("E0     =  {:1.4f} eV  ".format(best_par[0]))
    print("B(V0)  =  {:1.4f} eV/A^3".format(best_par[1]))
    print("B'(VO) =  {:1.4f} ".format(best_par[2]))
    # Theoretical lattice constant
    lattice_const = (best_par[3] / factor[lattice]) ** (1. / 3.)
    print("Theoretical lattice constant: {:1.4f} A".format(lattice_const))

    # Generate Murnaghan model with fitted parameters
    m_volume = np.linspace(volume.min(), volume.max(), 1000)
    m_energy = eos_murnaghan(m_volume, *best_par)

    # Plot data and model together
    lines = plt.plot(volume, energy, 'ok', m_volume, m_energy, '--r')
    plt.xlabel(r"Volume [$\rm{A}^3$]")
    plt.ylabel(r"Energy [$\rm{eV}$]")

    return best_par, lines
