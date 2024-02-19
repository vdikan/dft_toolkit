""" Convert SIESTA STRUCT_OUT file to POSCAR. """

from plumbum import cli

from ase.io.vasp import write_vasp
from ase.io.siesta import read_struct_out

class StructOutToPoscar(cli.Application):
    """ Convert SIESTA STRUCT_OUT file to POSCAR. """

    def main(self, struct_out, out_poscar=None):
        with open(struct_out, "r", encoding="utf-8") as struct_out_file:
            struct = read_struct_out(struct_out_file)

        out_poscar = out_poscar or "out.poscar.vasp"

        with open(out_poscar, "w", encoding="utf-8") as poscar_file:
            write_vasp(poscar_file, struct)

def main():
    StructOutToPoscar.run()
