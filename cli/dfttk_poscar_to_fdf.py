""" Convert POSCAR to SIESTA .FDF input file using ASE. """

from plumbum import cli
from ase.io.vasp import read_vasp

from dft_toolkit.siesta_utils import write_siesta_fdf


class PoscarToSiesta(cli.Application):
    " Convert POSCAR to SIESTA .FDF input file using ASE. "

    pseudos_dir = cli.SwitchAttr(
        ["-p", "--pseudos-dir"],
        help="Path to SIESTA Pseudopotential files library (directory)."
    )

    def main(self, poscar):
        with open(poscar, "r", encoding="utf-8") as poscar_file:
            struct = read_vasp(poscar_file)
            write_siesta_fdf(struct, self.pseudos_dir)


def main():
    PoscarToSiesta.run()
