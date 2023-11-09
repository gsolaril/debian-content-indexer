import os, sys, re, json
from pandas import Series, Index

sys.path.append("./")
from utils.constants import *
from core.base import DebianDownloader

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████   Main class   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

class DebianContentIndex(DebianDownloader):

    # Find like: "Contents- | alphanumeric whatever | .gz"
    REGEX_ARCH_LOCATE = "(?<=Contents-)\\w+(?=\\.gz)"
    # To keep the "alphanumeric whatever" from the middle.
    REGEX_ARCH_EXTRACT = "(Contents-|\\.gz)"

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def __init__(self, arch: str = None):

        super().__init__() # Construct parent class instance.

        # Regex patterns: hover mouse over "self.REGEX_ARCH_..." right below.
        finder_locate_arch = lambda s: re.findall(self.REGEX_ARCH_LOCATE, s)
        filter_extract_arch = lambda s: re.sub(self.REGEX_ARCH_EXTRACT, "", s)
        # Find filenames with an architecture string. Extract such strings.
        self._archs = filter(finder_locate_arch, self._directory.keys())
        self._archs = list(map(filter_extract_arch, self._archs))
        print("available architectures:", self._archs)
    
#█████████████████████████████████████████ Small test
    
if (__name__ == "__main__"):

    obj = DebianContentIndex("i386")

