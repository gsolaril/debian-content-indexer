import os, sys
sys.path.append("./")
from utils.constants import *
from argparse import ArgumentParser

if (__name__ == "__main__"):

    args = ArgumentParser(prog = "Debian Package Statistics",
        epilog = "By Gaston Solari Loudet, for Canonical recruitment process",
        description = """
            Gets a ranking of the largest packages in the Debian distribution
            for each one of the approved processor architectures. The ranking
            is based on the number of files included in the package.
        """)
    
    args.add_argument("arch", nargs = "?", type = str, default = None)
    arch = getattr(args.parse_args(), "arch", ARCH_LOCAL_MACHINE)

    print("Given architecture:", arch)