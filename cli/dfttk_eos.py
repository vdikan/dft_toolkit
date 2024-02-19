"""Murnaghan equation of state (energy as a function of volume).
From PRB 28,5480 (1983).

Thank you Javier Junquera,
https://personales.unican.es/junqueraj/siesta-tutorial.html

"""

import matplotlib.pyplot as plt

from plumbum import cli
from dft_toolkit.eos import fit_and_plot


class Eos(cli.Application):
    """Murnaghan equation of state (energy as a function of volume).
From PRB 28,5480 (1983).

Filename format:
```
cubic|bcc|fcc|diamond
alat1 (Ang)   TotEn1 (eV)
alat2 (Ang)   TotEn2 (eV)
...
```
    """

    def main(self, filename, fig_filename=None):
        # Fit and plot data from the file
        fit_and_plot(filename)
        # Draw the plot
        plt.draw()

        if fig_filename:
            plt.savefig(fig_filename)
        else:
            plt.show()

def main():
    Eos.run()
