"The module containing utility definitions to work with SIESTA."

from plumbum import local

from ase import Atoms
from ase.calculators.siesta import Siesta


def write_siesta_fdf(struct: Atoms, pseudo_path=None):
    "Output the .fdf file for a structure in `struct`."

    if not local.env["SIESTA_PP_PATH"] and not pseudo_path:
        raise FileNotFoundError(""" Provide path to pseudopotential
        files collection, either with `SIESTA_PP_PATH` variable or
        through `pseudo_path` flag. """)

    calc = Siesta(label="siesta",
                  symlink_pseudos=True,
                  pseudo_path=(local.env["SIESTA_PP_PATH"] or pseudo_path),
                  pseudo_qualifier="")  # omit default XC qualifier

    calc.write_input(struct, properties=['energy'])
