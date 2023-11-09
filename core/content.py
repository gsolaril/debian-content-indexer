import os, sys, re

sys.path.append("./")
from utils.constants import *
from core.base import DebianDownloader

#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#██████████████████████████████████████████████████████████████████████████████████████████████████████   Main class   ███
#█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

class DebianContentIndex(DebianDownloader):
    """
    Class to download and parse specific contents-index files from the Debian mirror.
    Inherits its structure from parent class "`DebianDownloader`". Upon instantiation, it will parse the
    associated contents-index file and tabulate its data based on existent Debian packages and inner files.
    Inputs:
     - "`arch`" (`str`): The architecture on which the contents-index file is to be downloaded. If not
        specified, it will consider the architecture of the machine where this code is executed in. An
        "`ArchitectureNotFound`" error will be triggered when given architecture is not available.\n
    Methods:
     - "`directory`" (property, `str`) to get the available files with download count.
     - "`list_archs`" (property, `list`) to get the architectures that are available on directory.
    For more info visit:
     - Help and definitions: "https://wiki.debian.org/RepositoryFormat#A.22Contents"
     - Mirror page with directory: "http://ftp.uk.debian.org/debian/dists/stable/main/"
    """

    class ArchitectureNotFound(Exception): pass

    FILENAME_ARCH = "Contents-{arch}.gz" # Filename format.
    URL_ARCH = DebianDownloader.URL_BASE + FILENAME_ARCH

    # Find like: "Contents- | alphanumeric whatever | .gz"
    REGEX_ARCH_LOCATE = "(?<=Contents-)\\w+(?=\\.gz)"
    # To keep the "alphanumeric whatever" from the middle.
    REGEX_ARCH_EXTRACT = "(Contents-|\\.gz)"

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def __init__(self, arch: str = None):

        super().__init__() # Construct parent class instance.
        if arch is None: # When no arch given, use the one found above.
            comment = "Warning - No architecture given. Using local:"
            print(comment, "\"%s\"" % (arch := ARCH_LOCAL_MACHINE))

        # Regex patterns: hover mouse over "self.REGEX_ARCH_..." right below.
        finder_locate_arch = lambda s: re.findall(self.REGEX_ARCH_LOCATE, s)
        filter_extract_arch = lambda s: re.sub(self.REGEX_ARCH_EXTRACT, "", s)
        # Find filenames with an architecture string. Extract such strings.
        self._archs = filter(finder_locate_arch, self._directory.keys())
        self._archs = list(map(filter_extract_arch, self._archs))
        # If the given architecture is not in the list, raise error.
        if not self._check_exist_arch(arch):
            error = f"\"{arch}\" is invalid. Please use one of these:\n  ==> "
            raise self.ArchitectureNotFound(error + str.join(", ", self._archs))
        
        self._arch = arch # Store arch and associated filename for URL.
        self._filename = self.FILENAME_ARCH.format(arch = self._arch)
        
        # Download decoded file content, like the parent class.
        content = super().download(self._filename)
        print(f"Downloaded content preview from \"{self._filename}\":")
        print(content[: 1000])
    
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def _check_exist_arch(self, arch: str):
        """[PRIVATE] Verify if specified file exists."""
        return (arch in self._archs)

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    @property
    def arch(self):
        """Getter for specified architecture."""
        return self._arch
    @property
    def list_archs(self):
        """Getter for available architectures"""
        return self._archs
    
#█████████████████████████████████████████ Small test
    
if (__name__ == "__main__"):

    obj = DebianContentIndex("i386")
    print("selected architecture:", obj.arch)
    print("available architectures:", obj.list_archs)
