""" Download Crystal Structures using Materials Project Database API. """

from plumbum import cli, local
from mp_api.client import MPRester, MPRestError
# https://next-gen.materialsproject.org/materials


class MPDownloadApp(cli.Application):
    """Download Crystal Structures using Materials Project Database API."""
    mp_api_key = cli.SwitchAttr(
        ["-k", "--api-key"], help="""Materials Project API key.
        When not specified is taken from the `MP_API_KEY` env variable.
        """
    )

    structure_filename = cli.SwitchAttr(
        ["-o", "--output"], default="infile.ucposcar",
        help="""Filename for the searched structure output."""
    )

    structure_format = cli.SwitchAttr(
        ["--format"], default="poscar",
        help="""Format of the searched structure output."""
    )

    structure_final = cli.SwitchAttr(
        ["-f", "--final"], argtype=bool, default=False,
        help="""Get the final structure,
        which is probably relaxed but with symmetry broken."""
    )

    def main(self, mp_structure_id):
        api_key = self.mp_api_key or local.env.get("MP_API_KEY")
        if api_key:
            try:
                mpr = MPRester(api_key)

                if self.structure_final:
                    structure = mpr.get_structure_by_material_id(mp_structure_id)
                    print("Requested final structure.")
                else:
                    structure = mpr.get_structure_by_material_id(
                        mp_structure_id, final=self.structure_final
                    )[0]

                structure.to(
                    fmt=self.structure_format,
                    filename=self.structure_filename
                )
                print(structure)
                # assert structure.is_3d_periodic

            except MPRestError:
                print("Please search for a valid structure Id: " +
                      "https://next-gen.materialsproject.org/materials")
        else:
            print("Please provide MP_API_KEY via env var or " +
                  "with \"--api-key\" cli switch.")

def main():
    MPDownloadApp.run()
