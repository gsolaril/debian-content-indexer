import os, sys
sys.path.append("./")

from argparse import ArgumentParser
from core.content import DebianContentIndex
from utils.constants import *

if (__name__ == "__main__"):

    args = ArgumentParser(prog = "Debian Package Statistics",
        epilog = "By Gaston Solari Loudet, for Canonical recruitment process",
        description = """
            Gets a ranking of the largest packages in the Debian distribution
            for each one of the approved processor architectures. The ranking
            is based on the number of files included in the package.
        """)
    
    # Leftmost positional parameter: the architecture name itself - optional.
    help = f"[str] Architecture to be analyzed. Default: \"{ARCH_LOCAL_MACHINE}\""
    args.add_argument("arch", nargs = "?", type = str, default = None, help = help)

    # Second named parameter: numbers of packages to appear on ranking - optional.
    help = f"[int] Amount of packages to appear on the ranking. Default: 10"
    args.add_argument("-n", "--top", type = int, default = 10, help = help)

    # Parse specified arguments in the given order.
    arch, top = args.parse_args().__dict__.values()

    # Instantiate the core class and get the ranking.
    print("Please wait a few moments...")
    obj = DebianContentIndex(arch = arch)
    ranking = obj.get_ranking(top = top)

    print(SEPARATOR)
    # Some early verbose.
    print(f"Ranking of the largest top {top} packages in the Debian",
          f"distribution for the given architecture: \"{obj.arch}\"")
    print("(based on file count - amount of files in package)")

    # Get the longest package name and later left-justify based on it.
    # Print the header for the future table, and add space to right.
    max_width = ranking.index.str.len().max()
    headers = ("Package name", "File count")
    ul, ur = list(map(len, headers))
    mid_gap_len = max_width - ul + 1

    # Just a fancy header for the table...
    line_1 = ("%s" + mid_gap_len * " " + "%s") % headers
    line_2 = ("‾" * ul) + (mid_gap_len * " ") + ("‾" * ur)
    print("", line_1, line_2, sep = "\n")

    # Print the ranking, row by row in descending order.
    for package, count in ranking.items():
        # Package name shall be left-justified.
        print(package.ljust(max_width), count)

    print(SEPARATOR)